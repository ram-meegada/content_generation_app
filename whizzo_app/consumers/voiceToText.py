import io
import random
# import base64
# import json
# from io import BytesIO
# from django.core.files.base import ContentFile
# from channels.generic.websocket import SyncConsumer
# from google.cloud import speech_v1 as speech
# from google.api_core.exceptions import GoogleAPICallError
# from channels.exceptions import StopConsumer
# import os

# credential_path = "C:/Users/PC/Downloads/apptunix-food-customer-9b7b1e98835c.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


# class AudioConsumer(SyncConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.audio_buffer = BytesIO()
#         self.transcript = ""

#     def websocket_connect(self, event):
#         self.terminate_process = False
#         self.send({
#             'type': 'websocket.accept'
#         })

#     def websocket_receive(self, event):
#         if self.terminate_process:
#             return

#         payload = json.loads(event["text"])

#         if "audio" in payload:
#             # Process audio file
#             audio_base64 = payload["audio"]
#             audio_data = base64.b64decode(audio_base64)

#             # Append new audio data to the buffer
#             self.audio_buffer.write(audio_data)
#             self.audio_buffer.seek(0)
            
#             # Transcribe audio from buffer
#             try:
#                 transcript = self.transcribe_streaming(self.audio_buffer)
#                 self.send({
#                     'type': 'websocket.send',
#                     'text': json.dumps({"transcript": transcript})
#                 })
#             except GoogleAPICallError as e:
#                 self.send({
#                     'type': 'websocket.send',
#                     'text': json.dumps({"error": str(e)})
#                 })

#         elif payload.get("signal") == 2:  # Signal to stop generating response
#             self.terminate_process = True
#             self.send({
#                 'type': 'websocket.send',
#                 'text': json.dumps({"data": "Response generation terminated successfully", "signal": 2})
#             })
#             self.send({
#                 "type": "websocket.close",
#             })
#             return

#     def websocket_disconnect(self, event):
#         print('websocket disconnected.....', event)
#         raise StopConsumer()

#     def transcribe_streaming(self, audio_stream: BytesIO) -> str:
#         """Streams transcription of the given audio stream."""
#         client = speech.SpeechClient()
        
#         # Prepare the audio stream for processing
#         audio_stream.seek(0)
#         content = audio_stream.read()

#         # Stream should be a generator yielding chunks of audio data.
#         stream = [content]

#         requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream)

#         config = speech.RecognitionConfig(
#             encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#             sample_rate_hertz=16000,
#             language_code="en-US",
#         )

#         streaming_config = speech.StreamingRecognitionConfig(config=config)

#         responses = client.streaming_recognize(
#             config=streaming_config,
#             requests=requests,
#         )

#         transcript = ""
#         for response in responses:
#             for result in response.results:
#                 for alternative in result.alternatives:
#                     transcript += alternative.transcript + " "
        
#         return transcript



from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
import base64
import json
from io import BytesIO
from django.core.files.base import ContentFile
from channels.generic.websocket import SyncConsumer
# from google.cloud import speech_v1 as speech
from google.api_core.exceptions import GoogleAPICallError
from channels.exceptions import StopConsumer
import os
from django.core.files.storage import FileSystemStorage

credential_path = "C:/Users/PC/Downloads/apptunix-food-customer-9b7b1e98835c.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

from channels.generic.websocket import AsyncWebsocketConsumer
# from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPICallError
import json

class AudioConsumer(AsyncWebsocketConsumer):
    recognize_stream = None
    speech_client = None
    requests = None
    responses = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if self.speech_client:
            self.speech_client.transport.channel.close()

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            if self.recognize_stream:
                try:
                    # Append the bytes data to the requests generator
                    await self.recognize_stream.write(bytes_data)
                except GoogleAPICallError as e:
                    print(f"Error calling Google API: {e}")
            else:
                print("Stream not initialized")
        else:
            print("Received non-bytes data")

    async def start_recognition_stream(self, data):
        # Initialize the Google Cloud Speech-to-Text client
        self.speech_client = speech.SpeechClient()
        
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US',
            # ... other settings ...
        )
        streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

        self.requests = []
        self.responses = []
        
        def request_generator():
            for request in self.requests:
                yield request
            while True:
                if self.requests:
                    yield self.requests.pop(0)
                else:
                    break

        self.recognize_stream = self.speech_client.streaming_recognize(streaming_config, request_generator())
        
        async for response in self.recognize_stream:
            for result in response.results:
                # Send the results to the client
                await self.send(text_data=json.dumps({'type': 'result', 'transcript': result.alternatives[0].transcript}))

        await self.send(text_data=json.dumps({'type': 'stream_started'}))

    async def stop_recognition_stream(self):
        if self.recognize_stream:
            self.recognize_stream = None
            await self.send(text_data=json.dumps({'type': 'stream_stopped'}))

    async def send_message(self, message):
        await self.send(text_data=json.dumps({'type': 'message', 'message': message}))

