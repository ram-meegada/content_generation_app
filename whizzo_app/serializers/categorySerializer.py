from rest_framework import serializers
from whizzo_app.models.assignmentModel import AssignmentModel
from whizzo_app.models.categoryModel import CategoryModel
from whizzo_app.models import FileSumarizationModel, NoteModel, ReseaerchModel, FileConversationModel
from whizzo_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer

class GetPreviousTestSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    class Meta:
        model = CategoryModel
        fields = ["id", "category", "sub_category", "created_at", "updated_at"]
    def get_category(self, obj):
        try:
            return obj.get_category_display()
        except:
            return obj.category
    def get_sub_category(self, obj):
        try:
            return obj.get_sub_category_display()
        except:
            return obj.sub_category
        
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
        


class GetNoteListSerializer(serializers.ModelSerializer):
    media = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = CategoryModel
        fields = ["id", "created_at", "updated_at", "media"]        
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
        fields = ["id","user","result"]

class FileConversionlistingSerializer(serializers.ModelSerializer):
    converted_media = CreateUpdateUploadMediaSerializer()
    sub_category = serializers.SerializerMethodField()
    class Meta:
        model = FileConversationModel
        fields = ["id", "converted_media", "images", "sub_category"]
    def get_sub_category(self, obj):
        try:
            return obj.get_sub_category_display()
        except:
            return obj.sub_category    