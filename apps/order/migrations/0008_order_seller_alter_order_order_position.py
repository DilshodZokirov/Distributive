# Generated by Django 4.0.5 on 2022-06-23 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0007_alter_order_order_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_seller', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_position',
            field=models.CharField(choices=[('Basket', 'Basket'), ('Verification', 'Verification'), ('Delivery', 'Delivery'), ('Finish', 'Finish')], default='Basket', max_length=400),
        ),
    ]