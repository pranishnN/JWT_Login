# Simple JWT
from rest_framework_simplejwt.tokens import RefreshToken

def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    token = {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }
    return token