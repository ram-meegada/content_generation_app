from rest_framework import serializers
from whizzo_app.utils.generateLoginToken import generate_login_token
from whizzo_app.models.userModel import UserModel

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
    class Meta:
        model = UserModel
        fields = ["id","email","name","phone_no","country_code","country_name","email","profile_status","purpose","profile_picture","first_name","last_name"]