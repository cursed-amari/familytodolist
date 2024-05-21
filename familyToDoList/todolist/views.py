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
        'shared_subtasks': shared_subtasks,
    }
    return render(request, 'todolist/todolist.html', context)


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(ToDoListModel, id=task_id)
    if request.user != task.created_by and not TaskShare.objects.filter(task=task, user=request.user).exists():
        return redirect('todolist')  # или другой обработчик ошибки

    if request.method == 'POST':
        form = ToDoListForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todolist')
    else:
        form = ToDoListForm(instance=task)
    return render(request, 'todolist/edit_task.html', {'form': form, 'task': task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(ToDoListModel, id=task_id)
    if request.user != task.created_by and not TaskShare.objects.filter(task=task, user=request.user).exists():
        return redirect('todolist')  # или другой обработчик ошибки

    if request.method == 'POST':
        task.delete()
        return redirect('todolist')

    return render(request, 'todolist/delete_task.html', {'task': task})


@login_required
def edit_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)
    task = subtask.task
    if request.user != task.created_by and not TaskShare.objects.filter(task=task, user=request.user).exists():
        return redirect('todolist')  # или другой обработчик ошибки

    if request.method == 'POST':
        form = SubTaskForm(request.POST, instance=subtask)
        if form.is_valid():
            form.save()
            return redirect('todolist')
    else:
        form = SubTaskForm(instance=subtask)
    return render(request, 'todolist/edit_subtask.html', {'form': form, 'subtask': subtask})


@login_required
def delete_subtask(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)
    task = subtask.task
    if request.user != task.created_by and not TaskShare.objects.filter(task=task, user=request.user).exists():
        return redirect('view_tasks')  # или другой обработчик ошибки

    if request.method == 'POST':
        subtask.delete()
        return redirect('todolist')

    return render(request, 'todolist/delete_subtask.html', {'subtask': subtask})


@login_required
def edit_shared_task(request, task_id):
    shared_task = get_object_or_404(TaskShare, user=request.user, task_id=task_id)
    if request.method == 'POST':
        form = ToDoListForm(request.POST, instance=shared_task.task)
        if form.is_valid():
            form.save()
            return redirect('todolist')
    else:
        form = ToDoListForm(instance=shared_task.task)
    return render(request, 'todolist/edit_shared_task.html', {'form': form, 'shared_task': shared_task})


@login_required
def delete_shared_task(request, task_id):
    shared_task = get_object_or_404(TaskShare, user=request.user, task_id=task_id)
    if request.method == 'POST':
        shared_task.delete()
        return redirect('todolist')
    return render(request, 'todolist/delete_shared_task.html', {'shared_task': shared_task})


@login_required
def edit_shared_subtask(request, subtask_id):
    shared_subtask = get_object_or_404(SubTask, task__shared_with__user=request.user, id=subtask_id)
    if request.method == 'POST':
        form = SubTaskForm(request.POST, instance=shared_subtask)
        if form.is_valid():
            form.save()
            return redirect('todolist')
    else:
        form = SubTaskForm(instance=shared_subtask)
    return render(request, 'todolist/edit_shared_subtask.html', {'form': form, 'shared_subtask': shared_subtask})


@login_required
def delete_shared_subtask(request, subtask_id):
    shared_subtask = get_object_or_404(SubTask, task__shared_with__user=request.user, id=subtask_id)
    if request.method == 'POST':
        shared_subtask.delete()
        return redirect('todolist')
    return render(request, 'todolist/delete_shared_subtask.html', {'shared_subtask': shared_subtask})


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
    return redirect('todolist')


@login_required
def toggle_task_completion(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(ToDoListModel, id=task_id)
        subtask_id = request.POST.get('subtask_id')
        if subtask_id:
            return toggle_subtask_completion(request, subtask_id)
        else:
            return toggle_main_task_completion(request, task)
    return JsonResponse({'success': False}, status=400)

@login_required
def toggle_main_task_completion(request, task_id):
    task = get_object_or_404(ToDoListModel, id=task_id)
    if task.created_by == request.user or TaskShare.objects.filter(task=task, user=request.user).exists():
        task.completed = not task.completed
        task.save()
        return JsonResponse({'success': True, 'completed': task.completed})
    return JsonResponse({'success': False}, status=403)

@login_required
def toggle_subtask_completion(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)
    if subtask.task.created_by == request.user or TaskShare.objects.filter(task=subtask.task, user=request.user).exists():
        subtask.completed = not subtask.completed
        subtask.save()
        return JsonResponse({'success': True, 'completed': subtask.completed})
    return JsonResponse({'success': False}, status=403)
