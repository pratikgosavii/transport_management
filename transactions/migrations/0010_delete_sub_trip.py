# Generated by Django 4.1.5 on 2023-04-15 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0009_alter_builty_delivery_no'),
    ]

    operations = [
        migrations.DeleteModel(
            name='sub_trip',
        ),
    ]
