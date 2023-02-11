from rest_framework import generics
from API.models import User
from API.serializers.user import UserSerializer
from API.permissions import IsAdmin
from django.db.models import Q
from django.http import JsonResponse
from API.funcs import getData


class StaffUsers(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    serializer_class = UserSerializer

    def get(self, request):
        try:
            users = User.objects.filter(Q(role=1) | Q(role=2)).values('id', 'username', 'role')
            result = []
            for i in users:
                if i['role'] == 1:
                    is_admin = True
                else:
                    is_admin = False
                result.append({'id': i['id'],
                               'username': i['username'],
                               'is_admin': is_admin})
            return JsonResponse(result, safe=False)
        except Exception:
            return JsonResponse({'detail': 'Exception'}, status=404)

    def post(self, request, id):
        try:
            data = getData(request)
            if data['rights'] == 'user':
                User.objects.filter(id=id).update(role=3, is_staff=False, is_superuser=False)
            elif data['rights'] == 'moderator':
                User.objects.filter(id=id).update(role=2, is_staff=True, is_superuser=False)
            elif data['rights'] == 'admin':
                User.objects.filter(id=id).update(role=1, is_staff=True, is_superuser=True)
            return JsonResponse({'success': True})
        except Exception as ex:
            return JsonResponse({'success': False}, status=404)


class UserSearch(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    serializer_class = UserSerializer

    def get(self, request, username):
        try:
            users = list(User.objects.filter(username__icontains=username, role=3).values('id', 'username'))
            return JsonResponse(users, safe=False)
        except Exception as ex:
            return JsonResponse({'success': False}, status=404)
