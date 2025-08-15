@echo off
REM Test Local Clipboard History - Standalone Offline Instance
REM =========================================================
REM
REM This batch script provides easy access to test local clipboard history
REM integration that can be run from IDE terminals.
REM
REM Author: Yourl.Cloud Inc.
REM Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
REM Environment: Local Test

setlocal enabledelayedexpansion

REM Parse command line arguments
set "Action=%1"
set "Query=%2"
set "Tags=%3"
set "Hours=%4"
set "Content=%5"

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
echo 🔧 Test Local Clipboard History - %Action%
echo =============================================
echo.

REM Build the command
set "command=python scripts\clipboard\test_clipboard_history_local.py %Action%"

if not "%Query%"=="" (
    set "command=!command! --query "%Query%""
)

if not "%Tags%"=="" (
    set "command=!command! --tags %Tags%"
)

if not "%Hours%"=="24" (
    set "command=!command! --hours %Hours%"
)

if not "%Content%"=="" (
    set "command=!command! --content "%Content%""
)

echo 🚀 Running: !command!
echo.

REM Execute the command
!command!

if errorlevel 1 (
    echo.
    echo ❌ Error executing clipboard history test
    echo 💡 Try running with 'help' action for usage information
    exit /b 1
)

goto :EOF

:ShowHelp
echo Test Local Clipboard History - Standalone Offline Instance
echo =========================================================
echo.
echo This script provides a standalone test environment for Windows clipboard
echo history integration that can be run from IDE terminals.
echo.
echo Usage:
echo     test_clipboard_local.bat [Action] [Query] [Tags] [Hours]
echo.
echo Actions:
echo     display     - Display recent clipboard items (default)
echo     search      - Search clipboard history with query
echo     recent      - Show recent items from last N hours
echo     yourl-codes - Show only items containing Yourl.Cloud codes
echo     stats       - Show statistics about clipboard history
echo     clear       - Clear all test data
echo     add         - Add a new test item
echo     help        - Show this help message
echo.
echo Examples:
echo     test_clipboard_local.bat display
echo     test_clipboard_local.bat search "yourl"
echo     test_clipboard_local.bat yourl-codes
echo     test_clipboard_local.bat recent 48
echo     test_clipboard_local.bat stats
echo     test_clipboard_local.bat add "Test content"
echo.
echo Features:
echo     - Offline clipboard history testing
echo     - Local storage only (no cloud sync)
echo     - Mock Yourl.Cloud code detection
echo     - Test data generation
echo     - IDE-friendly output
echo.
goto :EOF
