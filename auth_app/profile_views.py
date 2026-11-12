from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .profile_forms import UserProfileUpdateForm

@login_required
def profile_view(request):
    """
    Dedicated Profile Overview View.
    Displays user metadata and identity verification status.
    """
    return render(request, 'auth_app/profile.html', {
        'profile': request.user.profile,
        'user': request.user,
        'title': 'My Profile'
    })

@login_required
def edit_profile_view(request):
    """
    Dedicated Profile Edit View.
    Allows changing personal and contact information.
    """
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile details have been updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Failed to update profile. Please verify all inputs.")
    else:
        form = UserProfileUpdateForm(instance=profile)

    return render(request, 'auth_app/edit_profile.html', {
        'form': form,
        'title': 'Edit Profile'
    })

