from django.urls import path
from whizzo_app.views import categoryView

urlpatterns = [
    ##### testing ######
    path("testing/generate-response/", categoryView.GenerateTestingCategoryResponseView.as_view()),
    # path("testing/pdf/", categoryView.GenerateTestingCategoryResponseViewPdf.as_view()),
    path("testing/result/<int:id>/", categoryView.SubmitTestAndUpdateResultView.as_view()),
    path("testing/past-tests/", categoryView.TestingCategoryPastListingView.as_view()),
    path("testing/ablities/", categoryView.AbilityView.as_view()),
    path("testing/<int:id>/", categoryView.GetRecordByIdView.as_view()),
    path("testing/achievements/<int:id>/",categoryView.AchievementView.as_view()),
    path("download-file/", categoryView.DownloadArticleView.as_view()),

    ### file summarization ###
    path("file/summarization/", categoryView.FileSummarizationView.as_view()),
    path("change-language-file-summary/", categoryView.TextTranslationForFileSummaryView.as_view()),
    path("file/summarization-vocab/", categoryView.FileSummarizationVocabView.as_view()),
    path("file/history/", categoryView.FileSummaryHistoryView.as_view()),
    path("file/edit/<int:id>/", categoryView.FileSummaryUpdationView.as_view()),
    path("file/delete/<int:id>/", categoryView.FileSummaryDeleteView.as_view()),
    path("file/<int:file_id>/", categoryView.GetSummaryByIdView.as_view()),
    path("download-file-summary/<int:id>/", categoryView.DownloadFileSummaryView.as_view()),

    #### file conversions ####
    path("conversion/pdf-to-word/", categoryView.PdfToWordView.as_view()),
    # path("conversion/word-to-pdf/", categoryView.ConvertWordToPdfView.as_view()),
    path("conversion/pdf-to-excel/", categoryView.ConvertPdfToExcelView.as_view()),

    path("conversion/excel-to-pdf/", categoryView.ConvertExcelToPdfView.as_view()),
    path("conversion/pdf-to-image/", categoryView.ConvertPdfToImageView.as_view()),
    path("conversion/image-to-pdf/", categoryView.ConvertImageToPdfView.as_view()),
    # path("conversion/ppt-to-pdf/", categoryView.ConvertPptToPdfView.as_view()),
    path("conversion/pdf-to-ppt/", categoryView.ConvertPdfToPptView.as_view()),
    path("conversion/ppt-to-pdf/", categoryView.NewServiceView.as_view()),
    path("conversion/word-to-pdf/", categoryView.NewDocToPdfView.as_view()),
    path("conversion/history/", categoryView.FileConversionHistoryView.as_view()),


    #### Notes ####
    path("convert-voice-to-text/", categoryView.ConvertVoiceToTextView.as_view()),
    path("create-notes/", categoryView.CreateNotesView.as_view()),
    path("get-ai-explanation/", categoryView.GetAiExplanation.as_view()),
    path("change-language/", categoryView.TextTranslationView.as_view()),
    path("get-all-listing-notes/", categoryView.GetAllListingNotesView.as_view()),
    path("get-notes-by-id/<int:id>/", categoryView.GetListingNotesByIdView.as_view()),
    path("send-notes-via-mail/",categoryView.SendNotesViaMale.as_view()),

    #### research ####
    path("get-research-answer/", categoryView.GetResearchAnswerView.as_view()),

    path("regenerate-research-answer/<int:id>/", categoryView.RegenerateResearchAnswerView.as_view()),
    path("detailed-research-answer/<int:id>/", categoryView.DetailedResearchView.as_view()),
    path("save-research-topics/<int:id>/", categoryView.SaveResearchTopicsView.as_view()),
    path("research-answer-by-upload-reference/", categoryView.UploadReferenceForResearchView.as_view()),
    path("get-all-listing-research/", categoryView.GetAllResearchView.as_view()),
    path("get-research-by-id/<int:id>/", categoryView.GetResearchByIdView.as_view()),
    path("download-research-file/<int:id>/", categoryView.DownloadResearchView.as_view()),
    path("research-file/edit/<int:id>/", categoryView.ResearchTopicUpdationView.as_view()),
    path("research-file/delete/<int:id>/", categoryView.ResearchTopicDeleteView.as_view()),
 
    #### assignment ####
    path("get-assignmnet-answer/", categoryView.GetAssignmentSolutionView.as_view()),
    path("assignmnet/edit/<int:id>/", categoryView.AssignmentSolutionEditView.as_view()),
    path("assignmnet/delete/<int:id>/", categoryView.AssignmentSolutiondeleteView.as_view()),
    path("regenerate-solution/<int:id>/", categoryView.GetAssignmentSolutionReviewView.as_view()),

    path("fetch-all-assignment/",categoryView.GetAllAssginmentView.as_view()),
    path("update-assignment/<int:id>/", categoryView.updateAssignmentView.as_view()),
    path("get-assignment/<int:id>/",categoryView.GetAssigmentByIdView.as_view()),

    ##### setting app  ######
    path("get-faq-app-list/", categoryView.GetFaqListView.as_view()),
    path("get-terms-condition-app/", categoryView.GetTermsConditionAppView.as_view()),
    path("delete-user-app/", categoryView.DeleteUserAppView.as_view()),
    
    # #### articles #####
    # path("get-articles-response/", categoryView.GetArticlesView.as_view()),
    path("article-topics/", categoryView.ArticleListView.as_view()),
    path("regenerate-article/<int:id>/", categoryView.RegenerateArticleView.as_view()),
    path("detailed-article/", categoryView.DetailedArticleView.as_view()),
    path("articles/", categoryView.ArticlesListingView.as_view()),
    path("article/<int:id>/", categoryView.GetArticleByIdView.as_view()),
    path("download-article/", categoryView.DownloadArticleView.as_view()),
    path("article/edit/<int:id>/", categoryView.ArticleUpdationView.as_view()),
    path("article/delete/<int:id>/", categoryView.ArticleDeleteView.as_view()),

    ####common for all #####
    path("send-file-to-mail/",categoryView.SendFileToMailByToken.as_view()),


    #### presentation #####
    path("generate-slide-text/", categoryView.GetSlideContentView.as_view()),
    path("presentation-binary-data/", categoryView.SavePresentationBinaryDataView.as_view()),
    path("get-presentation/<int:id>/", categoryView.GetPresentationByIdView.as_view()),
    path("update-presentation/<int:id>/", categoryView.UpdatePresentationByIdView.as_view()),
    path("presentation-history/", categoryView.PresentationHistoryView.as_view()),

    #### notes #####
    path("save-notes/", categoryView.SaveNotesView.as_view()),
    path("notes-history/", categoryView.NotesHistoryView.as_view()),
    path("notes/<int:id>/", categoryView.GetNotesByIdView.as_view()),
    path("notes-actions/", categoryView.NotesActionsView.as_view()),
]
