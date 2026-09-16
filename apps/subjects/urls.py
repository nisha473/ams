from django.urls import path
from . import subject as views

urlpatterns = [
    path('semesters/<int:semester_id>/subjects/', views.subject_list, name='subject_list'),
    path('semesters/<int:semester_id>/subjects/create/', views.subject_create, name='subject_create'),
    path('update/<int:pk>/', views.subject_update, name='subject_update'),
    path('delete/<int:pk>/', views.subject_delete, name='subject_delete'),
]
