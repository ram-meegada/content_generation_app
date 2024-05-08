from whizzo_app.utils.encrytpion import payload_decrypt
from io import BytesIO
import json
from django.http import JsonResponse
import json
import datetime
from django.contrib import messages
from django.http import HttpResponseBadRequest
from Cryptodome.Cipher import AES
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
import time

class DecryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        try:
            if not request.headers.get('Sek'):
                if request.method == "POST" or request.method == "PUT":
                    data = json.loads(request.body)
                    updated_data = payload_decrypt(data)
                    request._body = json.dumps(updated_data).encode('utf-8')
                    data = self.get_response(request)
                    return data
            # print(request.META,'request.headers')
            sek = request.headers['Sek']
            hash_value = request.headers['Hash']
            hash_bytes = bytes.fromhex(hash_value)
            sek_bytes = bytes.fromhex(sek)
            iv = b'D904363DB8DACEB8'
            decipher = AES.new(hash_bytes, AES.MODE_CBC, iv)
            decrypted_bytes = decipher.decrypt(sek_bytes)
            string_data = decrypted_bytes.decode()
            clean_string = string_data.replace('\x08','')
            data_dict = json.loads(clean_string)
            code_time_stamp = int(data_dict['appkey']) / 1000
            ts = time.time()
            current_timestamp_before_15 = ts - 10
            # if int(code_time_stamp) < int(current_timestamp_before_15):
            #     print("=========ffffffffffffff=========")
            #     data = {"data":None,  "code": status.HTTP_400_BAD_REQUEST, 'message':'You are not Authenticated'}
            #     response = Response(data, status=status.HTTP_400_BAD_REQUEST)
            #     response.accepted_renderer = JSONRenderer()
            #     response.accepted_media_type = response.accepted_renderer.media_type
            #     response.renderer_context = {}
            #     response.render()
            #     return response
            if request.method == "POST" or request.method == "PUT":
                data = json.loads(request.body)
                updated_data = payload_decrypt(data)
                request._body = json.dumps(updated_data).encode('utf-8')
            data = self.get_response(request)
            return data
        except Exception as e:
            data = {"data": str(e),  "code": status.HTTP_400_BAD_REQUEST, 'message':'You are not Authenticated'}
            response = Response(data, status=status.HTTP_400_BAD_REQUEST)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = response.accepted_renderer.media_type
            response.renderer_context = {}
            response.render()
            return response



