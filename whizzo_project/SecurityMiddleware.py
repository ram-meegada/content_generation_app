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

                # Parse the extracted string as JSON
                data_dict = json.loads(decrypted_string)

                # Extract the authorization token
                # authorization_token = data_dict.get('authorization', '')
                authorization_token = data_dict.get('authorization', '')
                request.META["HTTP_AUTHORIZATION"] = data_dict.get('authorization', '')

                # Handle authorization logic
                if authorization_token:
                    pass
                #     # Add authorization token as a header in the request
                #     pass

                # Convert the date-time string to a timestamp
                try:
                    appkey_datetime_str = data_dict.get('appkey', '')
                    appkey_datetime = datetime.strptime(appkey_datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                    code_time_stamp = int(appkey_datetime.timestamp())
                except:
                    pass    

                if request.method in ["POST", "PUT"]:
                    try:
                        data = json.loads(request.body)
                        updated_data = payload_decrypt(data)
                        request._body = json.dumps(updated_data).encode('utf-8')
                    except Exception as err:
                        pass
            elif request.method in ["POST", "PUT"]:
                try:
                    data = json.loads(request.body)
                    updated_data = payload_decrypt(data)
                    request._body = json.dumps(updated_data).encode('utf-8')
                except:
                    pass            

            return self.get_response(request)

        except Exception as e:
            error_message = str(e)
            data = {"data": error_message, "code": status.HTTP_400_BAD_REQUEST, 'message': 'You are not Authenticated'}
            response = Response(data, status=status.HTTP_400_BAD_REQUEST)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = response.accepted_renderer.media_type
            response.renderer_context = {}
            response.render()
            return response

