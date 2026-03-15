import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hangarin.settings')
django.setup()

from faker import Faker
from tasks.models import Priority, Category, Task, SubTask, Note

fake = Faker()

# --- Priority (manual) ---
priorities = ['Low', 'Medium', 'High', 'Critical']
for p in priorities:
    Priority.objects.get_or_create(name=p)
print("✅ Priorities created")

# --- Category (manual) ---
categories = ['Work', 'School', 'Personal', 'Finance', 'Projects']
for c in categories:
    Category.objects.get_or_create(name=c)
print("✅ Categories created")

# --- Tasks ---
priority_list = list(Priority.objects.all())
category_list = list(Category.objects.all())
status_choices = ['Pending', 'In Progress', 'Completed']

for _ in range(20):
    Task.objects.create(
        title=fake.sentence(nb_words=5),
        description=fake.paragraph(nb_sentences=3),
        deadline=fake.date_time_this_month(),
        status=fake.random_element(elements=status_choices),
        priority=fake.random_element(elements=priority_list),
        category=fake.random_element(elements=category_list),
    )
print("✅ Tasks created")

# --- SubTasks ---
task_list = list(Task.objects.all())
for _ in range(30):
    SubTask.objects.create(
        title=fake.sentence(nb_words=4),
        status=fake.random_element(elements=status_choices),
        parent_task=fake.random_element(elements=task_list),
    )
print("✅ SubTasks created")

# --- Notes ---
for _ in range(20):
    Note.objects.create(
        task=fake.random_element(elements=task_list),
        content=fake.paragraph(nb_sentences=3),
    )
print("✅ Notes created")

print("\n🎉 All data populated successfully!")