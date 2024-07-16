# Generated by Django 4.2.13 on 2024-06-01 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0001_initial'),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='entity.entity'),
        ),
        migrations.AddField(
            model_name='post',
            name='ispublic',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='postfile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
