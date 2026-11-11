from django.urls import path
from .upload_views import upload_evidence_view
from .gallery_views import evidence_gallery_view

urlpatterns = [
    path('', evidence_gallery_view, name='evidence_gallery'),
    path('upload/', upload_evidence_view, name='upload_evidence'),
]

