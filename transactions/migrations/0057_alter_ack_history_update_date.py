# Generated by Django 4.1.5 on 2024-04-07 09:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0056_alter_ack_history_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ack_history',
            name='update_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 4, 7, 9, 6, 32, 866633, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
