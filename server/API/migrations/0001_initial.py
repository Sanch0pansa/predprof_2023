# Generated by Django 3.2.9 on 2023-01-11 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]