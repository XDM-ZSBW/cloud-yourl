# Test Local Clipboard History - Standalone Offline Instance
# =========================================================
#
# This PowerShell script provides easy access to test local clipboard history
# integration that can be run from IDE terminals.
#
# Author: Yourl.Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
# Environment: Local Test

param(
    [Parameter(Position=0)]
    [ValidateSet("search", "recent", "yourl-codes", "display", "stats", "clear", "add", "help")]
    [string]$Action = "display",
    
    [Parameter(Position=1)]
    [string]$Query,
    
    [Parameter(Position=2)]
    [string[]]$Tags,
    
    [Parameter(Position=3)]
    [int]$Hours = 24,
    
    [string]$Content
)

# Function to display help
function Show-Help {
    Write-Host @"
Test Local Clipboard History - Standalone Offline Instance
=========================================================

This script provides a standalone test environment for Windows clipboard
history integration that can be run from IDE terminals.

Usage:
    .\test_clipboard_local.ps1 [Action] [Query] [Tags] [Hours]

Actions:
    display     - Display recent clipboard items (default)
    search      - Search clipboard history with query
    recent      - Show recent items from last N hours
    yourl-codes - Show only items containing Yourl.Cloud codes
    stats       - Show statistics about clipboard history
    clear       - Clear all test data
    add         - Add a new test item
    help        - Show this help message

Examples:
    .\test_clipboard_local.ps1 display
    .\test_clipboard_local.ps1 search "yourl"
    .\test_clipboard_local.ps1 yourl-codes
    .\test_clipboard_local.ps1 recent 48
    .\test_clipboard_local.ps1 stats
    .\test_clipboard_local.ps1 add -Content "Test content"

Features:
    - Offline clipboard history testing
    - Local storage only (no cloud sync)
    - Mock Yourl.Cloud code detection
    - Test data generation
    - IDE-friendly output

"@
}

# Function to check if Python is available
function Test-PythonAvailable {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
    }
    catch {
        return $false
    }
    return $false
}

# Function to run the Python script
function Invoke-TestClipboardHistory {
    param(
        [string]$Action,
        [string]$Query = "",
        [string[]]$Tags = @(),
        [int]$Hours = 24,
        [string]$Content = ""
    )
    
    # Build the command
    $command = "python scripts\clipboard\test_clipboard_history_local.py $Action"
    
    if ($Query) {
        $command += " --query `"$Query`""
    }
    
    if ($Tags.Count -gt 0) {
        $command += " --tags $($Tags -join ' ')"
    }
    
    if ($Hours -ne 24) {
        $command += " --hours $Hours"
    }
    
    if ($Content) {
        $command += " --content `"$Content`""
    }
    
    Write-Host "🚀 Running: $command" -ForegroundColor Cyan
    Write-Host ""
    
    # Execute the command
    Invoke-Expression $command
}

# Main execution logic
try {
    # Check if Python is available
    if (-not (Test-PythonAvailable)) {
        Write-Host "❌ Python is not available. Please install Python and ensure it's in your PATH." -ForegroundColor Red
        Write-Host "💡 You can download Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
    
    # Handle help action
    if ($Action -eq "help") {
        Show-Help
        exit 0
    }
    
    # Execute the requested action
    Write-Host "🔧 Test Local Clipboard History - $Action" -ForegroundColor Green
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host ""
    
    Invoke-TestClipboardHistory -Action $Action -Query $Query -Tags $Tags -Hours $Hours -Content $Content
    
} catch {
    Write-Host "❌ Error executing clipboard history test: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Try running with 'help' action for usage information" -ForegroundColor Yellow
    exit 1
}
