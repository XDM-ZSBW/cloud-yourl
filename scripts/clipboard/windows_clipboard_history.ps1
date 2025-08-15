# Windows Clipboard History Integration for Yourl.Cloud
# ===================================================
#
# This PowerShell script provides easy access to Windows clipboard history
# integration with Yourl.Cloud clipboard bridge.
#
# Author: Yourl.Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

param(
    [Parameter(Position=0)]
    [ValidateSet("search", "recent", "yourl-codes", "monitor", "display", "help")]
    [string]$Action = "display",
    
    [Parameter(Position=1)]
    [string]$Query,
    
    [Parameter(Position=2)]
    [string[]]$Tags,
    
    [Parameter(Position=3)]
    [int]$Hours = 24,
    
    [string]$ProjectId = "yourl-cloud",
    [string]$BridgeUrl = "https://cb.yourl.cloud"
)

# Function to display help
function Show-Help {
    Write-Host @"
Windows Clipboard History Integration for Yourl.Cloud
====================================================

This script helps you find recent clipboard items from all your devices that contain your Yourl.Cloud codes.

Usage:
    .\windows_clipboard_history.ps1 [Action] [Query] [Tags] [Hours]

Actions:
    display     - Display recent clipboard items (default)
    search      - Search clipboard history with query
    recent      - Show recent items from last N hours
    yourl-codes - Show only items containing Yourl.Cloud codes
    monitor     - Start monitoring clipboard for new items
    help        - Show this help message

Examples:
    .\windows_clipboard_history.ps1 display
    .\windows_clipboard_history.ps1 search "yourl"
    .\windows_clipboard_history.ps1 yourl-codes
    .\windows_clipboard_history.ps1 recent 48
    .\windows_clipboard_history.ps1 monitor

Parameters:
    Query       - Search query for text content
    Tags        - Tags to filter by (e.g., "yourl-cloud-code", "url")
    Hours       - Hours to look back for recent items (default: 24)
    ProjectId   - Google Cloud project ID (default: yourl-cloud)
    BridgeUrl   - Clipboard bridge URL (default: https://cb.yourl.cloud)

Features:
    - Monitors Windows clipboard history
    - Syncs with Yourl.Cloud clipboard bridge
    - Searches for Yourl.Cloud codes across devices
    - Provides quick access to recent clipboard items
    - Integrates with Windows clipboard history (Win+V)

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

# Function to check if required Python packages are installed
function Test-PythonPackages {
    $requiredPackages = @("requests", "pywin32")
    $missingPackages = @()
    
    foreach ($package in $requiredPackages) {
        try {
            python -c "import $package" 2>$null
            if ($LASTEXITCODE -ne 0) {
                $missingPackages += $package
            }
        }
        catch {
            $missingPackages += $package
        }
    }
    
    return $missingPackages
}

# Function to run the Python script
function Invoke-WindowsClipboardHistory {
    param(
        [string]$Action,
        [string]$Query = "",
        [string[]]$Tags = @(),
        [int]$Hours = 24
    )
    
    # Build the command
    $command = "python scripts\clipboard\windows_clipboard_history.py $Action"
    
    if ($Query) {
        $command += " --query `"$Query`""
    }
    
    if ($Tags.Count -gt 0) {
        $command += " --tags $($Tags -join ' ')"
    }
    
    if ($Hours -ne 24) {
        $command += " --hours $Hours"
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
    
    # Check for required Python packages
    $missingPackages = Test-PythonPackages
    if ($missingPackages.Count -gt 0) {
        Write-Host "⚠️ Missing required Python packages: $($missingPackages -join ', ')" -ForegroundColor Yellow
        Write-Host "💡 Install them with: pip install $($missingPackages -join ' ')" -ForegroundColor Yellow
        Write-Host ""
    }
    
    # Handle help action
    if ($Action -eq "help") {
        Show-Help
        exit 0
    }
    
    # Execute the requested action
    Write-Host "🔧 Windows Clipboard History - $Action" -ForegroundColor Green
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host ""
    
    Invoke-WindowsClipboardHistory -Action $Action -Query $Query -Tags $Tags -Hours $Hours
    
} catch {
    Write-Host "❌ Error executing Windows clipboard history: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Try running with 'help' action for usage information" -ForegroundColor Yellow
    exit 1
}
