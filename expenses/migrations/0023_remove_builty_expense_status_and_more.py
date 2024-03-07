# Generated by Django 4.1.5 on 2024-03-03 20:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expenses', '0022_alter_builty_expense_entry_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='builty_expense',
            name='status',
        ),
        migrations.RemoveField(
            model_name='other_expense',
            name='status',
        ),
        migrations.RemoveField(
            model_name='truck_expense',
            name='status',
        ),
        migrations.AlterField(
            model_name='builty_expense',
            name='entry_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 3, 3, 20, 44, 7, 323920, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='fund',
            name='entry_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 3, 3, 20, 44, 7, 323920, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='other_expense',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 3, 20, 44, 7, 323920, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='salary',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 3, 20, 44, 7, 323920, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='truck_expense',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 3, 20, 44, 7, 323920, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='bank_expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('note', models.CharField(max_length=500)),
                ('expense_date', models.DateTimeField()),
                ('payment_date', models.DateTimeField()),
                ('entry_date', models.DateTimeField(default=datetime.datetime(2024, 3, 3, 20, 44, 7, 323920, tzinfo=datetime.timezone.utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]