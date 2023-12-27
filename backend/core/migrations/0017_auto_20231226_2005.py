# Generated by Django 3.2.23 on 2023-12-26 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20231206_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='coinactivity',
            name='comments',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coinactivity',
            name='status',
            field=models.CharField(choices=[('Q', 'Pending'), ('S', 'Success'), ('F', 'Failed')], default='Q', max_length=1),
        ),
        migrations.AlterField(
            model_name='coinactivity',
            name='type',
            field=models.CharField(choices=[('PARPTN', 'Participation'), ('CPARTN', 'Competition Participation'), ('CWINER', 'Competition Winner'), ('SIGNUP', 'SignUp'), ('REDEEM', 'Redeem')], max_length=100),
        ),
    ]
