"""
Day 9 — JSON Schema Contract Tests
Validates all Group 1 outputs against official data contracts
"""
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.schemas.validator import (
    validate_outcome_object,
    validate_unit_object,
    validate_programme_object,
    validate_review_entry,
    run_full_validation
)
from app.schemas.contracts import ALL_CONTRACTS

def print_result(test_name, passed):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status} — {test_name}")
    return passed

def divider(title=""):
    print(f"\n{'═'*60}")
    if title:
        print(f"  {title}")
        print(f"{'═'*60}")

# ── Test 1: Contracts Loaded ──────────────────────────────────────
def test_contracts_loaded():
    divider("Test 1 — Contracts Loaded")
    results = []

    results.append(print_result(
        "ALL_CONTRACTS has version field",
        "version" in ALL_CONTRACTS
    ))
    results.append(print_result(
        "OutcomeObject contract exists",
        "OutcomeObject" in ALL_CONTRACTS
    ))
    results.append(print_result(
        "CourseUnits contract exists",
        "CourseUnits" in ALL_CONTRACTS
    ))
    results.append(print_result(
        "MappingResponse contract exists",
        "MappingResponse" in ALL_CONTRACTS
    ))
    results.append(print_result(
        "TrainingLabel contract exists",
        "TrainingLabel" in ALL_CONTRACTS
    ))
    results.append(print_result(
        "Programme contract exists",
        "Programme" in ALL_CONTRACTS
    ))

    return results

# ── Test 2: Valid Outcome Objects ─────────────────────────────────
def test_valid_outcomes():
    divider("Test 2 — Valid Outcome Objects")
    results = []

    valid_outcomes = [
        {
            "text":                 "Apply binary search algorithms to optimize array searches",
            "bloom_level":          "apply",
            "assessment_suggestion":"Coding assignment",
            "confidence_est":       0.9,
            "flags":                [],
            "domain_tags":          ["algorithm","array","binary"]
        },
        {
            "text":                 "Analyze the time and space complexity of sorting algorithms",
            "bloom_level":          "analyze",
            "assessment_suggestion":"Written analysis report",
            "confidence_est":       0.85,
            "flags":                [],
            "domain_tags":          ["algorithm","sorting","complexity"]
        },
        {
            "text":                 "Design a neural network architecture for image classification",
            "bloom_level":          "create",
            "assessment_suggestion":"Project submission",
            "confidence_est":       0.92,
            "flags":                [],
            "domain_tags":          ["neural network","classification","design"]
        },
    ]

    for outcome in valid_outcomes:
        result = validate_outcome_object(outcome)
        results.append(print_result(
            f"Valid outcome passes — '{outcome['text'][:40]}...'",
            result["valid"] == True
        ))
        if result["errors"]:
            print(f"    Errors: {result['errors']}")

    return results

# ── Test 3: Invalid Outcome Objects ──────────────────────────────
def test_invalid_outcomes():
    divider("Test 3 — Invalid Outcome Objects")
    results = []

    # Missing required field
    invalid1 = {
        "text":       "Apply sorting algorithms to solve problems",
        "bloom_level":"apply"
        # missing confidence_est, flags, domain_tags
    }
    result = validate_outcome_object(invalid1)
    results.append(print_result(
        "Missing fields detected",
        result["valid"] == False
    ))

    # Invalid bloom level
    invalid2 = {
        "text":                 "Apply sorting algorithms to solve problems efficiently",
        "bloom_level":          "memorize",
        "assessment_suggestion":"Quiz",
        "confidence_est":       0.9,
        "flags":                [],
        "domain_tags":          []
    }
    result = validate_outcome_object(invalid2)
    results.append(print_result(
        "Invalid bloom level 'memorize' detected",
        result["valid"] == False
    ))

    # Confidence out of range
    invalid3 = {
        "text":                 "Apply sorting algorithms to solve complex problems",
        "bloom_level":          "apply",
        "assessment_suggestion":"Quiz",
        "confidence_est":       1.5,
        "flags":                [],
        "domain_tags":          []
    }
    result = validate_outcome_object(invalid3)
    results.append(print_result(
        "confidence_est > 1.0 detected",
        result["valid"] == False
    ))

    # Text too short
    invalid4 = {
        "text":                 "Apply sorting",
        "bloom_level":          "apply",
        "assessment_suggestion":"Quiz",
        "confidence_est":       0.9,
        "flags":                [],
        "domain_tags":          []
    }
    result = validate_outcome_object(invalid4)
    results.append(print_result(
        "Text too short detected",
        result["valid"] == False
    ))

    return results

# ── Test 4: Valid Unit Objects ────────────────────────────────────
def test_valid_units():
    divider("Test 4 — Valid Unit Objects")
    results = []

    valid_unit = {
        "unit_id":         "U1",
        "unit_title":      "Arrays and Linked Lists",
        "unit_objectives": [
            "Define the structure and operations of arrays",
            "Explain the concept of linked lists",
            "Compare arrays and linked lists"
        ],
        "unit_outcomes": [
            "Analyze time complexity of array operations",
            "Design efficient algorithms for linked list manipulation"
        ],
        "assessments": [
            "Mid-term exam",
            "Coding assignment"
        ],
        "readings": [
            "Chapter 1: Arrays — Goodrich et al.",
            "Chapter 2: Linked Lists — Cormen et al."
        ]
    }

    result = validate_unit_object(valid_unit)
    results.append(print_result(
        "Valid unit object passes",
        result["valid"] == True
    ))
    if result["warnings"]:
        print(f"    Warnings: {result['warnings']}")

    # Invalid unit — missing unit_outcomes
    invalid_unit = {
        "unit_id":   "U1",
        "unit_title":"Arrays",
        "unit_objectives": ["Define arrays"],
        "unit_outcomes":   [],
        "assessments":     ["Quiz"],
        "readings":        ["Chapter 1"]
    }
    result = validate_unit_object(invalid_unit)
    results.append(print_result(
        "Empty unit_outcomes detected",
        result["valid"] == False
    ))

    return results

# ── Test 5: Valid Programme Objects ──────────────────────────────
def test_valid_programme():
    divider("Test 5 — Valid Programme Objects")
    results = []

    valid_programme = {
        "programme_name": "B.Tech CSE",
        "peos": [
            {"peo_id":"PEO1","text":"Graduates will design software systems","focus_area":"Industry"},
            {"peo_id":"PEO2","text":"Alumni will pursue advanced research","focus_area":"Research"},
            {"peo_id":"PEO3","text":"Graduates will contribute to society","focus_area":"Society"},
        ],
        "pos": [
            {"po_id":f"PO{i}","title":f"PO Title {i}","text":f"PO text {i}"}
            for i in range(1, 13)
        ],
        "psos": [
            {"pso_id":"PSO1","text":"Apply ML algorithms to solve problems","domain":"Machine Learning"},
            {"pso_id":"PSO2","text":"Design secure network architectures","domain":"Networks"},
        ]
    }

    result = validate_programme_object(valid_programme)
    results.append(print_result(
        "Valid programme object passes",
        result["valid"] == True
    ))

    # Invalid programme — only 1 PEO
    invalid_programme = {
        "programme_name": "B.Tech CSE",
        "peos":  [{"peo_id":"PEO1","text":"Graduates will design systems","focus_area":"Industry"}],
        "pos":   [{"po_id":"PO1","title":"Engineering Knowledge","text":"Apply mathematics"}],
        "psos":  [{"pso_id":"PSO1","text":"Apply ML","domain":"ML"}]
    }
    result = validate_programme_object(invalid_programme)
    results.append(print_result(
        "Too few PEOs (1) detected",
        result["valid"] == False
    ))

    # Invalid programme — no PSOs
    invalid_programme2 = {
        "programme_name": "B.Tech CSE",
        "peos": [
            {"peo_id":"PEO1","text":"Graduates will design systems","focus_area":"Industry"},
            {"peo_id":"PEO2","text":"Alumni will research","focus_area":"Research"},
            {"peo_id":"PEO3","text":"Graduates will serve society","focus_area":"Society"},
        ],
        "pos":  [{"po_id":"PO1","title":"Engineering Knowledge","text":"Apply mathematics"}],
        "psos": []
    }
    result = validate_programme_object(invalid_programme2)
    results.append(print_result(
        "Empty PSOs detected",
        result["valid"] == False
    ))

    return results

# ── Test 6: Review Entry Validation ──────────────────────────────
def test_review_validation():
    divider("Test 6 — Review Entry Validation")
    results = []

    valid_review = {
        "outcome_id":       "OC001",
        "course_name":      "Data Structures",
        "original_text":    "Apply binary search to arrays",
        "final_text":       "Apply binary search to arrays",
        "action":           "accept",
        "reviewer_comment": "Good outcome",
        "reviewed_at":      "2026-05-15T10:00:00",
        "training_label": {
            "is_valid":      True,
            "was_edited":    False,
            "original_text": "Apply binary search to arrays",
            "approved_text": "Apply binary search to arrays",
            "bloom_level":   "apply"
        }
    }

    result = validate_review_entry(valid_review)
    results.append(print_result(
        "Valid review entry passes",
        result["valid"] == True
    ))

    # Invalid action
    invalid_review = {
        "outcome_id":  "OC001",
        "course_name": "Data Structures",
        "original_text":"Apply binary search to arrays",
        "action":      "approve",  # invalid
        "reviewed_at": "2026-05-15",
        "training_label": {
            "is_valid":True,"was_edited":False,
            "original_text":"text","approved_text":"text","bloom_level":"apply"
        }
    }
    result = validate_review_entry(invalid_review)
    results.append(print_result(
        "Invalid action 'approve' detected",
        result["valid"] == False
    ))

    return results

# ── Test 7: Real Reviews File Validation ─────────────────────────
def test_real_reviews_file():
    divider("Test 7 — Real reviews.json Validation")
    results = []

    reviews_path = "feedback/reviews.json"
    if not os.path.exists(reviews_path):
        print(f"  ⚠ {reviews_path} not found — skipping")
        return results

    with open(reviews_path, "r") as f:
        reviews = json.load(f)

    results.append(print_result(
        f"reviews.json has {len(reviews)} entries",
        len(reviews) > 0
    ))

    valid_count = 0
    for review in reviews:
        result = validate_review_entry(review)
        if result["valid"]:
            valid_count += 1

    results.append(print_result(
        f"All {len(reviews)} review entries are valid",
        valid_count == len(reviews)
    ))

    return results

# ── Test 8: Contract Export ───────────────────────────────────────
def test_contract_export():
    divider("Test 8 — Contract Export to JSON")
    results = []

    os.makedirs("outputs", exist_ok=True)
    export_path = "outputs/data_contracts_v1.json"

    try:
        with open(export_path, "w") as f:
            json.dump(ALL_CONTRACTS, f, indent=2)

        results.append(print_result(
            "Contracts exported to outputs/data_contracts_v1.json",
            os.path.exists(export_path)
        ))

        # Verify it can be read back
        with open(export_path, "r") as f:
            loaded = json.load(f)

        results.append(print_result(
            "Exported contracts file is valid JSON",
            "version" in loaded and "OutcomeObject" in loaded
        ))

        print(f"\n  Contract file size: {os.path.getsize(export_path)} bytes")
        print(f"  Contracts defined: {len([k for k in loaded if k not in ['version','last_updated','group']])}")

    except Exception as e:
        print(f"  ❌ Export failed: {e}")
        results.append(False)

    return results

# ── Main ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("═"*60)
    print("  GROUP 1 — JSON CONTRACT VALIDATION TESTS")
    print("═"*60)

    all_results = []
    all_results += test_contracts_loaded()
    all_results += test_valid_outcomes()
    all_results += test_invalid_outcomes()
    all_results += test_valid_units()
    all_results += test_valid_programme()
    all_results += test_review_validation()
    all_results += test_real_reviews_file()
    all_results += test_contract_export()

    passed = sum(all_results)
    total  = len(all_results)
    failed = total - passed

    print(f"\n{'═'*60}")
    print(f"  FINAL RESULT: {passed}/{total} tests passed")
    if failed == 0:
        print("  🎉 ALL CONTRACT TESTS PASSED!")
        print("  ✅ Group 1 data contracts are integration ready!")
    else:
        print(f"  ⚠  {failed} test(s) failed")
    print("═"*60)