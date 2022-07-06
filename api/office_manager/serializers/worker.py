from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.order.models import Order
from apps.user.models import User
from apps.user.models.models import District, UserMove


class UserCreateSerializer(serializers.ModelSerializer):
    profile_pic = serializers.FileField(required=False)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    role = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'district',
            'profile_pic',
            'username',
            'first_name',
            'last_name',
            'date_of_birth',
            'phone_number',
            'role',
            'password',
        ]

    def validate(self, attrs: dict):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        if User.objects.filter(Q(phone_number=phone_number) & ~Q(role="unemployed")).exists():
            raise ValidationError("Bunday ishchi boshqa korxonada ishlaydi bor !!!")
        if len(password) < 6:
            raise ValidationError("Iltimos passwordni 6 ta belgidan ko'proq kiriting !!!")
        return attrs

    @transaction.atomic
    def create(self, validated_data: dict):
        company = self.context['request'].user.company
        if User.objects.filter(Q(phone_number=validated_data.get("phone_number")) & Q(role="unemployed")).exists():
            user = User.objects.get(Q(phone_number=validated_data.get("phone_number")) & Q(role="unemployed"))
            user.district = validated_data.get("district")
            user.first_name = validated_data.get("first_name")
            user.last_name = validated_data.get("last_name")
            user.date_of_birth = validated_data.get("date_of_birth")
            user.role = validated_data.get("role")
            user.date_of_birth = validated_data.get("date_of_birth")
            user.phone_number = validated_data.get("phone_number")
            user.save()
        else:
            validated_data['company'] = company
            validated_data['role'] = validated_data.get("role")
            User.objects.create_user(
                **validated_data
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
            "district",
            "phone_number",
            'profile_pic'
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
