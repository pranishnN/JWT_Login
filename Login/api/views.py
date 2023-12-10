
import json, random, string

# ---rest-----
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


# django
from django.contrib.auth.hashers import make_password

# Project
from .models import masUser
from .email_function import send_email
from .serializer import UserSerializer


EXCEPTION_RESPONSE = {'data':{'message':'Oops, Something went wrong'}, 'status':status.HTTP_400_BAD_REQUEST}

otp_func = lambda length : ''.join(random.choices(string.digits, k=length))

class UserRegistrationAPI(APIView):

    def get(self, request):
        try:

            userId = request.GET.get('userId')
            userData = masUser.objects.filter(id=userId).values().first()
            return Response(userData)
        
        except Exception as e:
            return Response(**EXCEPTION_RESPONSE) 

    def post(self, request):
        try:
            serializer_class = UserSerializer(data=request.data)
            if serializer_class.is_valid():
                serializer_class.save()
                user_id = serializer_class.data.get('id')
                otp = otp_func(length=6)
                update = masUser.objects.filter(id=user_id).update(otp=otp)
                if update != 0:
                    print('-------OTP-------', otp)
                    # send_email(user_id=user_id, otp=otp)
                    data = {'message':'OTP send successfully', 'email_id':serializer_class.data.get('email_id')}
                    return Response(data=data, status=status.HTTP_201_CREATED)

            else:
                data = {'message':'Oops!, Something went wrong', 'errors':serializer_class.errors}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(**EXCEPTION_RESPONSE) 

class UserLoginAPI(APIView):
    
    def post(self, request):
        pass

class OTPVerifyAPI(APIView):
    
    def post(self, request):
        pass

