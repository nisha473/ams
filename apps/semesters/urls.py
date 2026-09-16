from django.urls import path
from . import semester as views

urlpatterns = [
    path('programs/<int:program_id>/semesters/', views.semester_list, name='semester_list'),
    path('programs/<int:program_id>/semesters/create/', views.semester_create, name='semester_create'),
    path('semesters/update/<int:pk>/', views.semester_update, name='semester_update'),
    path('semesters/delete/<int:pk>/', views.semester_delete, name='semester_delete'),
]
