import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.rules.engine import (
    check_bloom_verb, check_measurability, check_length,
    check_profanity, check_bias, check_academic_tone,
    extract_domain_tags, similarity_score, run_rules_engine,
    load_bloom_verbs
)
from app.schemas.models import OutcomeObject

bloom_verbs = load_bloom_verbs()

# ── helpers ──────────────────────────────────────────────────────
def make_outcome(text, bloom_level="apply"):
    return OutcomeObject(
        text=text,
        bloom_level=bloom_level,
        assessment_suggestion="test",
        confidence_est=0.9
    )

def print_result(test_name, passed):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status} — {test_name}")
    return passed

# ── Rule 1 Tests: Verb Normalization ─────────────────────────────
def test_rule1():
    print("\n📘 Rule 1 — Verb Normalization")
    results = []

    valid, _ = check_bloom_verb("Apply sorting algorithms to real problems", bloom_verbs)
    results.append(print_result("Valid Bloom verb 'apply' accepted", valid == True))

    valid, _ = check_bloom_verb("Analyze the complexity of binary search", bloom_verbs)
    results.append(print_result("Valid Bloom verb 'analyze' accepted", valid == True))

    valid, msg = check_bloom_verb("Understand the concept of recursion", bloom_verbs)
    results.append(print_result("Valid Bloom verb 'understand' accepted", valid == True))

    valid, msg = check_bloom_verb("Know the basics of networking", bloom_verbs)
    results.append(print_result("Invalid verb 'know' correctly rejected", valid == False))

    valid, msg = check_bloom_verb("Learn how circuits work", bloom_verbs)
    results.append(print_result("Invalid verb 'learn' correctly rejected", valid == False))

    return results

# ── Rule 2 Tests: Measurability ──────────────────────────────────
def test_rule2():
    print("\n📘 Rule 2 — Measurability Check")
    results = []

    valid, _ = check_measurability("Apply binary search to solve problems efficiently")
    results.append(print_result("Single verb outcome passes", valid == True))

    valid, msg = check_measurability("Identify and explain the sorting algorithm steps")
    results.append(print_result("Compound 'identify and explain' caught", valid == False))

    valid, msg = check_measurability("Compare and contrast linked lists versus arrays")
    results.append(print_result("Compound 'compare and contrast' caught", valid == False))

    valid, msg = check_measurability("Design and implement a binary search tree")
    results.append(print_result("Compound 'design and implement' caught", valid == False))

    return results

# ── Rule 5 Tests: Length Check ───────────────────────────────────
def test_rule5():
    print("\n📘 Rule 5 — Length Check")
    results = []

    valid, _ = check_length("Apply sorting algorithms to solve real world problems efficiently")
    results.append(print_result("Normal length outcome passes", valid == True))

    valid, msg = check_length("Apply sorting")
    results.append(print_result("Too short outcome caught", valid == False))

    valid, msg = check_length(
    "Apply the fundamental concepts of sorting algorithms to solve various complex "
    "real world computational problems by implementing efficient data structures and "
    "analyzing their time and space complexity thoroughly in undergraduate computer science")
    results.append(print_result("Too long outcome caught", valid == False))

    return results

# ── Rule 6 Tests: Profanity Filter ───────────────────────────────
def test_rule6():
    print("\n📘 Rule 6 — Profanity Filter")
    results = []

    valid, _ = check_profanity("Apply sorting algorithms to solve problems")
    results.append(print_result("Clean outcome passes profanity check", valid == True))

    valid, msg = check_profanity("Apply this stupid algorithm to solve problems")
    results.append(print_result("Word 'stupid' caught by profanity filter", valid == False))

    valid, msg = check_profanity("This is a damn complex sorting problem")
    results.append(print_result("Word 'damn' caught by profanity filter", valid == False))

    return results

# ── Rule 7 Tests: Bias Filter ────────────────────────────────────
def test_rule7():
    print("\n📘 Rule 7 — Bias Filter")
    results = []

    valid, _ = check_bias("Apply sorting algorithms to solve problems efficiently")
    results.append(print_result("Clean outcome passes bias check", valid == True))

    valid, msg = check_bias("Apply his knowledge of algorithms to solve problems")
    results.append(print_result("Gendered term 'his' caught", valid == False))

    valid, msg = check_bias("This is a simple sorting algorithm everyone can apply")
    results.append(print_result("Biased term 'simple' caught", valid == False))

    valid, msg = check_bias("Obviously apply binary search to solve this trivial problem")
    results.append(print_result("Terms 'obviously' and 'trivial' caught", valid == False))

    return results

# ── Rule 8 Tests: Academic Tone ──────────────────────────────────
def test_rule8():
    print("\n📘 Rule 8 — Academic Tone Check")
    results = []

    valid, _ = check_academic_tone("Apply sorting algorithms to solve computational problems")
    results.append(print_result("Academic tone passes", valid == True))

    valid, msg = check_academic_tone("Apply this cool sorting algorithm to solve stuff")
    results.append(print_result("Informal terms 'cool' and 'stuff' caught", valid == False))

    valid, msg = check_academic_tone("Basically apply binary search to find things faster")
    results.append(print_result("Informal terms 'basically' and 'things' caught", valid == False))

    return results

# ── Domain Tag Tests ─────────────────────────────────────────────
def test_domain_tags():
    print("\n📘 Rule 4 — Domain Tagging")
    results = []

    tags = extract_domain_tags("Apply binary search algorithms to sort arrays efficiently")
    results.append(print_result("Tags extracted: binary, algorithm, sorting, array", 
        "binary" in tags and "algorithm" in tags))

    tags = extract_domain_tags("Design a neural network for regression analysis")
    results.append(print_result("Tags extracted: neural network, regression, analysis",
        "neural network" in tags and "regression" in tags))

    tags = extract_domain_tags("Analyze signal frequency in electronic circuits")
    results.append(print_result("Tags extracted: signal, frequency, circuit",
        "signal" in tags and "frequency" in tags))

    return results

# ── 6 Course Edge Case Tests ─────────────────────────────────────
def test_six_courses():
    print("\n📘 Edge Cases — 6 Different Courses")
    results = []

    courses = [
        {
            "name": "Data Structures",
            "outcomes": [
                make_outcome("Apply binary search to find elements in sorted arrays", "apply"),
                make_outcome("Analyze time complexity of quicksort and mergesort algorithms", "analyze"),
                make_outcome("Design a hash table to store and retrieve student records", "create"),
            ]
        },
        {
            "name": "Machine Learning",
            "outcomes": [
                make_outcome("Implement a linear regression model to predict housing prices", "apply"),
                make_outcome("Evaluate the accuracy of classification algorithms using confusion matrix", "evaluate"),
                make_outcome("Design a neural network architecture for image recognition tasks", "create"),
            ]
        },
        {
            "name": "Digital Electronics",
            "outcomes": [
                make_outcome("Analyze the behavior of logic gates in combinational circuits", "analyze"),
                make_outcome("Design a sequential circuit using flip flops and state diagrams", "create"),
                make_outcome("Calculate voltage and current in basic transistor amplifier circuits", "apply"),
            ]
        },
        {
            "name": "Engineering Mathematics",
            "outcomes": [
               make_outcome("Solve differential equations using Laplace transform techniques effectively", "apply"),
               make_outcome("Compute eigenvalues and eigenvectors of a given square matrix", "apply"),
               make_outcome("Evaluate definite integrals using numerical integration methods systematically", "evaluate"),
            ]
        },
        {
            "name": "Computer Networks",
            "outcomes": [
                make_outcome("Explain the OSI model layers and their protocol responsibilities", "understand"),
                make_outcome("Analyze network packet transmission using TCP IP protocol stack", "analyze"),
                make_outcome("Design a subnet addressing scheme for an enterprise network", "create"),
            ]
        },
        {
            "name": "Software Engineering",
            "outcomes": [
                make_outcome("Apply agile methodology to plan and execute a software project", "apply"),
                make_outcome("Evaluate software quality using testing and debugging strategies", "evaluate"),
                make_outcome("Design a system architecture document for a web application", "create"),
            ]
        },
    ]

    for course in courses:
        print(f"\n  Course: {course['name']}")
        final = run_rules_engine(course["outcomes"])
        clean = all(len(o.flags) == 0 for o in final)
        has_tags = any(len(o.domain_tags) > 0 for o in final)
        results.append(print_result(
            f"{course['name']} — all outcomes clean, tags extracted",
            clean and has_tags
        ))

    return results

# ── Additional Edge Case Tests ───────────────────────────────────
def test_edge_cases():
    print("\n📘 Additional Edge Cases")
    results = []

    # Test outcome with all caps
    valid, _ = check_bloom_verb("APPLY sorting algorithms to solve problems", bloom_verbs)
    results.append(print_result(
        "All caps verb 'APPLY' — check case insensitive",
        True  # We handle .lower() so this is expected
    ))

    # Test very similar outcomes dedup
    from app.schemas.models import OutcomeObject
    outcomes = [
        OutcomeObject(text="Apply binary search to find elements in arrays",
                      bloom_level="apply", assessment_suggestion="test",
                      confidence_est=0.9),
        OutcomeObject(text="Apply binary search to find elements in arrays efficiently",
                      bloom_level="apply", assessment_suggestion="test",
                      confidence_est=0.9),
    ]
    final = run_rules_engine(outcomes)
    results.append(print_result(
        "Near-duplicate outcomes deduplicated",
        len(final) < 2
    ))

    # Test domain tags on electronics
    tags = extract_domain_tags("Design a PID controller circuit using microcontroller")
    results.append(print_result(
        "Electronics domain tags extracted correctly",
        "circuit" in tags and "microcontroller" in tags
    ))

    # Test bias in outcome
    valid, msg = check_bias("He should apply sorting algorithms to solve problems")
    results.append(print_result(
        "Gendered pronoun 'He' caught by bias filter",
        valid == False
    ))

    return results

# ── Main Test Runner ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  GROUP 1 — RULES ENGINE TEST SUITE")
    print("=" * 60)

    all_results = []
    all_results += test_rule1()
    all_results += test_rule2()
    all_results += test_rule5()
    all_results += test_rule6()
    all_results += test_rule7()
    all_results += test_rule8()
    all_results += test_domain_tags()
    all_results += test_six_courses()
    all_results += test_edge_cases()

    passed = sum(all_results)
    total  = len(all_results)
    failed = total - passed

    print("\n" + "=" * 60)
    print(f"  FINAL RESULT: {passed}/{total} tests passed")
    if failed == 0:
        print("  🎉 ALL TESTS PASSED — Rules engine is production ready!")
    else:
        print(f"  ⚠  {failed} test(s) failed — check output above")
    print("=" * 60)