@echo off
echo ===================================================================
echo Starting SafeIdentity Official Unified Web Platform
echo ===================================================================
echo Initializing clean database migrations...
python manage.py migrate 2>nul || py -3 manage.py migrate
echo.
echo ===================================================================
echo Server starting at http://127.0.0.1:8000
echo - Master Admin Login: admin  (or admin.sarwar)
echo - Master Password:    Admin@1234
echo - Modules Directory:  http://127.0.0.1:8000/modules/
echo ===================================================================
echo.
python manage.py runserver 8000 2>nul || py -3 manage.py runserver 8000
pause
