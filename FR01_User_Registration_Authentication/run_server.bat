@echo off
echo =======================================================
echo Starting User Registration & Account Management
echo =======================================================
python manage.py makemigrations auth_app
python manage.py migrate
echo.
echo Starting local development server at http://127.0.0.1:8000 ...
python manage.py runserver 8000
pause

