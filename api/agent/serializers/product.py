from rest_framework import serializers

from apps.product.models import Product


class ProductAllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        # name = models.CharField(max_length=300)
        # category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category")
        # price1 = models.FloatField(null=True, blank=True)
        # price2 = models.FloatField(null=True, blank=True)
        # compound = models.CharField(max_length=5000, null=True)
        # temporarily_unavailable = models.BooleanField(default=False)
        # pictures = models.FileField(upload_to='product', null=True, blank=True)
        # expiration_date = models.DateTimeField()
        # count = models.IntegerField(null=True, blank=True)
        # count_of_product = models.IntegerField(null=True, blank=True)
        model = Product
        fields = [
            'name',
            'price1',
            'price2',
            'compound',
            'pictures'
        ]
