# Generated by Django 4.1.5 on 2024-03-04 17:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0022_alter_ack_history_update_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ack_history',
            name='update_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 3, 4, 17, 42, 38, 855863, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
