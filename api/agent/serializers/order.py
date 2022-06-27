from rest_framework import serializers

from apps.order.models import Order


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id'
        ]


class CreateOrderSerializer(serializers.ModelSerializer):
    pass
