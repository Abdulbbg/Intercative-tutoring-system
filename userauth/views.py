from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            reg_number = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=reg_number, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.name}!")
                return redirect('course:course-selection')  # Redirect to the home page or dashboard after login
            else:
                messages.error(request, "Invalid registration number or password.")
        else:
            messages.error(request, "Invalid registration number or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})