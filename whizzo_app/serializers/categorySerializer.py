from rest_framework import serializers
from whizzo_app.models.assignmentModel import AssignmentModel
from whizzo_app.models.categoryModel import CategoryModel
from whizzo_app.models import FileSumarizationModel, NoteModel, ReseaerchModel, FileConversationModel, ArticleModel, TestingModel, NoteTakingModel
from whizzo_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
from whizzo_app.models.uploadMediaModel import UploadMediaModel
from whizzo_app.models import PresentationModel

class GetPreviousTestSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    correct_answers_percentage = serializers.SerializerMethodField()
    wrong_answers_percentage = serializers.SerializerMethodField()
    remaining_answers_percentage = serializers.SerializerMethodField()
    class Meta:
        model = TestingModel
        fields = ["id", "sub_category", "created_at", "updated_at", "result", "correct_answers", "wrong_answers", "remaining_answers","correct_answers_percentage","wrong_answers_percentage","remaining_answers_percentage", "sub_category_type"]
    def get_sub_category(self, obj):
        try:
            return obj.get_sub_category_display()
        except:
            return obj.sub_category
     
    def get_correct_answers_percentage(self, obj):
        try:
            total_questions = len(obj.result)
            correct_answers_percentage = round((obj.correct_answers/total_questions)*100, 2)
            return correct_answers_percentage
        except:
            return 0
        
    def get_wrong_answers_percentage(self, obj):
        try:
            total_questions = len(obj.result)
            wrong_answers_percentage = round((obj.wrong_answers/total_questions)*100, 2)
            return wrong_answers_percentage
        except:
            return 0
        
    def get_remaining_answers_percentage(self, obj):
        try:
            total_questions = len(obj.result)
            remaining_answers_percentage = round((obj.remaining_answers/total_questions)*100, 2)
            return remaining_answers_percentage
        except:
            return 0
        
class GetFileSummarySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    class Meta:
        model = CategoryModel
        fields = ["id", "category", "sub_category", "created_at", "updated_at", "result"]        
    def get_category(self, obj):
        try:
            return obj.get_category_display()
        except:
            return obj.category
        
class PresentationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentationModel
        fields = ["id", "created_at", "updated_at", "template_id"]

class GetNoteListSerializer(serializers.ModelSerializer):
    media = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = CategoryModel
        fields = ["id", "topic", "created_at", "updated_at", "media", "result"]        

class GetArticlesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel
        fields = ["id", "topic", "created_at", "updated_at", "result"]        
    # def get_category(self, obj):
    #     try:
    #         return obj.get_category_display()
    #     except:
    #         return obj.category



class GetFileSumarizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSumarizationModel
        fields = ["id", "created_at", "result"]    


class GetFileSummarizationIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSumarizationModel
        fields = ["id", "sub_category", "created_at", "result"]        
   


class AddNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteModel
        fields = ["id", "media", "sub_category", "voice_media"]    



class GetNoteSerializer(serializers.ModelSerializer):
    media=CreateUpdateUploadMediaSerializer()
    voice_media=CreateUpdateUploadMediaSerializer()
    class Meta:
        model = NoteModel
        fields = ["id", "media", "sub_category", "voice_media","created_at"] 


class GetResearchSerializer(serializers.ModelSerializer):
    media=CreateUpdateUploadMediaSerializer()
    voice_media=CreateUpdateUploadMediaSerializer()
    class Meta:
        model = ReseaerchModel
        fields = ["id", "media", "sub_category", "topic","page", "tone_of_voice", "specify_reference","is_reduce_citation", "description","created_at"] 

###assignment module 
class CreateAssignmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = AssignmentModel
        fields = ["id","user","result", "created_at"]

class FileConversionlistingSerializer(serializers.ModelSerializer):
    converted_media = CreateUpdateUploadMediaSerializer()
    sub_category = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    class Meta:
        model = FileConversationModel
        fields = ["id", "converted_media", "images", "sub_category"]
    def get_sub_category(self, obj):
        try:
            return obj.get_sub_category_display()
        except:
            return obj.sub_category
    def get_images(self, obj):
        try:
            image_objs = UploadMediaModel.objects.filter(id__in=obj.images)
            serializer = CreateUpdateUploadMediaSerializer(image_objs, many=True)
            return serializer.data
        except:
            return obj.images


class NoteTakingSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    class Meta:
        model = NoteTakingModel
        fields = ["id", "type", "binary_data", "note_screenshot", "count", "canvas_height", "is_duplicate", "is_favourite", "comments", "text_timestamp", "created_at"]
    def get_count(self, obj):
        try:
            return NoteTakingModel.objects.count()
        except:
            return 0
        
class AllNotesSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    class Meta:
        model = NoteTakingModel
        fields = ["id", "type", "note_screenshot", "count", "canvas_height", "is_duplicate", "is_favourite", "comments", "text_timestamp", "created_at"]
    def get_count(self, obj):
        try:
            return NoteTakingModel.objects.count()
        except:
            return 0