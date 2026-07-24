"""Mock AI provider — uses the medical triage knowledge base for accurate,
clinically-informed risk classification without an external LLM."""

import uuid
import logging
from typing import Any, Dict
from app.ai.providers.base import BaseProvider
from app.ai.providers.medical_triage import lookup_triage, collect_all_matches
from app.ai.models import (
    AnalysisInput,
    AnalysisResult,
    RiskAssessment,
    SpecialistRecommendation,
    HealthReport,
    SymptomAnalysis,
)

logger = logging.getLogger(__name__)


class MockProvider(BaseProvider):
    """Offline provider backed by a comprehensive medical triage knowledge base."""

    def __init__(self, api_key: str = None):
        super().__init__(api_key=api_key)
        self.is_initialized = True

    async def initialize(self) -> None:
        self.is_initialized = True

    # ------------------------------------------------------------------
    # 1. SYMPTOM ANALYSIS
    # ------------------------------------------------------------------
    async def analyze_symptoms_structured(self, input_data: AnalysisInput) -> SymptomAnalysis:
        text = (input_data.symptoms or "").lower()
        matches = collect_all_matches(text)

        detected = []
        severity_indicators = []
        affected_systems = set()
        is_critical = False

        for keyword, entry in matches:
            detected.append(keyword.title())
            severity_indicators.extend(entry.severity_indicators)
            affected_systems.add(entry.affected_system)
            if entry.risk_level == "high":
                is_critical = True

        if not detected:
            detected = ["General malaise", "Unspecified symptoms"]
            severity_indicators = ["Mild symptom onset"]
            affected_systems.add("General / Systemic")

        return SymptomAnalysis(
            detected_symptoms=detected,
            confidence=95.0 if is_critical else 85.0,
            summary=f"Analysis of reported symptoms: {', '.join(detected)}.",
            severity_indicators=severity_indicators or ["Mild to moderate symptom onset"],
            affected_systems=list(affected_systems) or ["General / Systemic"],
        )

    # ------------------------------------------------------------------
    # 2. RISK ASSESSMENT
    # ------------------------------------------------------------------
    async def analyze_risk_structured(self, symptom_analysis: dict) -> RiskAssessment:
        # Build a combined blob from all available symptom data
        detected_list = symptom_analysis.get("detected_symptoms", [])
        summary = symptom_analysis.get("summary", "")
        severity_list = symptom_analysis.get("severity_indicators", [])
        blob = f"{summary} {' '.join(detected_list)} {' '.join(severity_list)}"

        best_entry, best_kw = lookup_triage(blob)

        if best_entry:
            risk_level = best_entry.risk_level.upper()
            specialist_hint = best_entry.specialist

            if risk_level == "HIGH":
                reasoning = f"Symptoms match a HIGH-RISK condition ({best_kw.title()}). Immediate medical evaluation required."
                confidence = 0.95
                emergency_alert = True
                instructions = "CALL EMERGENCY SERVICES (911) IMMEDIATELY."
            elif risk_level == "MODERATE":
                reasoning = f"Symptoms match a MODERATE-RISK condition ({best_kw.title()}). Medical attention recommended."
                confidence = 0.88
                emergency_alert = False
                instructions = f"Schedule a consultation with a {specialist_hint}."
            else:
                reasoning = f"Symptoms match a LOW-RISK condition ({best_kw.title()}). Self-care with monitoring advised."
                confidence = 0.82
                emergency_alert = False
                instructions = "Monitor symptoms and seek care if they worsen."
        else:
            risk_level = "LOW"
            reasoning = "No specific high-risk pattern detected. Symptoms appear manageable."
            confidence = 0.75
            specialist_hint = "General Practitioner"
            emergency_alert = False
            instructions = "Monitor symptoms and seek care if they worsen."

        return RiskAssessment(
            risk_level=risk_level,
            confidence=confidence,
            emergency_alert=emergency_alert,
            red_flags_detected=best_entry.warning_signs if best_entry else [],
            recommended_specialist=specialist_hint,
            reasoning=reasoning,
            instructions=instructions,
        )

    # ------------------------------------------------------------------
    # 3. SPECIALIST RECOMMENDATION
    # ------------------------------------------------------------------
    async def analyze_specialist_structured(self, risk_assessment: RiskAssessment) -> SpecialistRecommendation:
        risk_level = risk_assessment.risk_level if hasattr(risk_assessment, "risk_level") else "MODERATE"
        specialist = risk_assessment.recommended_specialist if hasattr(risk_assessment, "recommended_specialist") else "General Practitioner (GP)"

        if risk_level == "HIGH":
            urgency = "Immediate / Call 911"
            explanation = f"IMMEDIATE EVALUATION REQUIRED by {specialist}. Seek emergency medical attention now."
        elif risk_level == "MODERATE":
            urgency = "24-48 hours"
            explanation = f"Schedule a consultation with {specialist} within {urgency}."
        else:
            urgency = "1-2 weeks"
            explanation = f"Routine consultation with {specialist} if symptoms persist beyond {urgency}."

        return SpecialistRecommendation(
            specialist=specialist,
            reasoning=f"Recommended {specialist} based on {risk_level} risk evaluation.",
            specialist_explanation=explanation,
            urgency=urgency,
        )

    # ------------------------------------------------------------------
    # 4. HEALTH REPORT
    # ------------------------------------------------------------------
    async def generate_health_report_structured(
        self,
        symptom_analysis: dict,
        risk_assessment: RiskAssessment,
        specialist_recommendation: SpecialistRecommendation,
    ) -> HealthReport:
        risk_level = risk_assessment.risk_level if hasattr(risk_assessment, "risk_level") else "MODERATE"
        specialist = specialist_recommendation.specialist if hasattr(specialist_recommendation, "specialist") else "GP"
        is_emergency = risk_level == "HIGH"

        if is_emergency:
            summary = f"CRITICAL ALERT: Your symptoms indicate a HIGH RISK emergency requiring immediate medical attention."
            summary_explanation = f"Your symptoms require IMMEDIATE evaluation. Do NOT wait — contact {specialist} or call emergency services."
            home_care = ["Sit or lie in a comfortable position", "Loosen tight clothing", "Do NOT exert yourself physically"]
            lifestyle = ["Avoid all physical and emotional stress", "Ensure someone is with you at all times"]
            monitoring = ["Monitor breathing and pulse continuously", "Note time of symptom onset for responders"]
            emergency_instructions = risk_assessment.instructions if hasattr(risk_assessment, "instructions") else "CALL EMERGENCY SERVICES (911) IMMEDIATELY."
        elif risk_level == "MODERATE":
            summary = f"Your symptoms indicate a MODERATE risk condition that requires professional medical evaluation."
            summary_explanation = f"Schedule an appointment with {specialist} within {specialist_recommendation.urgency}."
            home_care = ["Rest adequately", "Stay well hydrated", "Take OTC pain relief if appropriate"]
            lifestyle = ["Maintain a balanced diet", "Ensure 7-8 hours of sleep", "Avoid triggers if identified"]
            monitoring = ["Track symptom progression daily", "Note any new symptoms or worsening"]
            emergency_instructions = None
        else:
            summary = f"Your symptoms indicate a LOW risk condition that is generally manageable with self-care."
            summary_explanation = f"Based on your symptoms, consult {specialist} if symptoms persist beyond {specialist_recommendation.urgency}."
            home_care = ["Ensure adequate rest", "Stay well hydrated", "Avoid strenuous physical activity"]
            lifestyle = ["Maintain a balanced diet", "Ensure 7-8 hours of sleep"]
            monitoring = ["Track temperature and symptoms", "Note any changes"]
            emergency_instructions = None

        return HealthReport(
            summary=summary,
            summary_explanation=summary_explanation,
            confidence_explanation=f"Confidence: {int(risk_assessment.confidence * 100)}%",
            risk_explanation=risk_assessment.reasoning if hasattr(risk_assessment, "reasoning") else f"{risk_level} risk.",
            specialist_explanation=specialist_recommendation.specialist_explanation if hasattr(specialist_recommendation, "specialist_explanation") else f"See {specialist}.",
            home_care=home_care,
            personalized_home_care=home_care,
            lifestyle=lifestyle,
            personalized_lifestyle=lifestyle,
            monitoring=monitoring,
            monitoring_guidance=monitoring,
            emergency_instructions=emergency_instructions,
            references=["Clinical Emergency Triage Guidelines", "WHO ICD-11 Classification"],
        )

    # ------------------------------------------------------------------
    # LEGACY INTERFACE
    # ------------------------------------------------------------------
    async def analyze_symptoms(self, input_data: AnalysisInput) -> AnalysisResult:
        symptom_analysis = await self.analyze_symptoms_structured(input_data)
        risk_assessment = await self.analyze_risk_structured(symptom_analysis.model_dump())
        specialist = await self.analyze_specialist_structured(risk_assessment)
        report = await self.generate_health_report_structured(symptom_analysis.model_dump(), risk_assessment, specialist)
        return AnalysisResult(
            analysis_id=str(uuid.uuid4()),
            risk_assessment=risk_assessment,
            specialist_recommendation=specialist,
            health_report=report,
            emergency_alert=risk_assessment.risk_level == "HIGH",
        )

    async def generate_report(self, analysis_result: AnalysisResult) -> Dict[str, Any]:
        return {
            "report_id": str(uuid.uuid4()),
            "analysis_id": analysis_result.analysis_id,
            "status": "Report generated successfully",
        }

    async def health_check(self) -> bool:
        return True
