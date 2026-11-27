from django.urls import path
from . import views

urlpatterns = [
    path('track/', views.public_tracker_view, name='public_tracker'),
]
