import os
import fitz  # PyMuPDF
import json

def extract_text_from_pdf(uploaded_file):
    pdf_text = ""

    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as pdf_document:
        total_pages = pdf_document.page_count

        for page_number in range(total_pages):
            page = pdf_document[page_number]
            text = page.get_text()
            text = text.replace("\n", " ")
            pdf_text += text

    return pdf_text

def process_uploaded_pdf(uploaded_file, length_part, base_path="./local_cache"):
    pdf_text = extract_text_from_pdf(uploaded_file)

    # Criar o diretório se não existir
    save_directory = os.path.join(base_path)
    os.makedirs(save_directory, exist_ok=True)

    # Caminho completo do arquivo TXT
    txt_file_path = os.path.join(save_directory, "converted_text.txt")

    # Salvar o texto no arquivo TXT
    with open(txt_file_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(pdf_text)

    pdf_parts = []
    for i in range(0, len(pdf_text), length_part):
        part_text = pdf_text[i:i+length_part]
        pdf_parts.append({"id": len(pdf_parts) + 1, "text": part_text})

    json_file_path = os.path.join(save_directory, "converted_text.json")
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(pdf_parts, json_file, ensure_ascii=False, indent=3)
    
    # reload json and return it
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        json_object = json.load(json_file)

    return json_object
