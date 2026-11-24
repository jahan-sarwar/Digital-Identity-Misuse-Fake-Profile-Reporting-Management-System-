@echo off
rem Launch Case Notification & Alert System
echo ===================================================================
echo Starting Case Event Notification and Alert Dispatch System
echo ===================================================================
python manage.py makemigrations notification_app
python manage.py migrate
echo.
echo Starting local development server at http://127.0.0.1:8010 ...
python manage.py runserver 8010
pause
