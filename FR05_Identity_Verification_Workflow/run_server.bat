@echo off
rem Batch script to launch Identity Verification Workflow
echo ===================================================================
echo Starting Identity Verification Workflow System
echo ===================================================================
python manage.py makemigrations verification_app
python manage.py migrate
echo.
echo Starting local development server at http://127.0.0.1:8005 ...
python manage.py runserver 8005
pause
