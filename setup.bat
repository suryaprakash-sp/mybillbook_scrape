@echo off
REM Setup script for Windows

echo ==========================================
echo MyBillBook Scraper Setup
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed.
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Python found: %PYTHON_VERSION%
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo ✓ Created .env file
    echo.
    echo IMPORTANT: Please edit .env and add your MyBillBook credentials!
    echo.
) else (
    echo ✓ .env file already exists
)

REM Create output directory
if not exist output mkdir output

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your credentials
echo 2. Activate virtual environment: venv\Scripts\activate
echo 3. Run the scraper:
echo    - Basic: python scraper.py
echo    - Advanced: python cli.py --help
echo.
pause
