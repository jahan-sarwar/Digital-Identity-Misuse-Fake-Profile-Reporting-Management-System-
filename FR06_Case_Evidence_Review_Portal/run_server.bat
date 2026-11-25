@echo off
rem Launch Case & Evidence Review Portal
echo ===================================================================
echo Starting Case and Evidence Review System
echo ===================================================================
python manage.py makemigrations review_app
python manage.py migrate
echo.
echo Starting local development server at http://127.0.0.1:8006 ...
python manage.py runserver 8006
pause
