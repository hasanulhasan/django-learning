from django.urls import path
from task.views import dashboard, manager_dashboard, user_dashboard, create_task, view_tasks, tasks_with_filter, update_task

urlpatterns = [
    path('dashboard/', dashboard),
    path('manager-dashboard/', manager_dashboard),
    path('user-dashboard/', user_dashboard, name='user-dashboard'),
    path('create-task/', create_task, name='create-task'),
    path('view_task/', view_tasks),
    path('filter_task', tasks_with_filter),
    path('update-task/<int:id>/', update_task, name='update-task'),
]
