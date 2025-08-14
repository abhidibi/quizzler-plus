# question_model.py
class Question:
    def __init__(self, text, correct_answer, incorrect_answers, qtype, category, difficulty):
        self.text = text
        self.answer = correct_answer
        self.incorrect_answers = incorrect_answers or []
        self.type = qtype  # "boolean" or "multiple"
        self.category = category
        self.difficulty = difficulty
