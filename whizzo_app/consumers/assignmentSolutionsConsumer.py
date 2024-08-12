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
from whizzo_app.utils.Modules.assignmentSolutionsModule import assigment_chatGPT_pdf_processing, assignment_extract_text, chatGPT_image_processing,\
assignment_extract_text
from whizzo_app.utils.Modules.fileSummaryModule import image_processing_assignment_solution


class AssignmentSolutionsConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        try:
            payload = json.loads(event["text"])
            api_type = int(payload["type"])
            final_response = []
            if api_type == 1:
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
                    result = assigment_chatGPT_pdf_processing(input_text, input_language)
                    if result:
                        if result.get("questions"):
                            final_response += result["questions"]
                        elif not result.get("questions") and isinstance(result, dict):
                            final_response.append(result)
                    try:
                        for j, i in enumerate(final_response):
                            i["question_no"] = j + 1
                            if not i.get("options"):
                                i["question_type"] = 1
                            elif i["options"]:
                                i["question_type"] = 2
                    except:
                        pass
                    self.send({
                        "type": "websocket.send",
                        "text": json.dumps(final_response)
                    })
            elif api_type == 2:
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
                    query = "You are a teacher. Generate questions and answers based on the image I provide to you. Format should be proper Python Javascript object notation list of dictionaries where every dictionary contains keys as 'question_no', 'question', 'correct_answer' and 'options'(if available)."
                    img = save_image(uploaded_file)
                    result = image_processing_assignment_solution(
                        img[0], query)
                    temp = format_final_response(result)
                    self.send({
                        "type": "websocket.send",
                        "text": json.dumps(temp)
                    })
            self.send({
                        "type": "websocket.send",
                        "text": json.dumps({"data": "", "signal": 0})
                    })
        except Exception as error:
            print(error, '---error--error----error-----')
            self.send({
                        "type": "websocket.send",
                        "text": json.dumps({"data": "", "signal": 0, "message": "Something went wrong", "status": 400})
                    })
            self.send({
                "type": "websocket.close"
                })        

    def websocket_disconnect(self, event):
        print('websocket disconnected.....', event)
        raise StopConsumer()

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