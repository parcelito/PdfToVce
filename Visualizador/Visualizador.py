import tkinter as tk
from tkinter import messagebox

class QuizApp:
    def __init__(self, master, questions):
        self.master = master
        self.master.title("Simulador de Exámenes")
        
        self.question_index = 0
        self.score = 0
        self.time_limit = 60  # Tiempo límite en segundos por pregunta
        self.questions = questions
        self.total_questions = len(self.questions)
        
        self.question_label = tk.Label(master, text="", wraplength=600, justify="left")
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()
        self.options = [tk.Radiobutton(master, text="", variable=self.var, value=chr(65+i)) for i in range(4)]
        for option in self.options:
            option.pack(anchor="w")

        self.submit_button = tk.Button(master, text="Responder", command=self.check_answer)
        self.submit_button.pack(pady=20)

        self.time_label = tk.Label(master, text="Tiempo restante: ")
        self.time_label.pack(pady=10)

        self.show_question()
        self.update_timer()

    def show_question(self):
        self.time_remaining = self.time_limit
        question_data = self.questions[self.question_index]
        self.question_label.config(text=question_data['question'])
        for i, option in enumerate(question_data['options']):
            self.options[i].config(text=option)
        self.var.set(None)

    def check_answer(self):
        selected_answer = self.var.get()
        correct_answer = self.questions[self.question_index]['answer']
        if selected_answer == correct_answer:
            self.score += 1
        self.question_index += 1
        if self.question_index < self.total_questions:
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        messagebox.showinfo("Resultado", f"Has respondido correctamente {self.score} de {self.total_questions} preguntas.")
        self.master.quit()

    def update_timer(self):
        if self.time_remaining > 0:
            self.time_label.config(text=f"Tiempo restante: {self.time_remaining} segundos")
            self.time_remaining -= 1
            self.master.after(1000, self.update_timer)
        else:
            self.check_answer()

def load_questions(filename):
    questions = []
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    question_data = {'question': '', 'options': [], 'answer': ''}
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("QUESTION NO:"):
            if question_data['question']:
                questions.append(question_data)
                question_data = {'question': '', 'options': [], 'answer': ''}
            question_data['question'] = stripped_line + "\n\n"
        elif stripped_line.startswith("A.") or stripped_line.startswith("B.") or stripped_line.startswith("C.") or stripped_line.startswith("D."):
            question_data['options'].append(stripped_line)
        elif stripped_line.startswith("Answer:"):
            if ": " in stripped_line:
                question_data['answer'] = stripped_line.split(": ")[1]
            else:
                question_data['answer'] = stripped_line.split(":")[1]
        elif question_data['question']:
            question_data['question'] += stripped_line + " "
    
    if question_data['question']:
        questions.append(question_data)

    return questions

if __name__ == "__main__":
    questions = load_questions(r'.\preguntas_reformateadas.txt')
    root = tk.Tk()
    app = QuizApp(root, questions)
    root.mainloop()
