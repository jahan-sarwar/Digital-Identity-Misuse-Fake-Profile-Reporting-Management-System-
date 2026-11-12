from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

def logout_view(request):
    """
    Dedicated Session Logout View.
    Terminates the user's active session and redirects to login.
    """
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('login')

