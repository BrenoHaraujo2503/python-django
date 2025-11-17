from django.urls import path
from . import views
from . import api_views

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_task, name='create'),
    path('<int:pk>/edit/', views.edit_task, name='edit'),
    path('<int:pk>/delete/', views.delete_task, name='delete'),
    path('<int:pk>/toggle/', views.toggle_complete, name='toggle'),

    path('api/tasks/', api_views.task_list_create, name='api_tasks'),
    path('api/tasks/<int:pk>/', api_views.task_detail, name='api_task_detail'),
    path('api/tasks/<int:pk>/toggle/', api_views.task_toggle, name='api_task_toggle'),
]
