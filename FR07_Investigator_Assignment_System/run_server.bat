@echo off
rem Launch Investigator Assignment System
echo ===================================================================
echo Starting Investigator Assignment and Allocation System
echo ===================================================================
python manage.py makemigrations assignment_app
python manage.py migrate
echo.
echo Starting local development server at http://127.0.0.1:8007 ...
python manage.py runserver 8007
pause
