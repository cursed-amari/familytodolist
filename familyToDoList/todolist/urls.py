from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('add_task/', views.add_task, name='add_task'),
    path('add_subtask/<int:task_id>/', views.add_subtask, name='add_subtask'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('toggle_task_completion/<int:task_id>/', views.toggle_task_completion, name='toggle_task_completion'),
    path('', views.view_tasks, name='todolist'),
]