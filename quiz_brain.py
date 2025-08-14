# quiz_brain.py
import html
import random

class QuizBrain:
    def __init__(self, questions):
        self.question_number = 0
        self.score = 0
        self.question_list = questions
        self.current_question = None
        self.choices = []  # current shuffled choices

    def total_questions(self):
        return len(self.question_list)

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        """Returns (display_text, choices_list). choices_list can be 2 (TF) or 4 (MCQ)."""
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1

        q_text = html.unescape(self.current_question.text)
        if self.current_question.type == "boolean":
            self.choices = ["True", "False"]
        else:
            # multiple choice
            self.choices = [self.current_question.answer] + self.current_question.incorrect_answers
            self.choices = [html.unescape(c) for c in self.choices]
            random.shuffle(self.choices)

        display = f"Q.{self.question_number} ({self.current_question.category} | {self.current_question.difficulty.title()}):\n\n{q_text}"
        return display, self.choices

    def check_answer(self, user_answer):
        correct = html.unescape(self.current_question.answer)
        if str(user_answer).strip().lower() == str(correct).strip().lower():
            self.score += 1
            return True, correct
        return False, correct
