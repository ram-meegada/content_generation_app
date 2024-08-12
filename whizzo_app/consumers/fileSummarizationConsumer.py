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

class FileSummarizationConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        google_api_key = settings.GOOGLE_API_KEY
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)
        payload = json.loads(event["text"])
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
            temp = {1: 2000, 2: 4000, 3: 8000, 4: 12000}
            i, j = 0, 0
            # if payload["signal"] == 2: # 2 is for stop generating response
            #     self.terminate_process = True
            #     self.send({
            #             'type': 'websocket.send',
            #             'text': json.dumps({"data": "Response generation terminated successfully", "signal": 2})
            #             })
            #     self.send({
            #             "type": "websocket.close",
            #             })
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
                message = HumanMessage(
                    content=[
                        {"type": "text",
                            "text": f"Generate a summary of the input I provide you. And continue with previous response.(if previous response present)"},
                        {"type": "text", "text": input_text}
                    ]
                )
                full_response = ""
                for chunk in llm.stream([message]):
                    stream_chunk = chunk.content
                    self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({"data": stream_chunk, "signal": 1})
                    })
                    full_response += stream_chunk
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
                query = "You are summary provider. Generate a summary of images I provide you through links as soon as possible and the length of the summary should be atleast five hundred words and give me only text no * and extra symbols"
                img = save_image(uploaded_file)
                result = image_processing_assignment_solution(
                        img[0], query)
                self.send({
                            'type': 'websocket.send',
                            'text': json.dumps({"data": result, "signal": 1})
                        })
        self.send({
            'type': 'websocket.send',
            'text': json.dumps({"data": "", "signal": 0})
        })
        return

    def websocket_disconnect(self, event):
        print('websocket disconnected.....', event)
        raise StopConsumer()
