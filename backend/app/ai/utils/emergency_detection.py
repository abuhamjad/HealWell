import re

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

# Regex helper to match whole words only
def contains_word(text: str, word: str) -> bool:
    return bool(re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE))

def find_word_matches(text: str, words: list[str]) -> list[tuple[str, int, int]]:
    """Returns list of (matched_word, start_idx, end_idx) for exact word boundary matches."""
    matches = []
    for word in words:
        pattern = r'\b' + re.escape(word) + r'\b'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            matches.append((word, match.start(), match.end()))
    return matches

NEGATION_PREFIXES = [
    "no", "not", "without", "denies", "denied", "never", "zero", 
    "free of", "negative for", "neither", "nor", "don't have", "dont have", "didn't have", "didnt have"
]

RESOLVED_SUFFIXES = [
    "went away", "resolved", "disappeared", "subsided", "healed", "gone", "stopped"
]

HYPOTHETICAL_PREFIXES = [
    "worried i might", "fear of", "scared of", "afraid of", "might get", "someday", "risk of getting"
]

EMOTIONAL_CONTEXT = [
    "breakup", "divorce", "grief", "sad", "relationship", "ex-boyfriend", "ex-girlfriend", "heartbroken"
]

def is_negated_or_non_current(text: str, match_start: int, match_end: int) -> bool:
    """Checks if a match is negated, past/resolved, or purely hypothetical."""
    text_lower = text.lower()
    
    # Check 35 chars before match for negation/hypothetical
    prefix_start = max(0, match_start - 35)
    prefix = text_lower[prefix_start:match_start]
    
    # Check 35 chars after match for resolved status
    suffix_end = min(len(text_lower), match_end + 35)
    suffix = text_lower[match_end:suffix_end]

    # 1. Negation prefix
    for neg in NEGATION_PREFIXES:
        if re.search(r'\b' + re.escape(neg) + r'\b', prefix):
            return True

    # 2. Resolved suffix
    for res in RESOLVED_SUFFIXES:
        if re.search(r'\b' + re.escape(res) + r'\b', suffix) or re.search(r'\b' + re.escape(res) + r'\b', prefix):
            return True

    # 3. Hypothetical / Anxiety context
    for hyp in HYPOTHETICAL_PREFIXES:
        if hyp in prefix or hyp in suffix:
            return True

    return False

def detect_emergency(text: str) -> tuple[bool, list[str]]:
    text_lower = text.lower()
    flags = []

    # 1. Explicit phrase match (fast path with word boundary & negation check)
    for phrase in EXPLICIT_EMERGENCY_PHRASES:
        pattern = r'\b' + re.escape(phrase) + r'\b'
        for match in re.finditer(pattern, text_lower):
            if not is_negated_or_non_current(text_lower, match.start(), match.end()):
                flags.append(phrase)

    # If explicit phrase matched, return early
    if flags:
        return (True, flags)

    # 2. Check for emotional / breakup context (e.g. "heartbroken about my breakup")
    is_emotional = any(contains_word(text_lower, word) for word in EMOTIONAL_CONTEXT) or "heartbroken" in text_lower
    if is_emotional:
        return (False, [])

    # 3. Check for cough-induced chest soreness context (e.g. "chest hurts from coughing all day")
    is_cough_induced = ("cough" in text_lower or "coughing" in text_lower) and ("from coughing" in text_lower or "after coughing" in text_lower or "coughing all day" in text_lower)

    # 4. Conceptual match: body part + symptom co-occurring with word boundaries
    cardiac_matches = find_word_matches(text_lower, CARDIAC_TERMS)
    pain_matches = find_word_matches(text_lower, PAIN_TERMS)

    # Filter out negated cardiac or pain matches
    valid_cardiac = [m for m in cardiac_matches if not is_negated_or_non_current(text_lower, m[1], m[2])]
    valid_pain = [m for m in pain_matches if not is_negated_or_non_current(text_lower, m[1], m[2])]

    if valid_cardiac and valid_pain and not is_cough_induced:
        flags.append("cardiac-area pain (matched region + pain terms)")

    breath_matches = find_word_matches(text_lower, BREATH_TERMS)
    valid_breath = [m for m in breath_matches if not is_negated_or_non_current(text_lower, m[1], m[2])]
    
    if valid_breath and ("difficult" in text_lower or "can't" in text_lower or "cant" in text_lower or "short" in text_lower):
        if not is_negated_or_non_current(text_lower, valid_breath[0][1], valid_breath[0][2]):
            flags.append("breathing difficulty")

    neuro_matches = find_word_matches(text_lower, NEURO_TERMS)
    valid_neuro = [m for m in neuro_matches if not is_negated_or_non_current(text_lower, m[1], m[2])]
    if valid_neuro:
        flags.append("neurological red flag")

    conscious_matches = find_word_matches(text_lower, CONSCIOUSNESS_TERMS)
    valid_conscious = [m for m in conscious_matches if not is_negated_or_non_current(text_lower, m[1], m[2])]
    if valid_conscious:
        flags.append("loss of consciousness / seizure")

    return (len(flags) > 0, flags)

def classify_specificity(text: str) -> str:
    text_lower = text.lower()
    words = text_lower.split()
    
    generic_terms = ["problem", "issue", "not feeling well", "something wrong", "off", "weird", "sick"]
    has_generic = any(re.search(r'\b' + re.escape(term) + r'\b', text_lower) for term in generic_terms)
    
    specific_terms = PAIN_TERMS + BREATH_TERMS + NEURO_TERMS + CONSCIOUSNESS_TERMS + CARDIAC_TERMS + [
        "fever", "cough", "headache", "heartburn", "stomach", "bleed", "bleeding", "vomit", "vomiting", "diarrhea", "rash", "dizziness"
    ]
    has_specific = any(re.search(r'\b' + re.escape(term) + r'\b', text_lower) for term in specific_terms)
    has_duration = any(term in text_lower for term in ["day", "days", "hour", "hours", "week", "weeks", "month", "months", "year", "years", "since", "ago"])

    # VAGUE if (short <= 5 words AND no specific symptom/duration) OR (generic terms AND no specific symptom/duration)
    if (len(words) <= 5 and not (has_specific or has_duration)) or (has_generic and not (has_specific or has_duration)):
        return "VAGUE"
        
    return "SPECIFIC"
