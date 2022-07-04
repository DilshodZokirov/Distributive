from django.db import transaction
from rest_framework import serializers

from api.utils.serializer import DistrictUserSerializer
from apps.user.models import User
from apps.user.models.models import District


class ManagerUserProfileSerializer(serializers.ModelSerializer):
    district = DistrictUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            'first_name',
            "last_name",
            "role",
            "profile_pic",
            "date_of_birth",
            'district',
            "phone_number",
            "email"
        ]


class UserUpdateProfile(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    profile_pic = serializers.FileField(required=False)
    email = serializers.EmailField(required=False)
    date_of_birth = serializers.DateField(required=False)

    class Meta:
        model = User
        fields = [
            'district',
            'first_name',
            "username",
            "profile_pic",
            "last_name",
            "email",
            "date_of_birth"
        ]

    @transaction.atomic
    def update(self, instance, validated_data: dict):
        pk = self.context['request'].user.id
        user = User.objects.get(pk=pk)
        if validated_data.get("district"):
            user.district = validated_data.get("district")
        if validated_data.get("first_name"):
            user.first_name = validated_data.get("fist_name")
        if validated_data.get("username"):
            user.username = validated_data.get("username")
        if validated_data.get("profile_pic"):
            user.profile_pic = validated_data.get("profile_pic")
        if validated_data.get("last_name"):
            user.last_name = validated_data.get("last_name")
        if validated_data.get("email"):
            user.email = validated_data.get("email")
        if validated_data.get("date_of_birth"):
            user.date_of_birth = validated_data.get("date_of_birth")
        user.save()
        return {200: "successfully updated"}
