# Generated by Django 4.0.5 on 2022-06-23 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_remove_order_client_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_position',
            field=models.CharField(choices=[('Basket', 'Basket'), ('Verification', 'Verification'), ('Delivery', 'Delivery'), ('Finish', 'Finish')], default='Basket', max_length=400),
        ),
    ]
