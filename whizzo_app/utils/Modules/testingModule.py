import json
import openai
from io import BytesIO
import urllib.request as urlopener
from PyPDF2 import PdfReader
from decouple import config

openai.api_key = config("OPENAI_KEY")
API_KEY = config("OPENAI_KEY")



def chatGPT_pdf_processing(text_data, query):
    try:
        messages=[
                        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                        {"role": "user", "content": [
                                {"type": "text", "text": query},
                                {"type": "text", "text": f"Input data: {text_data}"}
                            ]}
                    ]
        chatbot = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages,response_format={ "type": "json_object" },temperature = 0.0,
        )
        reply = chatbot.choices[0].message.content
        final_data = json.loads(reply)
        data =[]
        try:
            for i in final_data:
                for j in final_data[i]:
                    data.append(j)
        except TypeError:
            data.append(final_data)            
        except Exception as err:
            print(err, type(err), '======')            
        return data
    except Exception as err:
        print(err, '--------chatgpt error--------')
        return []    

def extract_data_from_url(pdf_file):
    pdf_text = ''
    url_obj = urlopener.urlopen(pdf_file)
    pdf_stream = BytesIO(url_obj.read())
    pdf_reader = PdfReader(pdf_stream)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()         
    chunk_size = 12000
    chunks = [pdf_text[i:i+chunk_size] for i in range(0, len(pdf_text), chunk_size)]
    return chunks

def chatGPT_image_processing(img_file, query):
    try:
        messages=[
                        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                        {"role": "user", "content":[
                            {"type": "text","text": query},
                            {"type": "image_url", "image_url": {
                                "url":str(img_file)}
                            }
                        ]}
                    ]
        chatbot = openai.ChatCompletion.create(
            model="gpt-4o", messages=messages,response_format={ "type": "json_object" },temperature = 0.0,
        )
        reply = chatbot.choices[0].message.content
        final_data = json.loads(reply)
        data =[]
        for i in final_data:
            for j in final_data[i]:
                data.append(j)
        return data
    except:
        return []
    
def testing_extract_text(file):
    text_data = []
    temp = {1: [2000, 8], 2: [4000, 5], 3: [8000, 4], 4: [12000, 3]}
    with file.open() as f:
        pdf_stream = BytesIO(f.read())
        data = PdfReader(pdf_stream)
    i, j = 0, 0
    while i < len(data):
        end = i+temp[j+1][0]
        if end > len(data)-1:
            text_data.append(data[i:])
        else: 
            text_data.append(data[i: end])    
        i += temp[j+1][0]
        j += 1
    return text_data