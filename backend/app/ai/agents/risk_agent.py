"""Risk assessment agent."""

import logging
from typing import Any
from app.ai.agents.base import BaseAgent
from app.ai.providers.factory import create_provider

logger = logging.getLogger(__name__)


class RiskAgent(BaseAgent):
    """Agent for risk assessment using AI provider."""

    def __init__(self):
        """Initialize risk agent."""
        super().__init__(name="RiskAgent")

    async def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Assess health risk using AI provider and update workflow state.

        Reads symptom_analysis from state, calls provider for structured
        risk assessment, and updates state with results.

        Args:
            state: HealthAnalysisState containing symptom_analysis

        Returns:
            Updated state with risk_assessment results
        """
        try:
            symptom_analysis = state.get("symptom_analysis", {})

            if not symptom_analysis:
                logger.warning("No symptom_analysis in state, using empty fallback")
                symptom_analysis = {
                    "detected_symptoms": [],
                    "summary": "No symptom analysis available",
                    "severity_indicators": [],
                    "affected_systems": [],
                }

            provider = create_provider()
            await provider.initialize()

            risk_result = await provider.analyze_risk_structured(symptom_analysis)

            # Safety Guardrail: use medical triage DB to enforce correct risk
            from app.ai.providers.medical_triage import lookup_triage
            from app.ai.utils.emergency_detection import detect_emergency, classify_specificity
            
            user_input = (state.get("user_input") or "")
            symptom_summary = str(symptom_analysis.get("summary", ""))
            detected_str = " ".join(symptom_analysis.get("detected_symptoms", []))
            full_text = f"{user_input} {symptom_summary} {detected_str}"

            eval_text = user_input if user_input else full_text

            # Check emergency first
            is_emergency, red_flags = detect_emergency(eval_text)
            
            # Then specificity
            specificity = classify_specificity(eval_text)
            
            # Always force HIGH if emergency
            if is_emergency:
                logger.warning(f"Safety guardrail: detect_emergency triggered on '{', '.join(red_flags)}'. Overriding provider result to HIGH.")
                risk_result.risk_level = "HIGH"
                risk_result.confidence = max(risk_result.confidence, 0.95)
                risk_result.emergency_alert = True
                risk_result.instructions = "CALL EMERGENCY SERVICES (911) IMMEDIATELY."
                risk_result.reasoning = f"Evaluated as HIGH RISK — Emergency red flags detected: {', '.join(red_flags)}"
                risk_result.needs_followup = False
                current_flags = set(getattr(risk_result, 'red_flags_detected', []))
                current_flags.update(red_flags)
                risk_result.red_flags_detected = list(current_flags)
            elif specificity == "VAGUE":
                logger.warning("Safety guardrail: vague input detected, escalating from LOW (if any) to MODERATE.")
                if risk_result.risk_level == "LOW":
                    risk_result.risk_level = "MODERATE"
                    risk_result.confidence = 0.40
                    risk_result.emergency_alert = False
                    risk_result.instructions = "Please describe your symptoms in more detail: what exactly you feel, where, for how long, and how severe it is. Seek immediate care if symptoms are severe, sudden, or worsening."
                    risk_result.reasoning = "Symptoms provided are too vague for an accurate assessment."
                    risk_result.needs_followup = True
            else:
                # If neither emergency nor vague, do a standard medical triage lookup to see if we missed a high risk
                triage_entry, matched_kw = lookup_triage(full_text)
                if triage_entry and triage_entry.risk_level == "high" and risk_result.risk_level != "HIGH":
                    logger.warning(f"Safety guardrail: triage DB matched '{matched_kw}' as HIGH risk. Overriding provider result.")
                    risk_result.risk_level = "HIGH"
                    risk_result.confidence = max(risk_result.confidence, 0.95)
                    risk_result.emergency_alert = True
                    risk_result.instructions = "CALL EMERGENCY SERVICES (911) IMMEDIATELY."
                    risk_result.reasoning = f"Evaluated as HIGH RISK — {matched_kw.title()} is a potentially life-threatening condition."
                    risk_result.needs_followup = False
                    current_flags = set(getattr(risk_result, 'red_flags_detected', []))
                    current_flags.update(triage_entry.warning_signs)
                    risk_result.red_flags_detected = list(current_flags)

            state["risk_assessment"] = risk_result
            state["current_step"] = "risk_assessment"
            state["workflow_status"] = "risk_assessment_complete"

            logger.info(
                f"Risk assessment completed: risk_level={risk_result.risk_level}, "
                f"confidence={risk_result.confidence}%"
            )

        except Exception as e:
            logger.error(f"Risk assessment failed: {e}. Using MockProvider fallback.")
            state["errors"] = state.get("errors", []) + [f"Risk assessment error: {str(e)}"]
            state["current_step"] = "risk_assessment_fallback"
            from app.ai.providers.mock_provider import MockProvider
            mock_provider = MockProvider()
            symptom_analysis = state.get("symptom_analysis", {})
            risk_result = await mock_provider.analyze_risk_structured(symptom_analysis)
            state["risk_assessment"] = risk_result

        return state


