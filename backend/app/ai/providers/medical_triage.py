"""Medical Triage Knowledge Base for intelligent symptom-to-risk classification.

Based on clinical emergency triage protocols (ESI, Manchester Triage, WHO ICD-11).
Each entry maps a symptom/condition phrase to its risk level, specialist, affected body system,
severity indicators, and warning signs.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TriageEntry:
    """A single triage classification entry."""
    risk_level: str  # "high", "moderate", "low"
    specialist: str
    urgency: str
    affected_system: str
    severity_indicators: List[str] = field(default_factory=list)
    warning_signs: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# MASTER TRIAGE DATABASE
# Keys are lowercase phrases. Order matters: longer/more-specific phrases
# are checked first via the lookup function.
# ---------------------------------------------------------------------------

TRIAGE_DB: dict[str, TriageEntry] = {
    # ===== CARDIOVASCULAR — HIGH RISK =====
    "heart attack": TriageEntry("high", "Cardiologist / Emergency Medicine", "Immediate / Call 911", "Cardiovascular",
        ["Acute myocardial infarction suspected"], ["Crushing chest pain radiating to arm/jaw", "Cold sweat", "Nausea with chest pressure"]),
    "myocardial infarction": TriageEntry("high", "Cardiologist / Emergency Medicine", "Immediate / Call 911", "Cardiovascular",
        ["Acute MI suspected"], ["ST-elevation on ECG", "Troponin elevation"]),
    "cardiac arrest": TriageEntry("high", "Emergency Medicine / ICU", "Immediate / Call 911", "Cardiovascular",
        ["No pulse detected", "Loss of consciousness"], ["Begin CPR immediately", "Use AED if available"]),
    "chest pain": TriageEntry("high", "Cardiologist / Emergency Medicine", "Immediate / Call 911", "Cardiovascular",
        ["Possible acute coronary syndrome"], ["Pain radiating to left arm or jaw", "Shortness of breath with chest pain"]),
    "chest tightness": TriageEntry("high", "Cardiologist / Emergency Medicine", "Immediate / Call 911", "Cardiovascular",
        ["Possible angina or ACS"], ["Worsening with exertion", "Associated diaphoresis"]),
    "chest pressure": TriageEntry("high", "Cardiologist / Emergency Medicine", "Immediate / Call 911", "Cardiovascular",
        ["Possible cardiac event"], ["Pressure lasting >10 minutes", "Radiating to neck or back"]),
    "arrhythmia": TriageEntry("high", "Cardiologist", "Immediate", "Cardiovascular",
        ["Irregular heart rhythm"], ["Palpitations with syncope", "Rapid or very slow heart rate"]),
    "palpitations": TriageEntry("moderate", "Cardiologist", "24-48 hours", "Cardiovascular",
        ["Heart rhythm irregularity"], ["Associated dizziness", "Episodes lasting >30 minutes"]),
    "high blood pressure": TriageEntry("moderate", "Cardiologist / GP", "24-48 hours", "Cardiovascular",
        ["Hypertension detected"], ["BP >180/120 requires ER", "Headache with vision changes"]),
    "hypertension": TriageEntry("moderate", "Cardiologist / GP", "24-48 hours", "Cardiovascular",
        ["Elevated blood pressure"], ["Persistent readings above 140/90"]),
    "low blood pressure": TriageEntry("moderate", "Cardiologist / GP", "24-48 hours", "Cardiovascular",
        ["Hypotension"], ["Dizziness on standing", "Fainting episodes"]),

    # ===== NEUROLOGICAL — HIGH RISK =====
    "stroke": TriageEntry("high", "Neurologist / Emergency Medicine", "Immediate / Call 911", "Neurological",
        ["Acute cerebrovascular event"], ["Sudden facial drooping", "Arm weakness", "Speech difficulty (FAST)"]),
    "seizure": TriageEntry("high", "Neurologist / Emergency Medicine", "Immediate", "Neurological",
        ["Seizure activity"], ["Duration >5 min requires 911", "First-time seizure"]),
    "unconscious": TriageEntry("high", "Emergency Medicine", "Immediate / Call 911", "Neurological",
        ["Loss of consciousness"], ["Unresponsive to stimuli", "Check airway and breathing"]),
    "unresponsive": TriageEntry("high", "Emergency Medicine", "Immediate / Call 911", "Neurological",
        ["Patient unresponsive"], ["Begin emergency assessment"]),
    "fainting": TriageEntry("high", "Neurologist / Cardiologist", "Immediate", "Neurological / Cardiovascular",
        ["Syncope episode"], ["May indicate cardiac arrhythmia", "Head injury risk from fall"]),
    "fainted": TriageEntry("high", "Neurologist / Cardiologist", "Immediate", "Neurological / Cardiovascular",
        ["Syncope episode"], ["Evaluate for cardiac cause", "Check for head trauma"]),
    "collapse": TriageEntry("high", "Emergency Medicine", "Immediate / Call 911", "Neurological / Cardiovascular",
        ["Sudden collapse"], ["Assess consciousness and pulse"]),
    "paralysis": TriageEntry("high", "Neurologist / Emergency Medicine", "Immediate / Call 911", "Neurological",
        ["Acute motor deficit — possible stroke"], ["Sudden onset = stroke until proven otherwise"]),
    "numbness in face": TriageEntry("high", "Neurologist / Emergency Medicine", "Immediate", "Neurological",
        ["Possible TIA or stroke"], ["FAST assessment needed"]),
    "slurred speech": TriageEntry("high", "Neurologist / Emergency Medicine", "Immediate / Call 911", "Neurological",
        ["Possible stroke"], ["Sudden onset speech difficulty"]),
    "confusion": TriageEntry("high", "Neurologist / Emergency Medicine", "Immediate", "Neurological",
        ["Altered mental status"], ["Sudden confusion may indicate stroke or metabolic emergency"]),
    "severe headache": TriageEntry("high", "Neurologist / Emergency Medicine", "Immediate", "Neurological",
        ["Thunderclap headache — rule out SAH"], ["Worst headache of life", "Sudden onset"]),
    "thunderclap headache": TriageEntry("high", "Neurologist / Emergency Medicine", "Immediate / Call 911", "Neurological",
        ["Possible subarachnoid hemorrhage"], ["Sudden explosive headache"]),
    "meningitis": TriageEntry("high", "Infectious Disease / Emergency Medicine", "Immediate", "Neurological / Infectious",
        ["Suspected meningitis"], ["Neck stiffness with fever", "Photophobia", "Petechial rash"]),
    "migraine": TriageEntry("moderate", "Neurologist", "24-48 hours", "Neurological",
        ["Migraine episode"], ["Aura symptoms", "Sensitivity to light/sound"]),
    "headache": TriageEntry("low", "GP / Neurologist", "1-2 weeks", "Neurological",
        ["Tension-type or mild headache"], ["Monitor for worsening or recurring pattern"]),

    # ===== RESPIRATORY — HIGH RISK =====
    "not breathing": TriageEntry("high", "Emergency Medicine / ICU", "Immediate / Call 911", "Respiratory",
        ["Respiratory arrest"], ["Begin rescue breathing / CPR"]),
    "can't breathe": TriageEntry("high", "Emergency Medicine / Pulmonologist", "Immediate / Call 911", "Respiratory",
        ["Acute respiratory failure"], ["Severe dyspnea", "Cyanosis"]),
    "choking": TriageEntry("high", "Emergency Medicine", "Immediate / Call 911", "Respiratory",
        ["Airway obstruction"], ["Perform Heimlich maneuver"]),
    "shortness of breath": TriageEntry("high", "Pulmonologist / Emergency Medicine", "Immediate", "Respiratory",
        ["Acute dyspnea"], ["Oxygen saturation <94%", "Worsening at rest"]),
    "difficulty breathing": TriageEntry("high", "Pulmonologist / Emergency Medicine", "Immediate", "Respiratory",
        ["Respiratory distress"], ["Use of accessory muscles", "Inability to speak full sentences"]),
    "breathing difficulty": TriageEntry("high", "Pulmonologist / Emergency Medicine", "Immediate", "Respiratory",
        ["Respiratory distress"], ["Rapid shallow breathing"]),
    "asthma attack": TriageEntry("high", "Pulmonologist / Emergency Medicine", "Immediate", "Respiratory",
        ["Acute asthma exacerbation"], ["Inhaler not relieving symptoms", "Severe wheezing"]),
    "pneumonia": TriageEntry("high", "Pulmonologist / GP", "Immediate to 24 hours", "Respiratory",
        ["Lung infection"], ["High fever with productive cough", "Chest X-ray infiltrates"]),
    "pulmonary embolism": TriageEntry("high", "Pulmonologist / Emergency Medicine", "Immediate / Call 911", "Respiratory / Cardiovascular",
        ["Blood clot in lung"], ["Sudden chest pain with dyspnea", "Recent surgery or immobility"]),
    "coughing blood": TriageEntry("high", "Pulmonologist / Emergency Medicine", "Immediate", "Respiratory",
        ["Hemoptysis"], ["May indicate PE, TB, or malignancy"]),
    "wheezing": TriageEntry("moderate", "Pulmonologist / GP", "24-48 hours", "Respiratory",
        ["Bronchospasm"], ["Worsening at night", "Triggered by allergens"]),
    "bronchitis": TriageEntry("moderate", "Pulmonologist / GP", "24-48 hours", "Respiratory",
        ["Bronchial inflammation"], ["Persistent productive cough"]),
    "cough": TriageEntry("low", "GP", "1-2 weeks", "Respiratory",
        ["Upper respiratory symptom"], ["Monitor if persists >2 weeks"]),
    "cold": TriageEntry("low", "GP", "Self-care / 1-2 weeks", "Respiratory",
        ["Common cold / URTI"], ["Rest and hydration"]),
    "runny nose": TriageEntry("low", "GP", "Self-care", "Respiratory / ENT",
        ["Rhinorrhea"], ["Likely viral or allergic"]),
    "sore throat": TriageEntry("low", "GP / ENT", "1-2 weeks", "Respiratory / ENT",
        ["Pharyngitis"], ["Test for strep if severe"]),

    # ===== ALLERGIC / IMMUNE — HIGH RISK =====
    "anaphylaxis": TriageEntry("high", "Emergency Medicine / Allergist", "Immediate / Call 911", "Immune / Allergic",
        ["Anaphylactic shock"], ["Use EpiPen immediately", "Swelling of airway"]),
    "allergic reaction": TriageEntry("high", "Emergency Medicine / Allergist", "Immediate", "Immune / Allergic",
        ["Severe allergic response"], ["Monitor for anaphylaxis progression"]),
    "swollen throat": TriageEntry("high", "Emergency Medicine / ENT", "Immediate / Call 911", "Respiratory / Allergic",
        ["Airway compromise risk"], ["Difficulty swallowing or breathing"]),
    "swollen tongue": TriageEntry("high", "Emergency Medicine", "Immediate / Call 911", "Respiratory / Allergic",
        ["Angioedema — airway risk"], ["May progress to airway obstruction"]),
    "hives": TriageEntry("moderate", "Allergist / Dermatologist", "24-48 hours", "Immune / Dermatological",
        ["Urticaria"], ["Watch for progression to anaphylaxis"]),

    # ===== ABDOMINAL / GI =====
    "appendicitis": TriageEntry("high", "Surgeon / Emergency Medicine", "Immediate", "Gastrointestinal",
        ["Possible appendicitis"], ["RLQ pain with rebound tenderness", "Fever", "Risk of rupture"]),
    "vomiting blood": TriageEntry("high", "Gastroenterologist / Emergency Medicine", "Immediate / Call 911", "Gastrointestinal",
        ["Upper GI bleed"], ["Hematemesis — may indicate ulcer or variceal bleed"]),
    "blood in stool": TriageEntry("high", "Gastroenterologist / Emergency Medicine", "Immediate", "Gastrointestinal",
        ["GI hemorrhage"], ["Dark tarry stools or bright red blood"]),
    "severe abdominal pain": TriageEntry("high", "Surgeon / Emergency Medicine", "Immediate", "Gastrointestinal",
        ["Acute abdomen"], ["Rigid abdomen", "Rebound tenderness"]),
    "abdominal pain": TriageEntry("moderate", "Gastroenterologist / GP", "24-48 hours", "Gastrointestinal",
        ["Abdominal discomfort"], ["Localize the pain", "Watch for fever"]),
    "stomach pain": TriageEntry("moderate", "Gastroenterologist / GP", "24-48 hours", "Gastrointestinal",
        ["Epigastric discomfort"], ["May indicate gastritis or ulcer"]),
    "stomach ache": TriageEntry("moderate", "Gastroenterologist / GP", "24-48 hours", "Gastrointestinal",
        ["Epigastric discomfort"], ["Watch for fever or severe pain"]),
    "diarrhea": TriageEntry("low", "GP / Gastroenterologist", "1-2 weeks", "Gastrointestinal",
        ["Loose stools"], ["Hydrate well", "Seek care if bloody or >3 days"]),
    "constipation": TriageEntry("low", "GP", "1-2 weeks", "Gastrointestinal",
        ["Bowel irregularity"], ["Increase fiber and water intake"]),
    "nausea": TriageEntry("low", "GP", "1-2 weeks", "Gastrointestinal",
        ["Nausea without vomiting"], ["Monitor for dehydration"]),
    "vomiting": TriageEntry("moderate", "GP / Emergency Medicine", "24-48 hours", "Gastrointestinal",
        ["Active vomiting"], ["Risk of dehydration", "Seek care if persistent"]),
    "acid reflux": TriageEntry("low", "Gastroenterologist / GP", "1-2 weeks", "Gastrointestinal",
        ["GERD symptoms"], ["Avoid trigger foods"]),
    "heartburn": TriageEntry("low", "Gastroenterologist / GP", "1-2 weeks", "Gastrointestinal",
        ["Acid reflux symptom"], ["Rule out cardiac cause if persistent"]),

    # ===== TRAUMA / INJURY =====
    "severe bleeding": TriageEntry("high", "Emergency Medicine / Surgeon", "Immediate / Call 911", "Trauma",
        ["Active hemorrhage"], ["Apply direct pressure", "Tourniquet for limb"]),
    "bleeding": TriageEntry("moderate", "Emergency Medicine / GP", "Immediate to 24 hours", "Trauma",
        ["Active bleeding"], ["Assess volume and source"]),
    "broken bone": TriageEntry("high", "Orthopedic Surgeon / Emergency Medicine", "Immediate", "Musculoskeletal",
        ["Fracture suspected"], ["Immobilize the limb", "Do not attempt to realign"]),
    "fracture": TriageEntry("high", "Orthopedic Surgeon / Emergency Medicine", "Immediate", "Musculoskeletal",
        ["Bone fracture"], ["X-ray required", "Pain and deformity"]),
    "head injury": TriageEntry("high", "Neurosurgeon / Emergency Medicine", "Immediate / Call 911", "Neurological / Trauma",
        ["Traumatic brain injury risk"], ["Monitor consciousness", "Nausea/vomiting after injury"]),
    "concussion": TriageEntry("high", "Neurologist / Emergency Medicine", "Immediate", "Neurological",
        ["Mild traumatic brain injury"], ["Confusion or amnesia after impact"]),
    "burn": TriageEntry("moderate", "Emergency Medicine / Dermatologist", "Immediate to 24 hours", "Dermatological / Trauma",
        ["Burn injury"], ["Assess degree and body surface area"]),
    "sprain": TriageEntry("low", "Orthopedic / GP", "24-48 hours", "Musculoskeletal",
        ["Ligament strain"], ["RICE protocol: Rest, Ice, Compression, Elevation"]),

    # ===== METABOLIC / ENDOCRINE =====
    "diabetic emergency": TriageEntry("high", "Endocrinologist / Emergency Medicine", "Immediate / Call 911", "Endocrine",
        ["Diabetic ketoacidosis or hypoglycemia"], ["Check blood glucose immediately"]),
    "low blood sugar": TriageEntry("high", "Endocrinologist / Emergency Medicine", "Immediate", "Endocrine",
        ["Hypoglycemia"], ["Give glucose/sugar immediately", "Loss of consciousness risk"]),
    "high blood sugar": TriageEntry("high", "Endocrinologist / Emergency Medicine", "Immediate", "Endocrine",
        ["Hyperglycemia — possible DKA"], ["Check for ketones", "Fruity breath odor"]),
    "diabetes": TriageEntry("moderate", "Endocrinologist / GP", "24-48 hours", "Endocrine",
        ["Diabetes management"], ["Regular glucose monitoring"]),
    "thyroid": TriageEntry("moderate", "Endocrinologist", "1-2 weeks", "Endocrine",
        ["Thyroid disorder"], ["Check TSH levels"]),

    # ===== MENTAL HEALTH =====
    "suicidal": TriageEntry("high", "Psychiatrist / Emergency Medicine", "Immediate / Call 988", "Mental Health",
        ["CRITICAL: Suicidal ideation"], ["Call 988 Suicide & Crisis Lifeline", "Do NOT leave person alone"]),
    "suicide": TriageEntry("high", "Psychiatrist / Emergency Medicine", "Immediate / Call 988", "Mental Health",
        ["CRITICAL: Suicide risk"], ["Call 988 Suicide & Crisis Lifeline immediately"]),
    "self harm": TriageEntry("high", "Psychiatrist / Emergency Medicine", "Immediate", "Mental Health",
        ["Self-harm behavior"], ["Seek immediate professional help"]),
    "overdose": TriageEntry("high", "Emergency Medicine / Toxicology", "Immediate / Call 911", "Toxicology / Mental Health",
        ["Drug overdose"], ["Call Poison Control: 1-800-222-1222"]),
    "panic attack": TriageEntry("moderate", "Psychiatrist / GP", "24-48 hours", "Mental Health",
        ["Acute anxiety episode"], ["Rule out cardiac cause", "Breathing exercises"]),
    "anxiety": TriageEntry("moderate", "Psychiatrist / Psychologist", "1-2 weeks", "Mental Health",
        ["Anxiety disorder"], ["Consider therapy and/or medication"]),
    "depression": TriageEntry("moderate", "Psychiatrist / Psychologist", "1-2 weeks", "Mental Health",
        ["Depressive symptoms"], ["Screen for suicidal ideation"]),
    "insomnia": TriageEntry("low", "Psychiatrist / GP", "1-2 weeks", "Mental Health",
        ["Sleep difficulty"], ["Sleep hygiene counseling"]),

    # ===== INFECTIONS =====
    "sepsis": TriageEntry("high", "Emergency Medicine / ICU", "Immediate / Call 911", "Infectious / Systemic",
        ["Systemic infection — sepsis"], ["Fever with altered mental status", "Rapid heart rate"]),
    "high fever": TriageEntry("high", "Emergency Medicine / GP", "Immediate", "Infectious / Systemic",
        ["Pyrexia >103°F / 39.4°C"], ["Risk of febrile seizure", "Assess for source of infection"]),
    "fever": TriageEntry("moderate", "GP", "24-48 hours", "Infectious / Systemic",
        ["Elevated body temperature"], ["Monitor for >3 days", "Hydrate well"]),
    "infection": TriageEntry("moderate", "GP / Infectious Disease", "24-48 hours", "Infectious",
        ["Active infection"], ["May need antibiotics"]),
    "covid": TriageEntry("moderate", "Pulmonologist / GP", "24-48 hours", "Respiratory / Infectious",
        ["COVID-19 symptoms"], ["Monitor oxygen saturation", "Isolate"]),
    "flu": TriageEntry("low", "GP", "Self-care / 1-2 weeks", "Respiratory / Infectious",
        ["Influenza symptoms"], ["Rest and fluids", "Antivirals within 48 hours"]),

    # ===== KIDNEY / UROLOGICAL =====
    "kidney failure": TriageEntry("high", "Nephrologist / Emergency Medicine", "Immediate", "Renal",
        ["Acute renal failure"], ["Decreased urine output", "Swelling"]),
    "kidney stone": TriageEntry("high", "Urologist / Emergency Medicine", "Immediate", "Renal",
        ["Renal colic"], ["Severe flank pain", "Blood in urine"]),
    "blood in urine": TriageEntry("high", "Urologist / Nephrologist", "Immediate to 24 hours", "Renal / Urological",
        ["Hematuria"], ["May indicate stone, infection, or malignancy"]),
    "urinary tract infection": TriageEntry("moderate", "Urologist / GP", "24-48 hours", "Urological",
        ["UTI symptoms"], ["Burning urination", "Frequency"]),
    "uti": TriageEntry("moderate", "Urologist / GP", "24-48 hours", "Urological",
        ["Urinary tract infection"], ["Burning urination"]),

    # ===== SKIN =====
    "rash": TriageEntry("low", "Dermatologist / GP", "1-2 weeks", "Dermatological",
        ["Skin rash"], ["Monitor for spreading or fever"]),
    "itching": TriageEntry("low", "Dermatologist / GP", "1-2 weeks", "Dermatological",
        ["Pruritus"], ["May be allergic or dermatologic"]),
    "acne": TriageEntry("low", "Dermatologist", "1-2 weeks", "Dermatological",
        ["Acne vulgaris"], ["Topical treatment"]),

    # ===== MUSCULOSKELETAL =====
    "back pain": TriageEntry("moderate", "Orthopedic / GP", "24-48 hours", "Musculoskeletal",
        ["Back pain"], ["Red flags: numbness, bowel/bladder changes"]),
    "joint pain": TriageEntry("moderate", "Rheumatologist / Orthopedic", "1-2 weeks", "Musculoskeletal",
        ["Arthralgia"], ["Check for swelling, redness"]),
    "muscle pain": TriageEntry("low", "GP / Orthopedic", "1-2 weeks", "Musculoskeletal",
        ["Myalgia"], ["Rest and OTC pain relief"]),
    "neck pain": TriageEntry("moderate", "Orthopedic / Neurologist", "24-48 hours", "Musculoskeletal",
        ["Cervical pain"], ["Rule out trauma or meningitis if with fever"]),

    # ===== EYES / ENT =====
    "sudden vision loss": TriageEntry("high", "Ophthalmologist / Emergency Medicine", "Immediate", "Ophthalmological",
        ["Acute vision loss"], ["Possible retinal detachment or stroke"]),
    "eye pain": TriageEntry("moderate", "Ophthalmologist", "24-48 hours", "Ophthalmological",
        ["Ocular pain"], ["Check for glaucoma or foreign body"]),
    "ear pain": TriageEntry("low", "ENT / GP", "1-2 weeks", "ENT",
        ["Otalgia"], ["May indicate otitis"]),

    # ===== GENERAL / MILD =====
    "fatigue": TriageEntry("low", "GP", "1-2 weeks", "General / Systemic",
        ["General fatigue"], ["Check thyroid, anemia, depression"]),
    "dizziness": TriageEntry("moderate", "Neurologist / ENT", "24-48 hours", "Neurological / ENT",
        ["Vertigo or lightheadedness"], ["Rule out BPPV, cardiac, or neurological cause"]),
    "weakness": TriageEntry("moderate", "Neurologist / GP", "24-48 hours", "Neurological / General",
        ["Generalized weakness"], ["Check for stroke signs if sudden"]),
    "weight loss": TriageEntry("moderate", "GP / Oncologist", "1-2 weeks", "General / Systemic",
        ["Unexplained weight loss"], ["Screen for malignancy, thyroid, diabetes"]),
    "swelling": TriageEntry("moderate", "GP", "24-48 hours", "General / Cardiovascular",
        ["Edema"], ["Check for DVT if leg swelling"]),
    "dehydration": TriageEntry("moderate", "Emergency Medicine / GP", "24-48 hours", "General / Systemic",
        ["Fluid deficit"], ["Oral or IV rehydration"]),
    "sneezing": TriageEntry("low", "GP / Allergist", "Self-care", "Respiratory / ENT",
        ["Allergic or viral rhinitis"], ["Antihistamines if allergic"]),
    "hiccups": TriageEntry("low", "GP", "Self-care", "General",
        ["Diaphragm spasm"], ["Usually self-limiting"]),

    # ===== POISONING =====
    "poisoning": TriageEntry("high", "Emergency Medicine / Toxicology", "Immediate / Call 911", "Toxicology",
        ["Toxic ingestion"], ["Call Poison Control: 1-800-222-1222"]),
    "snake bite": TriageEntry("high", "Emergency Medicine", "Immediate / Call 911", "Toxicology / Trauma",
        ["Envenomation"], ["Immobilize limb", "Do NOT apply tourniquet"]),
    "drug reaction": TriageEntry("high", "Emergency Medicine / Allergist", "Immediate", "Immune / Toxicology",
        ["Adverse drug reaction"], ["May progress to anaphylaxis"]),

    # ===== PREGNANCY =====
    "pregnancy bleeding": TriageEntry("high", "OB-GYN / Emergency Medicine", "Immediate", "Obstetric",
        ["Vaginal bleeding in pregnancy"], ["Possible miscarriage or ectopic"]),
    "labor pains": TriageEntry("high", "OB-GYN", "Immediate", "Obstetric",
        ["Active labor"], ["Contractions <5 min apart"]),
    "pregnancy": TriageEntry("moderate", "OB-GYN", "1-2 weeks", "Obstetric",
        ["Prenatal care needed"], ["Schedule first prenatal visit"]),

    # ===== CANCER =====
    "cancer": TriageEntry("high", "Oncologist", "Immediate to 1 week", "Oncological",
        ["Malignancy suspected or diagnosed"], ["Urgent staging and treatment planning"]),
    "tumor": TriageEntry("high", "Oncologist / Surgeon", "Immediate to 1 week", "Oncological",
        ["Mass detected"], ["Biopsy and imaging required"]),
    "lump": TriageEntry("moderate", "GP / Oncologist", "1-2 weeks", "General / Oncological",
        ["Palpable mass"], ["Evaluate with imaging"]),
}


def lookup_triage(text: str) -> tuple[Optional[TriageEntry], Optional[str]]:
    """Look up the HIGHEST-risk matching triage entry for the given text.

    Checks all entries and returns the one with the highest risk level.
    Returns (entry, matched_keyword) or (None, None) if no match.
    """
    text_lower = text.lower()

    best_entry: Optional[TriageEntry] = None
    best_keyword: Optional[str] = None
    risk_priority = {"high": 3, "moderate": 2, "low": 1}

    for keyword, entry in TRIAGE_DB.items():
        if keyword in text_lower:
            entry_priority = risk_priority.get(entry.risk_level, 0)
            best_priority = risk_priority.get(best_entry.risk_level, 0) if best_entry else 0
            if entry_priority > best_priority:
                best_entry = entry
                best_keyword = keyword
            elif entry_priority == best_priority and best_keyword and len(keyword) > len(best_keyword):
                # Prefer longer (more specific) match at same risk level
                best_entry = entry
                best_keyword = keyword

    return best_entry, best_keyword


def collect_all_matches(text: str) -> list[tuple[str, TriageEntry]]:
    """Collect ALL matching triage entries for the given text, sorted by risk (highest first)."""
    text_lower = text.lower()
    risk_priority = {"high": 3, "moderate": 2, "low": 1}
    matches = []
    for keyword, entry in TRIAGE_DB.items():
        if keyword in text_lower:
            matches.append((keyword, entry))
    matches.sort(key=lambda x: risk_priority.get(x[1].risk_level, 0), reverse=True)
    return matches


# Group keywords by BODY PART and by SYMPTOM TYPE, then check for co-occurrence
CARDIAC_TERMS = [
    "heart", "chest", "cardiac", "sternum", "breastbone"
]
PAIN_TERMS = [
    "pain", "ache", "aching", "hurt", "hurts", "hurting", "pressure", 
    "tightness", "tight", "squeezing", "burning", "discomfort", "heavy", "heaviness"
]
BREATH_TERMS = [
    "breath", "breathing", "breathe", "gasping", "suffocating", "choking"
]
NEURO_TERMS = [
    "stroke", "slurred", "droop", "numbness", "numb", "weakness", "confusion"
]
CONSCIOUSNESS_TERMS = [
    "unconscious", "fainted", "fainting", "passed out", "seizure", "convulsing"
]

EXPLICIT_EMERGENCY_PHRASES = [
    "heart attack", "myocardial infarction", "cardiac arrest", 
    "anaphylaxis", "overdose", "suicidal", "can't breathe", "cant breathe"
]

def detect_emergency(text: str) -> tuple[bool, list[str]]:
    text_lower = text.lower()
    flags = []

    # 1. Explicit phrase match (fast path)
    for phrase in EXPLICIT_EMERGENCY_PHRASES:
        if phrase in text_lower:
            flags.append(phrase)

    # 2. Conceptual match: body part + symptom co-occurring anywhere in the text
    #    e.g. "pain in my heart", "heart hurts", "chest feels tight"
    has_cardiac_area = any(term in text_lower for term in CARDIAC_TERMS)
    has_pain = any(term in text_lower for term in PAIN_TERMS)
    if has_cardiac_area and has_pain:
        flags.append(f"cardiac-area pain (matched region + pain terms)")

    has_breath_issue = any(term in text_lower for term in BREATH_TERMS)
    if has_breath_issue and ("difficult" in text_lower or "can't" in text_lower 
                               or "cant" in text_lower or "short" in text_lower):
        flags.append("breathing difficulty")

    if any(term in text_lower for term in NEURO_TERMS):
        flags.append("neurological red flag")

    if any(term in text_lower for term in CONSCIOUSNESS_TERMS):
        flags.append("loss of consciousness / seizure")

    return (len(flags) > 0, flags)
