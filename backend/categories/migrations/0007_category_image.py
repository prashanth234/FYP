# Generated by Django 3.2.18 on 2023-04-21 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0006_auto_20230411_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='', upload_to='categories/'),
        ),
    ]
