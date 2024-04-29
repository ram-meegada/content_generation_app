from rest_framework_simplejwt.tokens import RefreshToken

def generate_login_token(user_obj):
    token = RefreshToken.for_user(user_obj)
    return str(token.access_token)