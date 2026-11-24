# URL configuration for notifications
from django.urls import path
from . import views

urlpatterns = [
    # Inbox listing
    path('', views.notification_inbox_view, name='notification_inbox'),
    # Mark notification as read
    path('read/<int:notif_id>/', views.mark_notification_read_view, name='mark_notification_read'),
    # Dispatch manual or test alert
    path('dispatch/', views.dispatch_notification_view, name='dispatch_notification'),
]
