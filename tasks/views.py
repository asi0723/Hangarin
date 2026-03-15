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
    recent_tasks = Task.objects.all().order_by('-created_at')[:5]

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'tasks_this_year': tasks_this_year,
        'recent_tasks': recent_tasks,
    }
    return render(request, 'tasks/dashboard.html', context)


def task_list(request):
    tasks = Task.objects.all()

    # Search
    search = request.GET.get('search', '')
    if search:
        tasks = tasks.filter(
            title__icontains=search
        ) | tasks.filter(
            description__icontains=search
        ) | tasks.filter(
            category__name__icontains=search
        )

    # Sort
    sort = request.GET.get('sort', '-created_at')
    allowed_sorts = ['title', '-title', 'created_at', '-created_at', 
                     'deadline', '-deadline', 'status', '-status']
    if sort in allowed_sorts:
        tasks = tasks.order_by(sort)

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(tasks, 10)  # 10 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
        'sort': sort,
    }
    return render(request, 'tasks/task_list.html', context)


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