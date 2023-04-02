# Generated by Django 4.1.5 on 2023-04-02 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_driver_mobil1e_no'),
        ('users', '0003_remove_user_office_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='office_location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.office_location'),
            preserve_default=False,
        ),
    ]
