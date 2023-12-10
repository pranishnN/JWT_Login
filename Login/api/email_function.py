# django
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


# app
from .models import masUser


def send_email(user_id=None, otp=None, email_type='signin', *args, **kwargs):
    try:
        if user_id:
            userData = masUser.objects.filter(id=user_id).values().first()
            user_name = userData.get('first_name') +' '+ userData.get('last_name')
            subject = 'OTP Verification'

            html_content = render_to_string('otp_verify.html',{'otp':otp, 'email_type':email_type, 'name':user_name})
            subject = subject
            from_address = settings.EMAIL_HOST_USER
            text = strip_tags(html_content)
            email_msg = EmailMultiAlternatives(subject,text,from_address,[userData.get('email_id')])
            email_msg.attach_alternative(html_content, 'text/html')
            email_msg.send()
            return True
    except Exception as e:
        pass
    