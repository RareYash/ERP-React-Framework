@echo off
REM Quick Start Script for Student Review System (Windows)

echo ==========================================
echo Student Review System - Quick Start
echo ==========================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

python --version
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet

if %errorlevel% neq 0 (
    echo X Failed to install dependencies
    echo   Try: pip install -r requirements.txt
    pause
    exit /b 1
)

echo Dependencies installed successfully
echo.

REM Check if CSV exists
if exist "data\student_reviews.csv" (
    echo Student data file found
) else (
    echo X student_reviews.csv not found in data\
    echo   Please add your student data CSV file
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To start the application, run:
echo   streamlit run app.py
echo.
echo Demo Credentials:
echo   Parent - username: parent1, password: pass1234
echo   Teacher - username: teacher, password: admin1234
echo.

pause
