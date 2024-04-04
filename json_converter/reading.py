import json
import os
from PyPDF2 import PdfReader #
import openai
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader

from .extraction import reading_extract, split
from .utils import save, load_txt
from .conversion import convert_txt, convert_title


load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

def main():
    pdf_path = input("Enter the path to the PDF file: ") ##换成你需要的pdf的路径
    example_json_path = "ref/阅读_template_format.json"

    save_path = reading_extract(pdf_path)
    sections = split(save_path)

    example_json_text = load_txt(example_json_path)  
    
    structured_results = {}
    max_retries_titles = 2  # 有时候模型自己output的json有问题，无法decode
    retry_count_title = 0
    while retry_count_title < max_retries_titles:
        try:
            titles = convert_title(pdf_path)
            json_string_titles = titles.replace('```json\n', '').replace('\n```', '')
            title = json.loads(json_string_titles)
            structured_results.update(title)
            print("Title converted successfully.")
            break  # Exit if successful
        except json.JSONDecodeError as e:
            print(f"Retry {retry_count_title + 1} failed for title. Error: {e}")
            retry_count_title += 1
            if retry_count_title == max_retries_titles:
                print("Max retries reached.")

    max_retries = 3
    for section_text in sections:
        retry_count = 0
        while retry_count < max_retries:
            obj = convert_txt(section_text, example_json_text)
            try:
                json_string_data = obj.replace('```json\n', '').replace('\n```', '')
                data = json.loads(json_string_data)
                structured_results.update(data)
                print("Section converted successfully.")
                break  # Exit if successful
            except json.JSONDecodeError as e:
                print(f"Retry {retry_count + 1} failed for a section. Error: {e}")
                retry_count += 1
                if retry_count == max_retries:
                    print("Max retries reached. Moving to the next section.")

    pdf_directory = os.path.dirname(pdf_path)
    new_title = title["title"]
    new_json_filename = f"Reading_{new_title}.json"
    new_json_path = os.path.join(pdf_directory, new_json_filename)
    
    save(structured_results, new_json_path)


if __name__ == "__main__":
    main()
