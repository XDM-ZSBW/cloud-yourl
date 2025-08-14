@echo off
REM Test Local Clipboard History - Standalone Offline Instance
REM =========================================================
REM
REM This batch file provides easy access to test local clipboard history
REM integration that can be run from IDE terminals.
REM
REM Author: Yourl.Cloud Inc.
REM Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
REM Environment: Local Test

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
if not exist "scripts\test_clipboard_history_local.py" (
    echo Error: Python script not found: scripts\test_clipboard_history_local.py
    echo Please ensure you're running this from the project root directory.
    pause
    exit /b 1
)

REM Parse command line arguments
set "action=display"
set "query="
set "tags="
set "hours=24"
set "content="

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
if "%~1"=="--content" (
    set "content=%~2"
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
echo Test Local Clipboard History - Standalone Offline Instance
echo =========================================================
echo.
echo This script provides a standalone test environment for Windows clipboard
echo history integration that can be run from IDE terminals.
echo.
echo Usage:
echo   test_clipboard_local.bat [action] [options]
echo.
echo Actions:
echo   display     - Display recent clipboard items (default)
echo   search      - Search clipboard history with query
echo   recent      - Show recent items from last N hours
echo   yourl-codes - Show only items containing Yourl.Cloud codes
echo   stats       - Show statistics about clipboard history
echo   clear       - Clear all test data
echo   add         - Add a new test item
echo   help        - Show this help message
echo.
echo Examples:
echo   test_clipboard_local.bat display
echo   test_clipboard_local.bat search "yourl"
echo   test_clipboard_local.bat yourl-codes
echo   test_clipboard_local.bat recent 48
echo   test_clipboard_local.bat stats
echo   test_clipboard_local.bat add --content "Test content"
echo.
echo Features:
echo   - Offline clipboard history testing
echo   - Local storage only (no cloud sync)
echo   - Mock Yourl.Cloud code detection
echo   - Test data generation
echo   - IDE-friendly output
echo.
pause
exit /b 0

:run
REM Build the command
set "command=python scripts\test_clipboard_history_local.py %action%"

if defined query (
    set "command=!command! --query "!query!""
)

if defined tags (
    set "command=!command! --tags !tags!"
)

if defined hours (
    set "command=!command! --hours !hours!"
)

if defined content (
    set "command=!command! --content "!content!""
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

