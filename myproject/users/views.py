from django.contrib.auth.forms import UserCreationForm
from users.forms import RegistrationForm, CustomRegistrationForm
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render, redirect

def sign_up(request):
    if request.method == 'GET':
        form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'registration/signup_success.html')
        
    return render(request, 'registration/signup.html', {"form": form})

def sign_in(request):    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            return render(request, 'registration/login.html', {"error": "Invalid credentials"})
    return render(request, 'registration/login.html')

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/home')