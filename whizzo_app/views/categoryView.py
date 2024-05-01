from rest_framework.views import APIView
from rest_framework.response import Response
from whizzo_app.services.categoryService import CategoryService

category_obj = CategoryService()

class GenerateTestingCategoryResponseView(APIView):
    def post(self, request):
        result = category_obj.generate_testing_category_result(request)
        return Response(result, status=result["status"])
    
class GenerateTestingCategoryResponseViewPdf(APIView):
    def post(self, request):
        result = category_obj.generate_testing_category_result_pdf(request)
        return Response(result, status = result["status"])

class SubmitTestAndUpdateResultView(APIView):
    def post(self, request):
        result = category_obj.submit_test_and_update_result(request)
        return Response(result, status = result["status"])

class TestingCategoryPastListingView(APIView):
    def get(self, request):
        result = category_obj.previous_tests_listing(request)
        return Response(result, status = result["status"])

class FileSummarizationView(APIView):
    def post(self, request):
        result = category_obj.generate_file_summary(request)
        return Response(result, status = result["status"])

class FileSummaryHistoryView(APIView):
    def get(self, request):
        result = category_obj.file_summary_history(request)
        return Response(result, status = result["status"])

class GetSummaryByIdView(APIView):
    def get(self, request, file_id):
        result = category_obj.get_file_summary_by_id(request, file_id)
        return Response(result, status = result["status"])

class PdfToWordView(APIView):
    def post(self, request):
        result = category_obj.pdf_to_word(request)
        return Response(result, status = result["status"])

class ConvertPdfToExcelView(APIView):
    def post(self, request):
        result = category_obj.convert_pdf_to_excel(request)
        return Response(result, status = result["status"])
    
class ConvertExcelToPdfView(APIView):
    def post(self, request):
        result = category_obj.excel_to_pdf(request)
        return Response(result, status = result["status"])

class ConvertPdfToImageView(APIView):
    def post(self, request):
        result = category_obj.convert_pdf_to_image(request)
        return Response(result, status = result["status"])

class ConvertImageToPdfView(APIView):
    def post(self, request):
        result = category_obj.image_to_pdf(request)
        return Response(result, status = result["status"])    