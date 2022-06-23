# Generated by Django 4.0.5 on 2022-06-20 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps_user', '0002_user_profile_pic_alter_role_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=400)),
            ],
        ),
        migrations.AlterField(
            model_name='role',
            name='type',
            field=models.CharField(choices=[('office_manager', 'Office Manager'), ('agent', 'Agent'), ('manager', 'Manager'), ('delivery', 'Delivery')], default='delivery', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=13, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='apps_user.company'),
        ),
    ]
