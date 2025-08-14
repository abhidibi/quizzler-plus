# 🧠 Quizzler+ – Python Trivia with Categories, Difficulty & History

Quizzler+ is a **feature-rich Python GUI quiz** that pulls live questions from the **Open Trivia Database** and lets you choose **category**, **difficulty**, and **question type (MCQ / True–False)**. It saves your **score history** locally and provides a clean end-of-quiz summary.

## ✨ What’s New vs. a Basic Quiz
- 🌐 **Live API** questions (with **local fallback** if offline)
- 🎛 **Category & Difficulty** pickers
- 🔀 **Multiple choice** *and* True/False modes
- 📊 **Score history** saved to `score_history.csv` + built-in viewer
- 🧠 **End-of-quiz summary** with percentage + replay
- 🧩 Clean **OOP separation** (data, model, logic, UI)

## 🛠 Tech
- Python 3
- Tkinter (GUI), Requests (API), CSV (history), `html` (entity decoding)

## 🚀 Run It
```bash
pip install requests
python main.py
