from django.shortcuts import render
from django.http import HttpResponse
from task.forms import TaskForm
from task.models import Employee, Task

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
    form = TaskForm(employees=employees)  #for get method

    if request.method == 'POST':
        form = TaskForm(request.POST, employees=employees)
        if form.is_valid():
            print(form.cleaned_data)
            data = form.cleaned_data
            title = data.get('title')
            description = data.get('description')
            due_date = data.get('due_date')
            assigned_to = data.get('assigned_to')
            task = Task.objects.create(
                title=title,
                description=description,
                due_date=due_date,
            )
            for emp_id in assigned_to:
                employee = Employee.objects.get(id=emp_id)
                task.assigned_to.add(employee)
            # task.save()
            return HttpResponse("<h1 style='color: green'>Task created successfully</h1>")
    context = {
        'form': form
    }
    return render(request, "task_form.html", context)