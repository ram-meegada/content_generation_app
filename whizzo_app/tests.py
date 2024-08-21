import asyncio
import websockets
import json
from google.cloud import speech
# Set up Google Speech-to-Text client
client = speech.SpeechClient()
# Set up WebSocket server
async def handle_websocket(websocket, path):
    # Handle incoming audio data
    audio_buffer = bytearray()
    while True:
        try:
            message = await websocket.recv()
            if message.type == websockets.MessageType.BINARY:
                audio_buffer.extend(message.data)
            elif message.type == websockets.MessageType.TEXT:
                print(f"Received text message: {message.data}")
        except websockets.ConnectionClosed:
            print("Connection closed")
            break
    # Send audio data to Google Speech-to-Text
    audio = speech.types.RecognitionAudio(content=audio_buffer)
    config = speech.types.RecognitionConfig(encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16)
    response = client.recognize(config, audio)
    # Print transcription results
    for result in response.results:
        for alternative in result.alternatives:
            print(f"Transcription: {alternative.transcript}")
async def main():
    async with websockets.serve(handle_websocket, "localhost", 8765):
        print("WebSocket server started on port 8765")
        await asyncio.Future()  # run forever
asyncio.run(main())