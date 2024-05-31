from re import search
from tabnanny import check
from rest_framework import status
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
        country_code = request.data.get("country_code")
        country_name = request.data.get("country_name")
        if "email" in request.data:
            check_user = UserModel.objects.filter(email = email)
            if check_user.exists() and check_user.first().profile_status > 1:
                return {"data": None, "message": messages.EMAIL_ALREADY_EXISTS, "status": 400}
            elif check_user.exists() and check_user.first().profile_status == 1:
                check_user.first().delete()
            user = UserModel(email=email)
            user.role = 2
            user.otp = otp
            user.otp_sent_time = datetime.now(tz=pytz.UTC)
            user.profile_status = 1
            user.set_password(password)
            user.save()
            Thread(target=sendMail.send_otp_to_mail, args=[email, otp]).start()
        elif "phone_no" in request.data:
            user = UserModel.objects.filter(phone_no = phone_no)
            if user.exists() and user.first().profile_status > 1:
                return {"data": None, "message": messages.PHONE_ALREADY_EXISTS, "status": 400}
            elif user.exists() and user.first().profile_status == 1:
                user.first().delete()
            user = UserModel(phone_no=phone_no)
            user.role = 2
            user.country_code=country_code
            user.country_name = country_name
            user.otp = otp
            user.otp_sent_time = datetime.now(tz=pytz.UTC)
            user.profile_status = 1
            user.save()
        return {"data": "", "message": messages.OTP_SENT_AFTER_REGISTRATION, "status": 201}
    
    def login_user(self, request):
        otp=sendMail.generate_otp()
        if request.data.get("email"):
            email = request.data["email"]
            password = request.data["password"]
            try:
                user = UserModel.objects.get(email = email, role=2)
            except UserModel.DoesNotExist:
                return {"data": None, "message": messages.EMAIL_NOT_FOUND, "status": 400}
            verify_password = check_password(password, user.password)
            if verify_password:
                give_login_token = True
                serializer = userSerializer.GetUserSerializer(user, context = {"give_login_token": give_login_token})
                return {"data": serializer.data, "message": messages.USER_LOGGED_IN, "status": 200}
            else:
                return {"data": None, "message": messages.PASSWORD_WRONG, "status": 400}
        if request.data.get("phone_no"):
            phone_no = request.data["phone_no"]
            country_name = request.data["country_name"]
            country_code = request.data["country_code"]
            try:
                user = UserModel.objects.get(phone_no = phone_no,country_name=country_name,country_code=country_code, role=2)
            except UserModel.DoesNotExist:
                return {"data": None, "message": messages.PHONE_NOT_FOUND, "status": 400}
        if user:
            user.otp=otp
            user.otp_sent_time = datetime.now(tz=pytz.UTC)
            user.save()
            return {"data": None, "message": messages.OTP_SENT_PHONE, "status": 200}
        else:
            return {"data": None, "message": messages.PASSWORD_WRONG, "status": 400}

    def logout(self, request):
        return {"data": "", "message": "Logged out successfully", "status": 200}


    def verify_otp(self, request):
        GIVE_LOGIN_TOKEN = False
        try:
            if "email" in request.data:
                user = UserModel.objects.get(email=request.data["email"])
            elif "phone_no" in request.data:
                user = UserModel.objects.get(phone_no=request.data["phone_no"])
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
        if "phone_no" in request.data:
            user.phone_verification = True
            if user.profile_status == 1:
                user.profile_status = 2
                GIVE_LOGIN_TOKEN = True
        user.save()
        user_serializer = userSerializer.GetUserSerializer(user, context={"give_login_token": GIVE_LOGIN_TOKEN})    
        return {"data": user_serializer.data, "message":  "OTP_VERIFIED", "status": 200}
    
    def resend_otp(self, request):
        otp = sendMail.generate_otp()
        try:
            if "email" in request.data:
                user = UserModel.objects.get(email=request.data["email"])
                Thread(target=sendMail.send_otp_to_mail, args=[request.data["email"], otp]).start()
            elif "phone_no" in request.data:
                user = UserModel.objects.get(phone_no=request.data["phone_no"])
            else:
                return {"data": None, "message": "Email or phone number not provided", "status": 400}
        except UserModel.DoesNotExist:
            return {"data": None, "message":  'USER_NOT_FOUND', "status": 400}
        user.otp_sent_time = datetime.now(tz=pytz.UTC)
        user.otp = otp
        user.save()
        return {"data": None, "message":  "OTP_SENT", "status": 200}
    
    def change_password(self, request):
        try:
            user = UserModel.objects.get(id=request.user.id)
        except UserModel.DoesNotExist:
            return {
                "data": None,
                "message":  'User not found',
                "status": status.HTTP_404_NOT_FOUND
            }
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        pswd = check_password(new_password, user.password)
        if pswd:
            return {"data":None,"messages":messages.PASSWORD_NOT_SAME,"status":status.HTTP_400_BAD_REQUEST}
        verify_password = check_password(old_password, user.password)
        if verify_password:
            user.set_password(new_password)
            user.save()
            return {
                "data": None,
                "message": "Password reset successfully.",
                "status": status.HTTP_200_OK
            }
        else:
            return {
                "data": None,
                "message": "Old password is incorrect",
                "status": status.HTTP_400_BAD_REQUEST
            }
        
    def forgot_password(self, request):
        otp = sendMail.generate_otp()
        try:
            if "email" in request.data:
                user = UserModel.objects.get(email=request.data["email"])
            else:
                return {"data": None, "message": "Email not provided", "status": 400}
        except UserModel.DoesNotExist:
            return {"data": None, "message":  'USER_NOT_FOUND', "status": 400}
        Thread(target=sendMail.send_otp_to_mail, args=[request.data["email"], otp]).start()
        user.otp_sent_time= datetime.now(tz=pytz.UTC)
        user.otp = otp
        user.save()
        return {"data": None, "message":  "Otp sent successfully", "status": status.HTTP_200_OK}    
    
    def reset_password(self, request):
        try:
            user = UserModel.objects.get(email=request.data["email"])
        except UserModel.DoesNotExist:
            return {
                "data": None,
                "message":  'USER_NOT_FOUND',
                "status": status.HTTP_404_NOT_FOUND
            }
        new_password = request.data.get("new_password")
        user.set_password(new_password)
        user.save()
        return {
            "data": None,
            "message": "Password reset successfully.",
            "status": status.HTTP_200_OK
        }
    
    def update_profile(self, request):
        try:
            user  = UserModel.objects.get(id = request.user.id)
            if request.data["profile_picture"]:
                serializer = userSerializer.updateUserSerializer(user,data=request.data, context={"user_profile":request.data["profile_picture"],"purpose":request.data["purpose"]})
                if serializer.is_valid():
                    serializer.save(profile_picture_id=request.data["profile_picture"], purpose_id=request.data["purpose"])
                    return {"data": serializer.data, "message": "Profile updated successfully", "status": 200}
            else:
                serializer = userSerializer.updateUserSerializer(user,data=request.data, context={"purpose":request.data["purpose"]})
                if serializer.is_valid():
                    serializer.save( purpose_id=request.data["purpose"])
                    return {"data": serializer.data, "message": "Profile updated successfully", "status": 200}
        except Exception as error:
            return {"data": None, "message": "Something went wrong", "status": 400}
        
    def user_details_by_token(self, request):
        user = UserModel.objects.get(id = request.user.id)
        serializer = userSerializer.GetAllDetailUserSerializer(user)
        return {"data": serializer.data, "message": "USER_DETAILS", "status": 200}  

    def delete_account(self, request):
        try:
            user = UserModel.objects.get(id = request.user.id)
            user.delete()
            return {"data":None,"message":messages.USER_DELETED,"status":200}
        except UserModel.DoesNotExist:
            return {"data":None,"message":"User Does not exist","status":400}


    # def social_login(self, request):
    #         social_login_id = request.data.get('social_login_id')
    #         social_login_type = request.data.get('social_login_type')
    #         email = request.data.get('email', None)
    #         phone_no = request.data.get('phone_no', None)
    #         if not social_login_id or not social_login_type:
    #             return {"data": None, "message": "Social login ID and type are required", "status": 400}
    #         try:
    #             user = UserModel.objects.get(social_login_id=social_login_id, social_login_type=social_login_type)
    #         except UserModel.DoesNotExist:
    #             if email:
    #                 user, created = UserModel.objects.get_or_create(email=email)
    #             elif phone_no:
    #                 user, created = UserModel.objects.get_or_create(phone_no=phone_no)
    #             else:
    #                 user = UserModel()
    #                 created = True
    #             user.social_login_id = social_login_id
    #             user.social_login_type = social_login_type
    #             user.is_active = True
    #             user.profile_status = 1
    #             user.save()
    #         if user.profile_status >= 1:
    #             give_token = True
    #             user.email_verification = True
    #             user.encoded_id = " "
    #             user.save()
    #             serializer = userSerializer.GetUserSerializer(user, context = {"give_token": give_token})
    #             user_details = serializer.data
    #             return {"data": user_details, "message": "SOCIAL LOGIN SUCCESSFUL", "status": 200}


    