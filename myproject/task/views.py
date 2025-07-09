from django.shortcuts import render
from django.http import HttpResponse


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