# Generated by Django 4.1.5 on 2023-03-18 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_consignor_builty_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='driving_licence',
            field=models.CharField(default='asasaS', max_length=120, unique=True),
            preserve_default=False,
        ),
    ]
