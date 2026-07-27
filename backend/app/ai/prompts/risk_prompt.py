"""Risk assessment prompt template."""


def get_risk_assessment_prompt(symptoms: str, analyzed_symptoms: str = None) -> str:
    """
    Generate risk assessment prompt for AI model.

    Returns a prompt that instructs the LLM to assess clinical risk and provide
    structured JSON output with risk level, confidence, reasoning, and the
    warning signs the patient should watch for.
    """
    prompt = f"""You are an experienced clinical triage AI assistant. Assess the risk level for the following patient presentation.

PATIENT SYMPTOMS:
{symptoms}

"""

    if analyzed_symptoms:
        prompt += f"PRIOR SYMPTOM ANALYSIS:\n{analyzed_symptoms}\n\n"

    prompt += """ASSESSMENT INSTRUCTIONS:
1. Determine the overall risk level: "low", "moderate", or "high"
2. State the clinical reasoning behind that risk level
3. List warning signs that would require the patient to seek urgent care
4. Provide an overall confidence level (0-100) for your assessment

RESPONSE FORMAT:
Provide your response as valid JSON with the following structure:
{
  "risk_level": "moderate",
  "confidence": 85,
  "reasoning": "Concise clinical reasoning for the assigned risk level",
  "warning_signs": ["difficulty breathing", "chest pain"]
}

IMPORTANT:
- Return ONLY valid JSON, no additional text
- risk_level: exactly one of "low", "moderate", "high" (lowercase)
- confidence: integer 0-100 representing assessment confidence
- reasoning: one or two sentence clinical justification
- warning_signs: list of red-flag symptoms that warrant urgent medical attention

Begin your assessment:"""

    return prompt
