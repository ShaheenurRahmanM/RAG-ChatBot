@echo off
REM Quick Start Script for SWS AI Policy Assistant
REM Windows version using 'py' command
REM This script sets up and starts the entire application on Windows

echo.
echo ============================================================
echo  SWS AI Policy Assistant - Quick Start (Windows)
echo ============================================================
echo.

REM Check Python
py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9+
    echo Download from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check Node
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 16+
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

echo Checking prerequisites...
echo Python version:
py --version
echo.
echo Node version:
node --version
echo.
echo npm version:
npm --version
echo.

REM Setup Backend
echo ============================================================
echo Setting up Backend...
echo ============================================================
cd backend

if not exist venv (
    echo Creating Python virtual environment...
    py -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -q -r app\requirements.txt

REM Check if .env file exists
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Edit backend\.env and add your Groq API key!
    echo Get key from: https://console.groq.com
    echo.
    pause
)

REM Ingest documents if data exists
if exist data\pdfs\*.pdf (
    echo.
    echo Ingesting PDF documents...
    py app\ingest.py
) else (
    echo.
    echo ℹ️  No PDF files found in backend\data\pdfs\
    echo You can add PDF files anytime and run: py app\ingest.py
)

cd ..

REM Setup Frontend
echo.
echo ============================================================
echo Setting up Frontend...
echo ============================================================
cd frontend

if not exist node_modules (
    echo Installing npm dependencies...
    call npm install
)

REM Check if .env file exists
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
)

cd ..

echo.
echo ============================================================
echo Setup complete!
echo ============================================================
echo.
echo To start the application, open TWO new PowerShell windows:
echo.
echo Window 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate
echo   py app\main.py
echo.
echo Window 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then open your browser: http://localhost:5173
echo.
pause
