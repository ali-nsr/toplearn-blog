from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout

# Create your views here.

User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(first_name=form.cleaned_data['first_name_form'], last_name=form.cleaned_data['last_name_form'],
                        email=form.cleaned_data['email_form'],
                        password=form.cleaned_data['confirm_password_form'])
            user.is_active = True
            user.role = 'simple_user'
            user.save()
            messages.success(request, 'your account created successfully.')
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/register_page.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email_form'], password=form.cleaned_data['password_form'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully')
                return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/login_page.html', context)


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'you logged out')
        return redirect('accounts:login')
