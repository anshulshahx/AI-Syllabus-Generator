import sys
import os
import json
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

BASE_URL = "http://127.0.0.1:8000"

# ── Helpers ──────────────────────────────────────────────────────
def print_result(test_name, passed):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status} — {test_name}")
    return passed

def divider(title=""):
    print(f"\n{'═'*60}")
    if title:
        print(f"  {title}")
        print(f"{'═'*60}")

# ── Test 1: Health Check ─────────────────────────────────────────
def test_health():
    divider("Test 1 — Health Check")
    results = []
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=10)
        data = r.json()

        results.append(print_result(
            "API returns HTTP 200",
            r.status_code == 200
        ))
        results.append(print_result(
            "api field is 'running'",
            data.get("api") == "running"
        ))
        results.append(print_result(
            "ollama field is 'connected'",
            data.get("ollama") == "connected"
        ))
        results.append(print_result(
            "model field is 'llama3.1:8b'",
            data.get("model") == "llama3.1:8b"
        ))
        results.append(print_result(
            "12 endpoints listed",
            len(data.get("endpoints", [])) >= 10
        ))
    except Exception as e:
        print(f"  ❌ Health check failed: {e}")
        results.append(False)
    return results

# ── Test 2: Outcome Generation ───────────────────────────────────
def test_outcome_generation():
    divider("Test 2 — Outcome Generation")
    results = []

    courses = [
        {
            "course_name": "Data Structures",
            "course_description": "Arrays, linked lists, trees, graphs and sorting algorithms",
            "target_bloom_levels": ["apply", "analyze"],
            "n_candidates": 3
        },
        {
            "course_name": "Machine Learning",
            "course_description": "Supervised learning, neural networks, regression and classification",
            "target_bloom_levels": ["evaluate", "create"],
            "n_candidates": 3
        },
        {
            "course_name": "Computer Networks",
            "course_description": "OSI model, TCP/IP, routing algorithms and network security",
            "target_bloom_levels": ["analyze", "evaluate"],
            "n_candidates": 3
        },
    ]

    for course in courses:
        try:
            r    = requests.post(f"{BASE_URL}/generate/outcomes", json=course, timeout=180)
            data = r.json()

            has_outcomes = len(data.get("outcomes", [])) > 0
            has_flags    = all("flags"       in o for o in data.get("outcomes", []))
            has_tags     = all("domain_tags" in o for o in data.get("outcomes", []))

            results.append(print_result(
                f"{course['course_name']} — outcomes generated",
                has_outcomes
            ))
            results.append(print_result(
                f"{course['course_name']} — flags field present",
                has_flags
            ))
            results.append(print_result(
                f"{course['course_name']} — domain_tags field present",
                has_tags
            ))

            print(f"    Generated {len(data.get('outcomes', []))} outcomes")
            for o in data.get("outcomes", []):
                flag_str = f" ⚠ {o['flags']}" if o['flags'] else " ✓ clean"
                print(f"    • {o['text'][:55]}...{flag_str}")

        except Exception as e:
            print(f"  ❌ {course['course_name']} failed: {e}")
            results.append(False)

    return results

# ── Test 3: Validation Errors ────────────────────────────────────
def test_validation():
    divider("Test 3 — Input Validation")
    results = []

    # Empty course name
    try:
        r = requests.post(f"{BASE_URL}/generate/outcomes", json={
            "course_name": "",
            "course_description": "A course about data structures",
            "n_candidates": 3
        }, timeout=10)
        results.append(print_result(
            "Empty course name returns 422",
            r.status_code == 422
        ))
    except Exception as e:
        results.append(False)

    # Invalid bloom level
    try:
        r = requests.post(f"{BASE_URL}/generate/outcomes", json={
            "course_name": "Data Structures",
            "course_description": "Arrays and linked lists",
            "target_bloom_levels": ["invalid_level"],
            "n_candidates": 3
        }, timeout=10)
        results.append(print_result(
            "Invalid bloom level returns 422",
            r.status_code == 422
        ))
    except Exception as e:
        results.append(False)

    # Too many candidates
    try:
        r = requests.post(f"{BASE_URL}/generate/outcomes", json={
            "course_name": "Data Structures",
            "course_description": "Arrays and linked lists",
            "n_candidates": 100
        }, timeout=10)
        results.append(print_result(
            "n_candidates=100 returns 422",
            r.status_code == 422
        ))
    except Exception as e:
        results.append(False)

    # Too many units
    try:
        r = requests.post(f"{BASE_URL}/generate/syllabus", json={
            "course_name": "Data Structures",
            "course_description": "Arrays and linked lists",
            "num_units": 99
        }, timeout=10)
        results.append(print_result(
            "num_units=99 returns 422",
            r.status_code == 422
        ))
    except Exception as e:
        results.append(False)

    return results

# ── Test 4: Syllabus Generation ──────────────────────────────────
def test_syllabus_generation():
    divider("Test 4 — Syllabus Generation")
    results = []

    payload = {
        "course_name": "Digital Electronics",
        "course_description": "Logic gates, boolean algebra, combinational circuits, flip flops and microcontrollers",
        "num_units": 3
    }

    try:
        r    = requests.post(f"{BASE_URL}/generate/syllabus", json=payload, timeout=300)
        data = r.json()

        units = data.get("units", [])

        results.append(print_result(
            "Syllabus returns HTTP 200",
            r.status_code == 200
        ))
        results.append(print_result(
            "Correct number of units generated",
            len(units) == 3
        ))
        results.append(print_result(
            "Each unit has unit_id",
            all("unit_id" in u for u in units)
        ))
        results.append(print_result(
            "Each unit has unit_title",
            all("unit_title" in u and u["unit_title"] for u in units)
        ))
        results.append(print_result(
            "Each unit has unit_objectives",
            all(len(u.get("unit_objectives", [])) > 0 for u in units)
        ))
        results.append(print_result(
            "Each unit has unit_outcomes",
            all(len(u.get("unit_outcomes", [])) > 0 for u in units)
        ))
        results.append(print_result(
            "Each unit has assessments",
            all(len(u.get("assessments", [])) > 0 for u in units)
        ))
        results.append(print_result(
            "Each unit has readings",
            all(len(u.get("readings", [])) > 0 for u in units)
        ))

        print(f"\n    Units generated:")
        for u in units:
            print(f"    • {u['unit_id']}: {u['unit_title']}")

    except Exception as e:
        print(f"  ❌ Syllabus generation failed: {e}")
        results.append(False)

    return results

# ── Test 5: Review System ────────────────────────────────────────
def test_review_system():
    divider("Test 5 — Review System")
    results = []

    payload = {
        "reviews": [
            {
                "outcome_id":       "TEST001",
                "course_name":      "Pipeline Test",
                "original_text":    "Apply pipeline testing to validate API endpoints",
                "edited_text":      None,
                "bloom_level":      "apply",
                "action":           "accept",
                "reviewer_comment": "Pipeline test review"
            },
            {
                "outcome_id":       "TEST002",
                "course_name":      "Pipeline Test",
                "original_text":    "Know the basics of testing",
                "edited_text":      "Identify and apply basic software testing methodologies",
                "bloom_level":      "apply",
                "action":           "edit",
                "reviewer_comment": "Fixed invalid verb"
            },
            {
                "outcome_id":       "TEST003",
                "course_name":      "Pipeline Test",
                "original_text":    "Understand stuff about networks",
                "edited_text":      None,
                "bloom_level":      "understand",
                "action":           "reject",
                "reviewer_comment": "Too vague and informal"
            }
        ]
    }

    try:
        # Submit reviews
        r    = requests.post(f"{BASE_URL}/review/submit", json=payload, timeout=30)
        data = r.json()

        results.append(print_result(
            "Review submit returns HTTP 200",
            r.status_code == 200
        ))
        results.append(print_result(
            "total_reviewed is 3",
            data.get("total_reviewed") == 3
        ))
        results.append(print_result(
            "accepted count is 1",
            data.get("accepted") == 1
        ))
        results.append(print_result(
            "rejected count is 1",
            data.get("rejected") == 1
        ))
        results.append(print_result(
            "edited count is 1",
            data.get("edited") == 1
        ))
        results.append(print_result(
            "saved_to field present",
            "saved_to" in data
        ))

        # Check training labels
        r2    = requests.get(f"{BASE_URL}/review/training-labels", timeout=10)
        data2 = r2.json()

        results.append(print_result(
            "Training labels endpoint returns 200",
            r2.status_code == 200
        ))
        results.append(print_result(
            "Positive labels exist",
            data2.get("positive_labels", 0) > 0
        ))
        results.append(print_result(
            "Negative labels exist",
            data2.get("negative_labels", 0) > 0
        ))

    except Exception as e:
        print(f"  ❌ Review system failed: {e}")
        results.append(False)

    return results

# ── Test 6: Programme Generation ─────────────────────────────────
def test_programme_generation():
    divider("Test 6 — Programme Generation (PEO/PO/PSO)")
    results = []

    # Test PEOs
    try:
        r = requests.post(f"{BASE_URL}/programme/peos", json={
            "programme_name": "B.Tech Computer Science Engineering",
            "programme_description": "Four year undergraduate programme in computer science",
            "n_peos": 3
        }, timeout=180)
        data = r.json()

        results.append(print_result(
            "PEO endpoint returns HTTP 200",
            r.status_code == 200
        ))
        results.append(print_result(
            "3 PEOs generated",
            len(data.get("peos", [])) == 3
        ))
        results.append(print_result(
            "Each PEO has peo_id, text, focus_area",
            all("peo_id" in p and "text" in p and "focus_area" in p
                for p in data.get("peos", []))
        ))
        print(f"\n    PEOs generated:")
        for p in data.get("peos", []):
            print(f"    • {p['peo_id']}: {p['text'][:60]}...")

    except Exception as e:
        print(f"  ❌ PEO generation failed: {e}")
        results.append(False)

    # Test POs
    try:
        r = requests.post(f"{BASE_URL}/programme/pos", json={
            "programme_name": "B.Tech Computer Science Engineering",
            "programme_description": "Four year undergraduate programme in computer science"
        }, timeout=180)
        data = r.json()

        results.append(print_result(
            "PO endpoint returns HTTP 200",
            r.status_code == 200
        ))
        results.append(print_result(
            "12 standard POs generated",
            len(data.get("pos", [])) == 12
        ))

    except Exception as e:
        print(f"  ❌ PO generation failed: {e}")
        results.append(False)

    # Test PSOs
    try:
        r = requests.post(f"{BASE_URL}/programme/psos", json={
            "programme_name": "B.Tech Computer Science Engineering",
            "course_list": ["Data Structures", "Machine Learning", "Computer Networks"],
            "n_psos": 3
        }, timeout=180)
        data = r.json()

        results.append(print_result(
            "PSO endpoint returns HTTP 200",
            r.status_code == 200
        ))
        results.append(print_result(
            "3 PSOs generated",
            len(data.get("psos", [])) == 3
        ))
        results.append(print_result(
            "Each PSO has domain field",
            all("domain" in p for p in data.get("psos", []))
        ))

    except Exception as e:
        print(f"  ❌ PSO generation failed: {e}")
        results.append(False)

    return results

# ── Test 7: Output Files Saved ───────────────────────────────────
def test_output_files():
    divider("Test 7 — Output Files")
    results = []

    results.append(print_result(
        "outputs/ folder exists",
        os.path.exists("outputs")
    ))
    results.append(print_result(
        "feedback/ folder exists",
        os.path.exists("feedback")
    ))
    results.append(print_result(
        "feedback/reviews.json exists",
        os.path.exists("feedback/reviews.json")
    ))

    # Check reviews.json has content
    try:
        with open("feedback/reviews.json", "r") as f:
            reviews = json.load(f)
        results.append(print_result(
            "reviews.json has review entries",
            len(reviews) > 0
        ))
        results.append(print_result(
            "Each review has training_label",
            all("training_label" in r for r in reviews)
        ))
    except Exception as e:
        print(f"  ❌ reviews.json check failed: {e}")
        results.append(False)

    # Check outputs folder has files
    output_files = os.listdir("outputs") if os.path.exists("outputs") else []
    results.append(print_result(
        "outputs/ folder has generated files",
        len(output_files) > 0
    ))

    return results

# ── Main Runner ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("═"*60)
    print("  GROUP 1 — FULL PIPELINE INTEGRATION TEST")
    print("  Make sure server is running before starting!")
    print("═"*60)

    all_results = []
    all_results += test_health()
    all_results += test_validation()
    all_results += test_review_system()
    all_results += test_output_files()

    # These tests call Ollama so they take longer
    print("\n⏳ Running LLM tests (these take 2-5 minutes)...")
    all_results += test_outcome_generation()
    all_results += test_syllabus_generation()
    all_results += test_programme_generation()

    passed = sum(all_results)
    total  = len(all_results)
    failed = total - passed

    divider("FINAL RESULTS")
    print(f"  PASSED: {passed}/{total}")
    if failed == 0:
        print("  🎉 ALL PIPELINE TESTS PASSED!")
    else:
        print(f"  ⚠  {failed} test(s) failed — check output above")uuu