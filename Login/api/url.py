# django
from django.urls import path

# app
from . import views

urlpatterns = [
    path('user/', views.UserRegistrationAPI.as_view()),
    path('login/', views.UserLoginAPI.as_view()),
    path('otpverify/', views.OTPVerifyAPI.as_view()),
]