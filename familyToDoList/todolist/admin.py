from django.contrib import admin
from .models import *


@admin.register(ToDoListModel)
class ToDoListModelAdmin(admin.ModelAdmin):
    # list_display = ["user", "user_img", "bio"]
    ...


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    ...


@admin.register(TaskShare)
class TaskShareAdmin(admin.ModelAdmin):
    ...