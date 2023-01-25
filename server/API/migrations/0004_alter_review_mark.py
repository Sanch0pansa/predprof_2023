# Generated by Django 4.1.5 on 2023-01-24 20:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_remove_user_login_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='mark',
            field=models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
    ]
