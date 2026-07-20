"""Symptom analysis prompt template."""


def get_symptom_analysis_prompt(symptoms: str, medical_history: str = None) -> str:
    """
    Generate symptom analysis prompt for AI model.

    TODO: Implement actual prompt engineering.
    """
    prompt = f"""
    Analyze the following health symptoms:

    Symptoms: {symptoms}
    """

    if medical_history:
        prompt += f"\nMedical History: {medical_history}"

    prompt += "\n\nTODO: Implement symptom analysis logic."

    return prompt
