# Generated by Django 4.1.5 on 2024-04-11 16:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0070_alter_ack_history_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ack_history',
            name='update_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 4, 11, 16, 6, 51, 210280, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]