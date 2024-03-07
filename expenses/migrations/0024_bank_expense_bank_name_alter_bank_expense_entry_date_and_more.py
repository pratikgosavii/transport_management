# Generated by Django 4.1.5 on 2024-03-03 20:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0023_remove_builty_expense_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank_expense',
            name='bank_name',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bank_expense',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 3, 20, 46, 20, 134220, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='builty_expense',
            name='entry_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 3, 3, 20, 46, 20, 134220, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='fund',
            name='entry_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 3, 3, 20, 46, 20, 134220, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='other_expense',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 3, 20, 46, 20, 134220, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='salary',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 3, 20, 46, 20, 134220, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='truck_expense',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 3, 20, 46, 20, 134220, tzinfo=datetime.timezone.utc)),
        ),
    ]