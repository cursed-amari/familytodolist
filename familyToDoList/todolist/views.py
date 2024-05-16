from django.shortcuts import render
from .models import ToDoListModel


def view_tasks(request):
    user = request.user
    personal_tasks = ToDoListModel.objects.filter(created_by=user, task_type='personal')
    # shared_tasks = ToDoListModel.objects.filter(task_type='shared', shared_with__user=user)
    context = {
        'personal_tasks': personal_tasks,
        # 'shared_tasks': shared_tasks,
    }
    return render(request, 'todolist/todolist.html', context)
