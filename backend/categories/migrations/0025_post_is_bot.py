# Generated by Django 3.2.20 on 2023-11-03 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0024_auto_20231014_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_bot',
            field=models.BooleanField(default=False),
        ),
    ]
