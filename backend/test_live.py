import urllib.request, json

req = urllib.request.Request(
    "http://localhost:8000/api/v1/analysis",
    data=json.dumps({"symptoms": "im having heart attack"}).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)
res = urllib.request.urlopen(req)
d = json.loads(res.read().decode("utf-8"))["data"]
print("Risk:", d["risk_level"])
print("Specialist:", d["specialist"])
print("Emergency:", d["emergency"])
print("Instructions:", d["emergency_instructions"])
