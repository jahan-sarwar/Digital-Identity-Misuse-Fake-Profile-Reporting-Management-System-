from django.urls import path
from .signup_views import signup_view
from .login_views import login_view
from .logout_views import logout_view
from .profile_views import profile_view, edit_profile_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
]

