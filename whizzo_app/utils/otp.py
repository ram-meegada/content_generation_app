import random
from rest_framework_simplejwt.tokens import RefreshToken
import base64
import string

def generate_otp():
    otp = ''.join([str(random.randint(0,9)) for _ in range(4)])
    # return otp
    return "1111"

def generate_access_token(user):
    token = RefreshToken.for_user(user)
    return str(token.access_token)

def generate_random_pasword():
    password = base64.b64encode(str(random.randint(100000,9999999)).encode()).decode()
    return password



def generate_password():
    # Define the character sets to choose from
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "@"
    # Choose one character from each set
    random_first_char = random.choice(string.ascii_letters)
    random_lowercase = random.choice(lowercase)
    random_uppercase = random.choice(uppercase)
    random_digit1 = random.choice(digits)
    random_digit2 = random.choice(digits)
    random_special_char = random.choice(special_chars)
    # Generate remaining characters randomly
    remaining_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=2))
    # Concatenate all the characters and shuffle them randomly
    password = ''.join([random_first_char, random_lowercase, random_uppercase, random_digit1, random_special_char, random_digit2, remaining_chars])
    password = ''.join(random.sample(password, len(password)))
    return password
