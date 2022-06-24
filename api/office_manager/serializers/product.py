from django.db import transaction
from rest_framework import serializers

from apps.product.models import Category, Product


class ProductGetAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price1',
            'price2',
            'compound',
            'temporarily_unavailable',
            'pictures',
            'expiration_date',
            'count',
            'count_of_product'
        ]


class CategoryGetAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name'
        ]


class CategoryOneProductAll(serializers.ModelSerializer):
    product_category = ProductGetAllSerializer(read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'product_category'
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    pictures = serializers.FileField(required=False)
    name = serializers.CharField(required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    price1 = serializers.FloatField(required=False)
    price2 = serializers.FloatField(required=False)
    compound = serializers.CharField(required=False)
    expiration_date = serializers.DateTimeField(required=True)

    # created_by = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Product
        fields = [
            'pictures',
            'name',
            'category',
            'price1',
            'price2',
            'compound',
            'expiration_date',
            'temporarily_unavailable',
            # 'created_by'
        ]

    @transaction.atomic
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        if self.data.get('temporarily_unavailable'):
            validated_data['temporarily_unavailable'] = self.data.get('temporarily_unavailable')
        else:
            validated_data['temporarily_unavailable'] = False
        Product.objects.create(**validated_data)
        return {"success"}


class ProductUpdateAllSerializer(serializers.ModelSerializer):
    pictures = serializers.FileField(required=False)
    name = serializers.CharField(required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    price1 = serializers.FloatField(required=False)
    price2 = serializers.FloatField(required=False)
    compound = serializers.CharField(required=False)
    expiration_date = serializers.DateTimeField(required=True)
    count = serializers.FloatField()
    count_of_product = serializers.FloatField()

    class Meta:
        model = Product
        fields = [
            'pictures',
            'name',
            'category',
            'price1',
            'price2',
            'compound',
            'expiration_date',
            'temporarily_unavailable',
            'count',
            'count_of_product'
        ]
