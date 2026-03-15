from django import forms
from .models import Task, SubTask, Note, Category, Priority

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status', 'priority', 'category']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'status', 'parent_task']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['task', 'content']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = ['name']