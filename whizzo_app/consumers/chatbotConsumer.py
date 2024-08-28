from channels.generic.websocket import AsyncWebsocketConsumer
import json
import openai
from decouple import config

openai.api_key = config("OPENAI_KEY")
API_KEY = config("OPENAI_KEY")


class ChatBotConsumer(AsyncWebsocketConsumer):

    async def connect(self):
       await  self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        payload = json.loads(text_data)
        context ="""You are a helpful assistant Please provide the answer in JSON format with fields "question", "answer", like this: {"question": "What is the capital of France?", "answer": "Paris"."""
        messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content":[
                        {"type": "text", "text": payload["query"]}
                    ]}
                ]
        chatbot = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages, response_format={ "type": "json_object" }, temperature = 0.0,
        )
        reply = chatbot.choices[0].message.content
        await self.send(reply)


    async def disconnect(self, code):
         await self.close()