from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('report/new/', views.submit_report_view, name='submit_report'),
    path('submit/', views.submit_report_view, name='submit_report_alias'),
    path('cases/', views.case_list_view, name='case_list'),
]
