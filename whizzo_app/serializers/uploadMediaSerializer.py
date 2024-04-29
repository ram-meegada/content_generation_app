from rest_framework import serializers
from whizzo_app.models.uploadMediaModel import UploadMediaModel

class CreateUpdateUploadMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadMediaModel
        fields = ["id", "media_url", "media_type", "media_name", "media_size"]