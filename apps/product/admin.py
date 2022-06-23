from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.product.models import Product, Category


@admin.register(Product)
class ModelProduct(ModelAdmin):
    list_display = ['id', 'name', 'price1', 'price2']


@admin.register(Category)
class ModelCategory(ModelAdmin):
    list_display = ['id', 'name']
