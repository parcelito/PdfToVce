import tkinter as tk
from tkinter import messagebox

class IncorrectQuestionsWindow:
    def __init__(self, master, incorrect_questions):
        self.master = master
        self.incorrect_questions = incorrect_questions
        self.incorrect_index = 0

        self.incorrect_window = tk.Toplevel(master)
        self.incorrect_window.title("Preguntas Incorrectas")

        self.incorrect_question_label = tk.Label(self.incorrect_window, text="", wraplength=600, justify="left")
        self.incorrect_question_label.pack(pady=20)

        self.incorrect_options_label = tk.Label(self.incorrect_window, text="", wraplength=600, justify="left")
        self.incorrect_options_label.pack(pady=10)

        self.incorrect_selected_label = tk.Label(self.incorrect_window, text="", wraplength=600, justify="left", fg="red")
        self.incorrect_selected_label.pack(pady=10)

        self.incorrect_correct_label = tk.Label(self.incorrect_window, text="", wraplength=600, justify="left", fg="green")
        self.incorrect_correct_label.pack(pady=10)

        self.incorrect_explanation_label = tk.Label(self.incorrect_window, text="", wraplength=600, justify="left")
        self.incorrect_explanation_label.pack(pady=10)

        self.next_button = tk.Button(self.incorrect_window, text="Siguiente", command=self.next_incorrect_question)
        self.next_button.pack(pady=20)

        self.show_incorrect_question()

    def show_incorrect_question(self):
        question_data = self.incorrect_questions[self.incorrect_index]
        options_text = "\n".join(question_data['options'])
        self.incorrect_question_label.config(text=question_data['question'])
        self.incorrect_options_label.config(text=f"Opciones:\n{options_text}")
        self.incorrect_selected_label.config(text=f"Tu respuesta: {question_data['selected_answer']}")
        self.incorrect_correct_label.config(text=f"Respuesta correcta: {question_data['correct_answer']}")
        self.incorrect_explanation_label.config(text=f"Explicación: {question_data['explanation']}\nReferencia: {question_data['reference']}")

    def next_incorrect_question(self):
        self.incorrect_index += 1
        if self.incorrect_index < len(self.incorrect_questions):
            self.show_incorrect_question()
        else:
            self.incorrect_window.destroy()
            self.ask_retry()

    def ask_retry(self):
        retry = messagebox.askyesno("Final del examen", "¿Quieres intentar el examen de nuevo?")
        if retry:
            for widget in self.master.winfo_children():
                widget.destroy()
            self.master.reset_quiz()
        else:
            self.master.quit()
