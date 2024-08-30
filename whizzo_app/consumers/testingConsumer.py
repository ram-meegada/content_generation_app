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
import string
from whizzo_app.utils.Modules.testingModule import chatGPT_pdf_processing, chatGPT_image_processing
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
import asyncio

class TestingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):

    # def websocket_receive(self, event):
        try:
            payload = json.loads(text_data)
            raw_pay = {**payload}
            raw_pay.pop("binary_data")
            print(raw_pay, "-------------testing----------------")
            access_token = AccessToken(payload["token"])
            token_payload = access_token.payload
            user_id = token_payload.get('user_id')
            USER_ID = user_id
            # payload = json.loads(event["text"])
            file_links = []
            api_type = int(payload["type"])
            # files = dict(request.data)["file"]
            # if api_type == 1:
            #     for i in files:
            #         file_links.append(save_image(i)[0])
            sub_category = int(payload["sub_category"])
            final_response = []
            if sub_category == 1:
                if api_type == 1:
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
                        img = save_image(uploaded_file)
                        query = f"Generate some mcqs with options and answers for this image and make in python json list format. Keys should be 'question_no', 'question', 'answer_option', 'correct_answer'.)"
                        result = chatGPT_image_processing(img[0], query)
                        await self.send(text_data=json.dumps({"data": result, "signal": 1}))
                        await asyncio.sleep(1)

                        # self.send({
                        #     "type": "websocket.send",
                        #     "text": json.dumps(result)
                        # })
                elif api_type == 2:
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
                    temp = {1: (2000, 3), 2: (4000, 5), 3: (8000, 7), 4: (12000, 9)}
                    start, ending = 0, 0
                    input_language = check_the_input_language(pdf_text[0].strip())
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
                        query = f"Generate {temp[ending+1][1]} mcqs with options and answers for the input in {input_language} language. Format should be in python json list of objects(key-value pair). Key names of objects should be strictly 'question_no', 'question', 'answer_option' and 'correct_answer'."
                        query1 = f"""Generate {temp[ending+1][1]} mcqs with options and answers for the input in {input_language} language. Format should be in python json list of objects(key-value pair). 
                                    Key names of objects should be strictly 'question_no', 'question', 'answer_option' and 'correct_answer'.
                                    Additionally, ensure the response is formatted as the following structure sample:
                                    {{"questions": [{{
                                        "question_no": "number",
                                        "question": "string",
                                        "answer_option": "list",
                                        "correct_answer": "string"
                                    }}, ....
                                    ]}}
                                """
                        result = await self.chatGPT_pdf_processing(input_text, query1)
                        # for index, body in enumerate(final_response):
                        #     if "answer_options" in body:
                        #         body["answer_option"] = body.pop("answer_options")
                        #     if isinstance(body["answer_option"], dict):
                        #         if "correct_answer" not in body and "correct_answer" in body["answer_option"]:
                        #             correct_answer = body["answer_option"].pop(
                        #                 "correct_answer")
                        #             body["correct_answer"] = correct_answer
                        #         if "correct_answer" in body:
                        #             for key, val in body["answer_option"].items():
                        #                 if key == body["correct_answer"]:
                        #                     body["correct_answer"] = val
                        #         body["answer_option"] = list(
                        #             body["answer_option"].values())
                        #     body["question_no"] = index + 1
                        print(result, "---------------------berwjfchsih------")
                        try:
                            final_response = result["questions"]
                            await self.send(text_data=json.dumps({"data": final_response, "signal": 1 }))
                        except:
                            pass    
                        await asyncio.sleep(1)

            elif sub_category == 2:
                if api_type == 1:
                    # number_of_questions = int(
                    #     settings.NUMBER_OF_QUESTIONS)//len(file_links)
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
                        img = save_image(uploaded_file)
                        query = f"Generate some flashcards for this image. Format should be in python json list. Keys should be 'question', 'answer'. 'question' and 'answer' should be different. if the question has multiple answers give them in list."
                        result = chatGPT_image_processing(img[0], query)
                        await self.send(text_data=json.dumps({"data": result, "signal": 1 }))
                        await asyncio.sleep(1)
                        # self.send({
                        #     "type": "websocket.send",
                        #     "text": json.dumps(result)
                        # })
                elif api_type == 2:
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
                    temp = {1: (2000, 3), 2: (4000, 5), 3: (8000, 7), 4: (12000, 9)}
                    start, ending = 0, 0

                    input_language = check_the_input_language(pdf_text[0].strip())
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
                        query = f"Generate {temp[ending+1][1]} flashcards for this input in {input_language} language. Format should be in list. Keys should be 'question', 'answer'. if the question has multiple answers give them in list. Make sure to generate every question and every answer in {input_language} language only. Proper names should also be in {input_language} language"
                        result = chatGPT_pdf_processing(input_text, query)

                        await self.send(text_data=json.dumps({"data": result, "signal": 1 }))
                        await asyncio.sleep(1)
                        # self.send({
                        #     "type": "websocket.send",
                        #     "text": json.dumps(result)
                        # })
            await self.send(text_data=json.dumps({"data": "", "signal": 0}))
            await self.close()
            # self.send({
            #             "type": "websocket.send",
            #             "text": json.dumps({"data": "", "signal": 0})
            #         })
        except Exception as error:
            print(error, '---error--error----error-----')
            await self.send(text_data=json.dumps({"data": "", "signal": 0, "message": "Something went wrong", "status": 400 }))
            # self.send({
            #             "type": "websocket.send",
            #             "text": json.dumps({"data": "", "signal": 0, "message": "Something went wrong", "status": 400})
            #         })
            await self.close()
            # self.send({
            #     "type": "websocket.close"
            #     })        

    # def websocket_disconnect(self, event):
    #     print('websocket disconnected.....', event)
    #     raise StopConsumer()
    async def disconnect(self, code):
        return await super().disconnect(code)
    
    async def chatGPT_pdf_processing(self, text_data, query):
        import openai
        try:
            messages=[
                            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
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
        except Exception as err:
            print(err, '--------chatgpt error--------')
            return []

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