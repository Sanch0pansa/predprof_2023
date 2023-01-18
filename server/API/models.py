from django.db import models

#  https://docs.djangoproject.com/en/3.2/topics/db/models/
#  python manage.py makemigrations
#  python manage.py migrate


class Role(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=32)


class User(models.Model):
    login = models.EmailField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    telegram_id = models.IntegerField(null=True)
    telegram_verification_code = models.IntegerField(blank=True, default=None, null=True, unique=True)
    telegram_verification_code_date = models.DateTimeField(blank=True, default=None, null=True)
    registred_at = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(Role, on_delete=models.SET_DEFAULT, default=1, to_field='id', related_name='users')


class Page(models.Model):
    added_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pages')
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, blank=True)
    url = models.URLField(max_length=128)
    moderated_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    is_moderated = models.BooleanField(null=True)
    is_checking = models.BooleanField()

class Report(models.Model):
    added_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reports')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='reports')
    message = models.CharField(max_length=256)
    added_at = models.DateTimeField(auto_now_add=True)
    moderated_by_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='+')
    is_publicated = models.BooleanField()


class Check(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='checks')
    checked_at = models.DateTimeField(auto_now_add=True)
    response_status_code = models.CharField(max_length=3)
    response_time = models.SmallIntegerField()


class Review(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='reviews')
    mark = models.SmallIntegerField()
    message = models.CharField(max_length=256)
    added_at = models.DateTimeField(auto_now_add=True)
    added_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    moderated_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    publicated = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='subscriptions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    subscripted_at = models.DateTimeField(auto_now_add=True)