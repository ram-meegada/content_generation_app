import random
from whizzo_project import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import threading
from whizzo_app.models.uploadMediaModel import UploadMediaModel
 
def send_otp_to_mail(email, otp,name="User"):
    try:
        context = {"name":name,"otp": otp, "logo_link":"https://enilcon.s3.ap-south-1.amazonaws.com/213448_logo.svg"}
        temp = render_to_string("sendOtpToMail.html", context=context)
        msg = EmailMultiAlternatives("Dont reply" ,temp, settings.DEFAULT_FROM_EMAIL, [email])
        msg.content_subtype = "html"
        msg.send()
    except Exception as error:
        pass
# def send_otp_to_mail(email, otp):
#     try:
#         context = {"otp": otp}
#         temp = render_to_string("sendOtpToMail.html", context=context)
#         msg = EmailMultiAlternatives("Dont reply" ,temp, settings.DEFAULT_FROM_EMAIL, [email])
#         msg.content_subtype = "html"
#         msg.send()
#     except Exception as error:

def generate_otp():
    # otp = random.randint(0000, 9999)
    otp = "1234"
    return otp

# class SendOtpToMail(threading.Thread):
#     def __init__(self, otp_or_password, email, name="User"):
#         self.otp_or_password = otp_or_password
#         self.email = email
#         self.name = name
#         threading.Thread.__init__(self)
def SendOtpToMail(otp_or_password, email, name="User"):
    context = {"otp_or_password": otp_or_password, "email": email[0], "name": name}
    temp = render_to_string("email_otp.html", context)
    msg = EmailMultiAlternatives("Dont Reply!", temp, settings.DEFAULT_FROM_EMAIL, email)
    msg.content_subtype = "html"
    msg.send()
    return
    
def SubadminCreated(otp_or_password, email, link):
    context = {"password": otp_or_password, "email": email, "link": link}
    print(context)
    temp = render_to_string("account-created.html", context)
    msg = EmailMultiAlternatives("Dont Reply!", temp, settings.DEFAULT_FROM_EMAIL, [email])
    msg.content_subtype = "html"
    msg.send()
    return

def SubadminUpdated(name, email, link):
    context = {"name": name, "email": email, "link": link}
    print(context)
    temp = render_to_string("account-updated.html", context)
    msg = EmailMultiAlternatives("Dont Reply!", temp, settings.DEFAULT_FROM_EMAIL, [email])
    msg.content_subtype = "html"
    msg.send()
    return

def DeleteUserNotification(email, name="User"):
    context = { "email": email[0], "name": name}
    temp = render_to_string("delete-user-notification.html", context)
    msg = EmailMultiAlternatives("Dont Reply!", temp, settings.DEFAULT_FROM_EMAIL, email)
    msg.content_subtype = "html"
    msg.send()
    return
# def SendOtpToMail( otp, email):    
#     context = {"otp": otp}
#     temp = render_to_string("email_otp.html", context)
#     msg = EmailMultiAlternatives("Dont Reply!", temp, settings.DEFAULT_FROM_EMAIL, email)
#     msg.content_subtype = "html"
#     msg.send()
#     return

class EmailThread(threading.Thread):
    def __init__(self, recipient_list, title, message):
        self.title = title
        self.recipient_list = recipient_list
        self.message = message
        threading.Thread.__init__(self)
    def run(self):
        context = {'message':self.message, 'title':self.title}
        temp = render_to_string('notification.html', context)
        msg = EmailMultiAlternatives(f"{self.title}", temp, settings.DEFAULT_FROM_EMAIL, [self.recipient_list])
        msg.content_subtype = 'html'
        msg.send()
        return None
def send_notification_to_mail(recipient_list, title, message):
    EmailThread(recipient_list, title, message).start()



def send_pdf_file_to_mail(email,file_link):
    try:
        context = {"link": file_link}
        temp = render_to_string("sendPdfFileToMail.html", context=context)
        msg = EmailMultiAlternatives("Dont reply" ,temp, settings.DEFAULT_FROM_EMAIL, [email])
        msg.content_subtype = "html"
        msg.send()
        print("----------------------------------", file_link, email)
    except Exception as error:
        pass