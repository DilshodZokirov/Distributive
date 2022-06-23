from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from rest_framework.authtoken.models import Token

from apps.user.models.company import Company


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number, password, **extra_fields):
        now = timezone.now()
        if not phone_number:
            raise ValueError('The given phone_number must be set')
        user = self.model(phone_number=phone_number, is_active=True, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        return self._create_user(phone_number, password,
                                 **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        user = self._create_user(phone_number, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class District(models.Model):
    name = models.CharField(max_length=200)


class User(AbstractBaseUser, PermissionsMixin):
    class TYPE(models.Choices):
        OFFICE_MANAGER = "office_manager"
        AGENT = "agent"
        MANAGER = "manager"
        DELIVERY = "delivery"

    username = models.CharField(max_length=500, null=True)
    phone_number = models.CharField(max_length=13, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='company')
    first_name = models.CharField(max_length=400)
    email = models.EmailField(null=True, blank=True)
    last_name = models.CharField(max_length=400, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True,
                                 related_name="district_user")
    profile_pic = models.FileField(upload_to='user/profile', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)
    lot = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    role = models.CharField(max_length=400, choices=TYPE.choices, default=TYPE.DELIVERY, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

#
# class Role(BaseModel):
#     class TYPE(models.Choices):
#         OFFICE_MANAGER = "office_manager"
#         AGENT = "agent"
#         MANAGER = "manager"
#         DELIVERY = "delivery"
#
#     type = models.CharField(max_length=50, choices=TYPE.choices, default=TYPE.DELIVERY)
#
#     def __str__(self):
#         return self.type
