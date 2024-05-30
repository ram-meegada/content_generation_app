from rest_framework import serializers
from whizzo_app.utils.generateLoginToken import generate_login_token
from whizzo_app.models import UserModel, PurposeModel
from whizzo_app.models.uploadMediaModel import UploadMediaModel
from whizzo_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
from whizzo_app.serializers.adminSerializer import PurposeSerializer

# class CreateUpdateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ["id", "email", ""]

class GetUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'name', 'phone_no', 'country_name', 'country_code', \
                  'email_verification', 'profile_status', 'token',"purpose","profile_picture","first_name","last_name"]

    def get_token(self, obj):
        give_login_token = self.context.get("give_login_token", False)
        if give_login_token:
            return generate_login_token(obj)
        else:
            return None

class updateUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    purpose = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = ["id","email","name","phone_no","country_code","country_name","email","profile_status","purpose","profile_picture","first_name","last_name"]
    
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            try:
                pic_data = UploadMediaModel.objects.get(id=self.context.get("user_profile"))
                serializer = CreateUpdateUploadMediaSerializer(pic_data)
                return serializer.data
            except UploadMediaModel.DoesNotExist:
                return None
        return None
    
    def get_purpose(self, obj):
        if obj.purpose:
            try:
                pic_data = PurposeModel.objects.get(id=self.context.get("purpose"))
                serializer = PurposeSerializer(pic_data)
                return serializer.data
            except PurposeModel.DoesNotExist:
                return None
        return None


class GetAllDetailUserSerializer(serializers.ModelSerializer):
    profile_picture=CreateUpdateUploadMediaSerializer()
    purpose=PurposeSerializer()
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'name', 'phone_no', 'country_name', 'country_code', \
                  'email_verification', 'profile_status', 'token',"purpose","profile_picture","first_name","last_name"]

  