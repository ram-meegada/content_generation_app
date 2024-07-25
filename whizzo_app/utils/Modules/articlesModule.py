import json
import openai
from io import BytesIO
import urllib.request as urlopener
from PyPDF2 import PdfReader
from decouple import config

openai.api_key = config("OPENAI_KEY")
API_KEY = config("OPENAI_KEY")


def generate_article_util(topic, tone, pov, region, words):
    query = f"""
        You are article generator. Generate an article on {topic} in the point of view of {pov} which I provide you. Whole Article should be in arabic language and of approximately {words} words with voice of tone as {tone} and article should belongs to {region} region. Format should be descriptive. Strictly keep Headings for article topics as(numbered as 1,2,3) and a small descriptive paragraph for each heading.

        Additionally, ensure the response is formatted as a JSON object with the following structure:
        {{
            "title": "string",
            "content": {{
                "1": {{
                    "heading": "string of minimum 10 lettes",
                    "content": "string"
                }}
            }}
        }}
        """
    messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output articles in JSON string based on prompt. The output should be strictly in arabic language."},
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
