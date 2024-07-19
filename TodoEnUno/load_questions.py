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
