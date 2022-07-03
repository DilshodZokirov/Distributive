from datetime import datetime

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.order.models import Order
from apps.order.models.order import OrderProduct
from apps.product.models import Product

# get all
from apps.user.models import Company
from apps.user.models.models import District, User
from utils import result


class OfficeManagerOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'pharmacy_name',
            'customer_name',
            'created_date'
        ]


# create
class OfficeManagerOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id'
        ]


# product
class ProductOrderAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
        ]


# order product
class OrderProductAllSerializer(serializers.ModelSerializer):
    product = ProductOrderAllSerializer()

    class Meta:
        model = OrderProduct
        fields = [
            'count',
            'product'
        ]


# district seller
class DistrictUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            'id',
            'name'
        ]


class SellerUserSerializer(serializers.ModelSerializer):
    district = DistrictUserSerializer()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'district'
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    order_product = OrderProductAllSerializer(many=True)
    seller = SellerUserSerializer()

    class Meta:
        model = Order
        fields = [
            'id',
            'pharmacy_name',
            'customer_name',
            'order_product',
            'seller',
            'created_date'
        ]


# income order
class OrderIncomeAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'pharmacy_name',
            'customer_name',
            'created_date',
            'paid_position',
            'paid_price'
        ]


class IncomeUpdateSerializer(serializers.ModelSerializer):
    paid_price = serializers.FloatField()

    class Meta:
        model = Order
        fields = [
            'id',
            'paid_price',
            'total_price'
        ]

    def validate(self, attrs):
        total_price = self.instance.total_price
        paid_price = self.instance.paid_price
        if not attrs.get('paid_price'):
            raise ValidationError("Uzr lekin siz summa kiritmadingiz !!!")
        if attrs.get('paid_price') < 0:
            raise ValidationError("Siz manfiy so'mma kiritdingiz !!!")
        if total_price < paid_price + attrs.get('paid_price'):
            raise ValidationError("Siz umumiy summadan ko'p summa kiritdingiz !!!")
        return attrs

    def update(self, instance: Order, validated_data: dict):
        paid_price = instance.paid_price
        total_price = instance.total_price
        if paid_price + validated_data.get('paid_price') == total_price:
            instance.paid_position = 'full_paid'
        else:
            instance.paid_position = "orphan_paid"
        instance.paid_price += validated_data.get('paid_price')
        instance.save()
        return instance


class CreditOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'created_date',
            'pharmacy_name',
            'customer_name',
        ]


class CreditOneOrderSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(CreditOneOrderSerializer, self).to_representation(instance)
        data['residue_price'] = data['total_price'] - data['paid_price']
        today = datetime.today().date()
        created_date = data["created_date"][:10]
        data['date'] = result(today=today, created_date=created_date)
        return data

    class Meta:
        model = Order
        fields = [
            'created_date',
            'total_price',
            'paid_price',
            'phone_number'
        ]
