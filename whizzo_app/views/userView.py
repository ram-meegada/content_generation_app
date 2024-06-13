from rest_framework.views import APIView
from rest_framework.response import Response
from whizzo_app.services.userService import UserService
from rest_framework.permissions import AllowAny

user_obj = UserService()

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = user_obj.user_registration(request)
        return Response(result, status=result["status"])
    
class UserLogInView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = user_obj.login_user(request)
        return Response(result, status=result["status"])

class UserLogOutView(APIView):
    def post(self, request):
        result = user_obj.logout(request)
        return Response(result, status=result["status"])

class VerifyOtpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = user_obj.verify_otp(request)
        return Response(result, status=result["status"])

class ResendOtpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = user_obj.resend_otp(request)
        return Response(result, status=result["status"])

class ChangePasswordView(APIView):
    def post(self, request):
        result = user_obj.change_password(request)
        return Response(result, status=result["status"])

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = user_obj.forgot_password(request)
        return Response(result, status=result["status"])

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = user_obj.reset_password(request)
        return Response(result, status=result["status"])

class UpdateProfileByTokenView(APIView):
    def put(self, request):
        result = user_obj.update_profile(request)
        return Response(result, status=result["status"])

class UserDetailsByTokenView(APIView):
    def get(self, request):
        result = user_obj.user_details_by_token(request)
        return Response(result, status=result["status"])


class DeleteAccountByTokenView(APIView):
    def delete(self, request):
        result = user_obj.delete_account(request)
        return Response(result, status=result["status"])

class QueryToAdminView(APIView):
    def post(self, request):
        result = user_obj.send_query_to_admin(request)
        return Response(result, status=result["status"])
    
class GetAllTestimonialUserView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = user_obj.get_all_testimonial_for_user(request)
        return Response(result, status=result["status"])

class GetAllSubscriptionUserView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = user_obj.get_all_subscriptions_for_user(request)
        return Response(result, status=result["status"])  
