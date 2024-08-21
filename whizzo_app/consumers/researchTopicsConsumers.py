import json
from langchain_google_genai import ChatGoogleGenerativeAI
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async            
from whizzo_app.models.categoryModel import CategoryModel
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from langchain_core.messages import HumanMessage

class ResearchTopicsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        return await super().connect()

    async def receive(self, text_data=None, bytes_data=None):
        payload = json.loads(text_data)
        result = ""
        access_token = AccessToken(payload["token"])
        token_payload = access_token.payload
        user_id = token_payload.get('user_id')
        USER_ID = user_id
        try:
            topic = payload.get("topic")
            page = payload.get("page")
            tone = payload.get("tone")
            reference = payload.get("reference")
            QUERY = f"You are a topics list generator. Generate research topics list based on {topic} strictly in HTML format. Only provide the content of the body tag of html output and give headings in h4 tag only and dont break li tag sentences in middle. Output should contain topics headings(strictly numbered like 1,2,3,.....) and slide headings(strictly numbered like i, ii, iii , ......)."
            llm = ChatGoogleGenerativeAI(model="gemini-pro")
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
                    stream_chunk = stream_chunk.replace("*", "").replace("<body>", "").replace("</body>", "")
                    result += stream_chunk
                    await self.send(text_data=json.dumps({"data": result, "signal": 1}))
            except:
                pass
            save_to_db = await database_sync_to_async(CategoryModel.objects.create)(
                user_id=USER_ID,
                topic=topic,
                page=page,
                tone=tone,
                reference=reference,
                category=4,
                result=result
            )
            await self.send(text_data=json.dumps({"data": "", "signal": 0, "record_id": save_to_db.id, "message": "Research topics generated successfully."}))
        except Exception as err:
            print(err, '-------errr---------')
            await self.send(text_data=json.dumps({"data": str(err), "signal": 0, "message": "Something went wrong", "status": 400}))
            await self.close()

    async def disconnect(self, code):
        return await super().disconnect(code)
