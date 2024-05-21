from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('add_task/', views.add_task, name='add_task'),
    path('add_subtask/<int:task_id>/', views.add_subtask, name='add_subtask'),
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('toggle_main_task_completion/<int:task_id>/', views.toggle_main_task_completion,
         name='toggle_main_task_completion'),
    path('toggle_subtask_completion/<int:subtask_id>/', views.toggle_subtask_completion,
         name='toggle_subtask_completion'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit_subtask/<int:subtask_id>/', views.edit_subtask, name='edit_subtask'),
    path('delete_subtask/<int:subtask_id>/', views.delete_subtask, name='delete_subtask'),
    path('edit_shared_task/<int:task_id>/', views.edit_shared_task, name='edit_shared_task'),
    path('delete_shared_task/<int:task_id>/', views.delete_shared_task, name='delete_shared_task'),
    path('edit_shared_subtask/<int:subtask_id>/', views.edit_shared_subtask, name='edit_shared_subtask'),
    path('delete_shared_subtask/<int:subtask_id>/', views.delete_shared_subtask, name='delete_shared_subtask'),
    path('', views.view_tasks, name='todolist'),
]