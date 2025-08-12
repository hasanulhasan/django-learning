from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from users.forms import RegistrationForm, CustomRegistrationForm

def sign_up(request):
    if request.method == 'GET':
        form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'registration/signup_success.html')
        
    return render(request, 'registration/signup.html', {"form": form})