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
from whizzo_app.models.articleModel import ArticleModel
from whizzo_app.utils.Modules.articlesModule import generate_article_util
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
class ArticleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        return await super().connect()

    async def receive(self, text_data=None, bytes_data=None):
        payload = json.loads(text_data)
        print(payload,'========')
        result = ""
        try:
            access_token = AccessToken(payload["token"])
            token_payload = access_token.payload
            user_id = token_payload.get('user_id')
            USER_ID = user_id            
            llm = ChatGoogleGenerativeAI(model="gemini-pro")
            if "record_id" not in payload:
                topic = payload.get("topic")
                words = payload.get("words")
                language = payload.get("language").lower()
                region = payload.get("region")
                tone = payload.get("tone")
                pov = payload.get("pronouns")
            elif "record_id" in payload:
                get_article_record = await database_sync_to_async(ArticleModel.objects.get)(
                    id=payload.get("record_id"))
                topic = get_article_record.topic
                tone = get_article_record.tone
                pov = get_article_record.pov
                language = get_article_record.language.lower()
                region = get_article_record.region
                words = get_article_record.words
            ####
            print(language,"====language==")
            if language == "english":
                QUERY = f"You are article generator  Whole Article should be in {language} language strictly. Generate an article on {topic} in the point of view of {pov} which I provide you. Whole Article should be  of approximately {words} words with voice of tone as {tone} and article should be from the perspective of a person from {region} . Format should be in strictly HTML format. Only provide the content of the body tag of html output and give headings in h4 tag only. Strictly keep Headings(numbered as 1,2,3)..Dont stop in middle at least complete the contents in a heading and then stop."
                message_content = [
                    {
                        "type": "text",
                        "text": QUERY
                    }
                ]
                message = HumanMessage(content=message_content)
                try:
                    async for chunk in llm.astream([message]):
                        stream_chunk = chunk.content
                        stream_chunk = stream_chunk.replace("*", "").replace("`", "").replace("html", "").replace("\n", "")
                        # print (stream_chunk)
                        result += stream_chunk
                        await self.send(text_data=json.dumps({"data": result, "signal": 1}))
                except:
                    pass    
            elif language == "arabic":
                # result = generate_article_util(topic, tone, pov, region, words)
                QUERY = f"You are article generator Whole Article should be in {language} language strictly. Generate an article on {topic} in the point of view of {pov} which I provide you. Whole Article should be  of approximately {words} words with voice of tone as {tone} and article should be from the perspective of a person from {region} . Format should be in strictly HTML format. Only provide the content of the body tag of html output and give headings in h4 tag only. Strictly keep Headings(numbered as 1,2,3).Dont stop in middle at least complete the contents in a heading and then stop "
                message_content = [
                    {
                        "type": "text",
                        "text": QUERY
                    }
                ]
                message = HumanMessage(content=message_content)
                try:
                    async for chunk in llm.astream([message]):
                        stream_chunk = chunk.content
                        stream_chunk = stream_chunk.replace("*", "").replace("<body>", "").replace("</body>", "").replace("```", "").replace("html", "").replace("\n", "")
                        result += stream_chunk
                        await self.send(text_data=json.dumps({"data": result, "signal": 1}))
                except:
                    pass
            # save record
            if "record_id" not in payload:
                get_article_record = await database_sync_to_async(ArticleModel.objects.create)(
                    user_id=USER_ID,
                    topic=topic,
                    language=language,
                    region=region,
                    pov=pov,
                    words=words,
                    tone=tone,
                    result=result,
                    file_name=payload.get("file_name")
                )
            elif "record_id" in payload:
                get_article_record.result = result
                await database_sync_to_async(get_article_record.save)()

                # get_article_record.save()
            await self.send(text_data=json.dumps({"data": "", "signal": 0 ,"record_id": get_article_record.id,}))
        except Exception as err:
            print(err, '-------errr---------')
            await self.send(text_data=json.dumps({
                        "text": json.dumps({"data": str(err), "signal": 0, "message": "Something went wrong", "status": 400})
                    }))
            await self.close()

    async def disconnect(self, code):
        return await super().disconnect(code)


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