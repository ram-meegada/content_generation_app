import json
from langchain_google_genai import ChatGoogleGenerativeAI
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async            
from whizzo_app.models.categoryModel import CategoryModel
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from langchain_core.messages import HumanMessage
from whizzo_app.utils.saveImage import save_image
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from io import BytesIO
from whizzo_project import settings
from PyPDF2 import PdfReader

class ResearchTopicsByReferenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        return await super().connect()

    async def receive(self, text_data=None, bytes_data=None):
        payload = json.loads(text_data)
        # result = ""
        # access_token = AccessToken(payload["token"])
        # token_payload = access_token.payload
        # user_id = token_payload.get('user_id')
        # USER_ID = user_id
        try:
            result = ""
            access_token = AccessToken(payload["token"])
            token_payload = access_token.payload
            user_id = token_payload.get('user_id')
            USER_ID = user_id
            if not payload.get("change_language"):
                if "record_id" not in payload:
                    description = payload.get("description", "")
                    reduce_citation = True if payload.get(
                        "reduce_citation") == "true" else False
                    binary_data = base64.b64decode(payload["binary_data"])
                elif "record_id" in payload:
                    record = await database_sync_to_async(CategoryModel.objects.get)(id=payload["record_id"])
                    description = record.description
                    reduce_citation = record.reduced_citations
                    binary_data = base64.b64decode(record.binary_data)
                # image_links = []
                # for img in dict(payload)["files"]:
                #     get_link = save_image(img)
                #     image_links.append(get_link[0])
                google_api_key = settings.GOOGLE_API_KEY
                llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
                file_content = ContentFile(binary_data)
                uploaded_file = InMemoryUploadedFile(
                    file_content,
                    None,
                    "file.pdf",
                    'application/octet-stream',
                    len(binary_data),
                    None
                )
                pdf_text = ""

                with uploaded_file.open() as f:
                    pdf_stream = BytesIO(f.read())
                    pdf_reader = PdfReader(pdf_stream)
                    for page in pdf_reader.pages:
                        pdf_text += page.extract_text()
                if not pdf_text.strip():
                    await self.send(text_data=json.dumps({"data": None, "signal": 400, "message": "No extractable text"}))
                    await self.close()
                temp = {1: 2000, 2: 4000, 3: 8000, 4: 12000}
                i, j = 0, 0
                result = ""
                while i < len(pdf_text):
                    end = i+temp[j+1]
                    if end > len(pdf_text)-1:
                        input_text = pdf_text[i:]
                    else: 
                        input_text = pdf_text[i: end]    
                    i += temp[j+1]
                    if j >= 3:
                        j = 3
                    else:    
                        j += 1
                    inp_lan = (input_text[:200]).strip()
                    inp_lan_rep = inp_lan.replace("\n", "")    
                    print(inp_lan_rep, '------input_text[:200]----')    
                    input_language = check_the_input_language(inp_lan_rep)    
                    print(input_language,"-------------------------language-------------------------")
                    # query = f"You are topics list generator. Generate research topics list based on topic I provide to you in {input_language} language only strictly in HTML format. Only provide the content of the body tag of html output and give headings in h4 tag only and dont break li tag sentences in middle. Reduce citations as {reduce_citation} and add some description of {description}. Output should contain only three topics headings(numbered like 1,2,3) and strictly two side headings(numbered like i, ii, iii)."
                    
                    query = f"""
                        "You are a topics list generator.Generate research topics list based on topic I provide to you in {input_language}  Reduce citations as {reduce_citation} and add some description of {description}.Generate research topics list based on input provided strictly in HTML format."
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


                    message = HumanMessage(
                        content=[
                            {"type": "text",
                                "text": query},
                            {"type": "text", "text": input_text}
                        ]
                    )
                    try:
                        async for chunk in llm.astream([message]):
                            stream_chunk = chunk.content
                            stream_chunk = stream_chunk.replace("*", "").replace("<body>", "").replace("</body>", "")
                            result += stream_chunk
                            await self.send(text_data=json.dumps({"data": result, "signal": 1}))
                    except:
                        pass
            if "record_id" not in payload:
                save_to_db = await database_sync_to_async(CategoryModel.objects.create)(
                    user_id=USER_ID,
                    description=description,
                    category=4,
                    research_type=2,
                    reduced_citations=reduce_citation,
                    result=result,
                    binary_data=payload["binary_data"]
                )
                record_id = save_to_db.id
            else:
                record_id = payload["record_id"]
            await self.send(text_data=json.dumps({"data": "", "signal": 0, "record_id": record_id, "message": "Research topics generated successfully."}))
        except Exception as err:
            print(err, '-------errr---------')
            await self.send(text_data=json.dumps({"data": str(err), "signal": 0, "message": "Something went wrong", "status": 400}))
            await self.close()

    async def disconnect(self, code):
        return await super().disconnect(code)


def check_the_input_language(text_data):
    import string
    LENGTH = len(text_data)
    non_english_chars = 0
    text_data = text_data.replace(" ", "").replace("/n","")
    for i in text_data:
        if i not in string.ascii_letters+string.digits+string.punctuation:
            non_english_chars += 1
    if non_english_chars > LENGTH//10:
        return "arabic"
    else:
        return "english"