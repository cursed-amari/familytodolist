from django import forms
from .models import ToDoListModel, SubTask


class ToDoListForm(forms.ModelForm):
    class Meta:
        model = ToDoListModel
        fields = ['title', 'task_type', 'context', 'complexity', 'run_time']


class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'context', 'complexity', 'run_time', 'completed']
