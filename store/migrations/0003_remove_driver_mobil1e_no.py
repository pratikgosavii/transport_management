# Generated by Django 4.1.5 on 2023-04-02 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_driver_mobil1e_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='mobil1e_no',
        ),
    ]
