from django.urls import path, include
from django.contrib import admin
from apps.api import api as views
from apps.attendances import attendance as views
from apps.programs import program as views
from apps.semesters import semester as views
from apps.subjects import subject as views

urlpatterns = [
      path("", include('apps.api.urls') ),
      path("attendance/", include('apps.attendances.urls') ),
      path("program/", include('apps.programs.urls') ),
      path("semester/", include('apps.semesters.urls') ),
      path("subject/", include('apps.subjects.urls') ),
]

admin.site.site_url = None
admin.site.site_header = 'NCMT'
