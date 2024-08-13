import openai
import os
from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from langchain_google_genai import ChatGoogleGenerativeAI
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from langchain_core.messages import HumanMessage
from whizzo_project import settings
import base64
import json
from io import BytesIO
from PyPDF2 import PdfReader
from whizzo_app.utils.saveImage import save_image
from whizzo_app.utils.Modules.fileSummaryModule import image_processing_assignment_solution, to_markdown
from whizzo_app.models.abilityModel import AbilityModel
from whizzo_app.utils.Modules.articlesModule import generate_article_util

class ArticleConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        try:
            llm = ChatGoogleGenerativeAI(model="gemini-pro")
            payload = json.loads(event["text"])
            if "record_id" not in payload:
                topic = payload.get("topic")
                words = payload.get("words")
                language = payload.get("language").lower()
                region = payload.get("region")
                tone = payload.get("tone")
                pov = payload.get("pronouns")
            elif "record_id" in payload:
                get_article_record = AbilityModel.objects.get(
                    id=payload.get("record_id"))
                topic = get_article_record.topic
                tone = get_article_record.tone
                pov = get_article_record.pov
                language = get_article_record.language.lower()
                region = get_article_record.region
                words = get_article_record.words
            ####
            if language == "english":
                QUERY = f"You are article generator. Generate an article on {topic} in the point of view of {pov} which I provide you. Whole Article should be in {language} and of approximately {words} words with voice of tone as {tone} and article should belongs to {region} region. Format should be descriptive. Strictly keep Headings(numbered as 1,2,3)."
                message_content = [
                    {
                        "type": "text",
                        "text": QUERY
                    }
                ]
                message = HumanMessage(content=message_content)
                # response = llm.invoke([message])
                # final_response = response.content.replace(
                #     "*", "").replace("#", "").replace("-", "")
                for chunk in llm.stream([message]):
                    stream_chunk = chunk.content
                    self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({"data": stream_chunk, "signal": 1})
                    })    
            elif language == "arabic":
                # result = generate_article_util(topic, tone, pov, region, words)
                QUERY = f"You are article generator. Generate an article on {topic} in the point of view of {pov} which I provide you. Whole Article should be in {language} and of approximately {words} words with voice of tone as {tone} and article should belongs to {region} region. Format should be descriptive. Strictly keep Headings(numbered as 1,2,3)."
                message_content = [
                    {
                        "type": "text",
                        "text": QUERY
                    }
                ]
                message = HumanMessage(content=message_content)
                # response = llm.invoke([message])
                # final_response = response.content.replace(
                #     "*", "").replace("#", "").replace("-", "")
                for chunk in llm.stream([message]):
                    stream_chunk = chunk.content
                    self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({"data": stream_chunk, "signal": 1})
                    })
            # save record
            # if "record_id" not in payload:
            #     get_article_record = AbilityModel.objects.create(
            #         user_id=,
            #         topic=topic,
            #         language=language,
            #         region=region,
            #         pov=pov,
            #         words=words,
            #         tone=tone,
            #         result=final_response
            #     )
            # elif "record_id" in payload:
            #     get_article_record.result = final_response
            #     get_article_record.save()
            self.send({
                        'type': 'websocket.send',
                        'text': json.dumps({"data": "", "signal": 0})
                    })    
        except Exception as err:
            print(err, '-------errr---------')
            self.send({
                        "type": "websocket.send",
                        "text": json.dumps({"data": str(err), "signal": 0, "message": "Something went wrong", "status": 400})
                    })
            self.send({
                "type": "websocket.close"
                })  

    def websocket_disconnect(self, event):
        print('websocket disconnected.....', event)
        raise StopConsumer()


def generate_article_util(topic, tone, pov, region, words):
    query = f"""
        You are article generator. Generate an article on {topic} in the point of view of {pov} which I provide you. Whole Article should be in arabic language and of approximately {words} words with voice of tone as {tone} and article should belongs to {region} region. Format should be descriptive. Strictly keep Headings for article topics as(numbered as 1,2,3) and a small descriptive paragraph for each heading.

        Additionally, ensure the response is formatted as a JSON object with the following structure:
        {{
            "title": "string",
            "content": {{
                "1": {{
                    "heading": "string of minimum 10 letters",
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
    for chunk in chatbot:
        if 'choices' in chunk:
            text = chunk['choices'][0]['text']
            print(text, end='')