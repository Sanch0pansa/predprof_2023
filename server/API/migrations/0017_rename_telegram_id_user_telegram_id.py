# Generated by Django 4.1.5 on 2023-01-18 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0016_rename_telegramid_user_telegram_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='telegram_ID',
            new_name='telegram_id',
        ),
    ]
