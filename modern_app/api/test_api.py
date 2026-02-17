"""Quick API integration test — run while the FastAPI server is up on port 8000."""
import requests

BASE = "http://localhost:8000"


def test_health():
    r = requests.get(f"{BASE}/api/health")
    assert r.status_code == 200
    print("  Health:", r.json())


def test_login_success():
    r = requests.post(f"{BASE}/api/auth/login", json={"username": "parent1", "password": "pass1234"})
    assert r.status_code == 200
    data = r.json()
    assert data["role"] == "parent"
    assert data["student_id"] == "01"
    print(f"  Login OK: role={data['role']}, student_id={data['student_id']}")
    return data["access_token"]


def test_login_failure():
    r = requests.post(f"{BASE}/api/auth/login", json={"username": "parent1", "password": "wrong"})
    assert r.status_code == 401
    print(f"  Bad login rejected: {r.status_code}")


def test_parent_own_student(token):
    r = requests.get(f"{BASE}/api/students/01", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    print(f"  Parent sees own student: {r.json().get('Student Name')}")


def test_parent_blocked_from_other(token):
    r = requests.get(f"{BASE}/api/students/02", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 403
    print(f"  Parent blocked from other student: {r.json().get('detail')}")


def test_unauthenticated():
    r = requests.get(f"{BASE}/api/students/")
    assert r.status_code == 401
    print(f"  Unauthenticated blocked: {r.status_code}")


def test_teacher_summary():
    r = requests.post(f"{BASE}/api/auth/login", json={"username": "teacher", "password": "admin1234"})
    token = r.json()["access_token"]
    r2 = requests.get(f"{BASE}/api/students/01/summary", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    summary = r2.json()
    sentiment = summary["overall_sentiment"]
    print(f"  Teacher summary: {sentiment['label']} ({sentiment['compound']:.2f})")
    print(f"  Categories: {list(summary['category_scores'].keys())}")
    return token


def test_analytics(token):
    r = requests.get(f"{BASE}/api/analytics/class", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    data = r.json()
    print(f"  Class analytics: {data['total_students']} students")


if __name__ == "__main__":
    print("=" * 50)
    print("FASTAPI BACKEND — INTEGRATION TESTS")
    print("=" * 50)

    print("\n1. Health check")
    test_health()

    print("\n2. Login (valid)")
    parent_token = test_login_success()

    print("\n3. Login (invalid)")
    test_login_failure()

    print("\n4. Parent accesses own student")
    test_parent_own_student(parent_token)

    print("\n5. Parent blocked from other student")
    test_parent_blocked_from_other(parent_token)

    print("\n6. Unauthenticated access blocked")
    test_unauthenticated()

    print("\n7. Teacher gets student summary")
    teacher_token = test_teacher_summary()

    print("\n8. Teacher gets class analytics")
    test_analytics(teacher_token)

    print("\n" + "=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
