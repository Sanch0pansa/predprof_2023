"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include,  re_path
from django.conf import settings
from django.conf.urls.static import static


ROOT_API_URL = "api/v1/"

urlpatterns = [
    path(ROOT_API_URL, include('API.urls.bot')),
    path(ROOT_API_URL, include('API.urls.checker')),
    path(ROOT_API_URL, include('API.urls.page')),
    path(ROOT_API_URL, include('API.urls.report')),
    path(ROOT_API_URL, include('API.urls.review')),
    path(ROOT_API_URL, include('API.urls.subscription')),
    path(ROOT_API_URL, include('API.urls.user')),
    path(ROOT_API_URL, include('API.urls.moderation')),
    path(ROOT_API_URL, include('API.urls.admin')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)