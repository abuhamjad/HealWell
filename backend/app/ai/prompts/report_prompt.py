"""Health report generation prompt template."""


def get_health_report_prompt(
    symptoms: str,
    risk_level: str = None,
    specialist: str = None,
) -> str:
    """
    Generate health report prompt for AI model.

    TODO: Implement actual report generation logic.
    """
    prompt = f"""
    Generate a comprehensive health report for:

    Symptoms: {symptoms}
    """

    if risk_level:
        prompt += f"\nRisk Level: {risk_level}"

    if specialist:
        prompt += f"\nRecommended Specialist: {specialist}"

    prompt += "\n\nTODO: Implement health report generation logic."

    return prompt
