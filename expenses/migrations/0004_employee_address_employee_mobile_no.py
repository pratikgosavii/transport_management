# Generated by Django 4.1.5 on 2023-07-09 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0003_employee_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='address',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='mobile_no',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
