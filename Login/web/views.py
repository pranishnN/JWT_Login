# django
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

import requests

# Create your views here.

api_url = settings.API_URL

mode = 'edit'


def register(request):

    if request.method == 'POST':
        firstName = request.POST.get('txtFirstName')
        lastName = request.POST.get('txtLastName')
        email = request.POST.get('txtEmail')

        data = {
            'first_name':firstName,
            'last_name':lastName,
            'email_id':email,
        }

        post = requests.post(f"{api_url}/user/", data=data)

        if post.status_code == 201:
            email = post.json()['email_id']
            messages.success(request, post.json()['message'])
            return render(request, 'otp_verify.html', context={'email':email})
        else:
            error = post.json()
            print('=====erros====', error)
            messages.error(request, error['message'])
            context = {"errors":error['errors']}
            return render(request, 'register.html', context=context)

    else:
        context = {'page_title':'Sign-Up'}
        return render(request, 'register.html', context=context)


def login(request):
    if request.method == 'POST':
        email = request.POST.get('txtEmail')
        data = {'email_id':email}
        post = requests.post(f"{api_url}/login/", data=data)
        print('======post=======', post)
        if post.status_code == 200:
            data = post.json()
            messages.success(request, data['message'])
            context = {'email': data['email_id']}
            return render(request, 'otp_verify.html', context=context)
        else:
            data = post.json()
            messages.error(request, data['message'])
            return redirect('login')

    else:
        context = {'page_title':'Sign-In'}
        return render(request, 'login.html', context=context)


def otp_verify(request):

    if request.method == 'POST':
        email = request.POST.get('hdnEmailId')
        otp = request.POST.get('txtOtp')

        data = { 'otp':otp, 'email':email }

        verify_otp = requests.post(f"{api_url}/otpverify/", data=data)

        data = verify_otp.json()
        if verify_otp.status_code in [200, 201]:
            print('======data======', data)
            messages.success(request, data['message'])
            context = dict()
            context['first_name'] = data['user']['first_name'] 
            context['last_name'] = data['user']['last_name'] 
            
            # userdata = requests.get(f'{api_url}/user/', params={'userId':userId})
            return render(request, 'home.html', context=context)
        else:
            print('======data======', data)
            messages.error(request, data['message'])
            return render(request, 'otp_verify.html', context={'email':email})


