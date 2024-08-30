import json
import openai
from io import BytesIO
import urllib.request as urlopener
from PyPDF2 import PdfReader
from decouple import config

openai.api_key = config("OPENAI_KEY")
API_KEY = config("OPENAI_KEY")



def assigment_chatGPT_pdf_processing(text_data, language):
    # query = f"""
    #     "You are a teacher. Generate questions and answers based on the data I provide to you and make sure to give output in {language} language only. Format should be proper Python Javascript object notation list of dictionaries where every dictionary contains keys as 'question_no', 'question', 'correct_answer' and 'options'(if available)."
    #     Additionally, ensure the response is formatted as a JSON object with the following structure:
    #     {{
    #         "question_no": "number",
    #         "question": "string",
    #         "question_type": "integer 1 for subjective type question and 2 for MCQ type question."
    #         "options": "list of options. if no options then empty list []",
    #         "correct_answer": "string",
    #     }}
    #     """
    query = f"""
            "You are a teacher. Generate questions and answers based on the data I provide to you and make sure to give output in {language} language only. Format should be proper pretty HTML format."
            Additionally, ensure the response is formatted as the following structure sample:
            {{"html_content":
                    <body>
                        <p><strong>Question 1:</strong> What is the origin of cricket?</p>
                        <p><strong>Answer 1:</strong> Cricket originated in England during the 16th century. It evolved from a game played by children in the countryside and became a popular sport by the 18th century. The first international match was played in 1844 between the United States and Canada.</p>
                        .......
                        <p><strong>Question n:</strong> who is kane williamson in cricket?</p>
                        <p><strong>Answer n:</strong> Cricket originated in England during the 16th century. It evolved from a game played by children in the countryside and became a popular sport by the 18th century. The first international match was played in 1844 between the United States and Canada.</p>
                    <body />    
            }}
        """
    try:
        messages=[
                        {"role": "system", "content": "You are a helpful assistant designed to provide HTML content in JSON"},
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
        return final_data
    except:
        return []    

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

def assignment_extract_text(file_link):
        pdf_text = ""
        with file_link.open() as f:
            pdf_stream = BytesIO(f.read())
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