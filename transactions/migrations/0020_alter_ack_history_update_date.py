# Generated by Django 4.1.5 on 2024-03-03 20:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0019_alter_ack_history_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ack_history',
            name='update_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 3, 3, 20, 59, 19, 379889, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
