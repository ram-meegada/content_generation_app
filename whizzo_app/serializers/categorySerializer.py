from rest_framework import serializers
from whizzo_app.models.categoryModel import CategoryModel
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