from django.shortcuts import render, redirect
from django.contrib import messages
from .signup_forms import UserSignUpForm

# ==============================================================================
# View: signup_view (ব্যবহারকারী নিবন্ধন ভিউ)
# Handles new user registration with Admin Approval workflow
# নতুন ব্যবহারকারীর অ্যাকাউন্ট তৈরি করে এবং অ্যাডমিন অনুমোদনের জন্য পেন্ডিং অবস্থায় রাখে
# ==============================================================================
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            # Save new user / নতুন ইউজার ডাটাবেজে সংরক্ষণ
            user = form.save(commit=False)
            
            # Set user as inactive until Admin approves / অ্যাডমিন অনুমোদন না দেওয়া পর্যন্ত একাউন্ট নিষ্ক্রিয় থাকবে
            user.is_active = False
            user.save()

            # Set user profile approval status to PENDING / প্রোফাইলে অনুমোদনের অবস্থা পেন্ডিং সেট করা
            profile = user.profile
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.nid_or_passport = form.cleaned_data.get('nid_or_passport')
            profile.approval_status = 'PENDING'
            profile.save()

            # Inform user about pending admin approval / ব্যবহারকারীকে অ্যাডমিন পর্যালোচনার বিষয়টি জানানো
            messages.success(
                request,
                f"Registration successful for '{user.username}'! Your account is currently pending Administrator approval. "
                f"Once an administrator accepts your account, you will be able to log in. "
                f"(আপনার অ্যাকাউন্ট সফলভাবে তৈরি হয়েছে এবং অ্যাডমিন অনুমোদনের অপেক্ষায় রয়েছে। অ্যাডমিন অনুমোদন দিলে লগইন করতে পারবেন।)"
            )
            return redirect('login')
        else:
            messages.error(request, "Registration could not be completed. Please fix the highlighted errors.")
    else:
        form = UserSignUpForm()

    return render(request, 'auth_app/signup.html', {
        'form': form,
        'title': 'Sign Up & Account Registration'
    })
