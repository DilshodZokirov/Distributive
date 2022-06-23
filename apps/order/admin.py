from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.order.models import Order


@admin.register(Order)
class ModelOrder(ModelAdmin):
    list_display = ['id', 'pharmacy_name', 'customer_name', 'phone_number']
