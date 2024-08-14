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
from google.cloud import speech_v1 as speech
from google.api_core.exceptions import GoogleAPICallError
from channels.exceptions import StopConsumer
import os
from django.core.files.storage import FileSystemStorage

credential_path = "C:/Users/PC/Downloads/apptunix-food-customer-9b7b1e98835c.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

class AudioConsumer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio_buffer = BytesIO()
        self.transcript = ""

    def websocket_connect(self, event):
        self.terminate_process = False
        self.send({'type': 'websocket.accept'})

    def websocket_receive(self, event):
        client = speech.SpeechClient.from_service_account_file("C:/Users/PC/Downloads/apptunix-food-customer-9b7b1e98835c.json")
        payload = json.loads(event["text"])
        audio_data = base64.b64decode(payload["audio"])

        random_file_name = f"{random.randint(1000, 9999)}_temp_audio.wav"

        with open(random_file_name, 'wb') as audio_file:
            audio_file.write(audio_data)

        with open(random_file_name, "rb") as f:
            audio_stream = f.read()

        audio_file = speech.RecognitionAudio(content=audio_stream)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=44100,
            enable_automatic_punctuation=True,
            language_code='en-US'
        )

        responses = client.recognize(
            config=config,
            audio=audio_file
        )
        print(responses, type(responses), '---response----')
        transcript = ""
        for response in responses.results:
            for alternative in response.alternatives:
                transcript += alternative.transcript + " "
        self.send({
            'type': 'websocket.send',
            'text': json.dumps({"data": json.dumps(transcript), "signal": 1})
        })
        if os.path.exists(random_file_name):
            os.remove(random_file_name)

    def websocket_disconnect(self, event):
        print('websocket disconnected.....', event)
        raise StopConsumer()
