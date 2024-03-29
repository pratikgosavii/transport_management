# Generated by Django 4.1.5 on 2023-05-07 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0012_driver_driving_licence_expiry_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='expense_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='truck_expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.expense_category')),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.truck_details')),
            ],
        ),
    ]
