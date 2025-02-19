from whizzo_app.views import userView
from django.urls import path

urlpatterns = [
    path("registration/", userView.UserRegistrationView.as_view()),
    path("login/", userView.UserLogInView.as_view()),
    path("logout/", userView.UserLogOutView.as_view()),
    path("verify-otp/", userView.VerifyOtpView.as_view()),
    path("resend-otp/", userView.ResendOtpView.as_view()),
    path("change-password/", userView.ChangePasswordView.as_view()),
    path("forgot-password/", userView.ForgotPasswordView.as_view()),
    path("reset-password/", userView.ResetPasswordView.as_view()),
    path("update-profile/", userView.UpdateProfileByTokenView.as_view()),
    path("user-details/", userView.UserDetailsByTokenView.as_view()),
    path("delete-user/",userView.DeleteAccountByTokenView.as_view()),

    path("send-otp-to-new-mail/", userView.SendOtpToNewMailView.as_view()),
    path("verify-new-mail/", userView.VerifyNewMailView.as_view()),
 

    #### customer support
    path("send-query/",userView.QueryToAdminView.as_view()),
    path("user-testimonial/",userView.GetAllTestimonialUserView.as_view()),
    path("user-subscription/",userView.GetAllSubscriptionUserView.as_view()),


    
]
