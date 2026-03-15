from django.shortcuts import render
from .models import Task
from django.utils import timezone

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