# Generated by Django 4.1.5 on 2023-01-21 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='registred_at',
        ),
    ]
