"""
Day 11 — Polish and Bug Fix Tests
"""
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.helpers import (
    sanitize_filename, save_json, load_json,
    success_response, error_response, get_system_stats
)

def print_result(test_name, passed):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status} — {test_name}")
    return passed

def divider(title=""):
    print(f"\n{'═'*60}")
    if title:
        print(f"  {title}")
        print(f"{'═'*60}")

def test_helpers():
    divider("Test 1 — Helper Utilities")
    results = []

    # Filename sanitization
    results.append(print_result(
        "Spaces replaced in filename",
        sanitize_filename("Data Structures") == "Data_Structures"
    ))
    results.append(print_result(
        "Special chars removed from filename",
        "_" in sanitize_filename("Data/Structures:Test")
    ))

    # JSON save/load
    test_data = {"test": "data", "value": 123}
    path = save_json(test_data, "outputs", "test", "HelperTest")
    results.append(print_result(
        "JSON file saved successfully",
        os.path.exists(path)
    ))
    loaded = load_json(path)
    results.append(print_result(
        "JSON file loaded correctly",
        loaded == test_data
    ))

    # Missing file
    missing = load_json("outputs/nonexistent_file.json")
    results.append(print_result(
        "Missing file returns None gracefully",
        missing is None
    ))

    return results

def test_response_wrappers():
    divider("Test 2 — Response Wrappers")
    results = []

    success = success_response({"key": "value"}, "Test passed")
    results.append(print_result(
        "success_response has status field",
        success.get("status") == "success"
    ))
    results.append(print_result(
        "success_response has timestamp",
        "timestamp" in success
    ))
    results.append(print_result(
        "success_response has data",
        success.get("data") == {"key": "value"}
    ))

    error = error_response("Something went wrong", 500)
    results.append(print_result(
        "error_response has status=error",
        error.get("status") == "error"
    ))
    results.append(print_result(
        "error_response has code",
        error.get("code") == 500
    ))

    return results

def test_system_stats():
    divider("Test 3 — System Stats")
    results = []

    stats = get_system_stats()

    results.append(print_result(
        "Stats has generated_files",
        "generated_files" in stats
    ))
    results.append(print_result(
        "Stats has total_reviews",
        "total_reviews" in stats
    ))
    results.append(print_result(
        "Stats has accepted_reviews",
        "accepted_reviews" in stats
    ))
    results.append(print_result(
        "Stats has rejected_reviews",
        "rejected_reviews" in stats
    ))
    results.append(print_result(
        "Stats has edited_reviews",
        "edited_reviews" in stats
    ))
    results.append(print_result(
        "generated_files count is a number",
        isinstance(stats["generated_files"], int)
    ))

    print(f"\n  Current system stats:")
    for k, v in stats.items():
        print(f"    {k}: {v}")

    return results

def test_logging():
    divider("Test 4 — Logging System")
    results = []

    results.append(print_result(
        "logs/ directory exists",
        os.path.exists("logs")
    ))
    results.append(print_result(
        "logs/app.log exists",
        os.path.exists("logs/app.log")
    ))

    # Check log has content
    if os.path.exists("logs/app.log"):
        with open("logs/app.log") as f:
            content = f.read()
        results.append(print_result(
            "app.log has content",
            len(content) > 0
        ))

    return results

def test_output_structure():
    divider("Test 5 — Output File Structure")
    results = []

    # Check all required directories
    for folder in ["outputs", "feedback", "logs"]:
        results.append(print_result(
            f"{folder}/ directory exists",
            os.path.exists(folder)
        ))

    # Check benchmark report exists
    results.append(print_result(
        "30-course benchmark report exists",
        os.path.exists("outputs/benchmark_30_courses.json")
    ))

    # Check contracts file exists
    results.append(print_result(
        "Data contracts file exists",
        os.path.exists("outputs/data_contracts_v1.json")
    ))

    # Check reviews file
    results.append(print_result(
        "feedback/reviews.json exists",
        os.path.exists("feedback/reviews.json")
    ))

    return results

def test_edge_cases():
    divider("Test 6 — Edge Cases")
    results = []

    # Empty string sanitize
    results.append(print_result(
        "Empty filename sanitized gracefully",
        isinstance(sanitize_filename(""), str)
    ))

    # Very long filename
    long_name = "A" * 200
    sanitized = sanitize_filename(long_name)
    results.append(print_result(
        "Very long filename handled",
        isinstance(sanitized, str)
    ))

    # None in success response
    resp = success_response(None, "Empty data")
    results.append(print_result(
        "None data in success_response handled",
        resp["data"] is None
    ))

    # Load invalid JSON
    with open("outputs/test_invalid.json", "w") as f:
        f.write("not valid json{{{")
    try:
        load_json("outputs/test_invalid.json")
        results.append(print_result(
            "Invalid JSON handled",
            False
        ))
    except Exception:
        results.append(print_result(
            "Invalid JSON raises exception as expected",
            True
        ))
    finally:
        os.remove("outputs/test_invalid.json")

    return results

if __name__ == "__main__":
    print("═"*60)
    print("  GROUP 1 — POLISH & BUG FIX TESTS")
    print("═"*60)

    all_results = []
    all_results += test_helpers()
    all_results += test_response_wrappers()
    all_results += test_system_stats()
    all_results += test_logging()
    all_results += test_output_structure()
    all_results += test_edge_cases()

    passed = sum(all_results)
    total  = len(all_results)
    failed = total - passed

    print(f"\n{'═'*60}")
    print(f"  FINAL RESULT: {passed}/{total} tests passed")
    if failed == 0:
        print("  🎉 ALL POLISH TESTS PASSED!")
        print("  ✅ Group 1 platform is production ready!")
    else:
        print(f"  ⚠ {failed} test(s) failed")
    print("═"*60)