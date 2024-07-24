import json
import openai
from io import BytesIO
import urllib.request as urlopener
from PyPDF2 import PdfReader
from decouple import config

openai.api_key = config("OPENAI_KEY")
API_KEY = config("OPENAI_KEY")



def chatGPT_pdf_processing(text_data, query):
    messages=[
                    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                    {"role": "user", "content":[
                        {"type": "text", "text": query},
                        {"type": "text", "text":text_data}
                    ]}
                ]
    chatbot = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages,response_format={ "type": "json_object" },temperature = 0.0,
    )
    reply = chatbot.choices[0].message.content
    final_data = json.loads(reply)
    data =[]
    for i in final_data:
        for j in final_data[i]:
            data.append(j)
    return data

def extract_data_from_url(pdf_file):
    pdf_text = ''
    url_obj = urlopener.urlopen(pdf_file)
    pdf_stream = BytesIO(url_obj.read())
    pdf_reader = PdfReader(pdf_stream)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()         
    chunk_size = 16000
    chunks = [pdf_text[i:i+chunk_size] for i in range(0, len(pdf_text), chunk_size)]
    return chunks

