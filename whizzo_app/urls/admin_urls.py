from django.urls import path
from whizzo_app.views import adminView


urlpatterns = [
    path("admin-login/", adminView.LoginAdminView.as_view()),
    path("get-admin-detail/", adminView.GetAdminDetailByTokenView.as_view()),
    path("update-admin-profile/", adminView.UpdateAdminProfileView.as_view()),
    path("verify-admin-otp/", adminView.VerifyAdminOtpView.as_view()),

    path("add-ability/", adminView.CreateAbilityView.as_view()),
    path("update-ability/<int:id>/", adminView.UpdateAbilityView.as_view()),
    path("delete-ability/<int:id>/", adminView.DeleteAbilityView.as_view()),

    path("add-achievement/", adminView.CreateAchievementView.as_view()),
    path("update-achievement/<int:id>/", adminView.UpdateAchievementView.as_view()),
    path("delete-achievement/<int:id>/", adminView.DeleteAchievementView.as_view()),

    path("add-subject/", adminView.CreateSubjectView.as_view()),
    path("get-all-subject/", adminView.GetAllSubjectView.as_view()),
    path("update-subject/<int:id>/", adminView.UpdateSubjectStatusView.as_view()),
    path("delete-subject/<int:id>/", adminView.DeleteSubjectView.as_view()),

    path("add-sub-role/", adminView.CreateSubRoleView.as_view()),
    path("get-all-sub-role/", adminView.GetAllSubRoleView.as_view()),

    path("add-module/", adminView.CreateModuleView.as_view()),
    path("get-all-module/", adminView.GetAllModuleView.as_view()),

    path("add-sub-admin/", adminView.CreateSubAdminView.as_view()),
    path("update-subadmin/<int:id>/", adminView.UpdateSubAdnibView.as_view()),
    path("get-all-subadmin/", adminView.GetAllSubAdminView.as_view()),
    path("get-subadmin-by-id/<int:id>/", adminView.GetSubAdminByIdView.as_view()),
    path("update-subadmin-status-by-id/<int:id>/", adminView.UpdateSubAdminStatusView.as_view()),
    path("delete-subadmin/<int:id>/", adminView.DeleteSubAdminView.as_view()),

    path("features/add/",adminView.AddFeaturesView.as_view()),
    path("features/get-all/",adminView.GetAllFeaturesView.as_view()),

    path('add-subscription/', adminView.AddSubscriptionView.as_view()),
    path('get-subscription/<int:subscription_id>/', adminView.GetSubscriptionView.as_view()),
    path('update-subscription/<int:subscription_id>/', adminView.UpdateSubscriptionView.as_view()),
    path('delete-subscription/<int:subscription_id>/', adminView.DeleteSubscriptionView.as_view()),
    path('get-all-subscriptions/', adminView.GetAllSubscriptionsView.as_view()),

    path('add-purpose/', adminView.AddPurposeView.as_view()),
    path('get-purpose/<int:purpose_id>/', adminView.GetPurposeView.as_view()),
    path('update-purpose/<int:purpose_id>/', adminView.UpdatePurposeView.as_view()),
    path('delete-purpose/<int:purpose_id>/', adminView.DeletePurposeView.as_view()),
    path('get-all-purpose/', adminView.GetAllPurposeView.as_view()),

    path("add/faq/",adminView.AddFaqView.as_view()),
    path("get/all-faq/",adminView.GetAllFaqView.as_view()),
    path("faq/detail/<int:faq_id>/",adminView.FaqDetailView.as_view()),
    path("faq/update/<int:faq_id>/",adminView.UpdateFaqView.as_view()),
    path("faq/delete/<int:faq_id>/",adminView.DeleteFaqView.as_view()),

]