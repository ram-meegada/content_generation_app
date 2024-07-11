from django.http import HttpResponse
from whizzo_app.utils import messages
from whizzo_app.serializers import adminSerializer, userSerializer
from whizzo_app.models import AbilityModel, AchievementModel, SubjectModel,NotificationModel, SubRoleModel, CustomerSupportModel, UserModel, PermissionModel, PurposeModel, FeaturesModel, ModuleModel, \
    SubscriptionModel, FaqModel, CmsModel, TestimonialModel,CategoryModel
from whizzo_app.utils.customPagination import CustomPagination
from whizzo_app.utils.otp import generate_password
from whizzo_app.utils.sendMail import SendOtpToMail
from django.contrib.auth.hashers import check_password
from django.utils import timezone
import pytz
from whizzo_app.services import categoryService
import csv
from io import StringIO
from whizzo_project import settings
import json
from datetime import datetime, timedelta
from whizzo_app.utils.saveImage import save_file_conversion_csv
from whizzo_app.utils.sendMail import send_notification_to_mail
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from io import BytesIO
from PyPDF2 import PdfReader
import textwrap
import string
import urllib.request as urlopener
from PyPDF2 import PdfReader
from io import BytesIO
import calendar
from dateutil.relativedelta import relativedelta
import pandas as pd
from django.core.files.uploadedfile import InMemoryUploadedFile
from whizzo_app.services.uploadMediaService import UploadMediaService

class AdminService:
# onboarding
    def login_admin(self, request):
        

        email = request.data["email"]
        password = request.data["password"]
        try:
            user = UserModel.objects.get(email = email, role__in=[1,3])
        except UserModel.DoesNotExist:
            return {"data": None, "message": messages.EMAIL_NOT_FOUND, "status": 400}
        
        verify_password = check_password(password, user.password)
        if verify_password:
            give_login_token = True
            serializer = adminSerializer.loginAdminSerializer(user, context = {"give_login_token": give_login_token})
            return {"data": serializer.data, "message": messages.USER_LOGGED_IN, "status": 200}
        else:
            return {"data": None, "message": messages.PASSWORD_WRONG, "status": 400}

    def get_admin_profile(self, request):
        user = UserModel.objects.get(id = request.user.id)
        serializer = adminSerializer.GetAdminSerializer(user)
        return {"data": serializer.data, "message": messages.FETCH, "status": 200}    
    
    def edit_admin_profile(self, request):
        try:
            user_obj=UserModel.objects.get(id=request.user.id)
        except UserModel.DoesNotExist:
            return {"data": None, "message": messages.USER_NOT_FOUND, "status": 400}
        serializer=adminSerializer.UpdateAdminSerializer(user_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message":messages.UPDATED_SUCCESSFULLY, "status": 200}
        return {"data": None, "message": serializer.errors, "status": 400}

    def verify_admin_otp(self, request):
        GIVE_LOGIN_TOKEN = False
        try:
            role =request.data.get("role")
            if "email" in request.data:
                if role ==2:
                    user = UserModel.objects.get(email=request.data["email"],role=role)
                else:
                    user = UserModel.objects.filter(email =request.data["email"]).exclude(role=2).first()
            elif "phone_number" in request.data:
                user = UserModel.objects.get(phone_no=request.data["phone_number"])
            else:
                return {"data": None, "message": messages.EMAIL_PHONE_NOT_FOUND, "status": 400}
        except UserModel.DoesNotExist:
            return {"data": None, "message": messages.USER_NOT_FOUND, "status": 400}
        
        now = datetime.now(tz=pytz.UTC)
        otp_sent_time = user.otp_sent_time
        if otp_sent_time is not None:
            otp_duration = (now - otp_sent_time).seconds
            if otp_duration > 60:
                return {"data": None, "message": messages.OTP_EXPIRED, "status": 400}
        else:
            return {"data": None, "message": messages.OTP_NOT_SENT, "status": 400}
        
        if user.otp != request.data["otp"]:
            return {"data": None, "message":  messages.WRONG_OTP, "status": 400}
        else:
            GIVE_LOGIN_TOKEN=True
        
        user.save()
        user_serializer = adminSerializer.AddAdminSerializer(user, context={"give_login_token": GIVE_LOGIN_TOKEN})    
        return {"data": user_serializer.data, "message": messages.OTP_VERIFIED, "status": 200}
# dashboard

    def dashboard_data(self, request):
        data={}
        data["total user"]=UserModel.objects.filter(role=2).count()
        data["total subscription"]=0
        data["total revenue"]=0
        return {"data": data, "message":messages.FETCH, "status": 200}
    

    def get_admin_user_graph_data(self, request, format=None):
        interval = request.GET.get("interval")
        filtered_users = UserModel.objects.filter(role=2)
        result = {}
        TODAY_DATETIME = datetime.now()
        YEAR = TODAY_DATETIME.year
        MONTH = TODAY_DATETIME.month
        if interval == "1":
            start_date = TODAY_DATETIME - timedelta(days=TODAY_DATETIME.weekday()+1)
            for i in range(7):
                filtered_users_count = filtered_users.filter(created_at__date=start_date).count()
                result[datetime.strftime(start_date, "%a")] = filtered_users_count
                start_date += timedelta(days=1)
        elif interval == "2":
            starting_dates = list(self.extract_month_dates(YEAR, MONTH))
            for idx, value in enumerate(starting_dates):
                filtered_users_count = filtered_users.filter(created_at__gte=value, created_at__lte=value+timedelta(days=7)).count()
                result[f"week{idx+1}"] = filtered_users_count
        elif interval == "3":
            for i in range(1, 13):
                filtered_users_count = filtered_users.filter(created_at__year=YEAR, created_at__month=i).count()
                result[datetime.strftime(datetime(YEAR, i, 1), "%b")] = filtered_users_count
        elif interval == "4":
            year = TODAY_DATETIME
            for i in range(10):
                year_label = year.year
                filtered_users_count = filtered_users.filter(created_at__year=year_label).count()
                result[str(year_label)] = filtered_users_count
                year -= relativedelta(years=1)
        return {'data': result, 'message': messages.FETCH, "status": 200}
    
    def get_revenue_graph_data(self, request, format=None):
        interval = request.GET.get("interval")
        if interval == "1":
            result = {'Sun': 0, 'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0}
        elif interval == "2":
            result = {'week1': 0, 'week2': 0, 'week3': 0, 'week4': 0, 'week5': 0}    
        elif interval == "3":
            result = {'Jan': 0, 'Feb': 0, 'Mar': 0, 'Apr': 0, 'May': 0, 'Jun': 0, 'Jul': 0, 'Aug': 0, 'Sep': 0, 'Oct': 0, 'Nov': 0, 'Dec': 0}
        elif interval == "4":
            result = {'2024': 0, '2023': 0, '2022': 0, '2021': 0, '2020': 0, '2019': 0, '2018': 0, '2017': 0, '2016': 0, '2015': 0}    
        return {'data': result, 'message': messages.FETCH, "status": 200}

    def get_subscription_graph_data(self, request, format=None):
        interval = request.GET.get("interval")
        if interval == "1":
            result = {'Sun': 0, 'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0}
        elif interval == "2":
            result = {'week1': 0, 'week2': 0, 'week3': 0, 'week4': 0, 'week5': 0}    
        elif interval == "3":
            result = {'Jan': 0, 'Feb': 0, 'Mar': 0, 'Apr': 0, 'May': 0, 'Jun': 0, 'Jul': 0, 'Aug': 0, 'Sep': 0, 'Oct': 0, 'Nov': 0, 'Dec': 0}
        elif interval == "4":
            result = {'2024': 0, '2023': 0, '2022': 0, '2021': 0, '2020': 0, '2019': 0, '2018': 0, '2017': 0, '2016': 0, '2015': 0}    
        return {'data': result, 'message': messages.FETCH, "status": 200}

    def extract_month_dates(self, year, month):
        month_range = calendar.monthrange(year, month)[1]
        for i in range(1, month_range + 1, 7):
            yield datetime(year, month, i)
    
    # def revenue_graph

# manage user

    def get_all_user_admin(self, request):
        sub_obj = UserModel.objects.filter(role=2).order_by("-created_at")
        pagination_obj = CustomPagination()
        search_keys = ["first_name__icontains", "email__icontains"]
        result = pagination_obj.custom_pagination(request, search_keys, adminSerializer.GetAdminManageUserSerializer, sub_obj)
        return{'data': result,'message':  messages.FETCH, 'status': 200}

    def get_manage_user_by_id(self,request, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return {"data":None,"message": messages.USER_NOT_FOUND, "status": 400}
        serializer = adminSerializer.GetAdminManageUserSerializer(user)
        return {"data": serializer.data,"message": messages.FETCH, "status": 200}


    def update_manage_user_by_id(self,request,user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return {"data":None,"message": messages.USER_NOT_FOUND, "status": 400}
        serializer = adminSerializer.UpdateAdminManageUserSerializer(user, data=request.data )
        if serializer.is_valid():
            serializer.save()
        return {"data": serializer.data,"message": messages.USER_UPDATED, "status": 200}
    
    def edit_manage_user_status(self, request, id):
        try:   
            user = UserModel.objects.get(id=id)
            serializer=adminSerializer.EditManageUserStatusSerializer(user,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message": messages.UPDATED, "status": 200}
            return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}

    def delete_manage_users_by_id(self,request, user_id):
        try:
            user_obj = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return {"data": None,"message": messages.USER_NOT_FOUND, "status": 404}
        user_obj.is_deleted = True
        return {"data": None,"message": messages.USER_DELETED, "status": 200}
    
# testimonial
    def add_testimonial(self, request):
        check_email = TestimonialModel.objects.filter(email=request.data["email"])
        if check_email.exists():
            return {"data": None, "message": messages.TESTIMONIAL_EMAIL_ALREADY_EXISTS, "status": 400}

        serializer = adminSerializer.TestimonialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message":messages.TESTIMONIAL_ADDED, "status": 201}
        else:
            return {"data": None, "message": serializer.errors, "status": 400}
    
    def get_testimonial(self, request, id):
        try:
            testimonial_obj = TestimonialModel.objects.get(id=id)
        except TestimonialModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer = adminSerializer.GetTestimonialSerializer(testimonial_obj)
        return {"data": serializer.data, "message": messages.FETCH, "status": 200}
    
    def update_testimonial(self, request, id):
        try:
            testimonial_obj = TestimonialModel.objects.get(id=id)
        except TestimonialModel.DoesNotExist:
            return {"data": None, "message":messages.RECORD_NOT_FOUND, "status": 400}
        serializer = adminSerializer.TestimonialSerializer(testimonial_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message": messages.TESTIMONIAL_UPDATED, "status": 200}
        return {"data": None, "message": serializer.errors, "status": 400}
    
    def edit_testimonial_status_by_id(self,request, id):
        try:
            sub_obj = TestimonialModel.objects.get(pk=id)
        except TestimonialModel.DoesNotExist:
            return {"data":None,"message": messages.RECORD_NOT_FOUND, "status": 404}
        serializer = adminSerializer.GeteditTestimonialStatusSerializer(sub_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return {"data": serializer.data,"message": messages.TESTIMONIAL_UPDATED, "status": 200}
    
    def delete_testimonial(self, request, id):
        try:
            address = TestimonialModel.objects.get(id=id)
        except TestimonialModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        address.delete()
        return {"data": None, "message": messages.TESTIMONIAL_DELETED, "status": 200}
    
    def get_all_testimonial(self, request):
        Testimonial_obj = TestimonialModel.objects.all().order_by("-created_at")
        pagination_obj = CustomPagination()
        search_keys = ["first_name__icontains"]
        result = pagination_obj.custom_pagination(request, search_keys, adminSerializer.GetTestimonialSerializer, Testimonial_obj)
        return{'data': result,'message':  messages.FETCH, 'status': 200}
    
# purpose
    
    def add_purpose(self, request):
        serializer = adminSerializer.PurposeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message":messages.PURPOSE_ADDED, "status": 201}
        return {"data": None, "message": serializer.errors, "status": 400}
    
    def get_purpose(self, request, purpose_id):
        try:
            purpose = PurposeModel.objects.get(id=purpose_id)
        except PurposeModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer = adminSerializer.PurposeSerializer(purpose)
        return {"data": serializer.data, "message": messages.FETCH, "status": 200}
    
    def update_purpose(self, request, purpose_id):
        try:
            purpose = PurposeModel.objects.get(id=purpose_id)
        except PurposeModel.DoesNotExist:
            return {"data": None, "message":messages.RECORD_NOT_FOUND, "status": 400}
        serializer = adminSerializer.PurposeSerializer(purpose, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message": messages.PURPOSE_UPDATED, "status": 200}
        return {"data": None, "message": serializer.errors, "status": 400}
    
    def edit_purpose_status_by_id(self,request, purpose_id):
        try:
            if request.data["is_active"] is False and len(PurposeModel.objects.filter(is_active=True)) == 1:
                return {"data": None, "message": messages.ACTION_RESTRICTED, "status": 400}
            sub_obj = PurposeModel.objects.get(pk=purpose_id)
        except PurposeModel.DoesNotExist:
            return {"data":None,"message": messages.RECORD_NOT_FOUND, "status": 404}
        serializer = adminSerializer.GeteditpurposeStatusSerializer(sub_obj,request.data)
        if serializer.is_valid():
            serializer.save()
        return {"data": serializer.data,"message": messages.PURPOSE_UPDATED, "status": 200}
    
    def delete_purpose(self, request, purpose_id):
        try:
            if len(PurposeModel.objects.filter(is_active=True)) == 1:
                return {"data": None, "message": messages.ACTION_RESTRICTED, "status": 400}
            address = PurposeModel.objects.get(id=purpose_id)
        except PurposeModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        address.delete()
        return {"data": None, "message": messages.PURPOSE_DELETED, "status": 200}
    
    def get_all_purpose(self, request):
        purpose_obj = PurposeModel.objects.all().order_by("-created_at")
        pagination_obj = CustomPagination()
        search_keys = ["name__icontains"]
        result = pagination_obj.custom_pagination(request, search_keys, adminSerializer.PurposeSerializer, purpose_obj)
        return{'data': result,'message':  messages.FETCH, 'status': 200}
    
    def get_purpose_listing(self, request):
        try:
            purpose = PurposeModel.objects.all()
        except PurposeModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer = adminSerializer.PurposeSerializer(purpose, many=True)
        return {"data": serializer.data, "message": messages.FETCH, "status": 200}

#features

    def add_features(self, request):
        try:
            serializer=adminSerializer.FeatureModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data,"message": messages.FEATURE_ADDED, "status": 200}
            return {"data": serializer.errors,"message": messages.WENT_WRONG, "status": 400}
        except Exception as e:
            return {"error": str(e),"message": messages.WENT_WRONG, "status": 400}
        
    def get_all_features(self, request):
        try:
            faqs_obj = FeaturesModel.objects.filter(is_active=True).order_by("-created_at")
            serializer = adminSerializer.FaqModelSerializer(faqs_obj, many=True)
            return {'data': serializer.data, 'message': messages.FETCH, "status": 200}
        except FeaturesModel.DoesNotExist:
            return {"data": None, "message": messages.WENT_WRONG, "status": 400} 

# subscription

    def add_subscription(self, request):
        serializer = adminSerializer.SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message": messages.SUBSCRIPTION_ADDED, "status": 201}
        return {"data": None, "message": serializer.errors, "status": 400}
    
    def get_subscription(self, request, subscription_id):
        try:
            subscription = SubscriptionModel.objects.get(id=subscription_id)
        except SubscriptionModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer = adminSerializer.GetSubscriptionSerializer(subscription)
        return {"data": serializer.data, "message": messages.FETCH, "status": 200}
    
    def update_subscription(self, request, subscription_id):
        try:
            subscription = SubscriptionModel.objects.get(id=subscription_id)
        except SubscriptionModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer = adminSerializer.SubscriptionSerializer(subscription, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message": messages.SUBSCRIPTION_UPDATED, "status": 200}
        return {"data": None, "message": serializer.errors, "status": 400}
    
    def delete_subscription(self, request, subscription_id):
        try:
            subscription = SubscriptionModel.objects.get(id=subscription_id)
        except SubscriptionModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        subscription.delete()
        return {"data": None, "message": messages.SUBSCRIPTION_DELETED, "status": 200}
    
    def get_all_subscriptions(self, request):
        try:
            subscription = SubscriptionModel.objects.all().order_by("-created_at")
        except SubscriptionModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        pagination_obj = CustomPagination()
        search_keys = ["plan_type__icontains"]
        result = pagination_obj.custom_pagination(request, search_keys, adminSerializer.GetSubscriptionSerializer, subscription)
        return {"data":result,"message":messages.FETCH,"status":200}


# ability

    def get_all_ability(self, request):
        try:
            data = AbilityModel.objects.all().order_by("-created_at")
            pagination_obj = CustomPagination()
            search_keys = ["question__icontains", "answer_option__icontains"]
            result = pagination_obj.custom_pagination(request, search_keys, adminSerializer.CreateAbilitySerializer, data)
            return {"data":result,"message":messages.FETCH,"status":200}
        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG,"status":400}
        

    def get_ability_by_id(self, request, id):
        try:
            data = AbilityModel.objects.get(id = id)
            serializer = adminSerializer.CreateAbilitySerializer(data)
            return {"data":serializer.data,"message":messages.FETCH,"status":200}
        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG,"status":400}
        
    def add_ability(self, request):
        try:   
            # data={
            #     "question":request.data.get("question"),
            #     "answer_option":request.data.get("answer_option",[]),
            #     "correct_answer":request.data.get("corect_answer"),
            #     "is_mcq":request.data.get("is_mcq")
            # }
            question = request.data.get("question")
            is_mcq = request.data.get("is_mcq")
            if AbilityModel.objects.filter(question=question, is_mcq=is_mcq).exists():
                return {"data": None, "message": "Ability with this question and value's already exists", "status": 400}

            serializer=adminSerializer.CreateAbilitySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message": messages.ABILITY_ADDED, "status": 200}
            return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        


    def update_ability(self, request, id):
        try:   
            # data={
            #     "question":request.data.get("question"),
            #     "answer_option":request.data.get("answer_option",[])
            # }
            ability_obj = AbilityModel.objects.get(id=id)
            serializer=adminSerializer.CreateAbilitySerializer(ability_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message": messages.ABILITY_UPDATED, "status": 200}
            return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        

    def delete_ability(self, request, id):
        try:
            ability_obj = AbilityModel.objects.get(id=id)
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        ability_obj.delete()
        return {"data": None, "message": messages.ABILITY_DELETED, "status": 200}

# subject
   
    def add_subject(self, request):
        try:   
            if SubjectModel.objects.filter(subject_name__iexact=request.data["subject_name"]):
                return {"data": None, "message": messages.SUBJECT_EXISTS, "status": 400}
            serializer=adminSerializer.CreateSubjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message": messages.SUBJECT_ADDED, "status": 200}
            return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}
        except Exception as err:
            return {"data": str(err), "message": messages.WENT_WRONG, "status": 400}
        
    def edit_status_subject(self, request, id):
        try:   
            sub_obj = SubjectModel.objects.get(id=id)
            if AchievementModel.objects.filter(subject=sub_obj.id).exists():
                return {"data": None, "message": messages.SUBJECT_CANNOT_DELETED, "status": 400}
            serializer=adminSerializer.EditSubjectSerializer(sub_obj,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message": messages.SUBJECT_UPDATED, "status": 200}
            return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}
        except Exception as err:
            return {"data": str(err), "message": messages.WENT_WRONG, "status": 400}
    
    def get_all_subject(self, request):
        try:   
            sub_obj = SubjectModel.objects.all().order_by("-created_at")
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        pagination_obj = CustomPagination()
        search_keys = ["subject_name__icontains",]
        result = pagination_obj.custom_pagination(request, search_keys, adminSerializer.GetSubjectSerializer, sub_obj)
        return {"data":result,"message":messages.FETCH,"status":200}

    def delete_subject(self, request, id):
        try:
            sub_obj = SubjectModel.objects.get(id=id)
            if AchievementModel.objects.filter(subject=sub_obj.id).exists():
                return {"data": None, "message": messages.SUBJECT_CANNOT_DELETED, "status": 400}
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        if AchievementModel.objects.filter(subject=sub_obj.id).exists():
            return {"data": None, "message": "This action cannot be done.", "status": 400}
        sub_obj.delete()
        return {"data": None, "message": messages.SUBJECT_DELETED, "status": 200}
        
# achievement

    def add_achievement(self, request):
        try:   
            # data={
            #     "question":request.data.get("question"),
            #     "subject":request.data.get("subject"),
            #     "answer_option":request.data.get("answer_option",[])
            # }
            subject_id = request.data.get("subject")     
            question = request.data.get("question")
            if AchievementModel.objects.filter(question=question, subject_id=subject_id).exists():
                return {"data": None, "message": "This combination of question and subject already exists.", "status": 400}
   
            if not SubjectModel.objects.filter(id=subject_id, is_active=True).exists():
                return {"data": None, "message": "Subject is inactive or does not exist", "status": 400}
        
            serializer=adminSerializer.CreateAcheivementSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message": messages.ACHIEVEMENT_ADDED, "status": 200}
            return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        


    def update_achievement(self, request, id):
        try:   
            # data={
            #     "question":request.data.get("question"),
            #     "subject":request.data.get("subject"),
            #     "answer_option":request.data.get("answer_option",[])
            # }
            achievement_obj = AchievementModel.objects.get(id=id)
            serializer=adminSerializer.CreateAcheivementSerializer(achievement_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message": messages.ACHIEVEMENT_UPDATED, "status": 200}
            return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        

    def delete_achievement(self, request, id):
        try:
            achievement_obj = AchievementModel.objects.get(id=id)
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        achievement_obj.delete()
        return {"data": None, "message": messages.ACHIEVEMENT_DELETED, "status": 200}
    
    def get_all_achievement(self, request):
        try:
            data = AchievementModel.objects.all().order_by("-created_at")
            pagination_obj = CustomPagination()
            search_keys = [ "question__icontains","corect_answer__icontains"]
            result = pagination_obj.custom_pagination(request, search_keys, adminSerializer.CreateAcheivementSerializer, data)
            return {"data":result,"message":messages.FETCH,"status":200}
        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG,"status":400}
        

    def get_achievement_by_id(self, request, id):
        try:
            data = AchievementModel.objects.get(id = id)
            serializer = adminSerializer.CreateAcheivementSerializer(data)
            return {"data":serializer.data,"message":messages.FETCH,"status":200}
        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG,"status":400}
    

# sub admin

    def add_role_sub_admin(self, request):
        try:
            if SubRoleModel.objects.filter(role_name__iexact=request.data["role_name"].lower()).exists():
                return {"data": None,"message": messages.ROLE_EXISTS, "status": 400}
            serializer=adminSerializer.CreateRoleSubAdminSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data,"message": messages.ROLE_ADDED, "status": 200}
            return {"data": serializer.errors,"message": messages.WENT_WRONG, "status": 400}
        except Exception as e:
            return {"error": str(e),"message": messages.WENT_WRONG, "status":400}

    def update_role(self, request, role_id):
        try:
            role = SubRoleModel.objects.get(id=role_id)
        except SubRoleModel.DoesNotExist:
            return {"data": None, "message":messages.RECORD_NOT_FOUND, "status": 400}
        serializer = adminSerializer.CreateRoleSubAdminSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message": messages.ROLE_UPDATED, "status": 200}
        return {"data": None, "message": serializer.errors, "status": 400}        



    def get_role_sub_admin(self,request):
        try:
            role_obj = SubRoleModel.objects.order_by("-created_at")
        except SubRoleModel.DoesNotExist:
            return {"data":None,"message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer = adminSerializer.CreateRoleSubAdminSerializer(role_obj, many=True)
        return {"data": serializer.data,"message": messages.FETCH, "status": 200}
    
    def add_module_sub_admin(self, request):
        try:
            serializer=adminSerializer.CreateModuleSubAdminSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data,"message": messages.MODULE_ADDED, "status": 200}
            return {"data": serializer.errors,"message": messages.WENT_WRONG, "status": 400}
        except Exception as e:
            return {"error": str(e),"message": messages.RECORD_NOT_FOUND, "status":400}
        

    def get_module_sub_admin(self,request):
        try:
            role_obj = ModuleModel.objects.all().order_by("id")
            serializer = adminSerializer.CreateModuleSubAdminSerializer(role_obj, many=True)
            return {"data": serializer.data,"message": messages.FETCH, "status": 200}
        except ModuleModel.DoesNotExist:
            return {"data":None,"message": messages.RECORD_NOT_FOUND, "status": 400}
            
    def delete_role(self, request, id):
        try:
            user = SubRoleModel.objects.get(id=id)
            user.delete()
            return {"data":None,"message":messages.ROLE_DELETE,"status":200}
        except Exception as e:
            return {"data":None,"message":messages.WENT_WRONG,"status":400}    

    def add_sub_admin(self, request):
        try:
            data = request.data
            if UserModel.objects.filter(email=data["email"]).first():
                return {'data': None, 'message': "Email already taken", 'status': 400}

            user_serializer = adminSerializer.CreateSubAdminSerializer(data=data)

            if user_serializer.is_valid():
                user_data = user_serializer.save()
                # password=generate_password()
                password="Test@123"
                user_data.set_password(password)
                user_data.save()
                SendOtpToMail(password, [user_data.email]).start()
                for i in request.data['role_permission']:
                    role_serializer = adminSerializer.CreateRolePermissionSubAdminSerializer(data=i)
                    if role_serializer.is_valid():
                        save_role_permission = role_serializer.save(user_id = user_serializer.data['id'])
                        # save_role_permission.user = user_serializer.data['id']
                        save_role_permission.save()
                    else:
                        return {'data':role_serializer.errors, 'status':400}    
                return {'data':request.data, 'message': messages.SUB_ADMIN_CREATED,'status':200}
            else:
                return {'data': user_serializer.errors, 'message': "Something went wrong",'status':400}
        except Exception as e:
            return {"error": str(e),"message": messages.INTERNAL_SERVER_ERROR, "status": 500}
        
    def update_sub_admin_by_id(self, request, sub_admin_id):
        user = UserModel.objects.filter(id = sub_admin_id).first()
        if not user:
            return {'data':None, "message": messages.RECORD_NOT_FOUND, 'status':404}
        try:
            data = {**request.data}
            role_permission_data = data.pop("role_permission")
            user_serializer = adminSerializer.CreateSubAdminSerializer(user, data=data)
            if user_serializer.is_valid():
                user_data = user_serializer.save()
                for i in role_permission_data:
                    try:
                        get_permission = PermissionModel.objects.get(id = i["id"])
                        role_serializer = adminSerializer.CreateRolePermissionSubAdminSerializer(get_permission, data=i)
                    except:
                        role_serializer = adminSerializer.CreateRolePermissionSubAdminSerializer(data=i)
                    if role_serializer.is_valid():
                        save_role_permission = role_serializer.save(user_id = user.id)
                    else:
                        return {'data':role_serializer.errors, 'status':400}    
                return {'data':request.data, 'message': messages.SUB_ADMIN_UPDATED,'status':200}
            return {'data':user_serializer.errors,"message": messages.WENT_WRONG,'status':400}
        except Exception as e:
            return {"error": str(e),"message": messages.INTERNAL_SERVER_ERROR, "status": 500}



    def get_all_sub_admin(self, request):
        sub_obj = UserModel.objects.filter(role=3).order_by("-created_at")
        pagination_obj = CustomPagination()
        search_keys = ["username__icontains","name__icontains","email__icontains"]
        result = pagination_obj.custom_pagination(request, search_keys, adminSerializer.GetSubAdminSerializer, sub_obj)
        return{'data': result,'message':  messages.FETCH, 'status': 200}
    

    def get_sub_admin_by_id(self,request, sub_admin_id):
        
        try:
            sub_obj = UserModel.objects.get(pk=sub_admin_id)
        except UserModel.DoesNotExist:
            return {"data":None,"message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer = adminSerializer.GetSubAdminSerializer(sub_obj)
        return {"data": serializer.data,"message": messages.FETCH, "status": 200}

    def edit_sub_admin_status_by_id(self,request, sub_admin_id):
        try:
            sub_obj = UserModel.objects.get(pk=sub_admin_id)
        except UserModel.DoesNotExist:
            return {"data":None,"message": messages.RECORD_NOT_FOUND, "status": 404}
        serializer = adminSerializer.GeteditSubAdminSerializer(sub_obj,request.data)
        if serializer.is_valid():
            serializer.save()
        return {"data": serializer.data,"message": messages.SUB_ADMIN_UPDATED, "status": 200}


    def delete_sub_admin_by_id(self,request, sub_admin_id):
        try:
            sub_obj = UserModel.objects.get(pk=sub_admin_id)
        except UserModel.DoesNotExist:
            return {"data":None,"message": messages.RECORD_NOT_FOUND, "status": 404}
        sub_obj.delete()
        return {"data": None,"message": messages.SUB_ADMIN_DELETED, "status": 200}
    

# faq 

    def add_faqs(self, request):
        try:
            serializer=adminSerializer.FaqModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data,"message": messages.FAQ_ADDED, "status": 200}
            return {"data": serializer.errors,"message": messages.WENT_WRONG, "status": 200}
        except Exception as e:
            return {"error": str(e),"message": messages.INTERNAL_SERVER_ERROR, "status": 200}
        
  
    

    def get_all_faqs(self, request):
        try:
            faqs_obj = FaqModel.objects.filter(is_active=True).order_by("-created_at")
            pagination_obj = CustomPagination()
            search_keys = ["question__icontains"]
            result = pagination_obj.custom_pagination(request, search_keys, adminSerializer.FaqModelSerializer, faqs_obj)
            return{'data': result,'message':  messages.FETCH, 'status': 200}
        except FaqModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}


    def faq_details_by_id(self, request,faq_id):
        try:
            faq = FaqModel.objects.get(id=faq_id)
            serializer = adminSerializer.FaqModelSerializer(faq)
            return {"data": serializer.data, "message":  messages.FETCH, "status": 200}
        except FaqModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 404}
        except Exception as e:
            return {"data": None, "message": messages.INTERNAL_SERVER_ERROR, "status": 500}
        
    def update_faq(self, request,faq_id):
        try:
            faq = FaqModel.objects.get(id=faq_id)
            serializer = adminSerializer.FaqModelSerializer(faq, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message":  messages.FAQ_UPDATED, "status": 200}
            else:
                return {"data": serializer.errors, "message":  messages.WENT_WRONG, "status": 400}
        except FaqModel.DoesNotExist:
            return {"data": None, "message":  messages.RECORD_NOT_FOUND, "status": 404}
        except Exception as e:
            return {"data": None, "message": messages.INTERNAL_SERVER_ERROR, "status": 500}
        
    def delete_faq(self, request, faq_id):
        try:
            faq = FaqModel.objects.get(id=faq_id)
            faq.delete()
            return {"data": None, "message": messages.FAQ_DELETED, "status": 200}
        except FaqModel.DoesNotExist:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 404}
        except Exception as e:
            return {"data": None, "message":  messages.INTERNAL_SERVER_ERROR, "status": 500}
        


# notification

    
# cms
    def contatct_support(self, request):
        try:
            cms_obj = CmsModel.objects.first()
            if not cms_obj:
                serializer = adminSerializer.AddContactSupportSerializer(data=request.data)
            else:
                serializer = adminSerializer.AddContactSupportSerializer(cms_obj, data=request.data)
        except Exception as e:
            return {"data": None, "message": str(e), "status": 400}
        if serializer.is_valid():
            serializer.save()
            message = "Contact support created successfully " if not cms_obj else "Contact support updated successfully"
            return {"data": None, "message": message, "status": 200}
        else:
            return {"data": None, "message": serializer.errors, "status": 400}


    def privacy_policy(self, request):
        try:
            cms_obj = CmsModel.objects.first()
            if not cms_obj:
                serializer = adminSerializer.AddPrivacyPolicySerializer(data=request.data)
            else:
                serializer = adminSerializer.AddPrivacyPolicySerializer(cms_obj, data=request.data)
        except Exception as e:
            return {"data": None, "message": str(e), "status": 400}
        if serializer.is_valid():
            serializer.save()
            message = "Privacy policy created successfully" if not cms_obj else "Privacy policy updated successfully"
            return {"data": None, "message": message, "status": 200}
        else:
            return {"data": None, "message": serializer.errors, "status": 400}


    def terms_conditions(self, request):
        try:
            cms_obj = CmsModel.objects.first()
            if not cms_obj:
                serializer = adminSerializer.AddTermsConditionSerializer(data=request.data)
            else:
                serializer = adminSerializer.AddTermsConditionSerializer(cms_obj, data=request.data)
        except Exception as e:
            return {"data": None, "message": str(e), "status": 400}
        if serializer.is_valid():
            serializer.save()
            message = "Terms conditions created successfully" if not cms_obj else "Terms conditions updated successfully"
            return {"data": None, "message": message, "status": 200}
        else:
            return {"data": None, "message": serializer.errors, "status": 400}


    def about_us(self, request):
        try:
            cms_obj = CmsModel.objects.first()
            if not cms_obj:
                serializer = adminSerializer.AddAboutUsSerializer(data=request.data)
            else:
                serializer = adminSerializer.AddAboutUsSerializer(cms_obj, data=request.data)
        except Exception as e:
            return {"data": None, "message": str(e), "status": 400}
        if serializer.is_valid():
            serializer.save()
            message = "about us created successfully" if not cms_obj else "about us updated successfully"
            return {"data": None, "message": message, "status": 200}
        else:
            return {"data": None, "message": serializer.errors, "status": 400}

    def add_arabic_values(self, request):
        try:
            support_data = CmsModel.objects.filter(id=1)
            if not support_data:
                serializer = adminSerializer.ArabicValueCMSSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return {"data":serializer.data,"message":messages.ADD,"status":200}
                else:
                    return {"data":None,"message":messages.WENT_WRONG,"status":400}
            else:
                support_data = CmsModel.objects.get(id=1)
                serializer = adminSerializer.ArabicValueCMSSerializer(support_data, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return {"data":serializer.data,"message":messages.ADD,"status":200}
                else:
                    return {"data":None,"message":messages.WENT_WRONG,"status":400}
        except Exception as e:
            return {"data":str(e),"message":messages.WENT_WRONG,"status":400}

        

    def get_all_cms_details(self, request):
        try:
            cms_obj = CmsModel.objects.first()
            if not cms_obj:
                return {"data": None, "message": "No CMS details found", "status": 404}

            contact_support_serializer = adminSerializer.AddContactSupportSerializer(cms_obj)
            privacy_policy_serializer = adminSerializer.AddPrivacyPolicySerializer(cms_obj)
            terms_condition_serializer = adminSerializer.AddTermsConditionSerializer(cms_obj)
            about_us_serializer = adminSerializer.AddAboutUsSerializer(cms_obj)

            data = {
                "contact_support": contact_support_serializer.data,
                "privacy_policy": privacy_policy_serializer.data,
                "terms_condition": terms_condition_serializer.data,
                "about_us": about_us_serializer.data
            }

            return {"data": data, "message": "CMS details retrieved successfully", "status": 200}
        except Exception as e:
            return {"data": None, "message": str(e), "status": 400}
        


##########CUSTOMER SUPPORT
    
    def get_all_customer_support(self,request):
        customer_support = CustomerSupportModel.objects.filter(reverted_back=request.data["reverted_back"]).order_by("-updated_at")
        pagination_obj = CustomPagination()
        search_keys = ["username__icontains", "email__icontains"]
        result = pagination_obj.custom_pagination(request, search_keys, adminSerializer.CustomerSupportListSerializer, customer_support)
        return {"data": result, "message": "retrieved successfully", "status": 200}
    
    def revert_query_by_admin(self,request,cs_id):
        try:
            query = CustomerSupportModel.objects.get(id=cs_id)
            query.answer = request.data["answer"]
            query.reverted_back = True
            query.save()
            send_notification_to_mail(query.email, "Hello user this is your response for query", request.data["answer"])
                # try:
                #     user = UserModel.objects.filter(id=faq.customer_id)
                #     try:
                #         device_tokens.append(UserSession.objects.get(user_id=user.id).device_token)
                #         for i in device_tokens:
                #             try:
                #                 push_service = FCMNotification(api_key=None)
                #                 result = push_service.notify_single_device(
                #                     registration_id=f"{i}",
                #                     message_title=request.data["title"],
                #                     message_body=request.data["message"],
                #                     )
                #             except:
                #                 pass
                #     except:
                #         pass


                # except:
                #         pass

            return {"data": request.data, "message":  "Message sent to user successfully", "status": 200}
        except CustomerSupportModel.DoesNotExist:
            return {"data": None, "message":  'NOT_FOUND', "status": 404}
        
    def delete_query_by_admin(self, request, cs_id):
        try:
            query = CustomerSupportModel.objects.get(id=cs_id)
            query.delete()
            return {"data": None, "message": "Query deleted successfully", "status": 200}
        except CustomerSupportModel.DoesNotExist:
            return {"data": None, "message":  'NOT_FOUND', "status": 400}




#=========================notification



    def add_notification_by_admin(self, request, format=None):
        try:
            notification_for = request.data["notification_for"]
            users_count = len(notification_for)
            if not notification_for:         
                notification_for = UserModel.objects.filter(role=2).values_list("email", flat=True)
                users_count = 0
            for email in request.data["notification_for"]:
                title=request.data['notification_title']
                message=request.data["notification_message"]
                
                send_notification_to_mail(email, title, message)
            NotificationModel.objects.create(title=request.data['notification_title'], message=request.data["notification_message"], notification_for=users_count)    
            return {'data':None, 'message': "Notification sent successfully", 'status':200}
        except Exception as e:
            return {'data':None, 'message':f"{e}", 'status':400}
        
    def users_listing(self, request):
        users = UserModel.objects.filter(role=2).values("first_name", "last_name", "email")
        return {'data': users, 'message': "Users listing", 'status':200}

        
    def get_all_notifications(self,request):
        notifications = NotificationModel.objects.all().order_by("-created_at")
        pagination_obj = CustomPagination()
        search_keys = ["title__icontains"]
        result = pagination_obj.custom_pagination(request, search_keys, adminSerializer.NotificationListSerializer, notifications)
        return {"data": result, "message": "retrieved successfully", "status": 200}
    

    def delete_notification_by_id(self,request, id):
        try:
            notifications = NotificationModel.objects.get(pk=id)
        except UserModel.DoesNotExist:
            return {"data": None,"message": messages.NOTIFICATION_NOT_FOUND, "status": 404}
        notifications.delete()
        return {"data": None,"message": messages.NOTIFICATION_DELETED, "status": 200}    


    def extract_text(self, file_link):
        pdf_text = ""
        with file_link.open() as f:
            pdf_stream = BytesIO(f.read())
            pdf_reader = PdfReader(pdf_stream)
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
        return pdf_text


    def generate_questions_for_ability_in_admin(self, request):
            file_link = request.FILES.get("file_link")
            try:
                result = self.gemini_solution_admin(file_link)
                if result == "Please upload valid file.":
                    return {"message": "Please upload a file which contains sufficient information.","status": 400}
                if isinstance(result, dict):
                    message = result.get('message')
                    if message == "Empty file provided.":
                        return {"message": "Empty file provided.","status": 400}
                
                final_response = ""
                try:
                    for i in range(len(result)-1, -1, -1):
                        if result[i] == "}":
                            break
                    final_response = result[result.index("["): i+1] + "]"
                    final_response = json.loads(final_response)
                except Exception as err:
                    pass
                try:
                    is_arabic = True
                    all_alphabets = string.ascii_letters 
                    first_question = final_response[0]["question"]
                    for i in first_question:
                        if i in all_alphabets:
                            is_arabic = False
                            break
                except Exception as err:

                    pass
                try:
                    for i in final_response:
                        if not i.get("answer_option"):
                            i["question_type"] = True
                        elif not i["answer_option"]:
                            i["question_type"] = True
                        elif i["answer_option"]:
                            i["question_type"] = False
                        final_data = AbilityModel.objects.create(
                            question=i["question"],
                            answer_option=i["answer_option"],
                            corect_answer=i["correct_answer"],
                            is_mcq=i["question_type"],
                            is_arabic=is_arabic  
                        )
                        final_data.save()
                except Exception as err:
                    pass         
                if not final_response:
                    return {"data": None, "message": "Please upload the file again", "status": 200}
                return {"data": final_response, "message": "Assignment solution generated successfully", "status": 200}
            except Exception as e:
                return{"data": str(e), "message": "Please upload the file again", "status": 400}
        


    def gemini_solution_admin(self, file_link):
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        text_data = self.extract_text_admin(file_link)
        if isinstance(text_data, dict):
            message = text_data.get('message')
            if message == "Empty file provided.":
                return {"message": "Empty file provided."}
        
        message = HumanMessage(
            content=[
                {"type": "text",
                    "text": "generate 20 multiple choice questions with  four different options to choose and correct answers for this document. Fomrat should be in python json list format with these keys (question , answer_option ,correct_answer(make sure the spellings remain same as here for keys ), (generate data in same language as text data(language options available english and arabic))). Make sure to keep constraint on non ascii characters.If you find that the provided data is not sufficient strictly return the output as 'Please upload valid file.'"},
                {"type": "text", "text":text_data}
            ]
        )
        response = llm.invoke([message])
        # result = self.to_markdown_admin(response.content)
        return response.content
    
    def extract_text_admin(self, file_link):
        pdf_text = ""
        with file_link.open() as f:
            pdf_stream = BytesIO(f.read())
            pdf_reader = PdfReader(pdf_stream)
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
                if isinstance(pdf_text, str) and pdf_text.strip() == "":
                    return {"message": "Empty file provided."}
        return pdf_text
    
    def export_users_graph_csv(self, request):
        try:
            interval = request.GET.get("interval")
            api_type = request.GET.get("type")
            if api_type == "1":
                filtered_users = UserModel.objects.filter(role=2)
                result = {}
                TODAY_DATETIME = datetime.now()
                YEAR = TODAY_DATETIME.year
                MONTH = TODAY_DATETIME.month
                if interval == "1":
                    start_date = TODAY_DATETIME - timedelta(days=TODAY_DATETIME.weekday()+1)
                    for i in range(7):
                        filtered_users |= filtered_users.filter(created_at__date=start_date)
                        start_date += timedelta(days=1)
                elif interval == "2":
                    starting_dates = list(self.extract_month_dates(YEAR, MONTH))
                    for idx, value in enumerate(starting_dates):
                        filtered_users |= filtered_users.filter(created_at__gte=value, created_at__lte=value+timedelta(days=7))
                elif interval == "3":
                    for i in range(1, 13):
                        filtered_users |= filtered_users.filter(created_at__year=YEAR, created_at__month=i)
                elif interval == "4":
                    year = TODAY_DATETIME
                    for i in range(10):
                        year_label = year.year
                        filtered_users |= filtered_users.filter(created_at__year=year_label)
                        year -= relativedelta(years=1)

                result = adminSerializer.GetAdminManageUserSerializer(filtered_users, many=True)        
                graph_data = result.data
            elif api_type == "2":
                graph_data = []
            elif api_type == "3":
                graph_data = []
            if not graph_data:
                return {"data": None, "message": "No data to export", "status": 400}    
            df = pd.DataFrame(graph_data)
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Users')
            excel_buffer.seek(0)
            excel_file = InMemoryUploadedFile(
                excel_buffer, 
                'media', 
                'users.xlsx', 
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                excel_buffer.getbuffer().nbytes, 
                None
            )
            upload_media_service = UploadMediaService()
            excel_upload_result = upload_media_service.create_upload_media_xl(request, excel_file)
            url = excel_upload_result['file_url']
            
            # Construct your response data
            response_data = {
                "file_urls": url,
                "messages": "Excel file uploaded successfully.",
                "status": 200
            }
            return {"data": response_data, "message": "Csv exported successfully", "status": 200}
        except Exception as err:
            return {"data": str(err), "message": messages.WENT_WRONG, "status": 400}

