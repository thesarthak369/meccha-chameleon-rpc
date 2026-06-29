@echo off
title MECCHA CHAMELEON - Discord RPC

echo.
echo  ==========================================
echo    MECCHA CHAMELEON - Discord RPC
echo  ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python is not installed or not in PATH.
    echo  Download Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Only install dependencies if NOT already installed
python -c "import pypresence, psutil" >nul 2>&1
if errorlevel 1 (
    echo  Installing dependencies for the first time...
    pip install -q pypresence psutil
    echo  Done!
    echo.
)

:: Check if the game is already running (checks all known process names)
tasklist | findstr /I "PenguinHotel Chameleon" >nul 2>&1
if errorlevel 1 (
    echo  Game is not running. Launching MECCHA CHAMELEON...
    start "" "E:\C folder\Downloads\MECCHA.CHAMELEON-SteamRIP.com\MECCHA CHAMELEON\PenguinHotel.exe"
    echo  Waiting for game to start...
    timeout /t 5 /nobreak >nul
    echo  Game launched!
    echo.
) else (
    echo  Game is already running.
    echo.
)

echo  Starting RPC...
echo.

python rpc.py

echo.
pause
