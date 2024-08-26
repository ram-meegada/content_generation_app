import json
from unittest import result
from langchain_google_genai import ChatGoogleGenerativeAI
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async            
from whizzo_app.models.categoryModel import CategoryModel
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from bs4 import BeautifulSoup
from langchain_core.messages import HumanMessage

class DetailedResearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        return await super().connect()

    async def receive(self, text_data=None, bytes_data=None):
        payload = json.loads(text_data)
        record_id = payload["record_id"]
        result = ""
        access_token = AccessToken(payload["token"])
        token_payload = access_token.payload
        user_id = token_payload.get('user_id')
        USER_ID = user_id
        try:
            PAGE_REFERENCES = {1: (600, 1200), 2: (
            1800, 3000), 3: (4200, 7200), 4: (9000, 15000)}
            get_research_record = await database_sync_to_async(CategoryModel.objects.get)(id=record_id)
            try:
                api_type = 1
                min_pages = PAGE_REFERENCES[get_research_record.page][0]
                max_pages = PAGE_REFERENCES[get_research_record.page][1]
                tone = get_research_record.tone
                reference = get_research_record.reference
                reduce_citations = get_research_record.reduced_citations
            except KeyError:
                api_type = 2
                # image_links = get_research_record.research_file_links
                # descriptoin = get_research_record.description
                reduce_citations = get_research_record.reduced_citations
            except Exception as err:
                await self.send(text_data=json.dumps({"data": str(err), "signal": 0, "message": "Something went wrong", "status": 400}))
                await self.close()
            llm = ChatGoogleGenerativeAI(model="gemini-pro")
            html_text = payload.get("html_text")
            # extract text from html
            print("1111111")
            if html_text:
                soup = BeautifulSoup(html_text, "html.parser")
                all_topics = []
                for ele in soup.find_all(["h4", "li"]):
                    print("33333333")
                    all_topics.append(ele.get_text())
                    print("44444444")
                    get_research_record.all_topics = all_topics
                    print("555555555")
                    await database_sync_to_async(get_research_record.save)()
                    print("22222222222")
            else:
                all_topics = get_research_record.all_topics
            ####
            if api_type == 1:
                QUERY = f"You are research generator. Generate some theory on the topics which I provide you strictly in HTML format. Only provide the content of the body tag of html output and give headings in h4 tag only and dont break li tag sentences in middle. Whole research should be of approximately {min_pages} to {max_pages} words with voice of tone as {tone} and take reference from {reference} with reduce citations as {reduce_citations}. Format should be descriptive. Keep the same name as topic heading which I provide you and also in same order of topics. Strictly keep Heading(numbered as 1,2,3) and side headings(numbered as i, ii, iii)."
            elif api_type == 2:
                QUERY = f"You are research generator. Generate some theory on the topics which I provide you strictly in HTML format. Only provide the content of the body tag of html output and give headings in h4 tag only and dont break li tag sentences in middle. Whole research should be of approximately 400 to 800 words along with reduce citations as {reduce_citations}. Format should be descriptive. Keep the same name as topic heading which I provide you in list and also in same order of topics. Strictly keep Headings (strictly numbered as 1,2,3) and side headings(strictly numbered as i, ii, iii)."
            message_content = [
                {
                    "type": "text",
                    "text": QUERY
                }
            ]
            for top in all_topics:
                message_content.append({
                    "type": "text",
                    "text": top
                })
            message = HumanMessage(content=message_content)
            try:
                async for chunk in llm.astream([message]):
                    stream_chunk = chunk.content
                    stream_chunk = stream_chunk.replace("*", "").replace("<body>", "").replace("</body>", "")
                    result += stream_chunk
                    await self.send(text_data=json.dumps({"data": result, "signal": 1}))
            except:
                pass
            await self.send(text_data=json.dumps({"data": "", "message": "Detailed research generated successfully", "status": 200}))
        except Exception as err:
            print(err, '-------errr---------')
            await self.send(text_data=json.dumps({"data": str(err), "signal": 0, "message": "Something went wrong", "status": 400}))
            await self.close()

    async def disconnect(self, code):
        return await super().disconnect(code)
