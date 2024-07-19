def reformat_questions(input_file, output_file):
    with open(input_file, 'r', encoding='latin-1') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        lines = infile.readlines()
        
        question_number = ""
        question_text = ""
        options = []
        answer = ""
        reference = ""
        in_options = False
        
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith("QUESTION NO:"):
                if question_text or options or answer:
                    write_question(outfile, question_number, question_text, options, answer, reference)
                question_number = stripped_line
                question_text = ""
                options = []
                answer = ""
                reference = ""
                in_options = False
            elif stripped_line.startswith("A.") or stripped_line.startswith("B.") or stripped_line.startswith("C.") or stripped_line.startswith("D."):
                options.append(stripped_line)
                in_options = True
            elif stripped_line.startswith("Answer:"):
                answer = stripped_line
                in_options = False
            elif stripped_line.startswith("Reference:") or stripped_line.startswith("Explanation:"):
                reference = stripped_line
                in_options = False
            else:
                if in_options:
                    options[-1] += " " + line.strip()
                elif question_number:
                    question_text += " " + line.strip()
        
        if question_text or options or answer:
            write_question(outfile, question_number, question_text, options, answer, reference)

def write_question(outfile, question_number, question_text, options, answer, reference):
    outfile.write(f"{question_number}\n\n")
    outfile.write(f"{question_text.strip()}\n\n")
    for option in options:
        outfile.write(f"{option}\n\n")
    outfile.write(f"{answer}\n")
    outfile.write(f"{reference}\n\n")

# Rutas de los archivos de entrada y salida
input_file = r'G:\Learn\CISSP\Testkings\CISSP.txt'
output_file = r'.\preguntas_reformateadas.txt'

reformat_questions(input_file, output_file)
