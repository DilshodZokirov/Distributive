from rest_framework import serializers

from apps.user.models.models import District


class DistrictUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            'name'
        ]
