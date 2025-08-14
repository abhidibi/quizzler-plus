# data.py
import requests
import random

# Minimal local fallback if API fails
FALLBACK_QUESTIONS = [
    {
        "category": "General Knowledge",
        "type": "boolean",
        "difficulty": "easy",
        "question": "The sky is blue.",
        "correct_answer": "True",
        "incorrect_answers": ["False"]
    },
    {
        "category": "Science & Nature",
        "type": "multiple",
        "difficulty": "easy",
        "question": "What is the chemical symbol for water?",
        "correct_answer": "H2O",
        "incorrect_answers": ["O2", "CO2", "HO"]
    }
]

# Common Open Trivia DB categories
CATEGORIES = {
    "Any": None,
    "General Knowledge": 9,
    "Books": 10,
    "Film": 11,
    "Music": 12,
    "Television": 14,
    "Video Games": 15,
    "Science & Nature": 17,
    "Computers": 18,
    "Mathematics": 19,
    "Mythology": 20,
    "Sports": 21,
    "Geography": 22,
    "History": 23,
    "Art": 25,
    "Animals": 27,
}

def fetch_questions(amount=10, qtype="mixed", category_name="Any", difficulty="Any"):
    """
    Returns a list of question dicts in the OpenTDB format.
    qtype: "boolean", "multiple", or "mixed"
    difficulty: "easy"/"medium"/"hard"/"Any"
    """
    params = {"amount": amount}

    # Type handling
    if qtype in ("boolean", "multiple"):
        params["type"] = qtype  # else mixed (omit type)

    # Difficulty handling
    if difficulty and difficulty.lower() in ("easy", "medium", "hard"):
        params["difficulty"] = difficulty.lower()

    # Category handling
    cat_id = CATEGORIES.get(category_name, None)
    if cat_id:
        params["category"] = cat_id

    try:
        resp = requests.get("https://opentdb.com/api.php", params=params, timeout=10)
        resp.raise_for_status()
        payload = resp.json()
        results = payload.get("results", [])
        # If OpenTDB returns no results for the combination, fallback
        if not results:
            return random.sample(FALLBACK_QUESTIONS, k=min(amount, len(FALLBACK_QUESTIONS)))
        return results
    except Exception:
        # Network error or bad response → fallback
        return random.sample(FALLBACK_QUESTIONS, k=min(amount, len(FALLBACK_QUESTIONS)))
