# Generated by Django 4.1.5 on 2023-01-24 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_alter_review_added_by_user_alter_review_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='message',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
