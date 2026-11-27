# Performance telemetry and strict authentication gatekeeper middleware
import time
from django.shortcuts import redirect
from django.contrib import messages


class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()
        response = self.get_response(request)
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        response['X-Response-Time-ms'] = f"{elapsed_ms:.2f}"
        return response


class StrictAuthenticationMiddleware:
    """
    Guarantees that no unauthenticated user can access or perform any action on the platform.
    Any request from an unauthenticated user is immediately redirected to /login/.
    Only /login/, /register/, and essential static/media files are accessible without an account.
    """
    EXEMPT_PREFIXES = (
        '/login/',
        '/register/',
        '/static/',
        '/media/',
        '/django-admin/',
    )
    EXEMPT_EXACT = (
        '/admin/',
        '/admin/login/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Allow unauthenticated access only to login, register, and assets
        if any(path.startswith(prefix) for prefix in self.EXEMPT_PREFIXES) or path in self.EXEMPT_EXACT:
            return self.get_response(request)

        # Block all other paths for unauthenticated visitors
        if not request.user.is_authenticated:
            if path != '/':
                messages.warning(request, "Authentication required. Please sign in to access this portal.")
                return redirect(f"/login/?next={path}")
            return redirect('/login/')

        return self.get_response(request)
