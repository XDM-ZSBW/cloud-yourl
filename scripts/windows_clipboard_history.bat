@echo off
REM Windows Clipboard History Integration for Yourl.Cloud
REM ===================================================
REM
REM This batch file provides easy access to Windows clipboard history
REM integration with Yourl.Cloud clipboard bridge.
REM
REM Author: Yourl.Cloud Inc.
REM Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

setlocal enabledelayedexpansion

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not available.
    echo Please install Python 3.7+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if the Python script exists
if not exist "scripts\windows_clipboard_history.py" (
    echo Error: Python script not found: scripts\windows_clipboard_history.py
    echo Please ensure you're running this from the project root directory.
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import requests, win32clipboard" >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: Missing Python packages (requests, pywin32)
    echo Installing required packages...
    pip install requests pywin32
    if %errorlevel% neq 0 (
        echo Error: Failed to install required packages.
        echo Please install them manually: pip install requests pywin32
        pause
        exit /b 1
    )
)

REM Parse command line arguments
set "action=display"
set "query="
set "tags="
set "hours=24"
set "project_id=yourl-cloud"
set "bridge_url=https://cb.yourl.cloud"

:parse_args
if "%~1"=="" goto :run
if "%~1"=="--action" (
    set "action=%~2"
    shift
    shift
    goto :parse_args
)
if "%~1"=="--query" (
    set "query=%~2"
    shift
    shift
    goto :parse_args
)
if "%~1"=="--tags" (
    set "tags=%~2"
    shift
    shift
    goto :parse_args
)
if "%~1"=="--hours" (
    set "hours=%~2"
    shift
    shift
    goto :parse_args
)
if "%~1"=="--project-id" (
    set "project_id=%~2"
    shift
    shift
    goto :parse_args
)
if "%~1"=="--bridge-url" (
    set "bridge_url=%~2"
    shift
    shift
    goto :parse_args
)
if "%~1"=="--help" (
    goto :show_help
)
shift
goto :parse_args

:show_help
echo Windows Clipboard History Integration for Yourl.Cloud
echo ===================================================
echo.
echo This script helps you find recent clipboard items from all your devices
echo that contain your Yourl.Cloud codes.
echo.
echo Usage:
echo   windows_clipboard_history.bat [action] [options]
echo.
echo Actions:
echo   display     - Display recent clipboard items (default)
echo   search      - Search clipboard history with query
echo   recent      - Show recent items from last N hours
echo   yourl-codes - Show only items containing Yourl.Cloud codes
echo   monitor     - Start monitoring clipboard for new items
echo   help        - Show this help message
echo.
echo Examples:
echo   windows_clipboard_history.bat display
echo   windows_clipboard_history.bat search "yourl"
echo   windows_clipboard_history.bat yourl-codes
echo   windows_clipboard_history.bat recent 48
echo   windows_clipboard_history.bat monitor
echo.
echo Features:
echo   - Monitors Windows clipboard history
echo   - Syncs with Yourl.Cloud clipboard bridge
echo   - Searches for Yourl.Cloud codes across devices
echo   - Provides quick access to recent clipboard items
echo   - Integrates with Windows clipboard history (Win+V)
echo.
pause
exit /b 0

:run
REM Build the command
set "command=python scripts\windows_clipboard_history.py --action %action%"

if defined query (
    set "command=!command! --query "!query!""
)

if defined tags (
    set "command=!command! --tags !tags!"
)

if defined hours (
    set "command=!command! --hours !hours!"
)

if defined project_id (
    set "command=!command! --project-id !project_id!"
)

if defined bridge_url (
    set "command=!command! --bridge-url !bridge_url!"
)

echo Running: !command!
echo.

REM Run the command
!command!

if %errorlevel% neq 0 (
    echo.
    echo Error: Command failed with exit code %errorlevel%
    pause
    exit /b %errorlevel%
)

echo.
echo Command completed successfully.
pause

