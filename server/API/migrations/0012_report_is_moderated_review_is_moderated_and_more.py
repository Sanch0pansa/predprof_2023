# Generated by Django 4.1.5 on 2023-02-07 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0011_rename_is_publicated_report_is_published_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='is_moderated',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='is_moderated',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='is_checking',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='page',
            name='is_moderated',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='users', to='API.role'),
        ),
    ]
