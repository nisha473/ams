from django.urls import path
from . import program as views

urlpatterns = [
    path('', views.program_list, name='program_list'),
    path('create/', views.program_create, name='program_create'),
    path('<int:pk>/edit/', views.program_update, name='program_update'),
    path('<int:pk>/delete/', views.program_delete, name='program_delete'),
    path('<int:pk>/toggle/', views.program_toggle_active, name='program_toggle_active'),
]
