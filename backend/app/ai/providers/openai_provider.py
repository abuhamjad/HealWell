"""OpenAI-compatible AI provider implementation."""

import uuid
import json
import logging
from typing import Any, Dict
from openai import AsyncOpenAI
from app.ai.models import (
    AnalysisInput,
    AnalysisResult,
    RiskAssessment,
    SpecialistRecommendation,
    HealthReport,
    SymptomAnalysis,
)
from app.ai.prompts.symptom_prompt import get_symptom_analysis_prompt
from app.ai.prompts.risk_prompt import get_risk_assessment_prompt
from app.ai.prompts.specialist_prompt import get_specialist_recommendation_prompt
from app.ai.prompts.report_prompt import get_health_report_prompt
from app.ai.providers.base import BaseProvider
from app.core.config import settings

logger = logging.getLogger(__name__)

RISK_LEVELS = ("low", "moderate", "high")
URGENCY_LEVELS = ("immediate", "24-48 hours", "1-2 weeks")


def _as_str(value: Any, default: str = "") -> str:
    """Coerce an AI-supplied value into a string, never None."""
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip() or default
    return str(value)


def _as_str_list(value: Any) -> list[str]:
    """Coerce an AI-supplied value into a list of strings, never None.

    A bare string is wrapped into a single-item list; other scalars are
    stringified; unusable values yield an empty list.
    """
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, (list, tuple, set)):
        return [_as_str(item) for item in value if _as_str(item)]
    return [_as_str(value)]


def _as_float(value: Any, default: float) -> float:
    """Coerce an AI-supplied value into a float, falling back to default."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class OpenAIProvider(BaseProvider):
    """OpenAI-compatible provider for health analysis via Aerolink gateway."""

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None, timeout: int = None):
        """Initialize OpenAI provider with optional overrides."""
        super().__init__(api_key=api_key)
        self.api_key = api_key or settings.LLM_API_KEY
        self.base_url = base_url or settings.LLM_BASE_URL
        self.model = model or settings.LLM_MODEL
        self.timeout = timeout or settings.LLM_TIMEOUT
        self.client = None

    async def initialize(self) -> None:
        """Initialize OpenAI client with configuration."""
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )
        self.is_initialized = True

    async def analyze_symptoms_structured(self, input_data: AnalysisInput) -> SymptomAnalysis:
        """Analyze symptoms using OpenAI-compatible API and return structured result.

        Args:
            input_data: AnalysisInput containing symptoms and medical context

        Returns:
            SymptomAnalysis with detected symptoms and assessment

        Raises:
            Exception: If API call fails or response is invalid JSON
        """
        if not self.is_initialized or not self.client:
            raise RuntimeError("Provider not initialized. Call initialize() first.")

        prompt = get_symptom_analysis_prompt(
            symptoms=input_data.symptoms,
            medical_history=input_data.medical_history,
            medications=input_data.medications,
            allergies=input_data.allergies,
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical analysis assistant. Respond with only valid JSON, no additional text.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.7,
                max_tokens=1000,
            )

            response_text = response.choices[0].message.content.strip()

            symptom_data = json.loads(response_text)

            return SymptomAnalysis(
                detected_symptoms=symptom_data.get("detected_symptoms", []),
                confidence=float(symptom_data.get("confidence", 75)),
                summary=symptom_data.get("summary", "Symptom analysis completed"),
                severity_indicators=symptom_data.get("severity_indicators", []),
                affected_systems=symptom_data.get("affected_systems", []),
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")
        except Exception as e:
            logger.error(f"Symptom analysis failed: {e}")
            raise

    async def assess_risk_structured(self, symptoms: str, symptom_analysis: Dict[str, Any] = None) -> RiskAssessment:
        """Assess health risk using OpenAI-compatible API and return structured result.

        Args:
            symptoms: Raw patient symptom text
            symptom_analysis: Prior SymptomAnalysis output as a dict, if available

        Returns:
            RiskAssessment with risk level, confidence, reasoning and warning signs

        Raises:
            Exception: If API call fails or response is invalid JSON
        """
        if not self.is_initialized or not self.client:
            raise RuntimeError("Provider not initialized. Call initialize() first.")

        analyzed_symptoms = json.dumps(symptom_analysis) if symptom_analysis else None

        prompt = get_risk_assessment_prompt(
            symptoms=symptoms,
            analyzed_symptoms=analyzed_symptoms,
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical analysis assistant. Respond with only valid JSON, no additional text.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.7,
                max_tokens=1000,
            )

            response_text = response.choices[0].message.content.strip()

            risk_data = json.loads(response_text)

            if not isinstance(risk_data, dict):
                raise ValueError(f"Expected JSON object from LLM, got {type(risk_data).__name__}")

            risk_level = _as_str(risk_data.get("risk_level"), "moderate").lower()
            if risk_level not in RISK_LEVELS:
                logger.warning(f"LLM returned unknown risk_level '{risk_level}', defaulting to 'moderate'")
                risk_level = "moderate"

            return RiskAssessment(
                risk_level=risk_level,
                confidence=_as_float(risk_data.get("confidence"), 75.0),
                reasoning=_as_str(risk_data.get("reasoning"), "Risk assessment completed"),
                warning_signs=_as_str_list(risk_data.get("warning_signs")),
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM risk response as JSON: {e}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")
        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            raise

    async def recommend_specialist_structured(self, symptoms: str, risk_level: str = None) -> SpecialistRecommendation:
        """Recommend a specialist using OpenAI-compatible API and return structured result.

        Args:
            symptoms: Raw patient symptom text
            risk_level: Previously assessed risk level, if available

        Returns:
            SpecialistRecommendation with specialist, reasoning and urgency

        Raises:
            Exception: If API call fails or response is invalid JSON
        """
        if not self.is_initialized or not self.client:
            raise RuntimeError("Provider not initialized. Call initialize() first.")

        prompt = get_specialist_recommendation_prompt(
            symptoms=symptoms,
            risk_level=risk_level,
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical analysis assistant. Respond with only valid JSON, no additional text.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.7,
                max_tokens=1000,
            )

            response_text = response.choices[0].message.content.strip()

            specialist_data = json.loads(response_text)

            if not isinstance(specialist_data, dict):
                raise ValueError(f"Expected JSON object from LLM, got {type(specialist_data).__name__}")

            urgency = _as_str(specialist_data.get("urgency"), "24-48 hours")
            if urgency.lower() not in URGENCY_LEVELS:
                logger.warning(f"LLM returned unknown urgency '{urgency}', defaulting to '24-48 hours'")
                urgency = "24-48 hours"

            return SpecialistRecommendation(
                specialist=_as_str(specialist_data.get("specialist"), "General Physician"),
                reasoning=_as_str(specialist_data.get("reasoning"), "Specialist recommendation completed"),
                urgency=urgency,
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM specialist response as JSON: {e}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")
        except Exception as e:
            logger.error(f"Specialist recommendation failed: {e}")
            raise

    async def generate_report_structured(
        self,
        symptoms: str,
        risk_level: str = None,
        specialist: str = None,
    ) -> HealthReport:
        """Generate a health report using OpenAI-compatible API and return structured result.

        Args:
            symptoms: Raw patient symptom text
            risk_level: Previously assessed risk level, if available
            specialist: Previously recommended specialist, if available

        Returns:
            HealthReport with summary, home care, lifestyle, monitoring and references

        Raises:
            Exception: If API call fails or response is invalid JSON
        """
        if not self.is_initialized or not self.client:
            raise RuntimeError("Provider not initialized. Call initialize() first.")

        prompt = get_health_report_prompt(
            symptoms=symptoms,
            risk_level=risk_level,
            specialist=specialist,
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical analysis assistant. Respond with only valid JSON, no additional text.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.7,
                max_tokens=2000,
            )

            response_text = response.choices[0].message.content.strip()

            report_data = json.loads(response_text)

            if not isinstance(report_data, dict):
                raise ValueError(f"Expected JSON object from LLM, got {type(report_data).__name__}")

            return HealthReport(
                summary=_as_str(report_data.get("summary"), "Health report generated"),
                home_care=_as_str_list(report_data.get("home_care")),
                lifestyle=_as_str_list(report_data.get("lifestyle")),
                monitoring=_as_str_list(report_data.get("monitoring")),
                references=_as_str_list(report_data.get("references")),
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM report response as JSON: {e}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")
        except Exception as e:
            logger.error(f"Health report generation failed: {e}")
            raise

    async def analyze_symptoms(self, input_data: AnalysisInput) -> AnalysisResult:
        """
        Analyze symptoms using OpenAI-compatible API.

        Placeholder implementation returns mock data.
        TODO: Implement actual LLM calls via prompts and agents.
        """
        # Placeholder logic
        risk_level = "moderate"
        if input_data.symptoms:
            if any(keyword in input_data.symptoms.lower() for keyword in ["chest", "emergency", "collapse"]):
                risk_level = "high"
            elif any(keyword in input_data.symptoms.lower() for keyword in ["pain", "fever", "headache"]):
                risk_level = "moderate"
            else:
                risk_level = "low"

        return AnalysisResult(
            analysis_id=str(uuid.uuid4()),
            risk_assessment=RiskAssessment(
                risk_level=risk_level,
                confidence=87.5,
                reasoning="Analysis pending implementation",
                warning_signs=[],
            ),
            specialist_recommendation=SpecialistRecommendation(
                specialist="General Practitioner",
                reasoning="Recommendation pending implementation",
                urgency="1-2 weeks",
            ),
            health_report=HealthReport(
                summary="Health assessment completed.",
                home_care=["Rest", "Stay hydrated"],
                lifestyle=["Maintain healthy habits"],
                monitoring=["Monitor symptoms"],
            ),
            emergency_alert=False,
        )

    async def generate_report(self, analysis_result: AnalysisResult) -> Dict[str, Any]:
        """
        Generate detailed health report.

        Placeholder implementation.
        TODO: Implement report generation via LLM.
        """
        return {
            "report_id": str(uuid.uuid4()),
            "analysis_id": analysis_result.analysis_id,
            "status": "Report generation pending implementation",
        }

    async def health_check(self) -> bool:
        """Check provider health status."""
        if not self.is_initialized or not self.client:
            return False
        try:
            # Test connectivity with a simple API call
            await self.client.models.list()
            return True
        except Exception:
            return False
