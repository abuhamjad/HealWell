"""Health report generation prompt template."""


def get_health_report_prompt(
    symptoms: str,
    risk_level: str = None,
    specialist: str = None,
) -> str:
    """
    Generate health report prompt for AI model.

    Returns a prompt that instructs the LLM to produce a patient-facing health
    report as structured JSON with a summary explanation, personalized home
    care, personalized lifestyle guidance, monitoring guidance, and references.
    """
    prompt = f"""You are an experienced medical AI assistant writing a patient-facing health report. Base the report on the following case.

PATIENT SYMPTOMS:
{symptoms}

"""

    if risk_level:
        prompt += f"ASSESSED RISK LEVEL:\n{risk_level}\n\n"

    if specialist:
        prompt += f"RECOMMENDED SPECIALIST:\n{specialist}\n\n"

    prompt += """REPORT INSTRUCTIONS:
1. Write a short plain-language summary explaining what the symptoms suggest
2. Give personalized home care steps the patient can follow now
3. Give personalized lifestyle adjustments relevant to this presentation
4. Give monitoring guidance: what to track, and the red-flag signs that mean
   the patient must seek emergency care immediately (state these explicitly)
5. List reputable general medical references for further reading

RESPONSE FORMAT:
Provide your response as valid JSON with the following structure:
{
  "summary": "Plain-language explanation of what these symptoms suggest",
  "home_care": ["Rest and stay hydrated", "Use a humidifier"],
  "lifestyle": ["Avoid strenuous activity", "Stop smoking"],
  "monitoring": ["Track temperature twice daily", "Seek emergency care immediately if breathing becomes difficult"],
  "references": ["WHO guidelines on respiratory infections"]
}

IMPORTANT:
- Return ONLY valid JSON, no additional text
- summary: two to four sentences, addressed to the patient, no diagnosis claims
- home_care, lifestyle, monitoring, references: lists of short strings
- monitoring MUST include explicit emergency instructions telling the patient
  when to seek immediate medical attention, scaled to the risk level
- references: names of reputable sources or guidelines, not invented URLs
- Do not omit any field

Begin your report:"""

    return prompt
