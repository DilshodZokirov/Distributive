# Generated by Django 4.0.5 on 2022-06-23 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_alter_order_client_phone_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='client_phone_number',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_position',
            field=models.CharField(choices=[('Basket', 'Basket'), ('Verification', 'Verification'), ('Delivery', 'Delivery'), ('Finish', 'Finish')], default='Basket', max_length=400),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=50),
        ),
    ]