from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Task
from .forms import TaskForm

def dashboard(request):
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='Completed').count()
    pending_tasks = Task.objects.filter(status='Pending').count()
    current_year = timezone.now().year
    tasks_this_year = Task.objects.filter(created_at__year=current_year).count()

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'tasks_this_year': tasks_this_year,
    }
    return render(request, 'tasks/dashboard.html', context)


def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


def task_create(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('task_list')
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Add Task'})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('task_list')
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task'})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})