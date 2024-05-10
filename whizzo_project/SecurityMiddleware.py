# from whizzo_app.utils.encrytpion import payload_decrypt
# from io import BytesIO
# import json
# from django.http import JsonResponse
# import json
# import datetime
# from django.contrib import messages
# from django.http import HttpResponseBadRequest
# from Cryptodome.Cipher import AES
# import json
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.renderers import JSONRenderer
# import time

# class DecryptionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#     def __call__(self, request):
#         try:
#             print("wwwwwwwwwwwwwwwwwwwwwwww")
#             if not request.headers.get('Sek'):
#                 print("yyyyyyyyyyyyyyyyyyyyyy")
#                 if request.method == "POST" or request.method == "PUT":
#                     print("yywwwwwwwwwwwwwwwwwwwyyyyyyyyyyyyyyyyyyyy")

#                     data = json.loads(request.body)
#                     print(data,"11111111111111111")
#                     updated_data = payload_decrypt(data)
#                     print(updated_data,"44444444444444444444444444444444444")
#                     request._body = json.dumps(updated_data).encode('utf-8')
#                     data = self.get_response(request)
#                     return data
#             print(request.headers,'request.headers')
            
#             sek = request.headers['Sek']
#             print(sek,"1111111111111111111111")
#             hash_value = request.headers['Hash']
#             print(hash_value,"1111111111111111111111")

#             print("came here11111111111111111111111111111111111111111")
#             hash_bytes = bytes.fromhex(hash_value)
#             sek_bytes = bytes.fromhex(sek)
#             iv = b'D904363DB8DACEB8'
#             decipher = AES.new(hash_bytes, AES.MODE_CBC, iv)
#             print("came here 1111111111111111111111111111176788")
#             decrypted_bytes = decipher.decrypt(sek_bytes)
#             print(decrypted_bytes,"headers========")
#             string_data = decrypted_bytes.decode()
#             print(string_data,"777777777777777")
#             clean_string = string_data.replace('\x08','')
#             print(clean_string,"888888888888888888888888888")
#             data_dict = json.loads(clean_string)
#             print(data_dict,"555555555555555555555")
#             code_time_stamp = int(data_dict['appkey']) / 1000
#             ts = time.time()
#             current_timestamp_before_15 = ts - 10
#             # if int(code_time_stamp) < int(current_timestamp_before_15):
#             #     print("=========ffffffffffffff=========")
#             #     data = {"data":None,  "code": status.HTTP_400_BAD_REQUEST, 'message':'You are not Authenticated'}
#             #     response = Response(data, status=status.HTTP_400_BAD_REQUEST)
#             #     response.accepted_renderer = JSONRenderer()
#             #     response.accepted_media_type = response.accepted_renderer.media_type
#             #     response.renderer_context = {}
#             #     response.render()
#             #     return response
#             if request.method == "POST" or request.method == "PUT":
#                 data = json.loads(request.body)
#                 updated_data = payload_decrypt(data)
#                 print(updated_data,"1111111111111111111111111111111111111")
#                 request._body = json.dumps(updated_data).encode('utf-8')
#             data = self.get_response(request)
#             return data
#         except Exception as e:
#             print(str(e),"hhhhhhhhhhhhhhhhhhhhhhhhh")
#             data = {"data": str(e),  "code": status.HTTP_400_BAD_REQUEST, 'message':'You are not Authenticated'}
#             response = Response(data, status=status.HTTP_400_BAD_REQUEST)
#             response.accepted_renderer = JSONRenderer()
#             response.accepted_media_type = response.accepted_renderer.media_type
#             response.renderer_context = {}
#             response.render()
#             return response



# import json

# from whizzo_app.utils.encrytpion import payload_decrypt
# from Cryptodome.Cipher import AES
# import time
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.renderers import JSONRenderer

# class DecryptionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         try:
#             if not request.headers.get('Sek'):
#                 if request.method in ["POST", "PUT"]:
#                     data = json.loads(request.body)
#                     updated_data = payload_decrypt(data)
#                     request._body = json.dumps(updated_data).encode('utf-8')

#             if 'Sek' in request.headers and 'Hash' in request.headers:
#                 sek = request.headers['Sek']
#                 hash_value = request.headers['Hash']

#                 hash_bytes = bytes.fromhex(hash_value)
#                 sek_bytes = bytes.fromhex(sek)
#                 iv = b'D904363DB8DACEB8'
#                 decipher = AES.new(hash_bytes, AES.MODE_CBC, iv)
#                 decrypted_bytes = decipher.decrypt(sek_bytes)
#                 print(decrypted_bytes,"============fdddddddddddddddddddddd")
#                 # Convert bytes to string and remove extraneous characters
#                 decrypted_string = decrypted_bytes.decode().strip('♂\x0b')
#                 print(decrypted_string,"=======fffffffffffffff======")
#                 # Parse the decrypted string as JSON
#                 data_dict = json.loads(decrypted_string)

#                 code_time_stamp = int(data_dict.get('appkey', 0)) / 1000
#                 ts = time.time()
#                 current_timestamp_before_15 = ts - 10

#                 if request.method in ["POST", "PUT"]:
#                     data = json.loads(request.body)
#                     updated_data = payload_decrypt(data)
#                     request._body = json.dumps(updated_data).encode('utf-8')

#             return self.get_response(request)

#         except Exception as e:
#             error_message = str(e)
#             print(error_message,"=========rrrrrrrrrrrrrrr===========")
#             data = {"data": error_message, "code": status.HTTP_400_BAD_REQUEST, 'message': 'You are not Authenticated'}
#             response = Response(data, status=status.HTTP_400_BAD_REQUEST)
#             response.accepted_renderer = JSONRenderer()
#             response.accepted_media_type = response.accepted_renderer.media_type
#             response.renderer_context = {}
#             response.render()
#             return response

# import json
# from datetime import datetime

# from whizzo_app.utils.encrytpion import payload_decrypt
# from Cryptodome.Cipher import AES
# import time
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.renderers import JSONRenderer

# class DecryptionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         try:
#             if not request.headers.get('Sek'):
#                 if request.method in ["POST", "PUT"]:
#                     data = json.loads(request.body)
#                     updated_data = payload_decrypt(data)
#                     request._body = json.dumps(updated_data).encode('utf-8')

#             if 'Sek' in request.headers and 'Hash' in request.headers:
#                 sek = request.headers['Sek']
#                 hash_value = request.headers['Hash']

#                 hash_bytes = bytes.fromhex(hash_value)
#                 sek_bytes = bytes.fromhex(sek)
#                 iv = b'D904363DB8DACEB8'
#                 decipher = AES.new(hash_bytes, AES.MODE_CBC, iv)
#                 decrypted_bytes = decipher.decrypt(sek_bytes)
                
#                 # Convert bytes to string and remove extraneous characters
#                 decrypted_string = decrypted_bytes.decode().strip('♂\x0b')
#                 print(decrypted_string,"")
                
#                 # Parse the decrypted string as JSON
#                 data_dict = json.loads(decrypted_string)

#                 # Convert the date-time string to a timestamp
#                 appkey_datetime_str = data_dict.get('appkey', '')
#                 appkey_datetime = datetime.strptime(appkey_datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')
#                 code_time_stamp = int(appkey_datetime.timestamp())

#                 ts = time.time()
#                 current_timestamp_before_15 = ts - 10

#                 if request.method in ["POST", "PUT"]:
#                     data = json.loads(request.body)
#                     updated_data = payload_decrypt(data)
#                     request._body = json.dumps(updated_data).encode('utf-8')

#             return self.get_response(request)

#         except Exception as e:
#             error_message = str(e)
#             print(error_message,"===========eeeeeeeeeeeeeeeeeeeeeee============")
#             data = {"data": error_message, "code": status.HTTP_400_BAD_REQUEST, 'message': 'You are not Authenticated'}
#             response = Response(data, status=status.HTTP_400_BAD_REQUEST)
#             response.accepted_renderer = JSONRenderer()
#             response.accepted_media_type = response.accepted_renderer.media_type
#             response.renderer_context = {}
#             response.render()
#             return response


import json
from datetime import datetime

from whizzo_app.utils.encrytpion import payload_decrypt
from Cryptodome.Cipher import AES
import time
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.http import HttpRequest

class DecryptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Check if Sek and Hash headers are present
            if 'Sek' in request.headers and 'Hash' in request.headers:
                sek = request.headers['Sek']
                hash_value = request.headers['Hash']

                hash_bytes = bytes.fromhex(hash_value)
                sek_bytes = bytes.fromhex(sek)
                iv = b'D904363DB8DACEB8'
                decipher = AES.new(hash_bytes, AES.MODE_CBC, iv)
                decrypted_bytes = decipher.decrypt(sek_bytes)
                
                # Convert bytes to string and remove extraneous characters
                decrypted_string = decrypted_bytes.decode().strip('♂\x0b♦')

                # Extract string until the last '}'
                decrypted_string = decrypted_string.rsplit('}', 1)[0] + '}'
                print(decrypted_string, "Processed Decrypted String")

                # Parse the extracted string as JSON
                data_dict = json.loads(decrypted_string)

                # Extract the authorization token
                print(data_dict)
                authorization_token = data_dict.get('authorization', '')
                print(authorization_token,"33333333333333333333333333333333333333333")

                # Handle authorization logic
                if authorization_token:
                    pass
                #     # Add authorization token as a header in the request
                #     pass

                # Convert the date-time string to a timestamp
                appkey_datetime_str = data_dict.get('appkey', '')
                appkey_datetime = datetime.strptime(appkey_datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                code_time_stamp = int(appkey_datetime.timestamp())

                if request.method in ["POST", "PUT"]:
                    data = json.loads(request.body)
                    updated_data = payload_decrypt(data)
                    request._body = json.dumps(updated_data).encode('utf-8')

            return self.get_response(request)

        except Exception as e:
            error_message = str(e)
            print(error_message, "Error Message")
            data = {"data": error_message, "code": status.HTTP_400_BAD_REQUEST, 'message': 'You are not Authenticated'}
            response = Response(data, status=status.HTTP_400_BAD_REQUEST)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = response.accepted_renderer.media_type
            response.renderer_context = {}
            response.render()
            return response

