# Generated by Django 3.2.18 on 2023-06-12 19:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0009_alter_post_competition'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='last_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='competition',
            name='points',
            field=models.IntegerField(default=500),
            preserve_default=False,
        ),
    ]
