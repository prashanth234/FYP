# Generated by Django 3.2.20 on 2023-08-23 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0015_redeem_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeem',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('R', 'Redeemed')], default='P', max_length=1),
        ),
    ]
