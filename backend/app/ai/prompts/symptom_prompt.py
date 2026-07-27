"""Symptom analysis prompt template."""

import json


def get_symptom_analysis_prompt(symptoms: str, medical_history: str = None, medications: list = None, allergies: list = None) -> str:
    """
    Generate symptom analysis prompt for AI model.

    Returns a prompt that instructs the LLM to analyze symptoms and provide
    structured JSON output with detected symptoms, severity assessment, and
    affected body systems.
    """
    prompt = f"""You are an experienced healthcare AI assistant. Analyze the following patient symptoms and provide a structured medical assessment.

PATIENT SYMPTOMS:
{symptoms}

"""

    if medical_history:
        prompt += f"MEDICAL HISTORY:\n{medical_history}\n\n"

    if medications:
        prompt += f"CURRENT MEDICATIONS:\n- " + "\n- ".join(medications) + "\n\n"

    if allergies:
        prompt += f"KNOWN ALLERGIES:\n- " + "\n- ".join(allergies) + "\n\n"

    prompt += """ANALYSIS INSTRUCTIONS:
1. Identify specific symptoms mentioned by the patient
2. Assess the severity and urgency of each symptom
3. Identify which body systems are likely affected
4. Provide an overall confidence level (0-100) for your assessment
5. Summarize the key findings

RESPONSE FORMAT:
Provide your response as valid JSON with the following structure:
{
  "detected_symptoms": ["symptom1", "symptom2", "symptom3"],
  "confidence": 85,
  "summary": "Brief assessment of the patient's condition based on reported symptoms",
  "severity_indicators": ["high fever", "persistent cough"],
  "affected_systems": ["respiratory", "immune"]
}

IMPORTANT:
- Return ONLY valid JSON, no additional text
- detected_symptoms: list of specific symptoms in lowercase
- confidence: integer 0-100 representing analysis confidence
- summary: one or two sentence clinical summary
- severity_indicators: list of concerning findings that may need urgent attention
- affected_systems: list of affected body systems (respiratory, cardiovascular, gastrointestinal, nervous, etc.)

Begin your analysis:"""

    return prompt
