from django.contrib import admin
from django.urls import path, include
from task.views import contact
from task.views import home
from core.views import no_permission
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("contact/", contact),
    path("home/", home),
    path("task/", include("task.urls")),
    path("users/", include("users.urls")),
    path("no-permission/", no_permission, name='no-permission')
] + debug_toolbar_urls()
