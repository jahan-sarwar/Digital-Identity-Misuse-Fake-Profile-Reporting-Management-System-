@echo off
rem Launch Citizen Public Case Status Tracker
echo ===================================================================
echo Starting Citizen Case Status Tracking System
echo ===================================================================
python manage.py makemigrations tracking_app
python manage.py migrate
echo.
echo Starting local development server at http://127.0.0.1:8009 ...
python manage.py runserver 8009
pause
