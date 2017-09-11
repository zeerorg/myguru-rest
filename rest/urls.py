"""rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework.authtoken import views as auth_views

from main import views as main_views
from rest import settings

urlpatterns = [
    url(r'^api-token-auth/', auth_views.obtain_auth_token),
    url(r'^api/get_student/', main_views.get_student),
    url(r'^api/get_teacher/', main_views.get_teacher),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^register/student', main_views.register_student),
    url(r'^register/teacher', main_views.register_teacher),
    url(r'^admin', admin.site.urls),
    url(r'^', main_views.main_page),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)