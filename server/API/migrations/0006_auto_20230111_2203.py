# Generated by Django 3.2.9 on 2023-01-11 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_alter_page_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='description',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='page',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]