# Convierte de PDF a CSV
import PyPDF2
import csv

def pdf_to_csv(pdf_path, csv_path):
    # Abrir el archivo PDF
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        
        # Abrir el archivo CSV para escritura
        with open(csv_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            
            # Iterar a través de todas las páginas y extraer texto
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                
                # Asumiendo que las preguntas y respuestas están separadas por líneas
                lines = text.split('\n')
                
                for line in lines:
                    csv_writer.writerow([line])

# Rutas a los archivos de entrada PDF y salida CSV
pdf_path = r'G:\Learn\CISSP\Testkings\CISSP.pdf'
csv_path = r'.\CISSP.csv'

pdf_to_csv(pdf_path, csv_path)
