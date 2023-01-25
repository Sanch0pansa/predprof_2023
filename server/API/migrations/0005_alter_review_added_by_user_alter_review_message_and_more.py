# Generated by Django 4.1.5 on 2023-01-24 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_alter_review_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='added_by_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='message',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='review',
            name='moderated_by_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='publicated',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]