from whizzo_app.utils import messages
from whizzo_app.serializers import adminSerializer, userSerializer
from whizzo_app.models import AbilityModel, AchievementModel, SubjectModel, SubRoleModel, UserModel, PermissionModel, PurposeModel, FeaturesModel, ModuleModel, \
    SubscriptionModel, FaqModel, CmsModel
from whizzo_app.utils.customPagination import CustomPagination
from whizzo_app.utils.otp import generate_password
from whizzo_app.utils.sendMail import SendOtpToMail
from django.contrib.auth.hashers import check_password
from django.utils import timezone
import pytz
from datetime import datetime

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
            serializer = adminSerializer.AddAdminSerializer(user, context = {"give_login_token": give_login_token})
            return {"data": serializer.data, "message": messages.USER_LOGGED_IN, "status": 200}
        else:
            return {"data": None, "message": messages.PASSWORD_WRONG, "status": 400}

    def get_admin_profile(self, request):
        user = UserModel.objects.get(id = request.user.id)
        serializer = adminSerializer.GetAdminSerializer(user)
        return {"data": serializer.data, "message": "USER_DETAILS", "status": 200}    
    
    def edit_admin_profile(self, request):
        try:
            user_obj=UserModel.objects.get(id=request.user.id)
        except UserModel.DoesNotExist:
            return {"data": None, "message": "NOT_FOUND", "status": 400}
        serializer=adminSerializer.GetAdminSerializer(user_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message":"Profile updated successfully", "status": 200}
        return {"data": None, "message": serializer.errors, "status": 400}

    def verify_admin_otp(self, request):
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
        otp_sent_time = user.otp_sent_time
        if otp_sent_time is not None:
            otp_duration = (now - otp_sent_time).seconds
            if otp_duration > 60:
                return {"data": None, "message": messages.OTP_EXPIRED, "status": 400}
        else:
            return {"data": None, "message": "OTP not sent yet", "status": 400}
        
        if user.otp != request.data["otp"]:
            return {"data": None, "message":  messages.WRONG_OTP, "status": 400}
        else:
            GIVE_LOGIN_TOKEN=True
        
        user.save()
        user_serializer = adminSerializer.AddAdminSerializer(user, context={"give_login_token": GIVE_LOGIN_TOKEN})    
        return {"data": user_serializer.data, "message":  "OTP_VERIFIED", "status": 200}
# dashboard

    def dashboard_data(self, request):
        data={}
        data["total user"]=UserModel.objects.filter(role=2).count()
        data["total subscription"]=0
        data["total revenue"]=0
        return {"data": data, "message":messages.FETCH, "status": 200}
    

    def get_admin_user_graph_data(self, request, format=None):
        # interval = request.data.get("interval")
        now = timezone.now()

        filtered_users = UserModel.objects.filter(role=2)
        # if not interval:
        current_year = now.year
        start_date = timezone.datetime(current_year, 1, 1).date()
        end_date = now.date()
        date_counts = {}

        current_date = start_date
        while current_date <= end_date:
            count = filtered_users.filter(created_at__year=current_year, created_at__month=current_date.month).count()
            date_counts[current_date.strftime("%Y-%m")] = count
            current_date = current_date.replace(month=current_date.month + 1)
        
        # Organize data into label and value arrays
        labels = list(date_counts.keys())
        values = list(date_counts.values())
        
        return {"labels": labels, "values": values, 'message': messages.FETCH,"status": 200}

# manage user

    def get_all_user_admin(self, request):
        sub_obj = UserModel.objects.filter(role=2).order_by("created_at")
        pagination_obj = CustomPagination()
        search_keys = ["first_name__icontains", "email__icontains"]
        result = pagination_obj.custom_pagination(request, search_keys, adminSerializer.GetAdminManageUserSerializer, sub_obj)
        return{'data': result,'message':  messages.FETCH, 'status': 200}

    def get_manage_user_by_id(self,request, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return {"data":None,"message": 'NOT_FOUND', "status": 400}
        serializer = adminSerializer.GetAdminManageUserSerializer(user)
        return {"data": serializer.data,"message": 'FETCH', "status": 200}


    def update_manage_user_by_id(self,request,user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return {"data":None,"message": 'NOT_FOUND', "status": 400}
        serializer = adminSerializer.UpdateAdminManageUserSerializer(user, data=request.data )
        print(serializer)
        if serializer.is_valid():
            serializer.save()
        return {"data": serializer.data,"message": 'FETCH', "status": 200}
    
    def edit_manage_user_status(self, request, id):
        try:   
            user = UserModel.objects.get(id=id)
            serializer=adminSerializer.EditManageUserStatusSerializer(user,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message": "Updated successfully", "status": 200}
            return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}

    def delete_manage_users_by_id(self,request, user_id):
        try:
            user_obj = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return {"data": None,"message": 'NOT_FOUND', "status": 404}
        user_obj.delete()
        return {"message": 'USER_DELETED', "status": 200}
    
# testimonial
    
    
# purpose
    
    def add_purpose(self, request):
        serializer = adminSerializer.PurposeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message":" ADDED", "status": 201}
        return {"data": None, "message": serializer.errors, "status": 400}
    
    def get_purpose(self, request, purpose_id):
        try:
            purpose = PurposeModel.objects.get(id=purpose_id)
        except PurposeModel.DoesNotExist:
            return {"data": None, "message": "NOT_FOUND", "status": 400}
        serializer = adminSerializer.PurposeSerializer(purpose)
        return {"data": serializer.data, "message": "DETAILS", "status": 200}
    
    def update_purpose(self, request, purpose_id):
        try:
            purpose = PurposeModel.objects.get(id=purpose_id)
        except PurposeModel.DoesNotExist:
            return {"data": None, "message":"NOT_FOUND", "status": 400}
        serializer = adminSerializer.PurposeSerializer(purpose, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message": "UPDATED", "status": 200}
        return {"data": None, "message": serializer.errors, "status": 400}
    
    def delete_purpose(self, request, purpose_id):
        try:
            address = PurposeModel.objects.get(id=purpose_id)
        except PurposeModel.DoesNotExist:
            return {"data": None, "message": "NOT_FOUND", "status": 400}
        address.delete()
        return {"data": None, "message": "DELETED", "status": 200}
    
    def get_all_purpose(self, request):
        purpose = PurposeModel.objects.all()
        serializer = adminSerializer.PurposeSerializer(purpose, many=True)
        return {"data": serializer.data, "message": "DETAILS", "status": 200}

#features

    def add_features(self, request):
        try:
            serializer=adminSerializer.FeatureModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data,"message": 'FEATURE_ADDED', "status": 200}
            return {"data": serializer.errors,"message": 'WENT_WRONG', "status": 200}
        except Exception as e:
            return {"error": str(e),"message": 'INTERNAL_SERVER_ERROR', "status": 200}
        
    def get_all_features(self, request):
        try:
            faqs_obj = FeaturesModel.objects.filter(is_active=True).order_by("created_at")
            serializer = adminSerializer.FaqModelSerializer(faqs_obj, many=True)
            return {'data': serializer.data, 'message': "FETCH", "status": 200}
        except FeaturesModel.DoesNotExist:
            return {"data": None, "message": 'NOT_FOUND', "status": 400} 

# subscription

    def add_subscription(self, request):
        serializer = adminSerializer.SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message": "ADDED", "status": 201}
        return {"data": None, "message": serializer.errors, "status": 400}
    
    def get_subscription(self, request, subscription_id):
        try:
            subscription = SubscriptionModel.objects.get(id=subscription_id)
        except SubscriptionModel.DoesNotExist:
            return {"data": None, "message": "NOT_FOUND", "status": 400}
        serializer = adminSerializer.SubscriptionSerializer(subscription)
        return {"data": serializer.data, "message": "DETAILS", "status": 200}
    
    def update_subscription(self, request, subscription_id):
        try:
            subscription = SubscriptionModel.objects.get(id=subscription_id)
        except SubscriptionModel.DoesNotExist:
            return {"data": None, "message": "NOT_FOUND", "status": 400}
        serializer = adminSerializer.SubscriptionSerializer(subscription, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": serializer.data, "message": "UPDATED", "status": 200}
        return {"data": None, "message": serializer.errors, "status": 400}
    
    def delete_subscription(self, request, subscription_id):
        try:
            subscription = SubscriptionModel.objects.get(id=subscription_id)
        except SubscriptionModel.DoesNotExist:
            return {"data": None, "message": "NOT_FOUND", "status": 400}
        subscription.delete()
        return {"data": None, "message": "DELETED", "status": 200}
    
    def get_all_subscriptions(self, request):
        try:
            subscription = SubscriptionModel.objects.all()
        except SubscriptionModel.DoesNotExist:
            return {"data": None, "message": "NOT_FOUND", "status": 400}
        serializer = adminSerializer.SubscriptionSerializer(subscription, many=True)
        return {"data": serializer.data, "message": "DETAILS", "status": 200}

# ability
    def add_ability(self, request):
        try:   
            data={
                "question":request.data.get("question"),
                "answer_option":request.data.get("answer_option",[])
            }
            serializer=adminSerializer.CreateAbilitySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message": messages.ABILITY_ADDED, "status": 200}
            return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        


    def update_ability(self, request, id):
        try:   
            data={
                "question":request.data.get("question"),
                "answer_option":request.data.get("answer_option",[])
            }
            ability_obj = AbilityModel.objects.get(id=id)
            serializer=adminSerializer.CreateAbilitySerializer(ability_obj, data=data)
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
            serializer=adminSerializer.CreateSubjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message": messages.SUBJECT_ADDED, "status": 200}
            return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        
    def edit_status_subject(self, request, id):
        try:   
            sub_obj = SubjectModel.objects.get(id=id)
            serializer=adminSerializer.EditSubjectSerializer(sub_obj,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message": messages.SUBJECT_UPDATED, "status": 200}
            return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
    
    def get_all_subject(self, request):
        try:   
            sub_obj = SubjectModel.objects.all()
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer=adminSerializer.GetSubjectSerializer(sub_obj,many=True)
        return {"data": serializer.data, "message": messages.FETCH, "status": 200}
    

    def delete_subject(self, request, id):
        try:
            sub_obj = SubjectModel.objects.get(id=id)
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        sub_obj.delete()
        return {"data": None, "message": messages.SUBJECT_DELETED, "status": 200}
        
# achievement

    def add_achievement(self, request):
        try:   
            data={
                "question":request.data.get("question"),
                "subject":request.data.get("subject"),
                "answer_option":request.data.get("answer_option",[])
            }
            serializer=adminSerializer.CreateAcheivementSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message": messages.ACHIEVEMENT_ADDED, "status": 200}
            return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}
        except:
            return {"data": None, "message": messages.RECORD_NOT_FOUND, "status": 400}
        


    def update_achievement(self, request, id):
        try:   
            data={
                "question":request.data.get("question"),
                "subject":request.data.get("subject"),
                "answer_option":request.data.get("answer_option",[])
            }
            achievement_obj = AchievementModel.objects.get(id=id)
            serializer=adminSerializer.CreateAcheivementSerializer(achievement_obj, data=data)
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
    

# sub admin

    def add_role_sub_admin(self, request):
        try:
            serializer=adminSerializer.CreateRoleSubAdminSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data,"message": messages.ROLE_ADDED, "status": 200}
            return {"data": serializer.errors,"message": messages.WENT_WRONG, "status": 400}
        except Exception as e:
            return {"error": str(e),"message": messages.RECORD_NOT_FOUND, "status":400}
        

    def get_role_sub_admin(self,request):
        try:
            role_obj = SubRoleModel.objects.order_by("created_at")
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
            role_obj = ModuleModel.objects.order_by("created_at")
        except ModuleModel.DoesNotExist:
            return {"data":None,"message": messages.RECORD_NOT_FOUND, "status": 400}
        serializer = adminSerializer.CreateModuleSubAdminSerializer(role_obj, many=True)
        return {"data": serializer.data,"message": messages.FETCH, "status": 200}
    

    def add_sub_admin(self, request):
        try:
            data = request.data
            user_serializer = adminSerializer.CreateSubAdminSerializer(data=data)
            if user_serializer.is_valid():
                user_data = user_serializer.save()
                # password=generate_password()
                password="123456"
                user_data.set_password(password)
                user_data.save()
                SendOtpToMail(password, [user_data.email]).run()
                for i in request.data['role_permission']:
                    role_serializer = adminSerializer.CreateRolePermissionSubAdminSerializer(data=i)
                    if role_serializer.is_valid():
                        save_role_permission = role_serializer.save(user_id = user_serializer.data['id'])
                        # save_role_permission.user = user_serializer.data['id']
                        save_role_permission.save()
                    else:
                        return {'data':role_serializer.errors, 'status':400}    
                return {'data':request.data, 'message': messages.SUB_ADMIN_CREATED,'status':200}
            return {'data':user_serializer.errors,"message": messages.WENT_WRONG,'status':400}
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
        sub_obj = UserModel.objects.filter(role=3).order_by("created_at")
        pagination_obj = CustomPagination()
        search_keys = ["username__icontains", "email__icontains"]
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
        return {"data": serializer.data,"message": messages, "status": 200}


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
                return {"data": serializer.data,"message": 'FAQ_ADDED', "status": 200}
            return {"data": serializer.errors,"message": 'WENT_WRONG', "status": 200}
        except Exception as e:
            return {"error": str(e),"message": 'INTERNAL_SERVER_ERROR', "status": 200}
        
  
    

    def get_all_faqs(self, request):
        try:
            faqs_obj = FaqModel.objects.filter(is_active=True).order_by("created_at")
            serializer = adminSerializer.FaqModelSerializer(faqs_obj, many=True)
            return {'data': serializer.data, 'message': "FETCH", "status": 200}
        except FaqModel.DoesNotExist:
            return {"data": None, "message": 'NOT_FOUND', "status": 400}


    def faq_details_by_id(self, request,faq_id):
        try:
            faq = FaqModel.objects.get(id=faq_id)
            serializer = adminSerializer.FaqModelSerializer(faq)
            return {"data": serializer.data, "message":  'FETCH', "status": 200}
        except FaqModel.DoesNotExist:
            return {"data": None, "message": 'NOT_FOUND', "status": 404}
        except Exception as e:
            return {"data": None, "message":  'INTERNAL_SERVER_ERROR', "status": 500}
        
    def update_faq(self, request,faq_id):
        try:
            faq = FaqModel.objects.get(id=faq_id)
            serializer = adminSerializer.FaqModelSerializer(faq, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return {"data": serializer.data, "message":  "FAQ_UPDATED", "status": 200}
            else:
                return {"data": serializer.errors, "message":  'WENT_WRONG', "status": 400}
        except FaqModel.DoesNotExist:
            return {"data": None, "message":  'NOT_FOUND', "status": 404}
        except Exception as e:
            return {"data": None, "message": 'INTERNAL_SERVER_ERROR', "status": 500}
        
    def delete_faq(self, request, faq_id):
        try:
            faq = FaqModel.objects.get(id=faq_id)
            faq.delete()
            return {"data": None, "message": "FAQ_DELETED", "status": 200}
        except FaqModel.DoesNotExist:
            return {"data": None, "message": 'NOT_FOUND', "status": 404}
        except Exception as e:
            return {"data": None, "message":  'INTERNAL_SERVER_ERROR', "status": 500}
        


# notification

    
# cms
    def contatct_support(self, request):
        try:
            cms_obj=CmsModel.objects.get(id=1)
            serializer=adminSerializer.AddContactSupportSerializer(cms_obj,data=request.data)
        except:
            serializer=adminSerializer.AddContactSupportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {"data": None, "message": "FAQ_DELETED", "status": 200}

        