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
            if "record_id" not in payload:
                topic = payload.get("topic")
                page = payload.get("page")
                tone = payload.get("tone")
                reference = payload.get("reference")
            elif "record_id" in payload:
                record = await database_sync_to_async(CategoryModel.objects.get)(id=payload["record_id"])
                topic = record.topic
            # QUERY = f"You are a topics list generator. Generate research topics list based on {topic} strictly in HTML format. Only provide the content of the body tag of html output and give headings in h4 tag only and dont break li tag sentences in middle. Output should contain topics headings(strictly numbered like 1,2,3,.....) and slide headings(strictly numbered like i, ii, iii , ......)."
            QUERY =  f"""
                        "You are a topics list generator. Generate research topics list based on {topic} strictly in HTML format."
                        Additionally, Strictly Ensure the response is formatted as the following structure sample. Don't use extra html tags which are not present in sample structure:
                        "
                            <ol style="list-style-type: decimal; margin-left: 20px;">
                                <li>Vegetable Production and Supply Chains
                                    <ul style="list-style-type: lower-roman; margin-left: 20px;">
                                        <li>Largescale vegetable production clusters</li>
                                        <li>FarmerProducer Organization and startup involvement in vegetable supply chains</li>
                                    </ul></li>
                                <li>Digital Infrastructure for Agriculture
                                    <ul style="list-style-type: lower-roman; margin-left: 20px;">
                                        <li>Implementation of Digital Public Infrastructure (DPI) in agriculture</li>
                                        <li>Digital crop surveys and farmer and land registries</li>
                                    </ul></li>
                                <li>Employment and Skilling
                                    <ul style="list-style-type: lower-roman; margin-left: 20px;">
                                        <li>Employment Linked Incentive schemes for firsttime employees, manufacturing sector job creation, and employer support</li>
                                        <li>Women's workforce participation and skilling programs</li>
                                    </ul></li>
                            </ol>    
                        "
                    """
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
                    stream_chunk = stream_chunk.replace("*", "").replace("html", "").replace("\n", "")
                    result += stream_chunk
                    await self.send(text_data=json.dumps({"data": result, "signal": 1}))
            except:
                pass
            if "record_id" not in payload:
                save_to_db = await database_sync_to_async(CategoryModel.objects.create)(
                    user_id=USER_ID,
                    topic=topic,
                    page=page,
                    tone=tone,
                    reference=reference,
                    category=4,
                    result=result,
                    file_name=payload.get("file_name")
                )
                record_id = save_to_db.id
            else:
                record_id = payload["record_id"]    
            print(result, '--------')    
            await self.send(text_data=json.dumps({"data": "", "signal": 0, "record_id": record_id, "message": "Research topics generated successfully."}))
        except Exception as err:
            print(err, '-------errr---------')
            await self.send(text_data=json.dumps({"data": str(err), "signal": 0, "message": "Something went wrong", "status": 400}))
            await self.close()

    async def disconnect(self, code):
        return await super().disconnect(code)
