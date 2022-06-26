from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.order.models import Order
from apps.user.models import User
from apps.user.models.models import District, UserMove


class UserCreateSerializer(serializers.ModelSerializer):
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'district',
            'username',
            'first_name',
            'last_name',
            'date_of_birth',
            'phone_number',
            'password',
            'company'
        ]

    def validate(self, attrs: dict):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Bunday raqamli ishchi bor !!!")
        if len(password) < 6:
            raise ValidationError("Iltimos passwordni 6 ta belgidan ko'proq kiriting !!!")
        return attrs

    @transaction.atomic
    def create(self, validated_data: dict):
        company = self.context['request'].user.company
        first_name = validated_data.get('first_name')
        username = validated_data.get('username')
        last_name = validated_data.get('last_name')
        district = validated_data.get('district')
        password = validated_data.get('password')
        phone_number = validated_data.get("phone_number")
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            phone_number=phone_number,
            company=company,
            role="agent",
            district=district
        )
        return {"message": "Success"}


class DistrictAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            'name'
        ]


class WorkerUserAllSerializer(serializers.ModelSerializer):
    district = DistrictAllSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            'first_name',
            'last_name',
            "district"
        ]


class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMove
        fields = [
            "lot",
            "lon"
        ]


class UserMoveSerializer(serializers.ModelSerializer):
    user_move = MoveSerializer(many=True)
    district = DistrictAllSerializer()

    class Meta:
        model = User
        fields = [
            'user_move',
            'first_name',
            'last_name',
            'district'
        ]


class OrderAllPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'total_price',
            'paid_price'
        ]


class UserSalarySerializer(serializers.ModelSerializer):
    # order_seller = OrderAllPriceSerializer(many=True)
    district = DistrictAllSerializer()

    def to_representation(self, instance: User):
        data = super(UserSalarySerializer, self).to_representation(instance)
        data['order_seller'] = OrderAllPriceSerializer(instance.order_seller, many=True).data
        data['total_all_price'] = sum(product['total_price'] for product in data['order_seller'])
        data['total_paid_price'] = sum(product['paid_price'] for product in data['order_seller'])
        return data

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'district'
        ]
