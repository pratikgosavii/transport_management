# Generated by Django 4.1.5 on 2023-03-18 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_driver_driving_licence'),
    ]

    operations = [
        migrations.AddField(
            model_name='truck_owner',
            name='pan_card',
            field=models.CharField(blank=True, max_length=120, null=True, unique=True),
        ),
    ]