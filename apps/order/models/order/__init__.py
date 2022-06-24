from Distributive.models import Auditable
from django.db import models

from apps.product.models import Product
from apps.user.models.models import BaseModel, User


class Order(BaseModel):
    class OrderPosition(models.TextChoices):
        BASKET = "Basket"
        VERIFICATION = "Verification"
        DELIVERY = "Delivery"
        FINISH = "Finish"

    class MoneyPaid(models.TextChoices):
        NOT_PAID = "not_paid"
        ORPHAN_PAID = "orphan_paid"
        FULL_PAID = "full_paid"

    pharmacy_name = models.CharField(max_length=30, null=True, blank=True)
    customer_name = models.CharField(max_length=300, null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='order_seller', null=True, blank=True)
    lot = models.CharField(max_length=400, null=True, blank=True)
    lon = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=False, blank=False)
    paid_price = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    paid_position = models.CharField(max_length=30, choices=MoneyPaid.choices, default=MoneyPaid.NOT_PAID)
    order_position = models.CharField(max_length=400, choices=OrderPosition.choices, default=OrderPosition.BASKET)

    def __str__(self):
        return self.customer_name


class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_product')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product')
    count = models.IntegerField(default=1)
    price = models.FloatField(default=0)

    @property
    def total_price(self):
        return self.price * self.count

    def __str__(self):
        return f"{self.product.name} {self.order.customer_name}"
