"""Automated triage test suite for HealWell AI backend."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

tests = [
    # --- Direct HIGH Risk (Emergency Keywords/Phrases) ---
    ("im having heart attack", "HIGH", None),
    ("pain in my heart", "HIGH", None),
    ("my heart hurts", "HIGH", None),
    ("chest feels really tight", "HIGH", None),
    ("shortness of breath, gasping for air", "HIGH", None),
    ("slurred speech and sudden weakness on left side", "HIGH", None),

    # --- Subtle / Contextual HIGH Risk ---
    ("left arm numb, face feels weird when i smile", "HIGH", None),

    # --- False-Positive Edge Cases (Must NOT be HIGH) ---
    ("i have heartburn after eating spicy food", "LOW", None),
    ("i have heartburn", "LOW", None),
    ("my chest hurts from coughing all day", "LOW", None),
    ("i feel heartbroken about my breakup", "LOW", None),
    ("no chest pain, just feeling tired", "LOW", None),
    ("chest pain went away yesterday", "LOW", None),
    ("worried i might get a heart attack someday", "LOW", None),

    # --- Vague Inputs (Must be MODERATE with needs_followup=True) ---
    ("im having brain problem", "MODERATE", True),
    ("not feeling well", "MODERATE", True),
    ("sick", "MODERATE", True),

    # --- Specific MODERATE Cases ---
    ("vomiting and diarrhea for 3 days, feeling weak", "MODERATE", None),
    ("fever of 102 for two days", "MODERATE", None),

    # --- LOW Risk Specific Cases ---
    ("mild headache for a day", "LOW", None),
    ("slight cough, 2 days", "LOW", None),
]


def run_tests():
    print("Running automated triage regression test suite...\n")
    passed = 0
    failed = 0

    for text, expected_risk, expected_followup in tests:
        res = client.post("/api/v1/analysis", json={"symptoms": text})
        assert res.status_code == 200, f"HTTP Error {res.status_code}: {res.text}"
        data = res.json()["data"]

        rl = data["risk_level"].upper()
        conf = data["confidence"]
        needs_followup = data.get("needs_followup", False)
        provider_used = data.get("provider_used", "unknown")

        # Check risk level
        if rl != expected_risk:
            print(f"FAIL | Expected {expected_risk:<8} | Got {rl:<8} | Input: '{text}'")
            failed += 1
            continue

        # Check needs_followup if specified
        if expected_followup is not None and needs_followup != expected_followup:
            print(f"FAIL | Expected needs_followup={expected_followup} | Got {needs_followup} | Input: '{text}'")
            failed += 1
            continue

        print(f"PASS | Risk: {rl:<8} | Conf: {conf:<4.2f} | Followup: {str(needs_followup):<5} | Provider: {provider_used:<6} | Input: '{text}'")
        passed += 1

    print(f"\nTest Summary: {passed} PASSED, {failed} FAILED out of {len(tests)} tests.")
    assert failed == 0, f"{failed} test(s) failed."


if __name__ == "__main__":
    run_tests()
