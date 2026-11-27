from django.urls import path
from . import views

urlpatterns = [
    path('cases/<str:case_id>/', views.case_detail_view, name='case_detail'),
]
