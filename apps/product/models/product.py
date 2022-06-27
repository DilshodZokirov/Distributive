from django.db import models
from Distributive.models import Auditable
from apps.user.models import Company
from apps.user.models.models import BaseModel


class Category(models.Model):
    name = models.CharField(max_length=300, unique=True)
    category_image = models.FileField(upload_to='category', null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='order_category')

    def __str__(self):
        return f"{self.name}"


class Product(Auditable):
    name = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category")
    price1 = models.FloatField(null=True, blank=True)
    price2 = models.FloatField(null=True, blank=True)
    compound = models.CharField(max_length=5000, null=True)
    temporarily_unavailable = models.BooleanField(default=False)
    pictures = models.FileField(upload_to='product', null=True, blank=True)
    expiration_date = models.DateTimeField()
    count = models.IntegerField(null=True, blank=True)
    count_of_product = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


# class OrderProduct(BaseModel):
    # order_id = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='rel_order')
    # product_id = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='rel_product')
    # count = models.IntegerField(default=1)
    #
    # def __str__(self):
    #     return f"{self.order_id.customer_name} - {self.product_id.name}"
