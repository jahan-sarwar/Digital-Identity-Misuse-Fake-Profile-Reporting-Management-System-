@echo off
rem Launch Case Audit History Log
echo ===================================================================
echo Starting Case Audit History and Activity Log System
echo ===================================================================
python manage.py makemigrations audit_app
python manage.py migrate
echo.
echo Starting local development server at http://127.0.0.1:8011 ...
python manage.py runserver 8011
pause
