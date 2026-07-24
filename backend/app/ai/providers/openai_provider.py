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
