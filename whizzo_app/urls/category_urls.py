from django.urls import path
from whizzo_app.views import categoryView

urlpatterns = [
    ##### testing ######
    path("testing/", categoryView.GenerateTestingCategoryResponseView.as_view()),
    path("testing/pdf/", categoryView.GenerateTestingCategoryResponseViewPdf.as_view()),
    path("testing/result/", categoryView.SubmitTestAndUpdateResultView.as_view()),
    path("testing/past-tests/", categoryView.TestingCategoryPastListingView.as_view()),

    ### file summarization ###
    path("file/summarization/", categoryView.FileSummarizationView.as_view()),
    path("file/history/", categoryView.FileSummaryHistoryView.as_view()),
    path("file/<int:file_id>/", categoryView.GetSummaryByIdView.as_view()),

    #### file conversions ####
    path("conversion/pdf-to-word/", categoryView.PdfToWordView.as_view()),
    path("conversion/word-to-pdf/", categoryView.ConvertWordToPdfView.as_view()),
    path("conversion/pdf-to-excel/", categoryView.ConvertPdfToExcelView.as_view()),

    path("conversion/excel-to-pdf/", categoryView.ConvertExcelToPdfView.as_view()),
    path("conversion/pdf-to-image/", categoryView.ConvertPdfToImageView.as_view()),
    path("conversion/image-to-pdf/", categoryView.ConvertImageToPdfView.as_view()),
    path("conversion/ppt-to-pdf/", categoryView.ConvertPptToPdfView.as_view()),

    #### Notes ####
    path("convert-voice-to-text/", categoryView.ConvertVoiceToTextView.as_view()),
    path("create-notes/", categoryView.CreateNotesView.as_view()),
    path("get-ai-explanation/", categoryView.GetAiExplanation.as_view()),
    path("change-language/", categoryView.ChangeLanguageNoteView.as_view()),
    path("get-all-listing-notes/", categoryView.GetAllListingNotesView.as_view()),
    path("get-notes-by-id/<int:id>/", categoryView.GetListingNotesByIdView.as_view()),
    path("send-notes-via-mail/",categoryView.SendNotesViaMale.as_view()),

    #### research ####
    path("get-research-answer/", categoryView.GetResearchAnswerView.as_view()),
    path("get-all-listing-research/", categoryView.GetAllResearchView.as_view()),
    path("get-research-by-id/<int:id>/", categoryView.GetResearchByIdView.as_view()),

    #### assignment ####
    path("get-assignmnet-answer/", categoryView.GetAssignmentSolutionView.as_view()),
    path("fetch-all-assignment/",categoryView.GetAllAssginmentView.as_view()),
    path("update-assignment/<int:id>/", categoryView.updateAssignmentView.as_view()),
    path("get-assignment/<int:id>/",categoryView.GetAssigmentByIdView.as_view()),

    ##### setting app  ######
    path("get-faq-app-list/", categoryView.GetFaqListView.as_view()),
    path("get-terms-condition-app/", categoryView.GetTermsConditionAppView.as_view()),
    path("delete-user-app/", categoryView.DeleteUserAppView.as_view()),
    

    # #### articles #####
    path("get-articles-response/", categoryView.GetArticlesView.as_view()),



    ####common for all #####

    path("send-file-to-mail/",categoryView.SendFileToMailByToken.as_view()),

]




