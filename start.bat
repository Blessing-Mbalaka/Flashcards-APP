@echo off
echo Starting StudyHub Flashcards Application...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Initialize demo data if needed
echo Initializing demo data...
python manage.py init_demo_data

REM Start server
echo.
echo ========================================
echo StudyHub is starting!
echo Visit: http://localhost:8000
echo Admin panel: http://localhost:8000/admin
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python manage.py runserver
