from whizzo_app.views import userView
from django.urls import path

urlpatterns = [
    path("registration/", userView.UserRegistrationView.as_view()),
    path("login/", userView.UserLogInView.as_view()),
    path("verify-otp/", userView.VerifyOtpView.as_view()),
]