# django
from django.urls import path

# app
from . import views

# simple-jwt
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('user/', views.UserRegistrationAPI.as_view()),
    path('login/', views.UserLoginAPI.as_view()),
    path('otpverify/', views.OTPVerifyAPI.as_view()),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]