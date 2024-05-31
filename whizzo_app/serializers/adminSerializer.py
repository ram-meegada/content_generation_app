from rest_framework import serializers
from whizzo_app.models import AbilityModel, AchievementModel, SubjectModel, SubRoleModel, UserModel, PermissionModel, ModuleModel, PurposeModel, \
       FeaturesModel, SubscriptionModel, FaqModel, CmsModel, TestimonialModel
from whizzo_app.utils.generateLoginToken import generate_login_token
from whizzo_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer



class CreateAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AbilityModel
        fields = ["id", "question", "answer_option","corect_answer","is_mcq"]



class CreateAcheivementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementModel
        fields = ["id", "question", "answer_option","subject","corect_answer","is_mcq"]


class CreateSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectModel
        fields = ["id", "subject_name","subject_detail"]


class GetSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectModel
        fields = ["id", "subject_name","is_active"]


class EditSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectModel
        fields = ["id","is_active"]

class CreateRoleSubAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubRoleModel
        fields = ["id","role_name"]

class CreateModuleSubAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleModel
        fields = ["id","module_name"]


class CreateRolePermissionSubAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionModel
        fields = ['id','module','can_add_edit','can_view','can_be_delete']

class GetRolePermissionSubAdminSerializer(serializers.ModelSerializer):
    module = CreateModuleSubAdminSerializer()
    class Meta:
        model = PermissionModel
        fields = ['id','module', 'can_add_edit', 'can_view', 'can_be_delete']

class CreateSubAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id","name","email","phone_no","profile_picture","country_code",'role','sub_role')
        extra_kwargs = {'role': {'default': 3}}



class GetSubAdminSerializer(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    role_permission = serializers.SerializerMethodField()
    sub_role=CreateRoleSubAdminSerializer()
    class Meta:
        model = UserModel
        fields = ("id", "username", "email","country_code","name", "phone_no", "profile_picture", 'is_active','sub_role', 'role_permission')
    def get_role_permission(self, obj):
        try:
            roles_permissions = PermissionModel.objects.filter(user_id = obj.id)
            serializer = GetRolePermissionSubAdminSerializer(roles_permissions, many = True)
            return serializer.data
        except:
            return []



class GeteditSubAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id','is_active')


class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurposeModel
        fields = ['id', 'name', 'detail', 'is_active']

class GeteditpurposeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurposeModel
        fields = ('id','is_active')

class FeatureModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturesModel
        fields = ['id', 'name']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionModel
        fields = ['id', 'plan_type', 'price', 'features', 'status']

class FaqModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqModel
        fields = ['id', 'question', 'answer']



class GetAdminSerializer(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'name', 'phone_no',  'country_code', 'profile_picture']

class UpdateAdminSerializer(serializers.ModelSerializer):
    # profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'name', 'phone_no',  'country_code', 'profile_picture']


class GetAdminManageUserSerializer(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = UserModel
        fields = ("id", "first_name", "last_name", "phone_no", "profile_picture","country_code", 'is_active')


class UpdateAdminManageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", "first_name", "last_name", "phone_no", "country_code","profile_picture")

class EditManageUserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id","is_active"]


class AddContactSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CmsModel
        fields = ["id","phone_no","email","country_code"]

class AddPrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = CmsModel
        fields = ["id","privacy_policy"]

class AddTermsConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CmsModel
        fields = ["id","terms_condition"]

class AddAboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CmsModel
        fields = ["id","about_us"]

class AddAdminSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'username', 'phone_no',  'country_code', 'profile_status', 'token']

    def get_token(self, obj):
        give_login_token = self.context.get("give_login_token", False)
        if give_login_token:
            return generate_login_token(obj)
        else:
            return None
        


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestimonialModel
        fields = ["id", "first_name", "last_name", "email", "country_code", "phone_no", "rating", "message", "profile_picture"]

class GeteditTestimonialStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestimonialModel
        fields = ["id","is_active"]

class GetTestimonialSerializer(serializers.ModelSerializer):
    profile_picture = CreateUpdateUploadMediaSerializer()
    class Meta:
        model = TestimonialModel
        fields = ["id","first_name","last_name","email","rating","message","profile_picture","country_code", "phone_no","is_active"]


