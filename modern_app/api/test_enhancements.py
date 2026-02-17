"""Test the new enhancement endpoints."""
import requests
import json

BASE = "http://localhost:8000"

# Login as teacher
r = requests.post(f"{BASE}/api/auth/login", json={"username": "teacher", "password": "admin1234"})
tok = r.json()["access_token"]
h = {"Authorization": f"Bearer {tok}"}

# ---- Test 1: Individual reviews ----
print("=== Individual Reviews ===")
r = requests.get(f"{BASE}/api/students/01/reviews", headers=h)
data = r.json()
print(f"Status: {r.status_code}")
fs = data["final_score"]
print(f"Total reviews: {fs['total_reviews']}")
print(f"Final score: {fs['label']} ({fs['compound']})")
for rev in data["reviews"][:3]:
    label = rev["sentiment"]["label"]
    comp = rev["sentiment"]["compound"]
    text = rev["text"][:60]
    print(f"  [{rev['date']}] {label} ({comp:.2f}) - {text}...")
assert r.status_code == 200
assert fs["total_reviews"] >= 1
print("PASS\n")

# ---- Test 2: Edit student details ----
print("=== Edit Details ===")
r = requests.put(f"{BASE}/api/students/01/details", headers=h, json={
    "name": "Test Student",
    "grade": "10th Grade",
    "archetype": "Scholar",
})
print(f"Status: {r.status_code}, Response: {r.json()}")
assert r.status_code == 200

# Verify change
r = requests.get(f"{BASE}/api/students/01", headers=h)
s = r.json()
print(f"Updated: {s['Student Name']}, {s['Grade']}, {s['Archetype']}")
assert s["Student Name"] == "Test Student"
assert s["Grade"] == "10th Grade"
assert s["Archetype"] == "Scholar"

# Revert
requests.put(f"{BASE}/api/students/01/details", headers=h, json={
    "name": "Aarav Sharma",
    "grade": "5th Grade",
    "archetype": "Creative Explorer",
})
r = requests.get(f"{BASE}/api/students/01", headers=h)
s = r.json()
print(f"Reverted: {s['Student Name']}, {s['Grade']}, {s['Archetype']}")
assert s["Student Name"] == "Aarav Sharma"
print("PASS\n")

# ---- Test 3: Analytics with student_sentiments ----
print("=== Analytics Drill-Down ===")
r = requests.get(f"{BASE}/api/analytics/class", headers=h)
data = r.json()
print(f"Status: {r.status_code}")
print(f"student_sentiments present: {'student_sentiments' in data}")
ss = data.get("student_sentiments", [])
print(f"Total: {len(ss)} students")
assert "student_sentiments" in data
assert len(ss) > 0
sample = ss[0]
print(f"Sample: {sample['name']} - {sample['label']} ({sample['compound']:.2f})")
assert "id" in sample
assert "name" in sample
assert "compound" in sample
assert "label" in sample
print("PASS\n")

print("=" * 50)
print("ALL NEW ENDPOINT TESTS PASSED!")
print("=" * 50)
