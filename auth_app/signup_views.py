from django.shortcuts import render, redirect
from django.contrib import messages
from .signup_forms import UserSignUpForm

def signup_view(request):
    """
    Dedicated User Registration View.
    Processes user registration and automatically links a UserProfile.
    """
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Welcome {user.username}! Your account has been registered. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Registration could not be completed. Please fix the highlighted errors.")
    else:
        form = UserSignUpForm()

    return render(request, 'auth_app/signup.html', {
        'form': form,
        'title': 'Sign Up'
    })

