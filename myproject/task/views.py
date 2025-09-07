from django.shortcuts import render, redirect
from django.http import HttpResponse
from task.forms import TaskForm, TaskModelForm, TaskDetailsModelForm
from task.models import *
from datetime import date, timedelta
from django.db.models import Q, Count, Sum, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

# Create your views here.
def dashboard(request):
    return render(request, "dashboard.html")

# @user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    return render(request, "manager-dashboard.html")

def user_dashboard(request):
    type = request.GET.get('type', 'all')
    print(type)

    tasks = Task.objects.select_related('details').prefetch_related('assigned_to').all()

    total_tasks = tasks.count()
    pending_tasks = tasks.filter(status='PENDING').count()
    completed_tasks = tasks.filter(status='COMPLETED').count()
    in_progress_tasks = tasks.filter(status='IN_PROGRESS').count()

    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')

    if type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    else:
        tasks = base_query.all()

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
    }
    return render(request, "user-dashboard.html", context)

def home(request):
    return render(request, 'home.html')

def contact(request):
    return HttpResponse("<h1 style='color: red'>This is contact page</h1>")

@login_required
@permission_required('task.add_task', login_url='no-permission')
def create_task(request):
    # employees = Employee.objects.all()
    form = TaskModelForm()  #for get method

    # task_form = TaskModelForm()
    task_details_form = TaskDetailsModelForm()

    if request.method == 'POST':
        form = TaskModelForm(request.POST)
        task_details_form = TaskDetailsModelForm(request.POST, request.FILES)  # For file uploads

        if form.is_valid() and task_details_form.is_valid():
            """For Model Form"""
            task = form.save()  # This will save the task using the ModelForm
            task_details = task_details_form.save(commit=False)  # Create TaskDetails instance without saving
            task_details.task = task  # Associate the TaskDetails with the Task
            task_details.save()  # Now save the TaskDetails instance
            # return render(request, "task_form.html", {'form': form, "message": "Task created successfully"})
            messages.success(request, "Task created successfully")
            return redirect('create-task')  # Redirect to user dashboard after successful creation
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
    # context = {
    #     'form': form
    # }
    context = {
        'task_form': form,
        'task_details_form': task_details_form
    }
    return render(request, "task_form.html", context)

@login_required
@permission_required('task.change_task', login_url='no-permission')
def update_task(request, id):
    task = Task.objects.get(id=id)
    form = TaskModelForm(instance=task)

    if task.details:
        task_details_form = TaskDetailsModelForm(instance=task.details) 

    if request.method == 'POST':
        form = TaskModelForm(request.POST, instance=task)
        task_details_form = TaskDetailsModelForm(request.POST, instance=task.details)

        if form.is_valid() and task_details_form.is_valid():
            """For Model Form"""
            task = form.save()  # This will save the task using the ModelForm
            task_details = task_details_form.save(commit=False)  # Create TaskDetails instance without saving   
            task_details.task = task  # Associate the TaskDetails with the Task
            task_details.save()  # Now save the TaskDetails instance

            messages.success(request, "Task updated successfully")
            return redirect('update-task', id)  
    context = {
        'task_form': form,
        'task_details_form': task_details_form
    }
    return render(request, "task_form.html", context)

@login_required
@permission_required('task.delete_task', login_url='no-permission')
def delete_task(request, id):
    task = Task.objects.get(id=id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted successfully")
        return redirect('user-dashboard')  # Redirect to user dashboard after deletion
    else:
        messages.error(request, "Something went wrong, please try again.")
        return redirect('user-dashboard') 

@login_required
@permission_required('task.view_task', login_url='no-permission')
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
    #contain a common word in title
    tasks_with_common_word = Task.objects.filter(title__icontains='common')
    #two or more conditions
    tasks_with_conditions = Task.objects.filter(status='PENDING', due_date__lt=date.today())
    #or operator
    tasks_with_or_condition = Task.objects.filter(status='PENDING') | Task.objects.filter(due_date__lt=date.today())
    #get the number of tasks by a specific employee
    employee_id = 1  # Example employee ID 
    tasks_by_employee = Task.objects.filter(assigned_to__id=employee_id)
    #get the most recent assigned task
    most_recent_task = Task.objects.order_by('-created_at').first()
    #Show tasks that have been overdue for more than a week
    overdue_tasks = Task.objects.filter(due_date__lt=date.today() - timedelta(days=7))
    #Show all projects that have no tasks assigned
    projects_with_no_tasks = Project.objects.annotate(task_count=Count('task')).filter(task_count=0)
    #Show all employees working on a specific project
    project_id = 1  # Example project ID
    # employees_on_project = Employee.objects.filter(task__project__id=1).distinct()
    #Show the tasks which are assigned to a specific employee
    specific_employee_tasks = Task.objects.filter(assigned_to__id=1)
    
    return render(request, "filter_task.html", {
        'pending_tasks': pending_tasks, 
        "tasks_before_today": tasks_before_today,
        "high_priority_tasks": high_priority_tasks,
        "not_low_priority_tasks": not_low_priority_tasks
        })

def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES

    if request.method == 'POST':
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)
            
    return render(request, "task_details.html", {'task': task, 'status_choices': status_choices})
