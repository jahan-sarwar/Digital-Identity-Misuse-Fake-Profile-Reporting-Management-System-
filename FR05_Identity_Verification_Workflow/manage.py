#!/usr/bin/env python
# Django administrative utility for management commands
import os
import sys

def main():
    # Set default Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        # Import Django execution entry point
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH?"
        ) from exc
    # Execute commands passed via command line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
