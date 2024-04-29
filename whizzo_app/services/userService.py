from whizzo_app.models.userModel import UserModel
from whizzo_app.utils import messages
from whizzo_app.serializers import userSerializer
from django.contrib.auth.hashers import check_password
from whizzo_app.utils import sendMail
from datetime import datetime
from threading import Thread
import pytz

class UserService:
    def user_registration(self, request):
        otp = sendMail.generate_otp()
        email = request.data.get("email")
        password = request.data.get("password")
        phone_no = request.data.get("phone_no")
        if "email" in request.data:
            check_user = UserModel.objects.filter(email = email)
            if check_user.exists() and check_user.first().profile_status > 1:
                return {"data": None, "message": messages.EMAIL_ALREADY_EXISTS, "status": 400}
            elif check_user.exists() and check_user.first().profile_status == 1:
                check_user.first().delete()
            user = UserModel(email=email)
            user.otp = otp
            user.otp_sent_time = datetime.now(tz=pytz.UTC)
            user.profile_status = 1
            user.set_password(password)
            user.save()
            Thread(target=sendMail.send_otp_to_mail, args=[email, otp]).start()
        elif "phone_no" in request.data:
            user = UserModel.objects.filter(phone_no = phone_no).exists()
            if user:
                return {"data": None, "message": messages.PHONE_ALREADY_EXISTS, "status": 400}
            user = UserModel(phone_no=phone_no)
            user.otp = otp
            user.otp_sent_time = datetime.now(tz=pytz.UTC)
            user.profile_status = 1
            user.save()
        return {"data": "", "message": messages.OTP_SENT_AFTER_REGISTRATION, "status": 201}
    
    def login_user(self, request):
        email = request.data["email"]
        password = request.data["password"]
        try:
            user = UserModel.objects.get(email = email)
        except UserModel.DoesNotExist:
            return {"data": None, "message": messages.EMAIL_NOT_FOUND, "status": 400}
        
        verify_password = check_password(password, user.password)
        if verify_password:
            give_login_token = True
            serializer = userSerializer.GetUserSerializer(user, context = {"give_login_token": give_login_token})
            return {"data": serializer.data, "message": messages.USER_LOGGED_IN, "status": 200}
        else:
            return {"data": None, "message": messages.PASSWORD_WRONG, "status": 400}

    def verify_otp(self, request):
        GIVE_LOGIN_TOKEN = False
        try:
            if "email" in request.data:
                user = UserModel.objects.get(email=request.data["email"])
            elif "phone_number" in request.data:
                user = UserModel.objects.get(phone_no=request.data["phone_number"])
            else:
                return {"data": None, "message": "Email or phone number not provided", "status": 400}
        except UserModel.DoesNotExist:
            return {"data": None, "message": 'USER_NOT_FOUND', "status": 400}
        now = datetime.now(tz=pytz.UTC)
        otp_duration = (now - user.otp_sent_time).seconds
        if otp_duration > 60:
            return {"data": None, "message": messages.OTP_EXPIRED, "status": 400}
        if user.otp != request.data["otp"]:
            return {"data": None, "message":  messages.WRONG_OTP, "status": 400}
        if "email" in request.data:
            user.email_verification = True
            if user.profile_status == 1:
                user.profile_status = 2
                GIVE_LOGIN_TOKEN = True
        user.save()
        user_serializer = userSerializer.GetUserSerializer(user, context={"give_login_token": GIVE_LOGIN_TOKEN})    
        return {"data": user_serializer.data, "message":  "OTP_VERIFIED", "status": 200}
    
    def resend_otp(self, request):
        email=request.data["email"]
        try:
            if "email" in request.data:
                user = UserModel.objects.get(email=email)
            elif "phone_number" in request.data:
                user = UserModel.objects.get(phone_no=request.data["phone_number"])
            else:
                return {"data": None, "message": "Email or phone number not provided", "status": 400}
        except UserModel.DoesNotExist:
            return {"data": None, "message":  'USER_NOT_FOUND', "status": 400}
        
        if "email" in request.data:
            Thread(target=sendMail.send_otp_to_mail, args=[email, otp]).start()
    
        user.otp = otp
        user.otp_sent_time = datetime.now(tz=pytz.UTC)
        user.save()
        
        return {"data": None, "message":  "OTP_SENT", "status": 200}