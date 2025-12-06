@echo off
REM ============================================
REM Build Script for Computer Voice Assistant
REM ============================================
REM Author: Manus AI (Operation Nexus)

echo.
echo ========================================
echo Computer Voice Assistant - Build Tool
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo [INFO] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

REM Check if build.spec exists
if not exist "build.spec" (
    echo [ERROR] build.spec not found!
    echo Please ensure build.spec is in the project directory.
    pause
    exit /b 1
)

REM Clean previous builds
echo [INFO] Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Build executable
echo.
echo [INFO] Building executable with PyInstaller...
echo This may take several minutes...
echo.
pyinstaller build.spec

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    echo Check the output above for errors.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] Build completed!
echo ========================================
echo.
echo Executable location: dist\ComputerVoiceAssi.exe
echo.
echo IMPORTANT: Remember to copy your .env file to the dist\ directory!
echo.
pause
