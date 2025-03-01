# Generated by Django 4.2.13 on 2024-06-01 16:28

import categories.models.Category
import categories.models.Competition
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('key', models.CharField(max_length=100, unique=True)),
                ('oftype', models.CharField(choices=[('TEXT', 'Text'), ('IMAGETEXT', 'Image and Text'), ('IMAGE', 'Image')], default='IMAGETEXT', max_length=100)),
                ('image', models.ImageField(default='', upload_to=categories.models.Category.custom_upload_to)),
                ('order', models.PositiveIntegerField(default=0)),
                ('hide', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('last_date', models.DateField()),
                ('key', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(default='', upload_to=categories.models.Competition.custom_path)),
                ('points', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Winner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('won_by_likes', models.IntegerField()),
                ('position', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3')])),
                ('points', models.PositiveBigIntegerField()),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='categories.competition')),
            ],
        ),
    ]
