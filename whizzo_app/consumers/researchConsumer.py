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
from whizzo_app.models.abilityModel import AbilityModel
from whizzo_app.utils.Modules.articlesModule import generate_article_util

class ResearchTopicsConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        payload = json.loads(event["text"])
        try:
            topic = payload.get("topic")
            QUERY = f"You are a topics list generator. Generate research topics list based on {topic}. Output should contain topics headings(strictly numbered like 1,2,3,.....) and slide headings(strictly numbered like i, ii, iii , ......)."
            llm = ChatGoogleGenerativeAI(model="gemini-pro")
            message_content = [
                    {
                        "type": "text",
                        "text": QUERY
                    }
                ]
            message = HumanMessage(content=message_content)
            for chunk in llm.stream([message]):
                    stream_chunk = chunk.content
                    result = to_markdown(stream_chunk)
                    self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({"data": result, "signal": 1})
                    })
            if "Invalid input provided" in result:
                self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({"data": "", "signal": 0, "message": "Something went wrong"})
                    })
        except:
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
