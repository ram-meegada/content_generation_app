from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from langchain_google_genai import ChatGoogleGenerativeAI
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from langchain_core.messages import HumanMessage
from whizzo_project import settings
import base64
import textwrap
from whizzo_app.models.assignmentModel import AssignmentModel
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from io import BytesIO
from PyPDF2 import PdfReader
from whizzo_app.utils.saveImage import save_image
import string
from whizzo_app.utils.Modules.assignmentSolutionsModule import assigment_chatGPT_pdf_processing, assignment_extract_text, chatGPT_image_processing,\
assignment_extract_text
from whizzo_app.utils.Modules.fileSummaryModule import image_processing_assignment_solution
import ast
from channels.db import SyncToAsync
import asyncio
import random

class AssignmentSolutionsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # self.send({
        #     'type': 'websocket.accept'
        # })

    async def receive(self, text_data=None, bytes_data=None):
        try:
            payload = json.loads(text_data)
            access_token = AccessToken(payload["token"])
            token_payload = access_token.payload
            user_id = token_payload.get('user_id')
            USER_ID = user_id
            google_api_key = settings.GOOGLE_API_KEY
            llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
            final_response = ""
            if "record_id" not in payload and "change_language" not in payload:
                if isinstance(payload.get("language"), str):
                    input_language = payload.get("language", "english")
                elif isinstance(payload.get("language"), dict):
                    input_language = payload["language"]["language"]
                raw_binary_data = payload["binary_data"]
                try:
                    binary_data = base64.b64decode(payload["binary_data"])
                except:
                    pass    
            elif "record_id" in payload:
                record = await database_sync_to_async(AssignmentModel.objects.get)(id=payload["record_id"])
                input_language = record.language
                try:
                    raw_binary_data = record.binary_data
                    payload["binary_data"] = raw_binary_data
                    print(payload["binary_data"],"--------------------------")
                except:
                    pass    
            if not payload.get("change_language"):
                # api_type = int(payload["type"])

                if isinstance(raw_binary_data, str):
                    binary_data = base64.b64decode(raw_binary_data)
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
                    print(len(pdf_text), '-----len------')        
                    temp = {1: (2000, 3), 2: (2000, 5), 3: (4000, 7), 4: (12000, 9)}
                    start, ending = 0, 0
                    
                    while start < len(pdf_text):
                        end = start+temp[ending+1][0]
                        if end > len(pdf_text)-1:
                            input_text = pdf_text[start:]
                        else: 
                            input_text = pdf_text[start: end]    
                        start += temp[ending+1][0]
                        if ending >= 3:
                            ending = 3
                        else:    
                            ending += 1
                        result = await self.assigment_chatGPT_pdf_processing(input_text, input_language)
                        print(result, '-----result------')
                        result_send = result["html_content"] 
                        # print(result_send, '-----result------')
                        final_response += result_send.replace("*", "").replace("<body>", "").replace("</body>", "").replace("html","").replace("`","")
                        # print(final_response, '----fianl esfsd-----')
                        await self.send(text_data=json.dumps({"data": final_response, "signal": 1}))
                        await asyncio.sleep(1)
                        # final_response += result["html_content"] + "<br />"

                        # if result:
                        #     if result.get("questions"):
                        #         final_response += result["questions"]
                        #     elif not result.get("questions") and isinstance(result, dict):
                        #         final_response.append(result)
                        # try:
                        #     for j, i in enumerate(final_response):
                        #         i["question_no"] = j + 1
                        #         if not i.get("options"):
                        #             i["question_type"] = 1
                        #         elif i["options"]:
                        #             i["question_type"] = 2
                        # except:
                        # with open()
                        #     pass

                        # self.send({
                        #     "type": "websocket.send",
                        #     "text": json.dumps(final_response)
                        # })
                elif isinstance(raw_binary_data, list):
                    final_response = ""
                    for bin_data in payload["binary_data"]:
                        binary_data = base64.b64decode(bin_data)
                        file_content = ContentFile(binary_data)
                        uploaded_file = InMemoryUploadedFile(
                            file_content,
                            None,
                            "image.jpeg",
                            'image/jpeg',
                            len(binary_data),
                            None
                        )
                        query = f"""
                                "You are a teacher. Generate questions and answers based on the data I provide to you .Format should be proper pretty HTML format and if there are multiple answers give it in list "
                                Additionally, ensure the response is formatted as the following structure sample:
                                {{"html_content":
                                        <body>
                                            <p><strong>Question 1:</strong> What is the origin of cricket?</p>
                                            <p><strong>Answer 1:</strong> Cricket originated in England during the 16th century. It evolved from a game played by children in the countryside and became a popular sport by the 18th century. The first international match was played in 1844 between the United States and Canada.</p>
                                            .......
                                            <p><strong>Question n:</strong> who is kane williamson in cricket?</p>
                                            <p><strong>Answer n:</strong> Cricket originated in England during the 16th century. It evolved from a game played by children in the countryside and became a popular sport by the 18th century. The first international match was played in 1844 between the United States and Canada.</p>
                                        <body />    
                                }}
                            """
                        # query = "You are a teacher. Generate questions and answers based on the image I provide to you. Format should be proper Python Javascript object notation list of dictionaries where every dictionary contains keys as 'question_no', 'question', 'correct_answer' and 'options'(if available)."
                        img = save_image(uploaded_file)

                        # result = await self.image_processing_assignment_solution(img[0], messages)
                        result = await self.chatGPT_image_processing(img[0], query)
                        final_response += result["html_content"]
                        final_response = final_response.replace("\n", '')
                        print(final_response, '-----result------')
                        # temp = format_final_response(result)
                        await self.send(text_data=json.dumps({"data": final_response, "signal": 1}))
                        await asyncio.sleep(1)
                        # self.send({
                        #     "type": "websocket.send",
                        #     "text": json.dumps(temp)
                        # })
                if "record_id" not in payload:
                    saved_data = await database_sync_to_async(AssignmentModel.objects.create)(
                        user_id=USER_ID,
                        result=final_response,
                        binary_data=payload["binary_data"],
                        language=payload.get("language", "english"),
                        file_name=payload.get("file_name"),
                    )
                    record_id = saved_data.id
                else:
                    record_id = payload["record_id"]
                await self.send(text_data=json.dumps({"data": "", "signal": 0, "record_id": record_id, }))
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
                    abc = (input_text[:200]).strip().replace("\n","")
                    input_language = check_the_input_language_for_change_language(abc)    
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
                            print(result,"----------result--------------")
                            await self.send(text_data=json.dumps({"data": result, "signal": 1}))
                    except:
                        pass
                await self.send(text_data=json.dumps({"data": None, "signal": 0, "message": "Translation done"}))

            # self.send({
            #             "type": "websocket.send",
            #             "text": json.dumps({"data": "", "signal": 0})
            #         })
        except Exception as error:
            print(error, '---error--error----error-----')

            await self.send(text_data=json.dumps({"data": "", "signal": 400, "message": "Something went wrong", "status": 400}))
            # self.send({
            #             "type": "websocket.send",
            #             "text": json.dumps({"data": "", "signal": 0, "message": "Something went wrong", "status": 400})
            #         })
            await self.send(text_data=json.dumps({"data": "", "signal": 0}))
            # self.send({
            #     "type": "websocket.close"
            #     })        
    async def disconnect(self, code):
        return await super().disconnect(code)
    
    async def assigment_chatGPT_pdf_processing(self, text_data, language):
        from decouple import config
        import openai
        openai.api_key = config("OPENAI_KEY")
        API_KEY = config("OPENAI_KEY")

        # query = f"""
        #     "You are a teacher. Generate questions and answers based on the data I provide to you and make sure to give output in {language} language only. Format should be proper Python Javascript object notation list of dictionaries where every dictionary contains keys as 'question_no', 'question', 'correct_answer' and 'options'(if available)."
        #     Additionally, ensure the response is formatted as a JSON object with the following structure:
        #     {{
        #         "question_no": "number",
        #         "question": "string",
        #         "question_type": "integer 1 for subjective type question and 2 for MCQ type question."
        #         "options": "list of options. if no options then empty list []",
        #         "correct_answer": "string",
        #     }}
        #     """
        query = f"""
                "You are a teacher. Generate questions and answers based on the data I provide to you and make sure to give output in {language} language only. Format should be proper pretty HTML format. and if there are multiple answers give it in list"
                Additionally, ensure the response is formatted as the following structure sample. html_content should be in string only not in any other format:
                {{"html_content": "
                            <p><strong>Question 1:</strong> What is the origin of cricket?</p>
                            <p><strong>Answer 1:</strong> Cricket originated in England during the 16th century. It evolved from a game played by children in the countryside and became a popular sport by the 18th century. The first international match was played in 1844 between the United States and Canada.</p>
                            .......
                            <p><strong>Question n:</strong> who is kane williamson in cricket?</p>
                            <p><strong>Answer n:</strong> Cricket originated in England during the 16th century. It evolved from a game played by children in the countryside and became a popular sport by the 18th century. The first international match was played in 1844 between the United States and Canada.</p>" 
                }}
            """
        try:
            messages=[
                            {"role": "system", "content": "You are a helpful assistant designed to provide HTML content in JSON"},
                            {"role": "user", "content": [
                                    {"type": "text", "text": query},
                                    {"type": "text", "text": f"Input data: {text_data}"}
                                ]}
                        ]
            chatbot = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages,response_format={ "type": "json_object" },temperature = 0.0,
            )
            reply = chatbot.choices[0].message.content
            final_data = json.loads(reply)
            return final_data
        except:
            return []  
        
    async def image_processing_assignment_solution(self, image_link, query):
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        # example
        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": query,
                },
                {"type": "image_url", "image_url": str(image_link)},
            ]
        )
        response = llm.invoke([message])
        result_qu = self.to_markdown(response.content)
        return result_qu    
    
    async def chatGPT_image_processing(self, img_file, query):
        import openai
        try:
            messages=[
                            {"role": "system", "content":"You are a helpful assistant designed to provide HTML content in JSON"},
                            {"role": "user", "content":[
                                {"type": "text","text": query},
                                {"type": "image_url", "image_url": {
                                    "url":str(img_file)}
                                }
                            ]}
                        ]
            chatbot = openai.ChatCompletion.create(
                model="gpt-4o", messages=messages,response_format={ "type": "json_object" },temperature = 0.0,
            )
            reply = chatbot.choices[0].message.content
            final_data = json.loads(reply)
            return final_data
        except:
            return []


    async def to_markdown(self, text):
        text = text.replace('*', '').replace('#', '').replace("-", "")
        intent_text = (textwrap.indent(text, '', predicate=lambda _: True))
        return intent_text



    # def websocket_disconnect(self, event):
    #     print('websocket disconnected.....', event)
    #     raise StopConsumer()

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

def format_final_response(result):
    final_response = ""
    try:
        for i in range(len(result)-1, -1, -1):
            if result[i] == "}":
                break
        final_response = result[result.index("["): i+1] + "]"
        final_response = json.loads(final_response)
    except:
        pass
    try:
        for i in final_response:
            if not i.get("options"):
                i["question_type"] = 1
            elif not i["options"]:
                i["question_type"] = 1
            elif i["options"]:
                i["question_type"] = 2
    except:
        pass
    return final_response        

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