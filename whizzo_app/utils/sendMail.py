import random
from whizzo_project import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def send_otp_to_mail(email, otp):
    try:
        context = {"otp": otp}
        temp = render_to_string("sendOtpToMail.html", context=context)
        msg = EmailMultiAlternatives("Dont reply" ,temp, settings.DEFAULT_FROM_EMAIL, [email])
        msg.content_subtype = "html"
        msg.send()
        print("########## sent ###########")
    except Exception as error:
        print(error, "----------error---------")    

def generate_otp():
    # otp = random.randint(0000, 9999)
    otp = "1111"
    return otp