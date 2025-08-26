from django.contrib import admin
from task.models import Task, TaskDetails , Project

admin.site.register(Task)
admin.site.register(TaskDetails)
admin.site.register(Project)