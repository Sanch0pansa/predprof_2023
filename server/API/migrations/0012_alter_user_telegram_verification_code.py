# Generated by Django 4.1.5 on 2023-01-14 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0011_alter_user_telegram_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telegram_verification_code',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
