# Generated by Django 4.1.5 on 2024-02-16 21:20

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0013_alter_builty_dc_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expenses', '0004_employee_address_employee_mobile_no'),
    ]

    operations = [
        migrations.RenameField(
            model_name='truck_expense',
            old_name='price',
            new_name='amount',
        ),
        migrations.RemoveField(
            model_name='truck_expense',
            name='expense_category',
        ),
        migrations.AddField(
            model_name='salary',
            name='salary_of_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salary',
            name='salary_paid_on',
            field=models.DateField(default=datetime.datetime(2024, 2, 17, 2, 50, 13, 951007)),
        ),
        migrations.AddField(
            model_name='salary',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='truck_expense',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='other_expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('note', models.CharField(max_length=500)),
                ('date', models.DateTimeField()),
                ('paid_on', models.DateField(default=datetime.datetime(2024, 2, 17, 2, 50, 13, 952007))),
                ('expense_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.expense_category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='builty_expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('note', models.CharField(max_length=500)),
                ('builty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.builty')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
