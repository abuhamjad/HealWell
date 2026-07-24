"""Specialist recommendation prompt template."""


def get_specialist_recommendation_prompt(risk_assessment: dict) -> str:
    """
    Generate specialist recommendation prompt for AI model.

    Returns a prompt that instructs the LLM to recommend appropriate healthcare
    professionals based on risk assessment results.
    """
    risk_level = risk_assessment.get("risk_level", "moderate")
    reasoning = risk_assessment.get("reasoning", "")
    warning_signs = risk_assessment.get("warning_signs", [])

    prompt = f"""You are an experienced medical triage AI. Recommend the most appropriate healthcare specialist based on the following risk assessment.

RISK ASSESSMENT:
Risk Level: {risk_level}
Reasoning: {reasoning}

WARNING SIGNS:
{chr(10).join("- " + sign for sign in warning_signs) if warning_signs else "- None identified"}

SPECIALIST RECOMMENDATION TASK:
1. Determine the most appropriate medical specialist for this patient
2. Provide clinical reasoning for the recommendation
3. Suggest appropriate urgency level for the appointment

VALID SPECIALISTS:
- General Practitioner (GP) - Initial assessment and coordination
- Internal Medicine - General medical conditions
- Cardiologist - Cardiac and cardiovascular issues
- Pulmonologist - Respiratory and lung conditions
- Neurologist - Nervous system and neurological issues
- Gastroenterologist - Digestive system conditions
- Rheumatologist - Autoimmune and joint disorders
- Endocrinologist - Metabolic and hormonal conditions
- Infectious Disease - Infections and communicable diseases
- Emergency Medicine - Immediate/life-threatening conditions

URGENCY LEVELS (select exactly one):
- immediate: Life-threatening or severe condition requiring emergency care
- 24-48 hours: Significant symptoms requiring prompt professional evaluation
- 1-2 weeks: Moderate symptoms requiring specialist consultation
- routine: Stable condition requiring standard follow-up care

RESPONSE FORMAT (RETURN ONLY VALID JSON):
{{
  "specialist": "Specialist Name",
  "reasoning": "2-3 sentence explanation of specialist choice based on risk assessment",
  "specialist_explanation": "In patient-friendly language, explain why this specialist. Connect to their actual symptoms. What does this specialist treat? 1-2 sentences.",
  "urgency": "immediate|24-48 hours|1-2 weeks|routine"
}}

IMPORTANT:
- specialist: Must be one of the valid specialists listed
- reasoning: Should reference the risk level and warning signs
- urgency: Must be exactly one of the four options listed
- Return ONLY valid JSON, no additional text

Begin recommendation:"""

    return prompt
