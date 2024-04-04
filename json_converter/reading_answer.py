# import json
# import openai
# import os
# from PyPDF2 import PdfReader
# from dotenv import load_dotenv
# load_dotenv()

# openai.api_key = os.environ.get("OPENAI_API_KEY")

# def extract(pdf_path):
#     reader = PdfReader(pdf_path)
#     extracted_text = ""
#     for page in reader.pages:
#         extracted_text += page.extract_text() + "\n"
    
#     start_identifier = "Reading Comprehension"
#     end_identifier = "Part  IV"
    
#     start_index = extracted_text.find(start_identifier)
#     end_index = extracted_text.find(end_identifier, start_index)
    
#     if start_index != -1:
#         start_index += len(start_identifier)
    
#     if end_index != -1:
#         desired_text = extracted_text[start_index:end_index].strip()
#     else:
#         desired_text = extracted_text[start_index:].strip() 

#     base_name = os.path.basename(pdf_path)
#     filename = os.path.splitext(base_name)[0]
#     save_path = f"{filename}_reading_answer.txt"
    
#     with open(save_path, 'w', encoding='utf-8') as file:
#         file.write(desired_text)
    
#     print(f"{save_path} created")
#     return save_path
    
# def split(path):
#     with open(path, 'r', encoding='utf-8') as f:
#         text = f.read()
#     sections = [section.strip() for section in text.split("Section") if section.strip()]
#     section = ["Section" + section for section in sections]
#     print(section[0])
#     return section

# def load_txt(path):
#     with open(path, 'r', encoding='utf-8') as f:
#         text = f.read()
#     return text

# def convert_txt(text, template, example_json):
#     messages = [
#         {"role": "system", "content": "You are an assistant skilled in structuring answer explanation text into JSON format based on provided templates and examples."},
#         {"role": "user", "content": f"Given the following template and an example of structured JSON, structure this provided answer explanation text into a JSON format.\n\nTemplate for reference:\n{template}\n\nExample JSON structure:\n{example_json}\n\nText excerpt to structure: \"{text}\""}
#     ]

#     response = openai.ChatCompletion.create(
#         model="gpt-4-turbo-0125",
#         messages=messages,
#         temperature=0.0,
#         max_tokens=4096,
#         top_p=1.0,
#         frequency_penalty=0.0,
#         presence_penalty=0.0
#     )

#     if response['choices']:
#         last_message = response['choices'][-1]['message']['content']
#         print(last_message.strip())
#         return last_message.strip()
#     else:
#         print("No response received.")
#         return ""
# ## extract answer key from the answer explanation json object from the model above

# def save(data, filename):
#     with open(filename, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=4)
#     print(f"{filename} created")

# def main():
#     pdf_path = "/Users/bryannnh/Desktop/第1套.pdf"
#     answer_template_path = "ref/material_template.txt"
#     explanation_template_path = "ref/material_template.txt"
#     example_answer_json_path = "ref/material_2013_06_Level6_1.json"
#     example_explanation_json_path = ""

#     save_path = extract(pdf_path)
#     sections = split(save_path)

#     answer_template_text = load_txt(answer_template_path)
#     example_answer_json_text = load_txt(example_json_path)  
#     explanation_template_text = load_txt(example_answer_json_path)
#     example_explanation_json_text = load_txt(example_explanation_json_path)  
    
#     structured_results = {}
#     titles = convert_title(pdf_path)

#     for section_text in sections:
#         obj = convert_txt(section_text, explanation_template_text, example_explanation_json_text)
#         answer = convert_answer(section_text, answer_template_text, example_answer_json_text)
#         try:
#             data = json.loads(obj)
#             title = json.loads(titles)
#             structured_results.update(title)
#             structured_results.update(data)
#         except json.JSONDecodeError as e:
#             print(f"Failed to decode the structured JSON for a section. Error: {e}")

#     new_title = convert_title(os.path.basename(pdf_path))
#     new_json_filename = f"material_{new_title}.json"
    
#     save(structured_results, new_json_filename)


# if __name__ == "__main__":
#     main()
