@echo off
title Safety Pass Management System
color 0A

echo.
echo ================================================================
echo         SAFETY PASS MANAGEMENT SYSTEM
echo ================================================================
echo.
echo Starting application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7 or higher from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Run the Python launcher
python run_app.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo Application exited with an error.
    pause
)