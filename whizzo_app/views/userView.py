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

class VerifyOtpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = user_obj.verify_otp(request)
        return Response(result, status=result["status"])