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

# Function to install missing Python packages
function Install-PythonPackages {
    param([string[]]$Packages)
    
    Write-Host "Installing missing Python packages: $($Packages -join ', ')"
    
    foreach ($package in $Packages) {
        Write-Host "Installing $package..."
        pip install $package
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to install $package"
            return $false
        }
    }
    
    return $true
}

# Function to run the Python script
function Invoke-ClipboardHistory {
    param(
        [string]$Action,
        [string]$Query = "",
        [string[]]$Tags = @(),
        [int]$Hours = 24,
        [string]$ProjectId = "yourl-cloud",
        [string]$BridgeUrl = "https://cb.yourl.cloud"
    )
    
    # Build the command
    $command = "python scripts/windows_clipboard_history.py --action $Action"
    
    if ($Query) {
        $command += " --query `"$Query`""
    }
    
    if ($Tags.Count -gt 0) {
        $command += " --tags $($Tags -join ' ')"
    }
    
    if ($Hours -ne 24) {
        $command += " --hours $Hours"
    }
    
    if ($ProjectId -ne "yourl-cloud") {
        $command += " --project-id $ProjectId"
    }
    
    if ($BridgeUrl -ne "https://cb.yourl.cloud") {
        $command += " --bridge-url $BridgeUrl"
    }
    
    Write-Host "Running: $command"
    Write-Host ""
    
    # Run the command
    Invoke-Expression $command
}

# Main execution
if ($Action -eq "help") {
    Show-Help
    exit 0
}

# Check if Python is available
if (-not (Test-PythonAvailable)) {
    Write-Error "Python is not available. Please install Python 3.7+ and try again."
    Write-Host "Download Python from: https://www.python.org/downloads/"
    exit 1
}

# Check if required packages are installed
$missingPackages = Test-PythonPackages
if ($missingPackages.Count -gt 0) {
    Write-Warning "Missing Python packages: $($missingPackages -join ', ')"
    $install = Read-Host "Would you like to install them? (y/n)"
    if ($install -eq "y" -or $install -eq "Y") {
        if (-not (Install-PythonPackages -Packages $missingPackages)) {
            Write-Error "Failed to install required packages. Please install them manually:"
            Write-Host "pip install $($missingPackages -join ' ')"
            exit 1
        }
    }
    else {
        Write-Error "Required packages not installed. Please install them manually:"
        Write-Host "pip install $($missingPackages -join ' ')"
        exit 1
    }
}

# Check if the Python script exists
$scriptPath = "scripts/windows_clipboard_history.py"
if (-not (Test-Path $scriptPath)) {
    Write-Error "Python script not found: $scriptPath"
    Write-Host "Please ensure you're running this from the project root directory."
    exit 1
}

# Run the clipboard history integration
try {
    Invoke-ClipboardHistory -Action $Action -Query $Query -Tags $Tags -Hours $Hours -ProjectId $ProjectId -BridgeUrl $BridgeUrl
}
catch {
    Write-Error "Failed to run clipboard history integration: $_"
    exit 1
}

