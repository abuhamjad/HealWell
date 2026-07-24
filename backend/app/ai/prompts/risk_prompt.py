"""Risk assessment prompt template."""


def get_risk_assessment_prompt(symptom_analysis: dict) -> str:
    """
    Generate risk assessment prompt for AI model.

    Returns a prompt that instructs the LLM to assess medical risk based on
    symptom analysis and return structured JSON with risk level, confidence,
    reasoning, and warning signs.
    """
    detected_symptoms = symptom_analysis.get("detected_symptoms", [])
    summary = symptom_analysis.get("summary", "")
    severity_indicators = symptom_analysis.get("severity_indicators", [])
    affected_systems = symptom_analysis.get("affected_systems", [])

    prompt = f"""You are an experienced medical risk assessment AI. Evaluate the health risk based on the following symptom analysis.

DETECTED SYMPTOMS:
- {chr(10).join(detected_symptoms) if detected_symptoms else "None reported"}

SUMMARY:
{summary}

SEVERITY INDICATORS:
- {chr(10).join(severity_indicators) if severity_indicators else "None identified"}

AFFECTED BODY SYSTEMS:
- {chr(10).join(affected_systems) if affected_systems else "Not determined"}

RISK ASSESSMENT TASK:
1. Determine the overall health risk level (low, moderate, high)
2. Assess your confidence in this assessment (0-100)
3. Provide medical reasoning for the risk level
4. Identify any warning signs that require urgent attention

RESPONSE FORMAT (RETURN ONLY VALID JSON):
{{
  "risk_level": "low|moderate|high",
  "confidence": 85,
  "reasoning": "Detailed medical reasoning for the risk assessment",
  "risk_explanation": "In patient-friendly language (no medical jargon), explain WHY this risk level based on their symptoms. 2-3 sentences.",
  "confidence_explanation": "Explain why this confidence level. What symptom patterns support it? What remains uncertain? 2-3 sentences.",
  "warning_signs": ["urgent sign 1", "urgent sign 2"]
}}

IMPORTANT:
- risk_level: Must be exactly "low", "moderate", or "high"
- confidence: Integer 0-100 representing assessment confidence
- reasoning: 2-3 sentence clinical reasoning
- warning_signs: List of findings that may require urgent medical attention
- Return ONLY valid JSON, no additional text

Begin assessment:"""

    return prompt
