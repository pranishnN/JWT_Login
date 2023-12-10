
import json, random, string

# ---rest-----
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


# django
from django.contrib.auth.hashers import make_password
from django.conf import settings

# Project
from .models import masUser
from .email_function import send_email
from .serializer import UserSerializer
from .jwt_auth import generate_jwt_token


EXCEPTION_RESPONSE = {'data':{'message':'Oops, Something went wrong'}, 'status':status.HTTP_400_BAD_REQUEST}

otp_func = lambda length : ''.join(random.choices(string.digits, k=length))

def update_request_data(data):
    data._mutable = True
    data['password'] = settings.DEFAULT_PASSWORD
    return data


class UserRegistrationAPI(APIView):

    def get(self, request):
        try:
            send_email(user_id=1, otp='543432')
            # userId = request.GET.get('userId')
            # userData = masUser.objects.filter(id=userId).values().first()
            return Response('userData')
        
        except Exception as e:

            return Response(**EXCEPTION_RESPONSE) 

    def post(self, request):
        try:
            request_data = update_request_data(request.data)
            serializer_class = UserSerializer(data=request_data)
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
                    data = {'message':'Oops!, Something went wrong'}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                

            else:
                data = {'message':'Oops!, Something went wrong', 'errors':serializer_class.errors}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print('=====except Exception=====', e)
            return Response(**EXCEPTION_RESPONSE) 

class UserLoginAPI(APIView):
    
    def post(self, request):
        email = request.data.get('email_id')
        user = masUser.objects.filter(email_id__iexact=email)
        if user.exists():
            otp = otp_func(length=6)
            update = user.update(otp=otp)
            if update != 0:
                print('-------OTP-------', otp)
                # send_email(user_id=user_id, otp=otp)
                data = {'message':'OTP send successfully', 'email_id':email}
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response(**EXCEPTION_RESPONSE) 

        else:
            data = {'message':'Entered email not exists'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyAPI(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        user = masUser.objects.filter(email_id__iexact=email)
        user_data = user.values().first()
        if user.exists() and user_data.get('otp') == str(otp):
            
            token = generate_jwt_token(user.first())
            data = {**token}
            data['user'] = user_data
           
            if not user_data.get('is_otp_verified'):
                update = user.update(is_otp_verified=1)
                if update != 0:
                    data.update({'message': 'User Registered Successfully'})
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response(**EXCEPTION_RESPONSE)
            else:
                data.update({'message': 'User LoggedIn Successfully'})
                return Response(data, status=status.HTTP_200_OK)

        else:
            data = {'message': 'Entered OTP not matching'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)




