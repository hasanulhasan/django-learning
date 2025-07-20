from django.shortcuts import render
from django.http import HttpResponse
from task.forms import TaskForm, TaskModelForm
from task.models import *
from datetime import date

# Create your views here.
def dashboard(request):
    return render(request, "dashboard.html")

def manager_dashboard(request):
    return render(request, "manager-dashboard.html")

def user_dashboard(request):
    return render(request, "user-dashboard.html")

def home(request):
    return render(request, 'home.html')

def contact(request):
    return HttpResponse("<h1 style='color: red'>This is contact page</h1>")

def create_task(request):
    employees = Employee.objects.all()
    form = TaskModelForm()  #for get method

    if request.method == 'POST':
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """For Model Form"""
            form.save()  # This will save the task using the ModelForm
            return render(request, "task_form.html", {'form': form, "message": "Task created successfully"})
        
            """For Django Form"""
            # print(form.cleaned_data)
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')
            # task = Task.objects.create(
            #     title=title,
            #     description=description,
            #     due_date=due_date,
            # )
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            # task.save()
            # return HttpResponse("<h1 style='color: green'>Task created successfully</h1>")
    context = {
        'form': form
    }
    return render(request, "task_form.html", context)

def view_tasks(request):
    #retrieve all tasks from the database
    tasks = Task.objects.all()
    #retrieve specific tasks based on the user type
    task_3 = Task.objects.filter(id=3)
    #fetch the first task
    first_task = Task.objects.first()
    return render(request, "show_task.html", {'tasks': tasks, "task_3": task_3, "first_task": first_task})

def tasks_with_filter(request):
    #showing all pending tasks
    pending_tasks = Task.objects.filter(status='PENDING')
    #showing all task before today
    tasks_before_today = Task.objects.filter(due_date__lt=date.today())
    tasks_today = Task.objects.filter(due_date=date.today())
    #tasks whose priority is high
    high_priority_tasks = TaskDetails.objects.filter(priority='H')
    #tasks whose priority is not low
    not_low_priority_tasks = TaskDetails.objects.exclude(priority='L')
    return render(request, "filter_task.html", {
        'pending_tasks': pending_tasks, 
        "tasks_before_today": tasks_before_today,
        "high_priority_tasks": high_priority_tasks,
        "not_low_priority_tasks": not_low_priority_tasks
        })