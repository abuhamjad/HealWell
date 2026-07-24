"""Health report generation prompt template."""


def get_health_report_prompt(
    symptom_analysis: dict,
    risk_assessment: dict,
    specialist_recommendation: dict,
) -> str:
    """
    Generate comprehensive health report prompt for AI model.

    Creates a synthesis prompt that combines symptom analysis, risk assessment,
    and specialist recommendation into a patient-friendly health guidance report.
    """
    detected_symptoms = symptom_analysis.get("detected_symptoms", [])
    symptom_summary = symptom_analysis.get("summary", "")
    severity_indicators = symptom_analysis.get("severity_indicators", [])
    affected_systems = symptom_analysis.get("affected_systems", [])

    risk_level = risk_assessment.get("risk_level", "moderate")
    risk_reasoning = risk_assessment.get("reasoning", "")
    warning_signs = risk_assessment.get("warning_signs", [])

    specialist = specialist_recommendation.get("specialist", "General Practitioner")
    specialist_reasoning = specialist_recommendation.get("reasoning", "")
    urgency = specialist_recommendation.get("urgency", "routine")

    prompt = f"""You are a patient education AI. Based on the complete medical analysis below, generate a comprehensive but patient-friendly health guidance report.

ANALYSIS SUMMARY:

DETECTED SYMPTOMS:
{chr(10).join("- " + s for s in detected_symptoms) if detected_symptoms else "- None reported"}

CLINICAL SUMMARY:
{symptom_summary}

SEVERITY INDICATORS:
{chr(10).join("- " + s for s in severity_indicators) if severity_indicators else "- None identified"}

AFFECTED BODY SYSTEMS:
{chr(10).join("- " + s for s in affected_systems) if affected_systems else "- Not determined"}

RISK ASSESSMENT:
Risk Level: {risk_level}
Clinical Reasoning: {risk_reasoning}

WARNING SIGNS:
{chr(10).join("- " + s for s in warning_signs) if warning_signs else "- None identified"}

SPECIALIST RECOMMENDATION:
Recommended Professional: {specialist}
Reasoning: {specialist_reasoning}
Appointment Urgency: {urgency}

REPORT GENERATION TASK:

Create a comprehensive health guidance report that:
1. Summarizes the findings in clear, patient-friendly language
2. Explains the clinical significance of the symptoms
3. Provides practical home care recommendations
4. Suggests lifestyle modifications
5. Lists warning signs requiring immediate attention
6. Clearly directs to the recommended specialist
7. Emphasizes that this is not a diagnosis but guidance for professional care

Use cautious, non-diagnostic language like "may indicate", "suggests", "could be consistent with".
Do NOT make definitive diagnoses.
Do NOT recommend specific medications.
Do NOT claim medical certainty.

RESPONSE FORMAT (RETURN ONLY VALID JSON):
{{
  "summary": "1-2 paragraph clinical summary of findings",
  "summary_explanation": "Patient-friendly plain language explanation of what we found. Start with 'Based on your symptoms...' Explain in simple terms.",
  "confidence_explanation": "Placeholder - will be filled from risk assessment",
  "risk_explanation": "Placeholder - will be filled from risk assessment",
  "specialist_explanation": "Placeholder - will be filled from specialist recommendation",
  "home_care": ["recommendation 1", "recommendation 2"],
  "personalized_home_care": ["Specific home care 1 for this patient's symptoms", "Specific home care 2 for this patient's symptoms", "Specific home care 3"],
  "lifestyle": ["suggestion 1", "suggestion 2"],
  "personalized_lifestyle": ["Lifestyle modification 1 specific to their condition", "Lifestyle modification 2 specific to their condition"],
  "monitoring": ["monitor 1", "monitor 2"],
  "monitoring_guidance": ["Specific warning sign 1 - explain what it means", "Specific warning sign 2 - explain when to seek help", "Specific warning sign 3"],
  "emergency_instructions": null,
  "references": ["reference 1", "reference 2"]
}}

IMPORTANT:
- summary: Clinical synthesis of findings
- summary_explanation: PLAIN LANGUAGE for patient. What did we find? Why is it important? 2-3 sentences. No medical jargon.
- confidence_explanation: Restate why we have confidence in this assessment based on symptom patterns.
- risk_explanation: Restate why this risk level based on specific symptoms.
- specialist_explanation: Restate why this specialist is appropriate for these symptoms.
- personalized_home_care: CRITICAL - These must be specific to THIS patient's actual symptoms. Not generic. Each recommendation must explain why it helps for their condition.
- personalized_lifestyle: CRITICAL - Specific to their diagnosis/symptoms. Not generic health tips.
- monitoring_guidance: CRITICAL - Specific warning signs for this patient's condition. Explain what each means and when to seek help.
- emergency_instructions: null (set to null always)
- home_care, lifestyle, monitoring, references: Keep for backward compatibility
- Use clear, accessible language throughout
- NO generic recommendations like "rest" or "stay hydrated" without explaining why for THIS patient
- Emphasize need for professional medical evaluation
- Return ONLY valid JSON, no additional text

PERSONALIZATION CRITICAL:
This patient's symptoms: {detected_symptoms}
This patient's affected systems: {affected_systems}
Risk level: {risk_level}
Specialist: {specialist}

ALL personalized fields MUST reference their actual symptoms.
NO generic advice.
NO default arrays.

Begin report generation:"""

    return prompt
