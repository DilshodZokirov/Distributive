from rest_framework import serializers

from apps.product.models import Product, Category


class CategoryAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'category_image'
        ]


class ProductAllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price1',
            'price2',
            'compound',
            'pictures'
        ]


class CategoryGetOneSerializer(serializers.ModelSerializer):
    product_category = ProductAllCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'category_image',
            'product_category'
        ]


class ProductOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'price1',
            'price2',
            'compound',
            'pictures'
        ]
