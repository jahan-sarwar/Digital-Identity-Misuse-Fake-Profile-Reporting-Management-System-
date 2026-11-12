@echo off
echo ==========================================================
echo Starting Platform Selection & Profile URL Module
echo ==========================================================
python manage.py makemigrations platform_app
python manage.py migrate
echo.
echo Starting local development server at http://127.0.0.1:8000 ...
python manage.py runserver 8000
pause

