import os
from django.core.exceptions import ValidationError

ALLOWED_EVIDENCE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.pdf']
MAX_EVIDENCE_SIZE_BYTES = 5 * 1024 * 1024  # 5 Megabytes

def validate_evidence_file(file):
    """
    FR-04: Strict Evidence Validator.
    1. Validates extension against whitelist (.jpg, .jpeg, .png, .pdf).
    2. Enforces maximum 5MB size limit.
    """
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EVIDENCE_EXTENSIONS:
        allowed_str = ", ".join(ALLOWED_EVIDENCE_EXTENSIONS)
        raise ValidationError(
            f"Unsupported file format '{ext}'. Only {allowed_str} files are permitted as evidence."
        )

    if file.size > MAX_EVIDENCE_SIZE_BYTES:
        size_mb = file.size / (1024 * 1024)
        raise ValidationError(
            f"File size exceeds the 5MB limit. Current file size: {size_mb:.2f} MB."
        )

