# rest_framework
from rest_framework import serializers

# app
from .models import masUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = masUser
        fields = ['id', 'first_name', 'last_name', 'email_id', 'otp', 'is_otp_verified', 'createdDate']