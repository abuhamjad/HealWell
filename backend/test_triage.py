from fastapi.testclient import TestClient
from app.main import app
c = TestClient(app)

tests = [
    ("im having heart attack", "HIGH"),
    ("pain in my heart", "HIGH"),
    ("my heart hurts", "HIGH"),
    ("chest feels really tight", "HIGH"),
    ("cant breath properly", "HIGH"),
    ("stroke symptoms face drooping", "HIGH"),
    ("seizure and unconscious", "HIGH"),
    ("severe bleeding from wound", "HIGH"),
    ("anaphylaxis cant breathe", "HIGH"),
    ("suicidal thoughts", "HIGH"),
    ("i have a headache", "LOW"),
    ("mild cough for 2 days", "LOW"),
    ("stomach ache after eating", "MODERATE"),
    ("mild cough and runny nose", "LOW"),
    ("fever and nausea", "MODERATE"),
]

print("Running automated triage regression tests...\n")
passed = 0
for text, expected in tests:
    r = c.post("/api/v1/analysis", json={"symptoms": text})
    d = r.json()["data"]
    rl = d["risk_level"].upper()
    conf = d["confidence"]
    spec = d["specialist"]
    
    assert rl == expected, f"FAILED: '{text}' → got {rl}, expected {expected}"
    print(f"PASS | {rl:>8} | {conf:>4}% | {text}")
    passed += 1

print(f"\nAll {passed} tests passed successfully!")
