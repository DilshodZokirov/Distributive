from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.order.models import Order
from apps.order.models.order import OrderProduct
from apps.product.models import Product


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id'
        ]


class CreateOrderSerializer(serializers.ModelSerializer):
    pharmacy_name = serializers.CharField(max_length=400, min_length=1, required=True)
    customer_name = serializers.CharField(max_length=400, required=False)
    lot = serializers.IntegerField()
    lon = serializers.IntegerField()
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = Order
        fields = [
            # 'seller',
            'id',
            'pharmacy_name',
            'customer_name',
            'lot',
            'lon',
            "phone_number"
        ]

    def create(self, validated_data: dict):
        user = self.context['request'].user
        validated_data['seller'] = user
        # product = Product
        order = Order.objects.create(**validated_data)
        order.save()
        return order


class OrderProductCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_deleted=False))
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.filter(is_deleted=False))

    class Meta:
        model = OrderProduct
        fields = [
            'order',
            "product"
        ]


class ProductOrderAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'pictures',
            "price1",
            "price2",
            "expiration_date"
        ]


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductOrderAllSerializer(many=True)

    class Meta:
        model = OrderProduct
        fields = [
            "id",
            "product"
        ]


class OrderAllProductSerializer(serializers.ModelSerializer):
    order_product = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'order_product'
        ]


class OrderPositionUpdatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "order_position"
        ]

    def update(self, instance: Order, validated_data):
        instance.order_position = "Basket"
        instance.save()
        return {"message": "Successfully Updated"}


class OrderEditSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    # order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = OrderProduct
        fields = [
            'id',
            "count"
        ]

    def validate(self, attrs):
        product_count = self.instance.product.count
        order_product_count = self.instance.count
        count = attrs.get('count')
        if count:
            if order_product_count < count:
                if product_count < count - order_product_count:
                    raise ValidationError("Uzr maxsulot boshqa qolmadi yo'q !!!")
            elif order_product_count > count:
                if product_count < order_product_count - count:
                    raise ValidationError("Uzr maxsulot boshqa qolmadi yo'q !!!")
        return attrs

    def update(self, instance: OrderProduct, validated_data: dict):
        count = instance.count
        product = Product.objects.get(pk=instance.product.pk)
        if product and validated_data.get("count"):
            if count >= validated_data.get("count"):
                product.count += count - validated_data.get("count")
            if validated_data.get("count") > count:
                product.count += validated_data.get("count") - count
        instance.count = validated_data.get("count")
        instance.price = instance.product.price1 * validated_data.get("count")
        instance.save()
        product.save()
        return {"message": "Successfully Updated"}


class OrderPositionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "order_position"
        ]


class OrderProductAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "price1",
            "price2",
            "compound",
            "temporarily_unavailable",
            "pictures",
            "count",
            "count_of_product"
        ]


class OrderDetailAllProductSerializer(serializers.ModelSerializer):
    class Meta:
        pass
