import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import matplotlib.pyplot as plt

class QuizApp:
    def __init__(self, master, questions):
        self.master = master
        self.master.title("Simulador de Exámenes")

        # Preguntar cuántas preguntas quiere el usuario
        num_questions = simpledialog.askinteger("Input", f"¿Cuántas preguntas quieres responder? (1-{len(questions)})",
                                                minvalue=1, maxvalue=len(questions))
        self.questions = random.sample(questions, num_questions)
        self.total_questions = num_questions
        
        self.question_index = 0
        self.score = 0
        self.incorrect_questions = []
        self.time_limit = 60  # Tiempo límite en segundos por pregunta

        self.question_label = tk.Label(master, text="", wraplength=600, justify="left")
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()
        self.options = [tk.Radiobutton(master, text="", variable=self.var, value=chr(65+i)) for i in range(4)]
        for option in self.options:
            option.pack(anchor="w")

        self.submit_button = tk.Button(master, text="Responder", command=self.check_answer)
        self.submit_button.pack(pady=20)

        self.result_label = tk.Label(master, text="", fg="blue")
        self.result_label.pack(pady=10)

        self.explanation_label = tk.Label(master, text="", fg="black", wraplength=600, justify="left")
        self.explanation_label.pack(pady=10)

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
        self.result_label.config(text="")
        self.explanation_label.config(text="")

    def check_answer(self):
        selected_answer = self.var.get()
        question_data = self.questions[self.question_index]
        correct_answer = question_data['answer']
        explanation = question_data.get('explanation', 'No hay explicación disponible.')
        reference = question_data.get('reference', '')
        
        if selected_answer == correct_answer:
            self.score += 1
            result = "Correcto"
            self.result_label.config(text=result, fg="green")
        else:
            result = f"Incorrecto. La respuesta correcta es {correct_answer}"
            self.result_label.config(text=result, fg="red")
            self.incorrect_questions.append(question_data['question'])
        
        self.explanation_label.config(text=f"Explicación: {explanation}\nReferencia: {reference}")
        
        self.question_index += 1
        if self.question_index < self.total_questions:
            self.master.after(5000, self.show_question)
        else:
            self.master.after(5000, self.show_result)

    def show_result(self):
        porcentaje_aciertos = (self.score / self.total_questions) * 100
        porcentaje_fallas = 100 - porcentaje_aciertos
        self.plot_results(porcentaje_aciertos, porcentaje_fallas)

    def plot_results(self, porcentaje_aciertos, porcentaje_fallas):
        fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(aspect="equal"))
        
        labels = [f'Aciertos ({self.score})', f'Fallos ({self.total_questions - self.score})']
        sizes = [porcentaje_aciertos, porcentaje_fallas]
        colors = ['#4CAF50', '#FF5733']
        
        wedges, texts, autotexts = ax.pie(sizes, colors=colors, autopct='%1.1f%%', startangle=90, 
                                          wedgeprops=dict(width=0.3), pctdistance=0.85)

        # Añadir círculo central para efecto de dona
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig.gca().add_artist(centre_circle)
        
        # Estilo del texto
        plt.setp(autotexts, size=12, weight="bold", color="white")

        # Añadir leyenda
        ax.legend(wedges, labels, title="Resultados", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        plt.title('Resultados del Examen', fontsize=16, weight='bold')
        plt.show()

        if self.incorrect_questions:
            incorrect_questions_text = "\n".join(self.incorrect_questions)
            with open("incorrect_questions.txt", "w", encoding="utf-8") as f:
                f.write(incorrect_questions_text)
            messagebox.showinfo("Preguntas Incorrectas", f"Las preguntas incorrectas se han guardado en 'incorrect_questions.txt'")

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
    
    question_data = {'question': '', 'options': [], 'answer': '', 'explanation': '', 'reference': ''}
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("QUESTION NO:"):
            if question_data['question']:
                questions.append(question_data)
                question_data = {'question': '', 'options': [], 'answer': '', 'explanation': '', 'reference': ''}
            question_data['question'] = stripped_line + "\n\n"
        elif stripped_line.startswith("A.") or stripped_line.startswith("B.") or stripped_line.startswith("C.") or stripped_line.startswith("D."):
            question_data['options'].append(stripped_line)
        elif stripped_line.startswith("Answer:"):
            if ": " in stripped_line:
                question_data['answer'] = stripped_line.split(": ")[1]
            else:
                question_data['answer'] = stripped_line.split(":")[1]
        elif stripped_line.startswith("Explanation:"):
            question_data['explanation'] = stripped_line.split(": ", 1)[1] if ": " in stripped_line else stripped_line.split(":", 1)[1]
        elif stripped_line.startswith("Reference:"):
            question_data['reference'] = stripped_line.split(": ", 1)[1] if ": " in stripped_line else stripped_line.split(":", 1)[1]
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
