# Generated by Django 4.1.5 on 2023-04-02 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_office_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_joined1',
        ),
    ]
