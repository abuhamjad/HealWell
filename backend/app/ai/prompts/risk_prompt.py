"""Risk assessment prompt template."""


def get_risk_assessment_prompt(symptoms: str, analyzed_symptoms: str = None) -> str:
    """
    Generate risk assessment prompt for AI model.

    TODO: Implement actual risk assessment logic.
    """
    prompt = f"""
    Assess the risk level for the following symptoms:

    Symptoms: {symptoms}
    """

    if analyzed_symptoms:
        prompt += f"\nAnalysis: {analyzed_symptoms}"

    prompt += "\n\nTODO: Implement risk assessment logic."

    return prompt
