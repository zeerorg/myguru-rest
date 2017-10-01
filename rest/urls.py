from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from rest_framework.authtoken import views as auth_views

from main import views as main_views
from rest import settings

urlpatterns = [
    url(r'^api-token-auth/', auth_views.obtain_auth_token),
    url(r'^api/get_student/', main_views.StudentView.as_view()),
    url(r'^api/get_teacher/', main_views.TeacherView.as_view()),
    url(r'^api/topic/', main_views.TopicView.as_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^register/student', main_views.StudentRegisterView.as_view()),
    url(r'^register/teacher', main_views.TeacherRegisterView.as_view()),
    url(r'^admin', admin.site.urls),
    url(r'^', main_views.main_page),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)