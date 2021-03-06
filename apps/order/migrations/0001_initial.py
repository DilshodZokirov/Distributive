# Generated by Django 4.0.5 on 2022-06-20 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('pharmacy_name', models.CharField(blank=True, max_length=30, null=True)),
                ('customer_name', models.CharField(blank=True, max_length=300, null=True)),
                ('lot', models.CharField(blank=True, max_length=400, null=True)),
                ('lon', models.CharField(blank=True, max_length=300, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('price_money', models.FloatField(blank=True, null=True)),
                ('total_price', models.FloatField(blank=True, null=True)),
                ('order_position', models.CharField(choices=[('Basket', 'Basket'), ('Verification', 'Verification'), ('Delivery', 'Delivery'), ('Finish', 'Finish')], default='Basket', max_length=400)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
