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
    path("conversion/pdf-to-excel/", categoryView.ConvertPdfToExcelView.as_view()),

]