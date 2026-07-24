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

    async def analyze_risk_structured(self, symptom_analysis: dict) -> RiskAssessment:
        """Analyze health risk based on symptom analysis and return structured result.

        Args:
            symptom_analysis: Dict with detected_symptoms, summary, etc. from SymptomAgent

        Returns:
            RiskAssessment with risk_level, confidence, reasoning, warning_signs

        Raises:
            Exception: If API call fails or response is invalid JSON
        """
        if not self.is_initialized or not self.client:
            raise RuntimeError("Provider not initialized. Call initialize() first.")

        prompt = get_risk_assessment_prompt(symptom_analysis)

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical risk assessment AI. Respond with only valid JSON, no additional text.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.7,
                max_tokens=500,
            )

            response_text = response.choices[0].message.content.strip()

            risk_data = json.loads(response_text)

            return RiskAssessment(
                risk_level=risk_data.get("risk_level", "moderate"),
                confidence=float(risk_data.get("confidence", 75)),
                reasoning=risk_data.get("reasoning", "Risk assessment completed"),
                risk_explanation=risk_data.get("risk_explanation", "Assessment completed."),
                confidence_explanation=risk_data.get("confidence_explanation", "Confidence level determined."),
                warning_signs=risk_data.get("warning_signs", []),
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")
        except Exception as e:
            logger.error(f"Risk analysis failed: {e}")
            raise

    async def analyze_specialist_structured(self, risk_assessment: RiskAssessment) -> SpecialistRecommendation:
        """Recommend specialist based on risk assessment and return structured result.

        Args:
            risk_assessment: RiskAssessment model from RiskAgent

        Returns:
            SpecialistRecommendation with specialist, reasoning, urgency

        Raises:
            Exception: If API call fails or response is invalid JSON
        """
        if not self.is_initialized or not self.client:
            raise RuntimeError("Provider not initialized. Call initialize() first.")

        # Convert RiskAssessment to dict for prompt
        risk_dict = {
            "risk_level": risk_assessment.risk_level,
            "reasoning": risk_assessment.reasoning,
            "warning_signs": risk_assessment.warning_signs,
        }

        prompt = get_specialist_recommendation_prompt(risk_dict)

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical triage specialist. Respond with only valid JSON, no additional text.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.7,
                max_tokens=500,
            )

            response_text = response.choices[0].message.content.strip()

            specialist_data = json.loads(response_text)

            return SpecialistRecommendation(
                specialist=specialist_data.get("specialist", "General Practitioner"),
                reasoning=specialist_data.get("reasoning", "Specialist recommendation completed"),
                specialist_explanation=specialist_data.get("specialist_explanation", "Recommendation completed."),
                urgency=specialist_data.get("urgency", "1-2 weeks"),
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")
        except Exception as e:
            logger.error(f"Specialist recommendation failed: {e}")
            raise

    async def generate_health_report_structured(
        self,
        symptom_analysis: dict,
        risk_assessment: RiskAssessment,
        specialist_recommendation: SpecialistRecommendation,
    ) -> HealthReport:
        """Generate comprehensive health report synthesizing all analysis results.

        Args:
            symptom_analysis: Dict with detected symptoms and analysis
            risk_assessment: RiskAssessment model from RiskAgent
            specialist_recommendation: SpecialistRecommendation from SpecialistAgent

        Returns:
            HealthReport with summary, home_care, lifestyle, monitoring, references

        Raises:
            Exception: If API call fails or response is invalid JSON
        """
        if not self.is_initialized or not self.client:
            raise RuntimeError("Provider not initialized. Call initialize() first.")

        # Convert models to dicts for prompt
        risk_dict = {
            "risk_level": risk_assessment.risk_level,
            "reasoning": risk_assessment.reasoning,
            "warning_signs": risk_assessment.warning_signs,
        }

        specialist_dict = {
            "specialist": specialist_recommendation.specialist,
            "reasoning": specialist_recommendation.reasoning,
            "urgency": specialist_recommendation.urgency,
        }

        prompt = get_health_report_prompt(symptom_analysis, risk_dict, specialist_dict)

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a patient education specialist. Generate clear, accurate health guidance. Respond with only valid JSON, no additional text.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.7,
                max_tokens=1200,
            )

            response_text = response.choices[0].message.content.strip()

            report_data = json.loads(response_text)

            return HealthReport(
                summary=report_data.get("summary", "Health assessment completed."),
                summary_explanation=report_data.get("summary_explanation", "Assessment completed."),
                confidence_explanation=report_data.get("confidence_explanation", "Confidence level determined."),
                risk_explanation=report_data.get("risk_explanation", "Risk assessment completed."),
                specialist_explanation=report_data.get("specialist_explanation", "Specialist recommended."),
                home_care=report_data.get("home_care", []),
                personalized_home_care=report_data.get("personalized_home_care", []),
                lifestyle=report_data.get("lifestyle", []),
                personalized_lifestyle=report_data.get("personalized_lifestyle", []),
                monitoring=report_data.get("monitoring", []),
                monitoring_guidance=report_data.get("monitoring_guidance", []),
                emergency_instructions=report_data.get("emergency_instructions"),
                references=report_data.get("references", []),
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
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
                risk_explanation="Assessment completed.",
                confidence_explanation="Confidence level determined.",
                warning_signs=[],
            ),
            specialist_recommendation=SpecialistRecommendation(
                specialist="General Practitioner",
                reasoning="Recommendation pending implementation",
                specialist_explanation="Recommendation completed.",
                urgency="1-2 weeks",
            ),
            health_report=HealthReport(
                summary="Health assessment completed.",
                summary_explanation="Assessment completed.",
                confidence_explanation="Confidence level determined.",
                risk_explanation="Assessment completed.",
                specialist_explanation="Recommendation completed.",
                home_care=["Rest", "Stay hydrated"],
                personalized_home_care=["Rest adequately", "Stay well-hydrated"],
                lifestyle=["Maintain healthy habits"],
                personalized_lifestyle=["Maintain healthy habits"],
                monitoring=["Monitor symptoms"],
                monitoring_guidance=["Monitor your condition"],
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
