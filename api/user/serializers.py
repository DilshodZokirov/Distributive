from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from apps.user.models.company import Company
from apps.user.models import User
from apps.user.models.models import District


class LoginUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    token = serializers.PrimaryKeyRelatedField(queryset=Token.objects.all(), required=False)

    class Meta:
        model = User
        fields = [
            "phone_number",
            "password"
        ]

    def validate(self, attrs):
        if attrs.get('phone_number') and attrs.get('password'):
            request = self.context['request']
            user = authenticate(request, phone_number=attrs.get('phone_number'), password=attrs.get('password'))
            if not user:
                raise serializers.ValidationError({"message": "Bad Request"})
            token, _ = Token.objects.get_or_create(user=user)
            attrs['user'] = user
            attrs['token'] = token
        return attrs


class RegistrationSerializer(serializers.ModelSerializer):
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password2 = serializers.CharField()
    company = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'district',
            "username",
            "first_name",
            "last_name",
            "email",
            'company',
            "phone_number",
            "password",
            "password2"
        ]
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def validate(self, attrs: dict):
        phone_number = attrs.get('phone_number')
        if 10 >= len(phone_number) >= 12:
            raise ValidationError("Iltimos telefon nomerni to'g'ri kiriting !!!")
        if attrs.get('password') != attrs.get("password2"):
            raise ValidationError("Iltimos parolni to'ri kiriting !!!")
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Bunaqa inson bizning ro'yxatda bor")
        if Company.objects.filter(name=attrs.get("company")).exists():
            raise ValidationError("Bunday Company bizda bor iltimos boshqa nom qo'ying !!!")
        return attrs

    @transaction.atomic
    def create(self, validated_data: dict):
        username = validated_data.get("username")
        district = validated_data.get('district')
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        email = validated_data.get("email")
        password = validated_data.get("password")
        phone_number = validated_data.get('phone_number')
        company_name = validated_data.get("company")
        company = Company.objects.create(name=company_name)
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone_number=phone_number,
            company=company,
            role="office_manager",
            district=district
        )
        company.save()
        user.save()
        return user


# 2022-06-28T14:18:15.840452+05:00

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'role',
        ]
