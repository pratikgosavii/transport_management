# Generated by Django 4.1.5 on 2024-04-13 07:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0066_alter_fund_entry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fund',
            name='entry_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
