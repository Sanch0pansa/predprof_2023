from django.urls import path
from API.views import admin

urlpatterns = [
    path('admin/staff_users/', admin.StaffUsers.as_view()),
    path('admin/change_user_rights/<int:id>/', admin.StaffUsers.as_view()),
    path('admin/search_user/<str:username>/', admin.UserSearch.as_view())
]
