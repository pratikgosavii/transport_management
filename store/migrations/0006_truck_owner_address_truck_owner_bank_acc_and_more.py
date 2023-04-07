# Generated by Django 4.1.5 on 2023-04-06 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_remove_truck_owner_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='truck_owner',
            name='address',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='truck_owner',
            name='bank_acc',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='truck_owner',
            name='pan_card',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='truck_owner',
            name='owner_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]