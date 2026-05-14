import json
import os
from datetime import datetime
from app.schemas.review_models import ReviewRequest, ReviewSummary, ReviewAction

FEEDBACK_FILE = "feedback/reviews.json"

def load_existing_reviews() -> list:
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_reviews(reviews: list):
    os.makedirs("feedback", exist_ok=True)
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(reviews, f, indent=2)

def process_reviews(request: ReviewRequest) -> ReviewSummary:
    existing = load_existing_reviews()
    
    accepted = 0
    rejected = 0
    edited   = 0

    for review in request.reviews:
        # Determine final text
        if review.action == ReviewAction.edit and review.edited_text:
            final_text = review.edited_text
            edited += 1
        elif review.action == ReviewAction.accept:
            final_text = review.original_text
            accepted += 1
        else:
            final_text = review.original_text
            rejected += 1

        # Build log entry
        entry = {
            "outcome_id":       review.outcome_id,
            "course_name":      review.course_name,
            "original_text":    review.original_text,
            "final_text":       final_text,
            "bloom_level":      review.bloom_level,
            "action":           review.action.value,
            "reviewer_comment": review.reviewer_comment,
            "reviewed_at":      datetime.now().isoformat(),
            # Label for Group 2 BERT training
            "training_label": {
                "is_valid":       review.action != ReviewAction.reject,
                "was_edited":     review.action == ReviewAction.edit,
                "original_text":  review.original_text,
                "approved_text":  final_text,
                "bloom_level":    review.bloom_level,
            }
        }
        existing.append(entry)

        # Print log
        status = "✓ ACCEPTED" if review.action == ReviewAction.accept else \
                 "✗ REJECTED" if review.action == ReviewAction.reject else \
                 "✎ EDITED"
        print(f"  {status} | '{review.original_text[:50]}...'")
        if review.action == ReviewAction.edit:
            print(f"    → Edited to: '{final_text[:50]}...'")

    save_reviews(existing)

    print(f"\n── Review Summary ──")
    print(f"  Accepted: {accepted}")
    print(f"  Rejected: {rejected}")
    print(f"  Edited:   {edited}")
    print(f"  Total logged: {len(existing)} reviews")

    return ReviewSummary(
        total_reviewed=len(request.reviews),
        accepted=accepted,
        rejected=rejected,
        edited=edited,
        saved_to=FEEDBACK_FILE
    )

def get_all_reviews() -> dict:
    reviews = load_existing_reviews()
    
    accepted = [r for r in reviews if r["action"] == "accept"]
    rejected = [r for r in reviews if r["action"] == "reject"]
    edited   = [r for r in reviews if r["action"] == "edit"]

    return {
        "total":    len(reviews),
        "accepted": len(accepted),
        "rejected": len(rejected),
        "edited":   len(edited),
        "reviews":  reviews
    }

def get_training_labels() -> dict:
    reviews  = load_existing_reviews()
    positive = [r["training_label"] for r in reviews if r["training_label"]["is_valid"]]
    negative = [r["training_label"] for r in reviews if not r["training_label"]["is_valid"]]

    return {
        "total_labels":    len(reviews),
        "positive_labels": len(positive),
        "negative_labels": len(negative),
        "positive":        positive,
        "negative":        negative
    }