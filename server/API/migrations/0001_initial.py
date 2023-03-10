# Generated by Django 4.1.5 on 2023-01-21 18:34

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(blank=True, max_length=256)),
                ('url', models.URLField(max_length=128)),
                ('is_moderated', models.BooleanField(null=True)),
                ('is_checking', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('login', models.EmailField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('username', models.CharField(max_length=32, unique=True)),
                ('telegram_id', models.IntegerField(null=True)),
                ('telegram_verification_code', models.IntegerField(blank=True, default=None, null=True, unique=True)),
                ('telegram_verification_code_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('registred_at', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('role', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='users', to='API.role')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscripted_at', models.DateTimeField(auto_now_add=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='API.page')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.SmallIntegerField()),
                ('message', models.CharField(max_length=256)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('publicated', models.DateTimeField(auto_now_add=True)),
                ('added_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('moderated_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='API.page')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=256)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('is_publicated', models.BooleanField()),
                ('added_by_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to=settings.AUTH_USER_MODEL)),
                ('moderated_by_user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='API.page')),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='added_by_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='page',
            name='moderated_by_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checked_at', models.DateTimeField(auto_now_add=True)),
                ('response_status_code', models.CharField(max_length=3)),
                ('response_time', models.SmallIntegerField()),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='API.page')),
            ],
        ),
    ]
