from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *


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


@login_required
def add_task(request):
    if request.method == 'POST':
        form = ToDoListForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('todolist')  # Предположим, что у вас есть URL с именем 'view_tasks'
    else:
        form = ToDoListForm()
    return render(request, 'todolist/add_task.html', {'form': form})


@login_required
def add_subtask(request, task_id):
    task = get_object_or_404(ToDoListModel, id=task_id)
    if request.method == 'POST':
        form = SubTaskForm(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.task = task
            subtask.save()
            return redirect('todolist')
    else:
        form = SubTaskForm()
    return render(request, 'todolist/add_subtask.html', {'form': form, 'task': task})


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(ToDoListModel, id=task_id)
    if task.created_by == request.user or TaskShare.objects.filter(task=task, user=request.user).exists():
        task.completed = True
        task.save()
    return redirect('view_tasks')


@login_required
def toggle_task_completion(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(ToDoListModel, id=task_id)
        if task.created_by == request.user or TaskShare.objects.filter(task=task, user=request.user).exists():
            task.completed = not task.completed
            task.save()
            return JsonResponse({'success': True, 'completed': task.completed})
    return JsonResponse({'success': False}, status=400)
