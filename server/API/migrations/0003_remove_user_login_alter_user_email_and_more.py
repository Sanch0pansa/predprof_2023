# Generated by Django 4.1.5 on 2023-01-21 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_remove_user_registred_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='login',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
