# Generated by Django 4.1.5 on 2024-03-03 20:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0014_builty_voucher_payment_bank_ac_ifsc_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ack_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challan_number', models.CharField(max_length=50)),
                ('challan_date', models.DateField(blank=True, null=True)),
                ('update_date', models.DateField(blank=True, default=datetime.datetime(2024, 3, 3, 20, 20, 50, 693281, tzinfo=datetime.timezone.utc), null=True)),
                ('builty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='have_ack3434', to='transactions.builty')),
            ],
        ),
    ]
