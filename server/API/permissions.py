from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.user.role_id
        is_superuser = request.user.is_superuser
        if role == 1 and is_superuser:
            return True
        else:
            return False


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.user.role_id
        is_staff = request.user.is_staff
        if (role == 1 or role == 2) and is_staff:
            return True
        else:
            return False
