import json
import os
from PyPDF2 import PdfReader #
import openai
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader

def reading_extract(pdf_path, attempt=1, max_attempts=2):
    pdf_directory = os.path.dirname(pdf_path)
    base_name = os.path.basename(pdf_path)
    filename = os.path.splitext(base_name)[0]
    save_path = os.path.join(pdf_directory, f"{filename}_reading_question.txt")

    if attempt > max_attempts:
        print("Maximum attempts reached. Exiting extraction.")
        return None

    if os.path.exists(save_path):
        print(f"{save_path} already exists. Checking content.")
        with open(save_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if len(content) >= 1000:  # 检查提取的文本是否足够长
                print("Existing content is satisfactory. No need for re-extraction.")
                return save_path
            else:
                print(f"Existing content in {save_path} is too short. Attempting re-extraction.")
                os.remove(save_path)  

    print(f"Attempt {attempt}: Using PdfReader to extract text.")
    ## 首先用pdfreader提取文本，速度比较快
    print("Using PdfReader to extract text.")
    reader = PdfReader(pdf_path)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text() + "\n"

    ## 有时候提取的文本不完整，用unstructured_file_loader重新提取
    if len(extracted_text.replace("\n", "").strip()) < 1000:
        print("Using UnstructuredFileLoader to extract text.")
        extracted_text = ""
        loader = UnstructuredFileLoader(pdf_path)
        reader = loader.load()
        extracted_text = [doc.page_content for doc in reader]
        extracted_text = "\n".join(extracted_text)

    start_identifier = "40 minutes"
    end_identifier = "Part  IV"
    
    start_index = extracted_text.find(start_identifier)
    end_index = extracted_text.find(end_identifier, start_index)
    
    if start_index != -1:
        start_index += len(start_identifier)
    
    desired_text = extracted_text[start_index:end_index if end_index != -1 else None].strip()

        # 如果提取的文本太短，用unstructured_file_loader重新提取
    if len(desired_text) < 1000 and attempt <= max_attempts:
        print("Desired text is incomplete, using UnstructuredFileLoader for a more thorough extraction.")
        return reading_extract(pdf_path, attempt + 1)  # 重新提取

    if len(desired_text) >= 1000:  # 检查提取的文本是否足够长
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(desired_text)
        print(f"{save_path} created.")
        return save_path
    else:
        print("Failed to extract sufficient content. No file created.")
        return None
        
def split(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    sections = [section.strip() for section in text.split("Section") if section.strip()]
    section = ["Section" + section for section in sections]
    return section