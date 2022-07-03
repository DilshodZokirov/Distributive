from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from Distributive.models import BaseModel
from django.db import models


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

    def __str__(self):
        return self.name


class UserMove(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_move')
    lon = models.IntegerField()
    lot = models.IntegerField()


class User(AbstractBaseUser, PermissionsMixin):
    class TYPE(models.Choices):
        UNEMPLOYED = "unemployed"
        OFFICE_MANAGER = "office_manager"
        AGENT = "agent"
        MANAGER = "manager"
        DELIVERY = "delivery"

    username = models.CharField(max_length=500, null=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True)
    company = models.ForeignKey("Company", on_delete=models.CASCADE, null=True, blank=True, related_name='company')
    first_name = models.CharField(max_length=400, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    last_name = models.CharField(max_length=400, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True,
                                 related_name="district_user")
    profile_pic = models.FileField(upload_to='user/profile', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_director = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=400, choices=TYPE.choices, default=TYPE.DELIVERY, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number


class Company(BaseModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400, null=True, blank=True)
    company_background = models.FileField(upload_to="company", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.description}"
