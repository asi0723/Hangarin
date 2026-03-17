from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Task, SubTask, Note, Category, Priority
from .forms import TaskForm, SubTaskForm, NoteForm, CategoryForm, PriorityForm


# ─── DASHBOARD ───────────────────────────────────────────
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


# ─── TASK ─────────────────────────────────────────────────
def task_list(request):
    tasks = Task.objects.all()
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    category_filter = request.GET.get('category', '')

    if search:
        tasks = tasks.filter(title__icontains=search) | \
                tasks.filter(description__icontains=search) | \
                tasks.filter(category__name__icontains=search)
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority__id=priority_filter)
    if category_filter:
        tasks = tasks.filter(category__id=category_filter)

    sort = request.GET.get('sort', '-created_at')
    allowed_sorts = ['title', '-title', 'created_at', '-created_at',
                     'deadline', '-deadline', 'status', '-status']
    if sort in allowed_sorts:
        tasks = tasks.order_by(sort)

    paginator = Paginator(tasks, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'search': search,
        'sort': sort,
        'priorities': Priority.objects.all(),
        'categories': Category.objects.all(),
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
    return render(request, 'tasks/task_confirm_delete.html', {'object': task, 'type': 'Task'})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    subtasks = task.subtasks.all()
    notes = task.notes.all()
    return render(request, 'tasks/task_detail.html', {'task': task, 'subtasks': subtasks, 'notes': notes})


# ─── SUBTASK ──────────────────────────────────────────────
def subtask_list(request):
    subtasks = SubTask.objects.all()
    search = request.GET.get('search', '')
    if search:
        subtasks = subtasks.filter(title__icontains=search) | \
                   subtasks.filter(status__icontains=search)
    sort = request.GET.get('sort', '-created_at')
    allowed_sorts = ['title', '-title', 'created_at', '-created_at', 'status', '-status']
    if sort in allowed_sorts:
        subtasks = subtasks.order_by(sort)
    paginator = Paginator(subtasks, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'tasks/subtask_list.html', {'page_obj': page_obj, 'search': search, 'sort': sort})

def subtask_create(request):
    form = SubTaskForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('subtask_list')
    return render(request, 'tasks/generic_form.html', {'form': form, 'title': 'Add SubTask', 'back_url': 'subtask_list'})

def subtask_update(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    form = SubTaskForm(request.POST or None, instance=subtask)
    if form.is_valid():
        form.save()
        return redirect('subtask_list')
    return render(request, 'tasks/generic_form.html', {'form': form, 'title': 'Edit SubTask', 'back_url': 'subtask_list'})

def subtask_delete(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    if request.method == 'POST':
        subtask.delete()
        return redirect('subtask_list')
    return render(request, 'tasks/task_confirm_delete.html', {'object': subtask, 'type': 'SubTask'})


# ─── NOTE ─────────────────────────────────────────────────
def note_list(request):
    notes = Note.objects.all()
    search = request.GET.get('search', '')
    if search:
        notes = notes.filter(content__icontains=search) | \
                notes.filter(task__title__icontains=search)
    paginator = Paginator(notes, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'tasks/note_list.html', {'page_obj': page_obj, 'search': search})

def note_create(request):
    form = NoteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('note_list')
    return render(request, 'tasks/generic_form.html', {'form': form, 'title': 'Add Note', 'back_url': 'note_list'})

def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    form = NoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        return redirect('note_list')
    return render(request, 'tasks/generic_form.html', {'form': form, 'title': 'Edit Note', 'back_url': 'note_list'})

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'tasks/task_confirm_delete.html', {'object': note, 'type': 'Note'})


# ─── CATEGORY ─────────────────────────────────────────────
def category_list(request):
    categories = Category.objects.all()
    search = request.GET.get('search', '')
    if search:
        categories = categories.filter(name__icontains=search)
    paginator = Paginator(categories, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'tasks/category_list.html', {'page_obj': page_obj, 'search': search})

def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'tasks/generic_form.html', {'form': form, 'title': 'Add Category', 'back_url': 'category_list'})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'tasks/generic_form.html', {'form': form, 'title': 'Edit Category', 'back_url': 'category_list'})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'tasks/task_confirm_delete.html', {'object': category, 'type': 'Category'})


# ─── PRIORITY ─────────────────────────────────────────────
def priority_list(request):
    priorities = Priority.objects.all()
    search = request.GET.get('search', '')
    if search:
        priorities = priorities.filter(name__icontains=search)
    paginator = Paginator(priorities, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'tasks/priority_list.html', {'page_obj': page_obj, 'search': search})

def priority_create(request):
    form = PriorityForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('priority_list')
    return render(request, 'tasks/generic_form.html', {'form': form, 'title': 'Add Priority', 'back_url': 'priority_list'})

def priority_update(request, pk):
    priority = get_object_or_404(Priority, pk=pk)
    form = PriorityForm(request.POST or None, instance=priority)
    if form.is_valid():
        form.save()
        return redirect('priority_list')
    return render(request, 'tasks/generic_form.html', {'form': form, 'title': 'Edit Priority', 'back_url': 'priority_list'})

def priority_delete(request, pk):
    priority = get_object_or_404(Priority, pk=pk)
    if request.method == 'POST':
        priority.delete()
        return redirect('priority_list')
    return render(request, 'tasks/task_confirm_delete.html', {'object': priority, 'type': 'Priority'})