# Generated by Django 4.1.5 on 2024-04-14 12:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0074_alter_builty_expense_entry_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='builty_expense',
            name='entry_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='fund',
            name='entry_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
