# Generated by Django 4.1.5 on 2023-01-29 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_check_check_status_alter_page_moderated_by_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='publicated',
            new_name='published_at',
        ),
        migrations.AlterField(
            model_name='user',
            name='telegram_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
