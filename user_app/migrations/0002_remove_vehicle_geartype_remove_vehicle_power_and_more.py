# Generated by Django 4.2.5 on 2023-10-17 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='geartype',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='power',
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='mileagae',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
