# File upload validation utilities for evidence and identity documents
import os
from django.core.exceptions import ValidationError


def validate_evidence_file(value):
    # Restrict uploaded evidence files to safe image and PDF formats under 5MB
    ext = os.path.splitext(value.name)[1].lower()
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    if ext not in allowed_extensions:
        raise ValidationError(
            f"Unsupported file format '{ext}'. Allowed formats: JPG, JPEG, PNG, PDF."
        )
    max_size_bytes = 5 * 1024 * 1024
    if value.size > max_size_bytes:
        raise ValidationError("Uploaded file size must not exceed 5MB.")
