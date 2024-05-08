from rest_framework.views import APIView
from rest_framework.response import Response
from whizzo_app.services.adminService import AdminService
from rest_framework.permissions import AllowAny



admin_obj=AdminService()

class LoginAdminView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = admin_obj.login_admin(request)
        return Response(result, status=result["status"])

class GetAdminDetailByTokenView(APIView):
    def get(self, request):
        result = admin_obj.get_admin_profile(request)
        return Response(result, status=result["status"])

class UpdateAdminProfileView(APIView):
    def put(self, request):
        result = admin_obj.edit_admin_profile(request)
        return Response(result, status=result["status"])


class CreateAbilityView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = admin_obj.add_ability(request)
        return Response(result, status=result["status"])
    
class UpdateAbilityView(APIView):
    permission_classes = [AllowAny]
    def put(self, request,id):
        result = admin_obj.update_ability(request, id)
        return Response(result, status=result["status"])
    
class DeleteAbilityView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request,id):
        result = admin_obj.delete_ability(request, id)
        return Response(result, status=result["status"])



class CreateAchievementView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = admin_obj.add_achievement(request)
        return Response(result, status=result["status"])
    
class UpdateAchievementView(APIView):
    permission_classes = [AllowAny]
    def put(self, request,id):
        result = admin_obj.update_achievement(request, id)
        return Response(result, status=result["status"])
    
class DeleteAchievementView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request,id):
        result = admin_obj.delete_achievement(request, id)
        return Response(result, status=result["status"])
    


class CreateSubjectView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = admin_obj.add_subject(request)
        return Response(result, status=result["status"])
    
class GetAllSubjectView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = admin_obj.get_all_subject(request)
        return Response(result, status=result["status"])
    
class UpdateSubjectStatusView(APIView):
    permission_classes = [AllowAny]
    def put(self, request,id):
        result = admin_obj.edit_status_subject(request, id)
        return Response(result, status=result["status"])
    
class DeleteSubjectView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request,id):
        result = admin_obj.delete_subject(request, id)
        return Response(result, status=result["status"])
    


class CreateSubRoleView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = admin_obj.add_role_sub_admin(request)
        return Response(result, status=result["status"])
    
class GetAllSubRoleView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = admin_obj.get_role_sub_admin(request)
        return Response(result, status=result["status"])
    
class CreateModuleView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = admin_obj.add_module_sub_admin(request)
        return Response(result, status=result["status"])
    
class GetAllModuleView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = admin_obj.get_module_sub_admin(request)
        return Response(result, status=result["status"])

class CreateSubAdminView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = admin_obj.add_sub_admin(request)
        return Response(result, status=result["status"])
    
class UpdateSubAdnibView(APIView):
    permission_classes = [AllowAny]
    def put(self, request,id):
        result = admin_obj.update_sub_admin_by_id(request, id)
        return Response(result, status=result["status"])
    
class GetAllSubAdminView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = admin_obj.get_all_sub_admin(request)
        return Response(result, status=result["status"])
    
class GetSubAdminByIdView(APIView):
    permission_classes = [AllowAny]
    def get(self, request,id):
        result = admin_obj.get_sub_admin_by_id(request, id)
        return Response(result, status=result["status"])
    
class UpdateSubAdminStatusView(APIView):
    permission_classes = [AllowAny]
    def put(self, request,id):
        result = admin_obj.edit_sub_admin_status_by_id(request, id)
        return Response(result, status=result["status"])
    
class DeleteSubAdminView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request,id):
        result = admin_obj.delete_sub_admin_by_id(request, id)
        return Response(result, status=result["status"])
    

class AddPurposeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = admin_obj.add_purpose(request)
        return Response(result, status=result["status"])
    
class GetPurposeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, purpose_id):
        result = admin_obj.get_purpose(request, purpose_id)
        return Response(result, status=result["status"])
    
class UpdatePurposeView(APIView):
    permission_classes = [AllowAny]
    def put(self, request, purpose_id):
        result = admin_obj.update_purpose(request, purpose_id)
        return Response(result, status=result["status"])
    
class DeletePurposeView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, purpose_id):
        result = admin_obj.delete_purpose(request, purpose_id)
        return Response(result, status=result["status"])
    
class GetAllPurposeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = admin_obj.get_all_purpose(request)
        return Response(result, status=result["status"])
    

class AddFeaturesView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = admin_obj.add_features(self,request)
        return Response(result)
    
class GetAllFeaturesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = admin_obj.get_all_features(request)
        return Response(result, status=result["status"])
    

class AddSubscriptionView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = admin_obj.add_subscription(request)
        return Response(result, status=result["status"])

class GetSubscriptionView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, subscription_id):
        result = admin_obj.get_subscription(request, subscription_id)
        return Response(result, status=result["status"])

class UpdateSubscriptionView(APIView):
    permission_classes = [AllowAny]
    def put(self, request, subscription_id):
        result = admin_obj.update_subscription(request, subscription_id)
        return Response(result, status=result["status"])

class DeleteSubscriptionView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, subscription_id):
        result = admin_obj.delete_subscription(request, subscription_id)
        return Response(result, status=result["status"])

class GetAllSubscriptionsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = admin_obj.get_all_subscriptions(request)
        return Response(result, status=result["status"])
    


class AddFaqView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = admin_obj.add_faqs(self,request)
        return Response(result)
    
class GetAllFaqView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = admin_obj.get_all_faqs(self,request)
        return Response(result)
    
class FaqDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self,request,faq_id):
        result=admin_obj.faq_details_by_id(request,faq_id)
        return Response(result)
    
class UpdateFaqView(APIView):
    permission_classes = [AllowAny]
    def put(self, request,faq_id):
        result = admin_obj.update_faq(self,request,faq_id)
        return Response(result)
    
class DeleteFaqView(APIView):
    permission_classes = [AllowAny]
    def delete(self,request,faq_id):
        result=admin_obj.delete_faq(self,request,faq_id)
        return Response(result)