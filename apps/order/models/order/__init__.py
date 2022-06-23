from Distributive.models import Auditable
from django.db import models

from apps.user.models.models import BaseModel


class Order(BaseModel):
    class OrderPosition(models.Choices):
        BASKET = "Basket"
        VERIFICATION = "Verification"
        DELIVERY = "Delivery"
        FINISH = "Finish"

    pharmacy_name = models.CharField(max_length=30, null=True, blank=True)
    customer_name = models.CharField(max_length=300, null=True, blank=True)
    lot = models.CharField(max_length=400, null=True, blank=True)
    lon = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    price_money = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    order_position = models.CharField(max_length=400, choices=OrderPosition.choices, default=OrderPosition.BASKET)
