# Generated by Django 4.1.5 on 2024-03-06 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_district_name_alter_from_station_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taluka',
            name='name',
            field=models.CharField(max_length=120),
        ),
    ]
