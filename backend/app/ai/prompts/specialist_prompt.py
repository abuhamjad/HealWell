"""Specialist recommendation prompt template."""


def get_specialist_recommendation_prompt(symptoms: str, risk_level: str = None) -> str:
    """
    Generate specialist recommendation prompt for AI model.

    Returns a prompt that instructs the LLM to select the most appropriate
    medical specialist and provide structured JSON output with the specialist,
    the clinical reasoning, and the consultation urgency.
    """
    prompt = f"""You are an experienced medical triage AI assistant. Recommend the most appropriate medical specialist for the following patient presentation.

PATIENT SYMPTOMS:
{symptoms}

"""

    if risk_level:
        prompt += f"ASSESSED RISK LEVEL:\n{risk_level}\n\n"

    prompt += """RECOMMENDATION INSTRUCTIONS:
1. Identify the single most appropriate specialist for this presentation
2. State the clinical reasoning for choosing that specialist
3. Determine how soon the consultation should happen

RESPONSE FORMAT:
Provide your response as valid JSON with the following structure:
{
  "specialist": "Cardiologist",
  "reasoning": "Concise clinical reasoning for this specialist choice",
  "urgency": "24-48 hours"
}

IMPORTANT:
- Return ONLY valid JSON, no additional text
- specialist: a single specialist title (e.g. "General Physician", "Cardiologist", "Pulmonologist")
- reasoning: one or two sentence clinical justification
- urgency: exactly one of "immediate", "24-48 hours", "1-2 weeks"

Begin your recommendation:"""

    return prompt
