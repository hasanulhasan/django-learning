from django.urls import path
from task.views import dashboard, manager_dashboard, user_dashboard, create_task, view_tasks

urlpatterns = [
    path('dashboard/', dashboard),
    path('manager-dashboard/', manager_dashboard),
    path('user-dashboard/', user_dashboard),
    path('create-task/', create_task),
    path('view_task/', view_tasks)
]
