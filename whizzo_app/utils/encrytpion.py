from Cryptodome.Cipher import AES 
import json
import time
import ast

# def payload_decrypt(data):
    # sek = data['sek']
    # hash_value = data['hash']
    # hash_bytes = bytes.fromhex(hash_value)
    # sek_bytes = bytes.fromhex(sek)
    # iv = b'9EFdvO3KmZX5rGT9'
    # decipher = AES.new(hash_bytes, AES.MODE_CBC, iv)
    # decrypted_bytes = decipher.decrypt(sek_bytes)
    # string_data = decrypted_bytes.decode()
    # decrypted = decrypted_bytes.decode('ascii')
    # decrypted_string = ''
    # for i in range(len(decrypted)-1,0,-1):
        # if decrypted[i] == '}':
            # decrypted_string = decrypted[:i+1]
            # break
    # if "null" in decrypted_string:
        # json_ans = json.loads(decrypted_string)
        # return json_ans
    # json_ans = ast.literal_eval(decrypted_string)
    # return json_ans
# 
# 
def payload_decrypt(data):
    sek = data['sek']
    hash_value = data['hash']
    hash_bytes = bytes.fromhex(hash_value)
    sek_bytes = bytes.fromhex(sek)
    iv = b'D904363DB8DACEB8'
    decipher = AES.new(hash_bytes, AES.MODE_CBC, iv)
    decrypted_bytes = decipher.decrypt(sek_bytes)
    # string_data = decrypted_bytes.decode()
    print(decrypted_bytes,'decrypted_bytes')
    decrypted = decrypted_bytes.decode('ascii')
    # cleaned_string = re.sub(r'[^a-zA-Z0-9\s{}:,._@""()\[\]]', '', a_decrypted)
    # converted_string = json.loads(cleaned_string)
    # print(converted_string,'converted_string')
    # return converted_string
    # for i in decrypted: 
        # print(i,'decrypted')
    decrypted_string = ''
    for i in range(len(decrypted)-1,0,-1):
        if decrypted[i] == '}' or decrypted[i] == ']':
            decrypted_string = decrypted[:i+1]
            break
    # if "null" in decrypted_string:
    json_ans = json.loads(decrypted_string)
    return json_ans
    # json_ans = ast.literal_eval(decrypted_string)
    # return json_ans

def header_decrypt(data):
    sek = data['HTTP_SEK']
    hash_value = data['HTTP_HASH']
    hash_bytes = bytes.fromhex(hash_value)
    sek_bytes = bytes.fromhex(sek)
    iv = b'D904363DB8DACEB8'
    decipher = AES.new(hash_bytes, AES.MODE_CBC, iv)
    decrypted_bytes = decipher.decrypt(sek_bytes)
    # string_data = decrypted_bytes.decode()
    decrypted = decrypted_bytes.decode('ascii')
    decrypted_string = ''
    for i in range(len(decrypted)-1,0,-1):
        if decrypted[i] == '}':
            decrypted_string = decrypted[:i+1]
            break
    json_ans = ast.literal_eval(decrypted_string)
    return json_ans
    # print(decrypted_bytes,'string_data')
    # if '\x08' in string_data:
    #     clean_string = string_data.replace('\x08','')
    #     data_dict = json.loads(clean_string)
    #     return data_dict
    # if '\x03' in string_data:
    #     clean_string = string_data.replace('\x03','')
    #     data_dict = json.loads(clean_string)
    #     return data_dict
