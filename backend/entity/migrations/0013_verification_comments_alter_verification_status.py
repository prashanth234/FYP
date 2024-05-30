# Generated by Django 4.2.13 on 2024-05-29 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entity', '0012_entity_updated_at_alter_verification_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='verification',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='verification',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('INVAILD', 'Invalid'), ('SUCCESS', 'Success')], default='PENDING', max_length=100),
        ),
    ]
