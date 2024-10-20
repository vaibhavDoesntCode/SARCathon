import google.generativeai as genai
import os
import textwrap
import json
# import dotenv

from IPython.display import display
from IPython.display import Markdown

GOOGLE_API_KEY = 'AIzaSyDAh7Ug0TKtRuq6w7RAjekLlvy8SRLza1M'
genai.configure(api_key=GOOGLE_API_KEY)

def read_data(file_path):
    with open(file_path, "r") as f:
        faq_data = json.load(f)
    return faq_data

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

model = genai.GenerativeModel('gemini-1.5-flash-8b-exp-0924')

chat = model.start_chat(history=[])

JSON_FILE_PATH = "faqs.json"
faqs_data = read_data(JSON_FILE_PATH)

prompt = "Who is Vaibhav?"

data = {
   "prompt": prompt,
   "data": faqs_data
}

model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat(history=[])

response = chat.send_message(json.dumps(data))


print(response.text)

# while True:
#     prompt = input("Ask me anything: ")
#     if (prompt == "exit"):
#         break
#     response = chat.send_message(prompt, stream=True)
#     for chunk in response:
#         if chunk.text:
#           print(chunk.text)

