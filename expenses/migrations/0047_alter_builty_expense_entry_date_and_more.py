# Generated by Django 4.1.5 on 2024-03-20 08:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0046_alter_builty_expense_entry_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='builty_expense',
            name='entry_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 3, 20, 8, 42, 22, 905347, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='diesel_expense',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 8, 42, 22, 905347, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='fund',
            name='entry_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 3, 20, 8, 42, 22, 905347, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='other_expense',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 8, 42, 22, 905347, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='salary',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 8, 42, 22, 905347, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='transfer_fund',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 8, 42, 22, 905347, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='truck_diesel_expense',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 8, 42, 22, 905347, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='truck_expense',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 8, 42, 22, 905347, tzinfo=datetime.timezone.utc)),
        ),
    ]
