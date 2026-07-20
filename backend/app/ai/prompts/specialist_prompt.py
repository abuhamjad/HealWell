"""Specialist recommendation prompt template."""


def get_specialist_recommendation_prompt(symptoms: str, risk_level: str = None) -> str:
    """
    Generate specialist recommendation prompt for AI model.

    TODO: Implement actual specialist matching logic.
    """
    prompt = f"""
    Recommend the appropriate medical specialist for:

    Symptoms: {symptoms}
    """

    if risk_level:
        prompt += f"\nRisk Level: {risk_level}"

    prompt += "\n\nTODO: Implement specialist recommendation logic."

    return prompt
