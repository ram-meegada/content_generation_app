from rest_framework.views import APIView
from rest_framework.response import Response
from whizzo_app.services.categoryService import CategoryService
from rest_framework.permissions import AllowAny

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
    


# note
class ConvertVoiceToTextView(APIView):
    def post(self, request):
        result = category_obj.voice_to_text(request)
        return Response(result, status = result["status"])
    
class CreateNotesView(APIView):
    def post(self, request):
        result = category_obj.add_notes(request)
        return Response(result, status = result["status"])

class GetAiExplanation(APIView):
    def post(self, request):
        result = category_obj.ai_explanation(request)
        return Response(result, status = result["status"])

class ChangeLanguageNoteView(APIView):
    def post(self, request):
        result = category_obj.change_language_note(request)
        return Response(result, status = result["status"])   
    
class GetAllListingNotesView(APIView):
    def post(self, request):
        result = category_obj.get_all_listing_notes(request)
        return Response(result, status = result["status"])   
    
class GetListingNotesByIdView(APIView):
    def post(self, request, id):
        result = category_obj.get_notes_by_id(request, id)
        return Response(result, status = result["status"]) 

class SendNotesViaMale(APIView):
    def post(self, request):
        pass
    

# research
class GetResearchAnswerView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = category_obj.get_research_answer(request)
        return Response(result, status = result["status"])
    
class GetAllResearchView(APIView):
    def post(self, request):
        result = category_obj.get_all_research(request)
        return Response(result, status = result["status"])   
    
class GetResearchByIdView(APIView):
    def post(self, request, id):
        result = category_obj.get_research_by_id(request, id)
        return Response(result, status = result["status"]) 


# assignment
class GetAssignmentSolutionView(APIView):
    def post(self, request):
        result = category_obj.get_assignment_solution(request)
        return Response(result, status = result["status"])
     


# setting app
class GetFaqListView(APIView):
    def get(self, request):
        result = category_obj.get_list_faq(request)
        return Response(result, status = result["status"])
    
class GetTermsConditionAppView(APIView):
    def get(self, request):
        result = category_obj.get_terms_condition(request)
        return Response(result, status = result["status"])
    

class DeleteUserAppView(APIView):
    def delete(self, request):
        result = category_obj.delete_user(request)
        return Response(result, status = result["status"])
    


# articles
class GetArticlesView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = category_obj.get_article_response(request)
        return Response(result, status = result["status"])