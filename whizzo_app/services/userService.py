from re import search
from tabnanny import check
from rest_framework import status
from whizzo_app.models.userModel import UserModel
from whizzo_app.models.testimonialModel import TestimonialModel
from whizzo_app.models.subscriptionModel import SubscriptionModel
from whizzo_app.utils import messages, otp, sendMail
from whizzo_app.serializers import userSerializer,adminSerializer
from django.contrib.auth.hashers import check_password
from datetime import datetime
from threading import Thread
import pytz
from whizzo_app.models.customerSupportModel import CustomerSupportModel
from whizzo_app.services.categoryService import generate_file_name

class UserService:
    def user_registration(self, request):
        otp = sendMail.generate_otp()
        email = request.data.get("email")
        password = request.data.get("password")
        phone_no = request.data.get("phone_no")
        country_code = request.data.get("country_code")
        country_name = request.data.get("country_name")
        if "@" not in email or ".com" not in email:
            return {"data": None, "message": messages.WRONG_EMAIL, "status": 400}
        if "email" in request.data:
            check_user = UserModel.objects.filter(email = email , role=2)
            if check_user.exists() and check_user.first().profile_status > 1 :
                return {"data": None, "message": messages.EMAIL_ALREADY_EXISTS, "status": 400}
            elif check_user.exists() and check_user.first().profile_status == 1 :
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
                if user.is_deleted is True:
                    return {"data": None, "message": "Your account is temporarily blocked by admin", "status": 400}
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
                # role =request.data.get("role")
                # if role ==2:
                    # user = UserModel.objects.get(email=request.data["email"],role=role)
                # else:
                user = UserModel.objects.get(email =request.data["email"])
            elif "phone_no" in request.data:
                # role =request.data.get("role")
                # if role ==2:
                    # user = UserModel.objects.get(email=request.data["phone_no"],role=role)
                # else:
                user = UserModel.objects.get(email =request.data["phone_no"])
            else:
                return {"data": None, "message": "Email or phone number not provided", "status": 400}
        except UserModel.DoesNotExist:
            return {"data": None, "message": messages.USER_NOT_FOUND, "status": 400}
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
        return {"data": user_serializer.data, "message":  "OTP verified successfully", "status": 200}
    def resend_otp(self, request):
        otp = sendMail.generate_otp()
        try:
            if "email" in request.data:
                # role =request.data.get("role")
                # if role ==2:
                user = UserModel.objects.get(email=request.data["email"])
                # else:
                    # user = UserModel.objects.filter(email =request.data["email"]).exclude(role=2).first()
                Thread(target=sendMail.send_otp_to_mail, args=[request.data["email"], otp, user.username]).start()
                # Thread(target=sendMail.send_otp_to_mail, args=[request.data["email"], otp]).start()
            elif "phone_no" in request.data:
                # role =request.data.get("role")
                # if role ==2:
                    # user = UserModel.objects.get(email=request.data["phone_no"],role=role)
                # else:
                user = UserModel.objects.filter(email =request.data["phone_no"])
            else:
                return {"data": None, "message": "Email or phone number not provided", "status": 400}
        except UserModel.DoesNotExist:
            return {"data": None, "message": messages.USER_NOT_FOUND, "status": 400}
        user.otp_sent_time = datetime.now(tz=pytz.UTC)
        user.otp = otp
        user.save()
        return {"data": None, "message":  "OTP sent successfully", "status": 200}
    def change_password(self, request):
        try:
            user = UserModel.objects.get(id=request.user.id)
        except UserModel.DoesNotExist:
            return {
                "data": None,
                "message":  messages.USER_NOT_FOUND,
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
                "message": "Password changed successfully.",
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
                # role =request.data.get("role")
                # if role ==2:
                user = UserModel.objects.get(email=request.data["email"])
                # else:
                    # user = UserModel.objects.filter(email =request.data["email"]).exclude(role=2).first()
            else:
                return {"data": None, "message": "Email not provided", "status": 400}
        except UserModel.DoesNotExist:
            return {"data": None, "message":  messages.USER_NOT_FOUND, "status": 400}
        # Thread(target=sendMail.send_otp_to_mail, args=[request.data["email"], otp]).start()
        Thread(target=sendMail.send_otp_to_mail, args=[ request.data["email"], otp,user.username]).start()
        user.otp_sent_time= datetime.now(tz=pytz.UTC)
        user.otp = otp
        user.save()
        return {"data": None, "message":  "Otp sent successfully", "status": status.HTTP_200_OK}
    def reset_password(self, request):
        try:
            # role =request.data.get("role")
            # if role ==2:
            user = UserModel.objects.get(email=request.data["email"])
            # else:
                # user = UserModel.objects.filter(email =request.data["email"]).exclude(role=2).first()
        except UserModel.DoesNotExist:
            return {
                "data": None,
                "message":  messages.USER_NOT_FOUND,
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
        print(request.data,"=================payload=========")
        EMAIL_CHANGED = False
        check_email = UserModel.objects.filter(email=request.data["email"])
        if request.user.email != request.data["email"]:
            EMAIL_CHANGED = True
            if check_email:
                return {'data': None, 'message': messages.EMAIL_ALREADY_EXISTS, 'status': 400}
        try:
            user  = UserModel.objects.get(id = request.user.id)
            if request.data.get("profile_picture"):
                serializer = userSerializer.updateUserSerializer(user,data=request.data, context={"user_profile":request.data["profile_picture"],"purpose":request.data["purpose"]})
                if serializer.is_valid():
                    serializer.save(profile_picture_id=request.data["profile_picture"], purpose_id=request.data["purpose"])
                    if user.profile_status==2:
                        user.profile_status = 3
                        user.save()
                    return {"data": serializer.data, "message": "Profile updated successfully", "status": 200}
            else:
                serializer = userSerializer.updateWithoutPPUserSerializer(user,data=request.data, context={"purpose":request.data["purpose"]})
                if serializer.is_valid():
                    serializer.save( purpose_id=request.data["purpose"])
                if user.profile_status==2:
                    user.profile_status = 3
                    user.save()
                return {"data": serializer.data, "EMAIL_CHANGED": EMAIL_CHANGED, "message": "Profile updated successfully", "status": 200}
        except Exception as e:
            return {"data": str(e), "message": "Something went wrong", "status": 400}
        
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


    def send_query_to_admin(self, request):
        customer_support = CustomerSupportModel.objects.create(
            customer_id=request.user.id,  
            username=request.data["fullname"],
            queries=request.data["query"],
        )
        return {"data": "", "message": "Query sent to admin successfully", "status": 200}
    


    def get_all_testimonial_for_user(self, request):
        try:
            Testimonial_obj = TestimonialModel.objects.all()
        except TestimonialModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer = adminSerializer.GetTestimonialSerializer(Testimonial_obj, many=True)
        serialized_data = serializer.data
        return {'data': serialized_data, 'message': messages.FETCH, 'status': 200}

    def get_all_subscriptions_for_user(self, request):
        try:
            subscription = SubscriptionModel.objects.all()
        except SubscriptionModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer = adminSerializer.GetSubscriptionSerializer(subscription, many=True)
        serialized_data = serializer.data
        return {'data': serialized_data, 'message': messages.FETCH, 'status': 200}

    def send_otp_to_new_mail(self, request):
        OTP = otp.generate_otp()
        check_email = UserModel.objects.filter(email=request.data["email"], role=2)
        if check_email:
            return {'data': None, 'message': messages.EMAIL_ALREADY_EXISTS, 'status': 400}
        try:
            user = UserModel.objects.get(id=request.user.id)
            Thread(target=sendMail.send_otp_to_mail, args=(request.data["email"], OTP)).start()
            user.otp = OTP
            user.otp_sent_time = datetime.now(tz=pytz.UTC)
            user.save()
            return {'data': None, 'message': messages.OTP_SENT_AFTER_REGISTRATION, 'status': 200}
        except Exception as err:
            return {'data': str(err), 'message': messages.WENT_WRONG, 'status': 400}

    def verify_new_mail_otp(self, request):
        try:
            user = UserModel.objects.get(id=request.user.id)
            if user.otp == request.data["otp"]:
                return {'data': None, 'message': messages.OTP_VERIFIED, 'status': 200}
            elif user.otp != request.data["otp"]:
                return {'data': None, 'message': messages.WRONG_OTP, 'status': 400}
        except:
            return {'data': None, 'message': messages.WENT_WRONG, 'status': 400}

    def word_to_pdf(self, request):
        import random
        import os
        from whizzo_app.models.fileConversionModel import FileConversationModel
        import tempfile
        from docx import Document
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet
        from docx2pdf import convert
        from whizzo_app.utils.saveImage import save_file_conversion
        from whizzo_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
        from django.core.files.uploadedfile import UploadedFile
        import win32com.client

        word_file: UploadedFile = request.FILES.get("word_file")
        if not word_file:
            return {"message": "No Word file provided", "status": 400}
        
        OUTPUT_FILE_NAME = generate_file_name(word_file.name)[0] + ".pdf"

        # Generate unique file names
        file_name = "".join((word_file.name).split(" "))
        base_name = f"output_{random.randint(10000, 99999)}"
        temp_dir = tempfile.gettempdir()
        input_word_file = os.path.join(temp_dir, f"{base_name}.docx")
        output_pdf_file = os.path.join(f"{base_name}.pdf")

        # Save the uploaded Word file temporarily
        with open(input_word_file, 'wb') as f:
            for chunk in word_file.chunks():
                f.write(chunk)

        # Convert Word to PDF using win32com.client
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            doc = word.Documents.Open(input_word_file)
            doc.SaveAs(output_pdf_file, FileFormat=17)  # 17 represents the PDF format
            doc.Close()
            word.Quit()
        except Exception as e:
            # if os.path.exists(input_word_file):
            #     os.remove(input_word_file)
            return {"message": f"Error converting Word to PDF: {e}", "status": 500}

        # Generate PDF using ReportLab
        try:
            document = Document(input_word_file)
            content = [paragraph.text for paragraph in document.paragraphs]
            doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
            styles = getSampleStyleSheet()
            paragraphs = [Paragraph(text, styles["Normal"]) for text in content]
            doc.build(paragraphs)
        except Exception as e:
            if os.path.exists(input_word_file):
                os.remove(input_word_file)
            if os.path.exists(output_pdf_file):
                os.remove(output_pdf_file)
            return {"message": f"Error generating PDF: {e}", "status": 500}

        # Handle the converted PDF
        try:
            SAVED_FILE_RESPONSE = save_file_conversion(output_pdf_file, OUTPUT_FILE_NAME, "application/pdf")
            data = {
                "media_url": SAVED_FILE_RESPONSE[0],
                "media_type": "pdf",
                "media_name": SAVED_FILE_RESPONSE[1]
            }
            serializer = CreateUpdateUploadMediaSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            save_file_in_model = FileConversationModel.objects.create(
                user_id=request.user.id,
                converted_media_id=serializer.data["id"],
                sub_category=11
            )
        finally:
            # Clean up temporary files
            if os.path.exists(input_word_file):
                os.remove(input_word_file)
            if os.path.exists(output_pdf_file):
                os.remove(output_pdf_file)

        return {"data": data, "message": "done", "status": 200}