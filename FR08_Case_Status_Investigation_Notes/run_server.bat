@echo off
rem Launch Case Status & Investigation Notes System
echo ===================================================================
echo Starting Case Status and Investigation Notes System
echo ===================================================================
python manage.py makemigrations investigation_app
python manage.py migrate
echo.
echo Starting local development server at http://127.0.0.1:8008 ...
python manage.py runserver 8008
pause
