@echo off
rem Launch Administrative Dashboard and User Approval Portal
echo ===================================================================
echo Starting Executive Administration and User Governance System
echo ===================================================================
python manage.py makemigrations dashboard_app
python manage.py migrate
echo.
echo Starting local development server at http://127.0.0.1:8012 ...
python manage.py runserver 8012
pause
