from rest_framework.views import APIView
from rest_framework.response import Response
from whizzo_app.services.categoryService import CategoryService
from whizzo_app.services.userService import UserService
from rest_framework.permissions import AllowAny
from django.http import JsonResponse

category_obj = CategoryService()
user_obj = UserService()

class GenerateTestingCategoryResponseView(APIView):
    def post(self, request):
        result = category_obj.generate_testing_category_result(request)
        return Response(result, status=result["status"])
    
class GenerateTestingCategoryResponseViewPdf(APIView):
    def post(self, request):
        result = category_obj.generate_testing_category_result_pdf(request)
        return Response(result, status = result["status"])

class SubmitTestAndUpdateResultView(APIView):
    def post(self, request, id):
        result = category_obj.submit_test_and_update_result(request, id)
        return Response(result, status = result["status"])

class TestingCategoryPastListingView(APIView):
    def post(self, request):
        result = category_obj.previous_tests_listing(request)
        return Response(result, status = result["status"])

class FileSummarizationView(APIView):
    def post(self, request):
        result = category_obj.generate_file_summary(request)
        return Response(result, status = result["status"])
    

class FileSummarizationVocabView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = category_obj.generate_file_important_vocabulary(request)
        return Response(result, status = result["status"])

class FileSummaryHistoryView(APIView):
    def post(self, request):
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

class ConvertWordToPdfView(APIView):
    def post(self, request):
        result = user_obj.word_to_pdf(request)
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

class ConvertPptToPdfView(APIView):
    def post(self, request):
        result = category_obj.ppt_to_pdf(request)
        return Response(result, status = result["status"])    
    
class ConvertPdfToPptView(APIView):
    # permission_classes =[AllowAny]
    def post(self, request):
        result = category_obj.pdf_to_ppt(request)
        return Response(result, status = result["status"])  

class FileConversionHistoryView(APIView):
    def post(self, request):
        result = category_obj.file_conversions_history(request)
        return Response(result, status = result["status"])  


# note
class ConvertVoiceToTextView(APIView):
    def post(self, request):
        result = category_obj.voice_to_text(request)
        return Response(result, status = result["status"])
    
class CreateNotesView(APIView):
    def post(self, request):
        result = category_obj.add_notes_audio_to_text(request)
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
    def post(self, request):
        result = category_obj.get_research_answer(request)
        return Response(result, status = result["status"])
    

class RegenerateResearchAnswerView(APIView):
    def get(self, request, id):
        result = category_obj.regenerate_research_solution(request, id)
        return Response(result, status = result["status"])

class UploadReferenceForResearchView(APIView):
    def post(self, request):
        result = category_obj.research_based_on_reference(request)
        return Response(result, status = result["status"])

class DetailedResearchView(APIView):
    def post(self, request, id):
        result = category_obj.generate_detailed_research_based_on_topics(request, id)
        return Response(result, status = result["status"])

class SaveResearchTopicsView(APIView):
    def post(self, request, id):
        result = category_obj.save_research_topic_list(request, id)
        return Response(result, status = result["status"])

class GetAllResearchView(APIView):
    def post(self, request):
        result = category_obj.get_history_research(request)
        return Response(result, status = result["status"])   
    
class GetResearchByIdView(APIView):
    def get(self, request, id):
        result = category_obj.get_research_by_id(request, id)
        return Response(result, status = result["status"]) 

class DownloadResearchView(APIView):
    def post(self, request, id):
        result = category_obj.download_research_file(request, id)
        return Response(result, status = result["status"]) 
    


# assignment
class GetAssignmentSolutionView(APIView):
    def post(self, request):
        result = category_obj.get_assignment_solution(request)
        return Response(result, status = result["status"])
        
class TextTranslationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        result = category_obj.text_translation(request)
        return Response(result, status = result["status"])
    
class GetAssignmentSolutionReviewView(APIView):
    def post(self, request, id):
        result = category_obj.get_assignment_solution_review(request, id)
        return Response(result, status = result["status"])     

class GetAllAssginmentView(APIView):
    def post(self, request):
        result = category_obj.get_all_assignment(request)
        return Response(result, status = result["status"])

class updateAssignmentView(APIView):
    # permission_classes = [AllowAny]
    def post(self, request, id):
        result = category_obj.update_download_file(request, id)
        return Response(result, status=result["status"])

class DownloadFileSummaryView(APIView):
    # permission_classes = [AllowAny]
    def post(self, request, id):
        result = category_obj.file_summary_download(request, id)
        return Response(result, status=result["status"])
    
class GetAssigmentByIdView(APIView):
    def get(self, request, id):
        result = category_obj.get_assignment_by_id(request, id)
        return Response(result, status=result["status"])

# setting app
class GetFaqListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = category_obj.get_list_faq(request)
        return Response(result, status = result["status"])
    
class GetTermsConditionAppView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = category_obj.get_terms_condition(request)
        return Response(result, status = result["status"])
    

class DeleteUserAppView(APIView):
    def delete(self, request):
        result = category_obj.delete_user(request)
        return Response(result, status = result["status"])
    


# articles
# class GetArticlesView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         result = category_obj.get_article_response(request)
#         return Response(result, status = result["status"])



#common for all 

class SendFileToMailByToken(APIView):
    permission_classes =[AllowAny]
    def get(self, request):
        result = category_obj.send_file_to_mail(request)
        return Response(result, status = result["status"])
    


class ArticleListView(APIView):
    def post(self, request):
        result = category_obj.get_article_response_list(request)
        return Response(result, status = result["status"])

class RegenerateArticleView(APIView):
    def get(self, request, id):
        result = category_obj.regenerate_article(request, id)
        return Response(result, status = result["status"])
    
class DetailedArticleView(APIView):
    def post(self, request):
        result = category_obj.generate_detailed_article_based_on_topics(request)
        return Response(result, status = result["status"])

class ArticlesListingView(APIView):
    def post(self, request):
        result = category_obj.get_article_history(request)
        return Response(result, status = result["status"])

class GetArticleByIdView(APIView):
    def get(self, request, id):
        result = category_obj.get_article_by_id(request, id)
        return Response(result, status = result["status"])

class DownloadArticleView(APIView):
    def post(self, request):
        result = category_obj.download_article(request)
        return Response(result, status = result["status"])

class NewServiceView(APIView):
    def post(self, request):
        result = category_obj.new_service(request)
        return Response(result, status=result["status"])

class NewDocToPdfView(APIView):
    def post(self, request):
        result = category_obj.new_doc_to_pdf_service(request)
        return Response(result, status=result["status"])
    
    
class AchievementView(APIView):
    def get(self, request, id):
        result = category_obj.achievement(request, id)
        return Response(result, status=result["status"])

class AbilityView(APIView):
    def get(self, request):
        result = category_obj.ability(request)
        return Response(result, status=result["status"])

class GetRecordByIdView(APIView):
    def get(self, request, id):
        result = category_obj.get_testing_record_by_id(request, id)
        return Response(result, status=result["status"])
    
class GetSlideContentView(APIView):
    def post(self, request):
        result = category_obj.get_presentation_text(request)
        return Response(result, status = result["status"])