# Generated by Django 4.2.5 on 2023-10-18 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0006_vehicle_created_vehicle_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='model',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='purpose',
            field=models.CharField(max_length=10, null=True),
        ),
    ]