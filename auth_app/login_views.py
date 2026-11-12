from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .login_forms import UserLoginForm

def login_view(request):
    """
    Dedicated User Login View.
    Authenticates user credentials, sets session cookie, and redirects.
    """
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next', 'profile')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password. Please verify and try again.")
    else:
        form = UserLoginForm()

    return render(request, 'auth_app/login.html', {
        'form': form,
        'title': 'Sign In'
    })

