from tkinter import Tk
from quiz_app import QuizApp
from load_questions import load_questions

if __name__ == "__main__":
    questions = load_questions(r'.\preguntas_reformateadas.txt')
    root = Tk()
    app = QuizApp(root, questions)
    root.mainloop()
