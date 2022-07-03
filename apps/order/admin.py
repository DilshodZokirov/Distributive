from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.order.models import Order
from apps.order.models.order import OrderProduct


@admin.register(Order)
class ModelOrder(ModelAdmin):
    list_display = ['id', 'pharmacy_name', 'seller', 'phone_number']


@admin.register(OrderProduct)
class ModelOrderProduct(ModelAdmin):
    list_display = ['order', 'product']
