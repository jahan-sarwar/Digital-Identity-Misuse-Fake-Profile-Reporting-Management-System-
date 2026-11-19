from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .login_forms import UserLoginForm

# ==============================================================================
# View: login_view (ব্যবহারকারী লগইন ভিউ)
# Authenticates user credentials and enforces Admin Approval verification
# ইউজার পরিচয় যাচাই এবং অ্যাডমিন অনুমোদন প্রাপ্ত কি না তা নিশ্চিত করে লগইন করায়
# ==============================================================================
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_portal')
        return redirect('profile')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Attempt standard authentication / সাধারণ ইউজার প্রমাণীকরণ
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # User authenticated and active / ইউজার সঠিক এবং সক্রিয়
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                
                # Direct staff/administrators directly to the Admin Portal / অ্যাডমিন হলে সরাসরি অ্যাডমিন পোর্টালে রিডাইরেক্ট
                if user.is_staff or user.is_superuser:
                    return redirect('admin_portal')
                
                next_url = request.GET.get('next', 'profile')
                return redirect(next_url)
            else:
                # Check if user exists but is inactive due to pending approval / ইউজার পাসওয়ার্ড সঠিক কিন্তু অ্যাডমিন অনুমোদন বাকি কি না পরীক্ষা
                try:
                    existing_user = User.objects.get(username__iexact=username)
                    if existing_user.check_password(password):
                        profile = getattr(existing_user, 'profile', None)
                        if profile and profile.approval_status == 'PENDING':
                            messages.warning(
                                request,
                                f"Account '{existing_user.username}' is currently PENDING Administrator approval. "
                                f"An administrator must accept your account before you can log in. "
                                f"(আপনার অ্যাকাউন্টটি অ্যাডমিন অনুমোদনের অপেক্ষায় রয়েছে। অ্যাডমিন অনুমোদন দিলে লগইন করতে পারবেন।)"
                            )
                            return render(request, 'auth_app/login.html', {'form': form, 'title': 'Sign In'})
                        elif profile and profile.approval_status == 'REJECTED':
                            messages.error(
                                request,
                                f"Account registration for '{existing_user.username}' was rejected by the administrator. "
                                f"(আপনার অ্যাকাউন্ট আবেদনটি অ্যাডমিন দ্বারা বাতিল করা হয়েছে।)"
                            )
                            return render(request, 'auth_app/login.html', {'form': form, 'title': 'Sign In'})
                except User.DoesNotExist:
                    pass

                messages.error(request, "Invalid username or password. Please verify and try again.")
    else:
        form = UserLoginForm()

    return render(request, 'auth_app/login.html', {
        'form': form,
        'title': 'Sign In'
    })
