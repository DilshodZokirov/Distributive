from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.user.models import User, Company


class DeleteCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id"
        ]

    @transaction.atomic
    def update(self, instance: Company, validated_data: dict):
        user: User = self.context['request'].user
        user.company_id = None
        user.role = "unemployed"
        if user.is_director is True:
            user.is_director = False
            workers = User.objects.filter(company_id=instance.pk)
            for worker in workers:
                worker.company_id = None
                worker.role = "unemployed"
                worker.save()
        instance.is_deleted = True
        instance.save()
        user.save()


class CompanyUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    company_background = serializers.FileField(required=False)

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "description",
            "company_background"
        ]

    def validate(self, attrs: dict):
        if attrs.get("name"):
            if Company.objects.filter(name=attrs.get("name")).exists():
                raise ValidationError("Uzr bunday kompaniya bor edi!!!")
        return attrs
