from rest_framework import serializers

from apps.user.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    lon = serializers.IntegerField()
    lot = serializers.IntegerField()
    phone_number = serializers.CharField()

    class MEta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'lon',
            'lot',
            'phone_number',
            'password'
        ]
