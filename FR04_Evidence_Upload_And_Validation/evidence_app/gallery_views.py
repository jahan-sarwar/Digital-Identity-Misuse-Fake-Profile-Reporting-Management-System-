from django.shortcuts import render
from .models import EvidenceFile

def evidence_gallery_view(request):
    """
    FR-04: Dedicated View displaying evidence gallery with thumbnail previews,
    captions, file sizes, and full-resolution inspection links.
    """
    files = EvidenceFile.objects.all()
    return render(request, 'evidence_app/evidence_gallery.html', {
        'files': files,
        'title': 'Evidence Gallery - FR-04'
    })

