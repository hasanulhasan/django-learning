from django.contrib.auth.forms import UserCreationForm
from users.forms import RegistrationForm, CustomRegistrationForm, AssignedRoleForm, CreateGroupForm
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
# from django.contrib.auth.forms import AuthenticationForm
from users.forms import CustomLoginForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

def sign_up(request):
    if request.method == 'GET':
        form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # print(f"User data: {user}")
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False  # User is inactive until they activate their account
            user.save()
            messages.success(request, 'Registration successful! Please check your email to activate your account.')            
            # form.save()
            return redirect('sign-in')
        else:
            print("Form is not valid")
    return render(request, 'registration/signup.html', {"form": form})

def sign_in(request):
    form = CustomLoginForm()    
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/home')
    return render(request, 'registration/login.html', {"form": form})

# previous sign in
# def sign_in(request):
#     form = AuthenticationForm()    
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
#             return redirect('/home')
#         else:
#             return render(request, 'registration/login.html', {"error": "Invalid credentials"})
#     return render(request, 'registration/login.html')

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/home')

def activate_user(request, user_id, token):    
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully!')
            return redirect('sign-in')
        else:
            return HttpResponse("Activation link is invalid or has expired.")
    except User.DoesNotExist:
        return HttpResponse("User does not exist")

def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin/dashboard.html', {'users': users})

def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignedRoleForm()
    if request.method == 'POST':
        form = AssignedRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user.groups.clear()  # Clear existing roles
            user.groups.add(role)  # Assign new role
            user.save()
            messages.success(request, f"Role '{role.name}' assigned to {user.username}.")
            return redirect('admin-dashboard')
    else:
        form = AssignedRoleForm()
    return render(request, 'admin/assign_role.html', {'form': form, 'user': user})

def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{group.name}' created successfully.")
            return redirect('admin-dashboard')
    return render(request, 'admin/create_group.html', {'form': form})

def group_list(request):
    groups = User.objects.all()
    return render(request, 'admin/group_list.html', {'groups': groups})