from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

#  https://docs.djangoproject.com/en/3.2/topics/db/models/
#  python manage.py makemigrations
#  python manage.py migrate

class Role(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=32)


class User(AbstractUser):
    email = models.EmailField(max_length=128, unique=True)
    password = models.CharField(validators=[MinLengthValidator(8)], max_length=128)
    username = models.CharField(max_length=128, unique=True)
    telegram_id = models.IntegerField(null=True, blank=True, unique=True)
    telegram_verification_code = models.IntegerField(blank=True, default=None, null=True, unique=True)
    telegram_verification_code_date = models.DateTimeField(blank=True, default=None, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_DEFAULT, default=3, related_name='users')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

class Page(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True)
    url = models.URLField(max_length=128)
    added_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pages')
    is_moderated = models.BooleanField(null=True, default=None, blank=True)
    moderated_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagesm')
    is_checking = models.BooleanField(default=False)


class Report(models.Model):
    added_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reports')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='reports')
    message = models.CharField(max_length=256)
    added_at = models.DateTimeField()
    is_moderated = models.BooleanField(null=True, default=None, blank=True)
    moderated_by_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None, related_name='+')
    is_published = models.BooleanField(default=False)


class Check(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='checks')
    checked_at = models.DateTimeField()
    response_status_code = models.CharField(max_length=3)
    response_time = models.PositiveSmallIntegerField()
    check_status = models.CharField(default=3, max_length=1)

class Review(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='reviews')
    mark = models.DecimalField(decimal_places=1, max_digits=2, validators=[MaxValueValidator(5), MinValueValidator(1)])
    message = models.CharField(max_length=256, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    added_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', null=True)
    is_moderated = models.BooleanField(null=True, default=None, blank=True)
    moderated_by_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None, related_name='+')
    is_published = models.BooleanField(default=False)


class Subscription(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='subscriptions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscripted_at = models.DateTimeField(auto_now_add=True)


class CheckReport(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, default=None)
    requested_url = models.CharField(max_length=128)
    ping = models.PositiveSmallIntegerField(null=True, default=None)
    response_status_code = models.CharField(max_length=3)
    response_time = models.PositiveSmallIntegerField(null=True, default=None)
    first_content_loading_time = models.PositiveIntegerField(null=True, default=None)
    first_meaningful_content_loading_time = models.PositiveIntegerField(null=True, default=None)
    largest_content_loading_time = models.PositiveIntegerField(null=True, default=None)
    speed_index = models.PositiveIntegerField(null=True, default=None)
    score = models.PositiveSmallIntegerField(null=True, default=None)
    full_page_loading_time = models.PositiveIntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    report_file = models.FileField(upload_to='reports/', null=True, blank=True)

