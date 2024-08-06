import json
import openai
from io import BytesIO
import urllib.request as urlopener
from PyPDF2 import PdfReader
from decouple import config

openai.api_key = config("OPENAI_KEY")
API_KEY = config("OPENAI_KEY")


def generate_presentation_util(topic, slides, input_language):
    query = f"""
        You are a presentation maker. Give me contents to make a presentation of {slides} slides on the topic - {topic} in {input_language} language. The content of each slide should be more than 500 words strictly with proper headings. 

        Additionally, ensure the response is formatted as a JSON object with the following structure:
        {{
            "Slide_number(string number)": {{
            "heading": "string",
            "content": "text"
            }}
        }}
        """
    messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output presentation content in JSON string based on prompt"},
                {"role": "user", "content":[
                    {"type": "text", "text": query}
                ]}
            ]
    chatbot = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, response_format={ "type": "json_object" }, temperature = 0.0,
    )
    reply = chatbot.choices[0].message.content
    final_data = json.loads(reply)
    return final_data
