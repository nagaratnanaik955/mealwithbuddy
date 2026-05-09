from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib import messages

from django.contrib.auth.decorators import user_passes_test

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"DEBUG: Attempting login for {username}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"DEBUG: Login successful for {username}")
            return redirect('user_home')
        else:
            print(f"DEBUG: Login failed for {username}")
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')
