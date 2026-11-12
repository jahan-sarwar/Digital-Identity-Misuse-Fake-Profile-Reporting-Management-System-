from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EvidenceFile
from .upload_forms import MultiEvidenceUploadForm, SingleEvidenceUploadForm

def upload_evidence_view(request):
    """
    FR-04: Dedicated View handling evidence uploads, format validation, and storage.
    """
    if request.method == 'POST':
        form = MultiEvidenceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            case_id = form.cleaned_data['case_id']
            uploader_name = form.cleaned_data['uploader_name']

            # Process Primary Evidence
            f1 = request.FILES.get('primary_evidence')
            if f1:
                EvidenceFile.objects.create(
                    case_id=case_id,
                    uploader_name=uploader_name,
                    file=f1,
                    file_type='DOCUMENT' if f1.name.lower().endswith('.pdf') else 'SCREENSHOT',
                    caption=form.cleaned_data.get('primary_caption') or 'Primary Evidence'
                )

            # Process Secondary Evidence if attached
            f2 = request.FILES.get('secondary_evidence')
            if f2:
                EvidenceFile.objects.create(
                    case_id=case_id,
                    uploader_name=uploader_name,
                    file=f2,
                    file_type='DOCUMENT' if f2.name.lower().endswith('.pdf') else 'SCREENSHOT',
                    caption=form.cleaned_data.get('secondary_caption') or 'Secondary Evidence'
                )

            messages.success(request, f"Evidence uploaded and verified successfully for Case: {case_id}!")
            return redirect('evidence_gallery')
        else:
            messages.error(request, "Upload failed. Please ensure file format (.jpg, .png, .pdf) and size (<= 5MB) are valid.")
    else:
        form = MultiEvidenceUploadForm()

    return render(request, 'evidence_app/upload_evidence.html', {
        'form': form,
        'title': 'Upload Supporting Evidence - FR-04'
    })

