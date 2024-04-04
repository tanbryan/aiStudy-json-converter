import json
import os
from PyPDF2 import PdfReader #
import openai
from dotenv import load_dotenv
from langchain_community.document_loaders import UnstructuredFileLoader

def convert_txt(text, example_json):
    messages = [
        {"role": "system", "content": "You are an assistant skilled in structuring text into JSON format based on provided templates and examples."},
        {"role": "user", "content": f"Given the following template and an example of structured JSON, structure this provided text only into a JSON format with no other information, only the json object.\n\nPlease strictly follow this example JSON structure:\n{example_json}\n\nText excerpt to structure: \"{text}\""}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        temperature=0.0,
        max_tokens=4096,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    if response['choices']:
        last_message = response['choices'][-1]['message']['content']
        return last_message.strip()
    else:
        print("No response received.")
        return ""

def convert_title(title):
    instruction = (
        "Convert a filename into a formatted title json object. "
        "The filename format is typically like '大学英语六级考试 YYYY年MM月真题(第N套).pdf', "
        "where YYYY is the year, MM is the month, and N is the set number. "
        "The output should simply be a JSON object with the format 'YYYY-MM-Level6-N'. "
        "For example, given the filename '大学英语六级考试 2023年12月真题(第三套).pdf', "
        "the corresponding JSON object should be 'title': '2023-12-Level6-3'. "
        "Now, given a new filename: '{}', convert it into the expected JSON object format with no other information, only the json object."
    ).format(title)

    messages = [
        {"role": "system", "content": "You are an assistant skilled in converting a filename into a formatted title json object based on provided templates and examples."},
        {"role": "user", "content": instruction}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        temperature=0.0,
        max_tokens=1000,
    )

    if 'choices' in response and response['choices']:
        message = response['choices'][-1]['message']['content']
        return message.strip()
    else:
        print("No response received.")
        return ""