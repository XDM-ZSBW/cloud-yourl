@echo off
REM Windows Clipboard History Integration for Yourl.Cloud
REM ===================================================
REM
REM This batch script provides easy access to Windows clipboard history
REM integration with Yourl.Cloud clipboard bridge.
REM
REM Author: Yourl.Cloud Inc.
REM Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

setlocal enabledelayedexpansion

REM Parse command line arguments
set "Action=%1"
set "Query=%2"
set "Tags=%3"
set "Hours=%4"

REM Set defaults
if "%Action%"=="" set "Action=display"
if "%Hours%"=="" set "Hours=24"

REM Display help if requested
if /i "%Action%"=="help" goto :ShowHelp
if /i "%Action%"=="/?" goto :ShowHelp
if /i "%Action%"=="-h" goto :ShowHelp

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not available. Please install Python and ensure it's in your PATH.
    echo 💡 You can download Python from: https://www.python.org/downloads/
    exit /b 1
)

REM Execute the requested action
echo 🔧 Windows Clipboard History - %Action%
echo =============================================
echo.

REM Build the command
set "command=python scripts\clipboard\windows_clipboard_history.py %Action%"

if not "%Query%"=="" (
    set "command=!command! --query "%Query%""
)

if not "%Tags%"=="" (
    set "command=!command! --tags %Tags%"
)

if not "%Hours%"=="24" (
    set "command=!command! --hours %Hours%"
)

echo 🚀 Running: !command!
echo.

REM Execute the command
!command!

if errorlevel 1 (
    echo.
    echo ❌ Error executing Windows clipboard history
    echo 💡 Try running with 'help' action for usage information
    exit /b 1
)

goto :EOF

:ShowHelp
echo Windows Clipboard History Integration for Yourl.Cloud
echo ===================================================
echo.
echo This script helps you find recent clipboard items from all your devices
echo that contain your Yourl.Cloud codes.
echo.
echo Usage:
echo     windows_clipboard_history.bat [Action] [Query] [Tags] [Hours]
echo.
echo Actions:
echo     display     - Display recent clipboard items (default)
echo     search      - Search clipboard history with query
echo     recent      - Show recent items from last N hours
echo     yourl-codes - Show only items containing Yourl.Cloud codes
echo     monitor     - Start monitoring clipboard for new items
echo     help        - Show this help message
echo.
echo Examples:
echo     windows_clipboard_history.bat display
echo     windows_clipboard_history.bat search "yourl"
echo     windows_clipboard_history.bat yourl-codes
echo     windows_clipboard_history.bat recent 48
echo     windows_clipboard_history.bat monitor
echo.
echo Parameters:
echo     Query       - Search query for text content
echo     Tags        - Tags to filter by (e.g., "yourl-cloud-code", "url")
echo     Hours       - Hours to look back for recent items (default: 24)
echo.
echo Features:
echo     - Monitors Windows clipboard history
echo     - Syncs with Yourl.Cloud clipboard bridge
echo     - Searches for Yourl.Cloud codes across devices
echo     - Provides quick access to recent clipboard items
echo     - Integrates with Windows clipboard history (Win+V)
echo.
goto :EOF
