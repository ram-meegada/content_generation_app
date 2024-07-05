from django.urls import path
from whizzo_app.views import adminView


urlpatterns = [
    path("admin-login/", adminView.LoginAdminView.as_view()),
    path("get-admin-detail/", adminView.GetAdminDetailByTokenView.as_view()),
    path("update-admin-profile/", adminView.UpdateAdminProfileView.as_view()),
    path("verify-admin-otp/", adminView.VerifyAdminOtpView.as_view()),
    
    path("get-dashboard-data/", adminView.GetDashboardDataView.as_view()),
    path("get-dashboard-user-graph-data/", adminView.GetDashboardUserGraphDataView.as_view()),

    path("get-all-manage-user/", adminView.GetAllManageUserView.as_view()),
    path("get-manage-user/<int:id>/", adminView.GetManageUserByIdView.as_view()),
    path("update-manage-user/<int:id>/", adminView.UpdateManageUserView.as_view()),
    path("update-manage-user-status/<int:id>/", adminView.UpdateManageUserStatusView.as_view()),
    path("delete-manage-user/<int:id>/", adminView.DeleteManageUserView.as_view()),
    
    path("add-ability/", adminView.CreateAbilityView.as_view()),
    path("update-ability/<int:id>/", adminView.UpdateAbilityView.as_view()),
    path("delete-ability/<int:id>/", adminView.DeleteAbilityView.as_view()),
    path("get-all-ability/",adminView.GetAllAbilityView.as_view()),
    path("get-abiity-by-id/<int:id>/",adminView.GetAbilityByIdView.as_view()),
    path("ability/pdf/", adminView.GenerateAbilityQuestionsFromPDFViewPdf.as_view()),


    path("add-achievement/", adminView.CreateAchievementView.as_view()),
    path("update-achievement/<int:id>/", adminView.UpdateAchievementView.as_view()),
    path("delete-achievement/<int:id>/", adminView.DeleteAchievementView.as_view()),
    path("get-all-achievement/",adminView.GetAllAchivementVeiw.as_view()),
    path("get-achievement-by-id/<int:id>/",adminView.GetAllAchivementByIdVeiw.as_view()),


    path("add-subject/", adminView.CreateSubjectView.as_view()),
    path("get-all-subject/", adminView.GetAllSubjectView.as_view()),
    path("update-subject/<int:id>/", adminView.UpdateSubjectStatusView.as_view()),
    path("delete-subject/<int:id>/", adminView.DeleteSubjectView.as_view()),

    path("add-sub-role/", adminView.CreateSubRoleView.as_view()),
    path("update-role/<int:role_id>/", adminView.UpdateRoleView.as_view()),
    path("get-all-sub-role/", adminView.GetAllSubRoleView.as_view()),

    path("add-module/", adminView.CreateModuleView.as_view()),
    path("get-all-module/", adminView.GetAllModuleView.as_view()),
    path("delete-role/<int:id>/",adminView.DeleteRoleView.as_view()),

    path("add-sub-admin/", adminView.CreateSubAdminView.as_view()),
    path("update-subadmin/<int:id>/", adminView.UpdateSubAdnibView.as_view()),
    path("get-all-subadmin/", adminView.GetAllSubAdminView.as_view()),
    path("get-subadmin-by-id/<int:id>/", adminView.GetSubAdminByIdView.as_view()),
    path("update-subadmin-status-by-id/<int:id>/", adminView.UpdateSubAdminStatusView.as_view()),
    path("delete-subadmin/<int:id>/", adminView.DeleteSubAdminView.as_view()),

    path("add-features/",adminView.AddFeaturesView.as_view()),
    path("get-all-features/",adminView.GetAllFeaturesView.as_view()),

    path('add-subscription/', adminView.AddSubscriptionView.as_view()),
    path('get-subscription/<int:subscription_id>/', adminView.GetSubscriptionView.as_view()),
    path('update-subscription/<int:subscription_id>/', adminView.UpdateSubscriptionView.as_view()),
    path('delete-subscription/<int:subscription_id>/', adminView.DeleteSubscriptionView.as_view()),
    path('get-all-subscriptions/', adminView.GetAllSubscriptionsView.as_view()),

    path('add-purpose/', adminView.AddPurposeView.as_view()),
    path('get-purpose/<int:purpose_id>/', adminView.GetPurposeView.as_view()),
    path('update-purpose/<int:purpose_id>/', adminView.UpdatePurposeView.as_view()),
    path("update-purpose-status-by-id/<int:purpose_id>/", adminView.UpdatePurposeStatusView.as_view()),
    path('delete-purpose/<int:purpose_id>/', adminView.DeletePurposeView.as_view()),
    path('get-all-purpose/', adminView.GetAllPurposeView.as_view()),
    path('get-all-purpose-listing/', adminView.GetAllPurposeListingView.as_view()),
    

    path("add-faq/",adminView.AddFaqView.as_view()),
    path("get-all-faq/",adminView.GetAllFaqView.as_view()),
    path("faq-detail/<int:faq_id>/",adminView.FaqDetailView.as_view()),
    path("faq-update/<int:faq_id>/",adminView.UpdateFaqView.as_view()),
    path("faq-delete/<int:faq_id>/",adminView.DeleteFaqView.as_view()),

    path("add-contact-suport/",adminView.AddContactSupportView.as_view()),
    path("add-privacy-policy/",adminView.AddPrivacyPolicyView.as_view()),
    path("add-terms-condition/",adminView.AddTermsConditionView.as_view()),
    path("add-about-us/",adminView.AddAboutUsView.as_view()),
    path("arabic-cms/",adminView.AddArabicValues.as_view()),
    path("get-cms-detail/",adminView.GetCmsDetailView.as_view()),

    path('add-testimonial/', adminView.AddTestimonialView.as_view()),
    path('get-testimonial/<int:id>/', adminView.GetTestimonialView.as_view()),
    path('update-testimonial/<int:id>/', adminView.UpdateTestimonialView.as_view()),
    path("update-testimonial-status-by-id/<int:id>/", adminView.UpdateTestimonialStatusView.as_view()),
    path('delete-testimonial/<int:id>/', adminView.DeleteTestimonialView.as_view()),
    path('get-all-testimonial/', adminView.GetAllTestimonialView.as_view()),

    path("all-queries/", adminView.AllQueryView.as_view()),
    path("revert-query/<int:cs_id>/", adminView.RevertQueryByIdView.as_view()),
    path("delete-query/<int:cs_id>/", adminView.DeleteQueryByIdView.as_view()),


    path("add/notification/", adminView.AddNotificationView.as_view()),
    path("users-listing-for-notification/", adminView.UsersListingView.as_view()),
    path("all-notifications/", adminView.AllNotificationView.as_view()),
    path("delete-notification/<int:id>/", adminView.DeleteNotificationByIdView.as_view()),

    path("csv-users/",adminView.ExportUsersCsvView.as_view()),
    path("customers-queries-csv/", adminView.CustomerSupportCSV.as_view()),

]