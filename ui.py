# ui.py
from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime
from quiz_brain import QuizBrain
from data import CATEGORIES, fetch_questions

THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self):
        self.quiz = None

        self.window = Tk()
        self.window.title("Quizzler+")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # ======= Top Bar =======
        self.header = Frame(self.window, bg=THEME_COLOR)
        self.header.grid(row=0, column=0, sticky="ew")
        self.title_label = Label(self.header, text="Quizzler+", fg="white", bg=THEME_COLOR, font=("Arial", 20, "bold"))
        self.title_label.pack(side=LEFT)

        self.score_label = Label(self.header, text="Score: 0", fg="white", bg=THEME_COLOR, font=("Arial", 12, "bold"))
        self.score_label.pack(side=RIGHT)

        # ======= Start Panel (Config) =======
        self.start_panel = LabelFrame(self.window, text="Quiz Setup", bg=THEME_COLOR, fg="white", padx=10, pady=10)
        self.start_panel.grid(row=1, column=0, sticky="ew")

        # Category
        Label(self.start_panel, text="Category", bg=THEME_COLOR, fg="white").grid(row=0, column=0, sticky="w")
        self.category_var = StringVar(value="Any")
        self.category_dd = ttk.Combobox(self.start_panel, textvariable=self.category_var, values=list(CATEGORIES.keys()), state="readonly", width=30)
        self.category_dd.grid(row=0, column=1, padx=10, pady=5)

        # Difficulty
        Label(self.start_panel, text="Difficulty", bg=THEME_COLOR, fg="white").grid(row=1, column=0, sticky="w")
        self.difficulty_var = StringVar(value="Any")
        self.difficulty_dd = ttk.Combobox(self.start_panel, textvariable=self.difficulty_var, values=["Any", "Easy", "Medium", "Hard"], state="readonly", width=30)
        self.difficulty_dd.grid(row=1, column=1, padx=10, pady=5)

        # Type
        Label(self.start_panel, text="Question Type", bg=THEME_COLOR, fg="white").grid(row=2, column=0, sticky="w")
        self.type_var = StringVar(value="mixed")
        self.type_dd = ttk.Combobox(self.start_panel, textvariable=self.type_var, values=["mixed", "multiple", "boolean"], state="readonly", width=30)
        self.type_dd.grid(row=2, column=1, padx=10, pady=5)

        # Amount
        Label(self.start_panel, text="Number of Questions", bg=THEME_COLOR, fg="white").grid(row=3, column=0, sticky="w")
        self.amount_var = StringVar(value="10")
        self.amount_entry = ttk.Entry(self.start_panel, textvariable=self.amount_var, width=10)
        self.amount_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        self.start_btn = ttk.Button(self.start_panel, text="Start Quiz", command=self.start_quiz)
        self.start_btn.grid(row=4, column=0, pady=10, sticky="w")

        self.history_btn = ttk.Button(self.start_panel, text="View Score History", command=self.view_history)
        self.history_btn.grid(row=4, column=1, pady=10, sticky="e")

        # ======= Question Canvas =======
        self.canvas = Canvas(width=400, height=280, bg="white", highlightthickness=0)
        self.canvas.grid(row=2, column=0, pady=20)
        self.question_text = self.canvas.create_text(200, 140, width=360, text="Configure your quiz and press Start.", fill=THEME_COLOR, font=("Arial", 16, "italic"))

        # ======= Answer Buttons (dynamic) =======
        self.btn_frame = Frame(self.window, bg=THEME_COLOR)
        self.btn_frame.grid(row=3, column=0)
        self.answer_buttons = []  # dynamic buttons

        self.window.mainloop()

    # ----- Quiz lifecycle -----
    def start_quiz(self):
        try:
            amount = max(1, int(self.amount_var.get()))
        except ValueError:
            messagebox.showerror("Invalid Input", "Number of questions must be an integer.")
            return

        category = self.category_var.get()
        difficulty = self.difficulty_var.get()
        qtype = self.type_var.get()

        raw_questions = fetch_questions(amount=amount, qtype=qtype, category_name=category, difficulty=difficulty)

        # Build Question objects
        from question_model import Question
        q_objects = []
        for q in raw_questions:
            q_objects.append(
                Question(
                    text=q["question"],
                    correct_answer=q["correct_answer"],
                    incorrect_answers=q.get("incorrect_answers", []),
                    qtype=q["type"],
                    category=q.get("category", "General"),
                    difficulty=q.get("difficulty", "easy")
                )
            )
        if not q_objects:
            messagebox.showerror("No Questions", "Could not load questions. Try different settings.")
            return

        self.quiz = QuizBrain(q_objects)
        self.score_label.config(text=f"Score: {self.quiz.score}/{self.quiz.total_questions()}")
        self.next_question()

    def next_question(self):
        self.canvas.config(bg="white")
        for b in self.answer_buttons:
            b.destroy()
        self.answer_buttons.clear()

        if self.quiz and self.quiz.still_has_questions():
            text, choices = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=text)

            # Build answer buttons dynamically (2 for TF, 4 for MCQ)
            for idx, choice in enumerate(choices):
                btn = ttk.Button(self.btn_frame, text=choice, command=lambda c=choice: self.submit_answer(c))
                btn.grid(row=idx // 2, column=idx % 2, padx=10, pady=8, ipadx=10, ipady=6, sticky="ew")
                self.answer_buttons.append(btn)

        else:
            # End of quiz
            self.finish_quiz()

    def submit_answer(self, choice):
        is_right, correct = self.quiz.check_answer(choice)
        self.give_feedback(is_right, correct)

    def give_feedback(self, is_right, correct_answer):
        if is_right:
            self.canvas.config(bg="#2e7d32")  # green
        else:
            self.canvas.config(bg="#c62828")  # red
            # also show correct answer inline
            current_text = self.canvas.itemcget(self.question_text, "text")
            self.canvas.itemconfig(self.question_text, text=f"{current_text}\n\nCorrect: {correct_answer}")

        self.score_label.config(text=f"Score: {self.quiz.score}/{self.quiz.total_questions()}")
        self.window.after(900, self.next_question)

    def finish_quiz(self):
        percent = round((self.quiz.score / max(1, self.quiz.total_questions())) * 100, 1)
        self.canvas.itemconfig(self.question_text, text=f"🎉 Done!\n\nFinal Score: {self.quiz.score}/{self.quiz.total_questions()} ({percent}%)")
        self.save_score(self.quiz.score, self.quiz.total_questions())

        # Replace answer buttons with actions
        for b in self.answer_buttons:
            b.destroy()
        self.answer_buttons.clear()

        replay = ttk.Button(self.btn_frame, text="Play Again", command=self.reset_to_start)
        replay.grid(row=0, column=0, padx=10, pady=10, ipadx=10, ipady=6)
        view_hist = ttk.Button(self.btn_frame, text="View Score History", command=self.view_history)
        view_hist.grid(row=0, column=1, padx=10, pady=10, ipadx=10, ipady=6)

    def reset_to_start(self):
        self.canvas.config(bg="white")
        self.canvas.itemconfig(self.question_text, text="Configure your quiz and press Start.")
        for b in self.answer_buttons:
            b.destroy()
        self.answer_buttons.clear()
        self.quiz = None
        self.score_label.config(text="Score: 0")
        # nothing else to do; start panel always visible

    # ----- Score history -----
    def save_score(self, score, total):
        try:
            with open("score_history.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), score, total])
        except Exception:
            pass  # non-fatal

    def view_history(self):
        top = Toplevel(self.window)
        top.title("Score History")
        top.config(padx=10, pady=10)
        Label(top, text="Date", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=6, pady=4, sticky="w")
        Label(top, text="Score", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=6, pady=4, sticky="w")
        Label(top, text="Total", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=6, pady=4, sticky="w")

        try:
            with open("score_history.csv", "r", encoding="utf-8") as f:
                reader = list(csv.reader(f))[-30:]  # show last 30
            for i, row in enumerate(reader, start=1):
                for j, val in enumerate(row):
                    Label(top, text=str(val)).grid(row=i, column=j, padx=6, pady=2, sticky="w")
        except FileNotFoundError:
            Label(top, text="No history yet. Play a quiz first!").grid(row=1, column=0, columnspan=3, padx=6, pady=6)
