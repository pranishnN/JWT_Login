from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager, PermissionsMixin

# Create your models here.
class Usermanager(BaseUserManager):

    def create_user(self, email_id, password=None,**kwargs):
            # if not Email:
            #     raise ValueError('user must have an email address')

            # Email=self.normalize_email(Email)

            user = self.model(email_id=email_id,  **kwargs)

            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, emailId=None, password=None, **kwargs):

        user = self.create_user(
            email_id=emailId,
            password=password,
            isSuperAdmin=True,
            is_otp_verified=True
            isAdmin=True,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class masUser(AbstractBaseUser, PermissionsMixin):
     
    first_name = models.CharField(null=True, max_length=100, blank=True)
    last_name = models.CharField(null=True, max_length=100, blank=True)
    email_id = models.CharField(max_length=200, unique=True, error_messages={'unique':'This emailId already exists'})
    otp = models.CharField(max_length=10, null=True, blank=True)
    is_otp_verified = models.BooleanField(default=False)
    createdDate = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['password','emailId']
    USERNAME_FIELD = 'email_id'