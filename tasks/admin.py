from django.contrib import admin
from .models import Priority, Category, Task, SubTask, Note


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'deadline', 'priority', 'category']
    list_filter = ['status', 'priority', 'category']
    search_fields = ['title', 'description']


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'parent_task']
    list_filter = ['status']
    search_fields = ['title']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['task', 'created_at']
    search_fields = ['content']