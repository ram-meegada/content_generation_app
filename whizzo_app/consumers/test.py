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
from time import sleep
from whizzo_app.models.fileSumarizationModel import FileSumarizationModel
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
    

class FileSummarizationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        return await super().connect()

    async def receive(self, text_data=None, bytes_data=None):
        payload = json.loads(text_data)
        try:
            access_token = AccessToken(payload["token"])
            token_payload = access_token.payload
            user_id = token_payload.get('user_id')
            USER_ID = user_id
            google_api_key = settings.GOOGLE_API_KEY
            llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
            result = ""
            if not payload.get("change_language"):
                if payload["type"] == 1:
                    binary_data = base64.b64decode(payload["binary_data"])
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
                        input_language = check_the_input_language((input_text[:200]).strip())    
                        message = HumanMessage(
                            content=[
                                {"type": "text",
                                    # "text": f"Generate a summary of the input I provide you in arabic language only. And continue with previous response.(if previous response present)"},
                                    "text": f"Generate a summary of the input I provide you in strictly HTML format in {input_language} language. Only provide the content of the body tag of html output and give headings in h4 tag only and sub heaings un h3 tag only. Strictly dont give any symbols, unwanted text or characters not belongs to {input_language} language. Maintain pure language. And continue with previous response.(if previous response present)And please return output in a good structured format like (<ol> <li> <ul> <li> </li> </ul> </li> </ol>). Also if there are list in any paragraph ,convert those list also in <ul> or <ol> or <li>"},
                                {"type": "text", "text": input_text}
                            ]
                        )
                        try:
                            async for chunk in llm.astream([message]):
                                stream_chunk = chunk.content
                                stream_chunk = stream_chunk.replace("*", "").replace("<body>", "").replace("</body>", "").replace("html", "")
                                result += stream_chunk
                                await self.send(text_data=json.dumps({"data": result, "signal": 1}))
                        except:
                            pass
                elif payload["type"] == 2:
                    for bin_data in payload["binary_data"]:
                        binary_data = base64.b64decode(bin_data)
                        file_content = ContentFile(binary_data)
                        uploaded_file = InMemoryUploadedFile(
                            file_content,
                            None,
                            "image.jpg",
                            'image/jpg',
                            len(binary_data),
                            None
                        )
                        query = f"Generate a summary of the input I provide you in strictly HTML format in atleast five hundred words. Only provide the content of the body tag of html output and give headings in h4 tag only. And continue with previous response.(if previous response present)"
                        img = save_image(uploaded_file)
                        # print(img, '----img------')
                        result = image_processing_assignment_solution(
                                img[0], query)
                        await self.send(text_data=json.dumps({"data": result, "signal": 1}))  
                save_file_summary_record = await database_sync_to_async(FileSumarizationModel.objects.create)(
                        user_id=USER_ID,
                        sub_category=5,
                        result=result,
                        file_name=payload.get("file_name")
                    )          
                await self.send(text_data=json.dumps({"data": "", "signal": 0, "record_id": save_file_summary_record.id, "message": "Summary generated successfully."}))
            elif payload.get("change_language"):
                text = payload.get("text")
                format_text = text.replace("\n", " ")
                temp = {1: 2000, 2: 4000, 3: 8000, 4: 12000}
                i, j = 0, 0
                result = ""
                while i < len(format_text):
                    end = i+temp[j+1]
                    if end > len(format_text)-1:
                        input_text = format_text[i:]
                    else: 
                        input_text = format_text[i: end]    
                    i += temp[j+1]
                    if j >= 3:
                        j = 3
                    else:    
                        j += 1
                    input_language = check_the_input_language_for_change_language((input_text[:200]).strip())    
                    query = f"""Translate the given input to {input_language} language. Translate proper nouns also. 
                            Output format should be proper HTML"""
                    message = HumanMessage(
                        content=[
                            {"type": "text",
                                # "text": f"Generate a summary of the input I provide you in arabic language only. And continue with previous response.(if previous response present)"},
                                "text": query},
                            {"type": "text", "text": input_text}
                        ]
                    )
                    try:
                        async for chunk in llm.astream([message]):
                            stream_chunk = chunk.content
                            stream_chunk = stream_chunk.replace("*", "").replace("<body>", "").replace("</body>", "").replace("html","").replace("`","")
                            result += stream_chunk
                            await self.send(text_data=json.dumps({"data": result, "signal": 1}))
                    except:
                        pass
                await self.send(text_data=json.dumps({"data": None, "signal": 0, "message": "Translation done"}))

        except TokenError or InvalidToken:
            await self.send(text_data=json.dumps({"data": "", "message": "Invalid token", "signal": 401}))
            await self.close()
        except Exception as err:
            print(err, '-------errr---------')
            await self.send(text_data=json.dumps({"data": str(err), "signal": -1, "message": "Something went wrong", "status": 400}))
            await self.close()

    async def disconnect(self, code):
        return await super().disconnect(code)

def check_the_input_language(text_data):
    import string
    LENGTH = len(text_data)
    non_english_chars = 0
    text_data = text_data.replace(" ", "")
    for i in text_data:
        if i not in string.ascii_letters+string.digits+string.punctuation:
            non_english_chars += 1
    if non_english_chars > LENGTH//2:
        return "arabic"
    else:
        return "english" 

def check_the_input_language_for_change_language(text_data):
    import string
    LENGTH = len(text_data)
    non_english_chars = 0
    text_data = text_data.replace(" ", "")
    for i in text_data:
        if i not in string.ascii_letters+string.digits+string.punctuation:
            non_english_chars += 1
    if non_english_chars > LENGTH//2:
        return "english"
    else:
        return "arabic" 