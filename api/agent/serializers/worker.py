from rest_framework import serializers

from apps.order.models import Order
from apps.user.models import User
from apps.user.models.models import District


class AllPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'total_price',
            'paid_price'
        ]


class DistrictUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            'name'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    district = DistrictUserSerializer()

    def to_representation(self, instance: User):
        data = super(UserProfileSerializer, self).to_representation(instance)
        data['order_seller'] = AllPriceSerializer(instance.order_seller, many=True).data
        data['all_total_price'] = sum(product['total_price'] for product in data['order_seller'])
        data['all_paid_price'] = sum(product['paid_price'] for product in data['order_seller'])
        return data

    class Meta:
        model = User
        fields = [
            'id',
            'profile_pic',
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'district',
            'phone_number',
            'role'
        ]
