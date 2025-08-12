from django.contrib import admin
from task.models import Task, TaskDetails , Project, Employee
# Register your models here.

admin.site.register(Task)
admin.site.register(TaskDetails)
admin.site.register(Employee)
admin.site.register(Project)