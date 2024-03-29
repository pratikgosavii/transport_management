# Generated by Django 4.1.5 on 2024-02-16 23:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0010_alter_builty_expense_date_alter_other_expense_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='builty_expense',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 17, 4, 36, 27, 262555)),
        ),
        migrations.AlterField(
            model_name='other_expense',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 17, 4, 36, 27, 264588)),
        ),
        migrations.AlterField(
            model_name='salary',
            name='salary_paid_on',
            field=models.DateField(default=datetime.datetime(2024, 2, 17, 4, 36, 27, 263591)),
        ),
        migrations.AlterField(
            model_name='truck_expense',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 17, 4, 36, 27, 262555)),
        ),
    ]
