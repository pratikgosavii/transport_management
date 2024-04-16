# Generated by Django 4.1.5 on 2024-04-09 04:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0059_alter_ack_history_update_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='builty',
            name='voucher_payment_bank_ac_ifsc',
        ),
        migrations.RemoveField(
            model_name='builty',
            name='voucher_payment_bank_ac_no',
        ),
        migrations.RemoveField(
            model_name='builty',
            name='voucher_payment_mode',
        ),
        migrations.RemoveField(
            model_name='builty',
            name='voucher_payment_status',
        ),
        migrations.AddField(
            model_name='ack',
            name='voucher_payment_bank_ac_ifsc',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ack',
            name='voucher_payment_bank_ac_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ack',
            name='voucher_payment_mode',
            field=models.CharField(blank=True, choices=[('cash', 'cash'), ('online', 'online')], default='cash', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='ack',
            name='voucher_payment_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ack_history',
            name='update_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 4, 9, 4, 55, 31, 9824, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]