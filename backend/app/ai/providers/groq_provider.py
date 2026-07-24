"""Groq LLM provider for clinical triage reasoning using gpt-oss-120b."""

import json
import logging
from typing import Any, Dict, List, Optional
from app.ai.providers.base import BaseProvider
from app.ai.providers.mock_provider import MockProvider
from app.ai.models import (
    AnalysisInput,
    AnalysisResult,
    RiskAssessment,
    SpecialistRecommendation,
    HealthReport,
    SymptomAnalysis,
)
from app.ai.utils.emergency_detection import detect_emergency, classify_specificity
from app.core.config import settings

logger = logging.getLogger(__name__)

# Logger specifically for recording rule vs LLM triage disagreements
disagreement_logger = logging.getLogger("triage_disagreements")

SYSTEM_PROMPT = """You are a clinical triage reasoning assistant. Think step by step through the patient's symptoms before producing your final classification.

Step 1: List every symptom mentioned, including vague ones.
Step 2: For each symptom, note which body system it involves and whether it could indicate a time-sensitive condition (cardiac, neurological, respiratory, allergic/anaphylactic, obstetric emergency, psychiatric crisis).
Step 3: Consider symptom combinations together, not in isolation — some combinations are red flags even if no single symptom is.
Step 4: If the input is too vague to classify confidently (short, no specific body part/duration/severity), do NOT default to low risk — mark needs_followup=true and set risk_level to at least MODERATE.
Step 5: Assign final risk_level, confidence, and specialist recommendation.

Bias toward caution: a false alarm costs a doctor visit; a missed emergency can cost a life. When uncertain, escalate risk_level rather than downgrade it.

Respond ONLY with valid JSON in this exact schema, no other text:
{
  "reasoning_steps": ["step 1 text", "step 2 text"],
  "risk_level": "LOW" | "MODERATE" | "HIGH",
  "confidence": 0.0-1.0,
  "red_flags_detected": ["specific phrase or concern"],
  "needs_followup": true | false,
  "followup_questions": ["question if needs_followup is true"],
  "recommended_specialist": "string",
  "reasoning": "1-2 sentence summary for the user",
  "instructions": "what the user should do next"
}

If risk_level is HIGH, emergency_alert must be true and instructions must start with "CALL EMERGENCY SERVICES (911) IMMEDIATELY."
"""


class GroqProvider(BaseProvider):
    """Primary LLM provider backed by Groq's openai/gpt-oss-120b model with safety overrides."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        super().__init__(api_key=api_key or settings.LLM_API_KEY)
        self.base_url = base_url or settings.LLM_BASE_URL or "https://api.groq.com/openai/v1"
        self.model = model or settings.LLM_MODEL or "openai/gpt-oss-120b"
        self.timeout = timeout or settings.LLM_TIMEOUT or 30
        self.fallback_provider = MockProvider()
        self.client = None

    async def initialize(self) -> None:
        """Initialize the Groq client (using Groq SDK or OpenAI-compatible client)."""
        if not self.api_key:
            logger.warning("GroqProvider initialized without API key. Fallback to MockProvider will be triggered.")
            return

        try:
            try:
                from groq import AsyncGroq
                # AsyncGroq default base_url is https://api.groq.com/openai/v1
                kwargs = {"api_key": self.api_key, "timeout": self.timeout}
                if self.base_url and "groq.com" not in self.base_url:
                    kwargs["base_url"] = self.base_url
                self.client = AsyncGroq(**kwargs)
            except ImportError:
                from openai import AsyncOpenAI
                base_url = self.base_url or "https://api.groq.com/openai/v1"
                self.client = AsyncOpenAI(
                    api_key=self.api_key,
                    base_url=base_url,
                    timeout=self.timeout,
                )
            self.is_initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            self.client = None
            self.is_initialized = False

    async def analyze_symptoms_structured(self, input_data: AnalysisInput) -> SymptomAnalysis:
        """Use fallback provider or quick parsing for symptom extraction."""
        return await self.fallback_provider.analyze_symptoms_structured(input_data)

    async def analyze_risk_structured(
        self, symptom_analysis: dict, user_input: str = ""
    ) -> RiskAssessment:
        """Assess risk via Groq's gpt-oss-120b with CoT reasoning and safety net merge logic."""
        if not self.is_initialized or not self.client:
            logger.warning("Groq client unavailable; falling back to MockProvider for risk assessment.")
            res = await self.fallback_provider.analyze_risk_structured(symptom_analysis)
            res.provider_used = "mock"
            return res

        raw_text = user_input or symptom_analysis.get("raw_text", "") or symptom_analysis.get("summary", "")

        prompt_user_content = (
            f"Patient Input: {raw_text}\n\n"
            f"Extracted Symptoms: {', '.join(symptom_analysis.get('detected_symptoms', []))}\n"
            f"Severity Cues: {', '.join(symptom_analysis.get('severity_indicators', []))}\n"
            f"Affected Systems: {', '.join(symptom_analysis.get('affected_systems', []))}"
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt_user_content},
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            parsed = json.loads(content)

            risk_level = str(parsed.get("risk_level", "MODERATE")).upper()
            if risk_level not in ["LOW", "MODERATE", "HIGH"]:
                risk_level = "MODERATE"

            confidence = float(parsed.get("confidence", 0.85))
            confidence = max(0.0, min(1.0, confidence))

            red_flags = list(parsed.get("red_flags_detected", []))
            needs_followup = bool(parsed.get("needs_followup", False))
            recommended_specialist = str(parsed.get("recommended_specialist", "General Practitioner"))
            reasoning = str(parsed.get("reasoning", ""))
            instructions = str(parsed.get("instructions", ""))
            reasoning_steps = list(parsed.get("reasoning_steps", []))

            # -------------------------------------------------------------
            # Safety Net Merge Logic
            # -------------------------------------------------------------
            rule_is_emergency, rule_red_flags = detect_emergency(raw_text)
            rule_specificity = classify_specificity(raw_text)

            # Rule 1: Emergency override
            if rule_is_emergency and risk_level != "HIGH":
                disagreement_msg = (
                    f"TRIAGE DISAGREEMENT OVERRIDE: Rule-based detect_emergency() triggered HIGH "
                    f"due to red flags {rule_red_flags}, but Groq classified as {risk_level}. Overriding to HIGH."
                )
                logger.warning(disagreement_msg)
                disagreement_logger.warning(
                    json.dumps({
                        "event": "triage_disagreement",
                        "raw_text": raw_text,
                        "rule_risk": "HIGH",
                        "groq_risk": risk_level,
                        "rule_red_flags": rule_red_flags,
                        "groq_red_flags": red_flags,
                        "reasoning_steps": reasoning_steps,
                    })
                )
                risk_level = "HIGH"
                confidence = max(confidence, 0.95)
                instructions = "CALL EMERGENCY SERVICES (911) IMMEDIATELY."
                reasoning = f"Evaluated as HIGH RISK — Emergency red flags detected: {', '.join(rule_red_flags)}"
                needs_followup = False
                red_flags = list(set(red_flags + rule_red_flags))

            elif risk_level == "HIGH":
                # Rule 2: Trust Groq when it predicts HIGH even if rules didn't detect it
                logger.info("Groq predicted HIGH risk; keeping HIGH risk classification.")
                if not instructions.startswith("CALL EMERGENCY SERVICES"):
                    instructions = f"CALL EMERGENCY SERVICES (911) IMMEDIATELY. {instructions}".strip()

            # Rule 3: Vague input override
            if rule_specificity == "VAGUE" and not needs_followup:
                logger.warning("Safety guardrail: rule-based specificity checker flagged input as VAGUE. Overriding needs_followup=True.")
                needs_followup = True
                if risk_level == "LOW":
                    risk_level = "MODERATE"
                    confidence = min(confidence, 0.40)

            emergency_alert = (risk_level == "HIGH")

            return RiskAssessment(
                risk_level=risk_level,
                confidence=confidence,
                emergency_alert=emergency_alert,
                red_flags_detected=red_flags,
                recommended_specialist=recommended_specialist,
                reasoning=reasoning,
                instructions=instructions,
                needs_followup=needs_followup,
                provider_used="groq",
                reasoning_steps=reasoning_steps,
            )

        except Exception as e:
            logger.error(f"Groq API call failed: {e}. Falling back to MockProvider.")
            fallback_res = await self.fallback_provider.analyze_risk_structured(symptom_analysis)
            fallback_res.provider_used = "mock"
            return fallback_res

    async def analyze_specialist_structured(
        self, risk_assessment: RiskAssessment
    ) -> SpecialistRecommendation:
        return await self.fallback_provider.analyze_specialist_structured(risk_assessment)

    async def generate_health_report_structured(
        self,
        symptom_analysis: dict,
        risk_assessment: RiskAssessment,
        specialist_recommendation: SpecialistRecommendation,
    ) -> HealthReport:
        return await self.fallback_provider.generate_health_report_structured(
            symptom_analysis=symptom_analysis,
            risk_assessment=risk_assessment,
            specialist_recommendation=specialist_recommendation,
        )

    async def analyze_symptoms(self, input_data: AnalysisInput) -> AnalysisResult:
        """Complete analysis workflow execution using Groq provider."""
        symptom_analysis = (await self.analyze_symptoms_structured(input_data)).model_dump()
        risk = await self.analyze_risk_structured(symptom_analysis, user_input=input_data.symptoms)
        specialist = await self.analyze_specialist_structured(risk)
        report = await self.generate_health_report_structured(symptom_analysis, risk, specialist)

        import uuid
        return AnalysisResult(
            analysis_id=str(uuid.uuid4()),
            risk_assessment=risk,
            specialist_recommendation=specialist,
            health_report=report,
            emergency_alert=risk.emergency_alert,
            provider_used=risk.provider_used,
        )

    async def generate_report(self, analysis_result: AnalysisResult) -> Dict[str, Any]:
        """Generate a detailed health report dict from analysis result."""
        import uuid
        return {
            "report_id": str(uuid.uuid4()),
            "analysis_id": analysis_result.analysis_id,
            "status": "Report generated successfully",
        }

    async def health_check(self) -> bool:
        """Health check for Groq provider."""
        if not self.is_initialized or not self.client:
            return False
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=5,
            )
            return bool(response.choices)
        except Exception:
            return False
