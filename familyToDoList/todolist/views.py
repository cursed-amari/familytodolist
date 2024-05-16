from django.shortcuts import render
from .models import *


def view_tasks(request):
    user = request.user
    personal_tasks = ToDoListModel.objects.filter(created_by=user, task_type='personal')

    # Получение всех общих задач, включая подзадачи
    shared_tasks = TaskShare.objects.filter(user=user)
    shared_task_ids = shared_tasks.values_list('task__id', flat=True)
    shared_subtasks = SubTask.objects.filter(task_id__in=shared_task_ids)

    context = {
        'personal_tasks': personal_tasks,
        'shared_tasks': shared_tasks,
        'shared_subtasks': shared_subtasks,  # Передача общих подзадач в контекст
    }
    return render(request, 'todolist/todolist.html', context)
