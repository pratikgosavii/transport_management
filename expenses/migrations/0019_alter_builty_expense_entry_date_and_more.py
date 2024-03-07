# Generated by Django 4.1.5 on 2024-03-03 12:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0018_remove_fund_employee_fund_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='builty_expense',
            name='entry_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 3, 3, 12, 38, 12, 456026, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='fund',
            name='entry_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 3, 3, 12, 38, 12, 456026, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='other_expense',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 3, 12, 38, 12, 456026, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='salary',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 3, 12, 38, 12, 456026, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='truck_expense',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 3, 12, 38, 12, 456026, tzinfo=datetime.timezone.utc)),
        ),
    ]