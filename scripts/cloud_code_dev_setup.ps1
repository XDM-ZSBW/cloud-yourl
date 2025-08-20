#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Yourl.Cloud Cloud Code Development Setup Script
    
.DESCRIPTION
    This script sets up the Google Cloud Code development environment for Yourl.Cloud.
    It initializes the development environment, configures necessary services,
    and provides a streamlined development workflow.
    
.PARAMETER ProjectId
    The Google Cloud Project ID to use for development.
    
.PARAMETER Region
    The Google Cloud region for deployment (default: us-west1).
    
.PARAMETER Environment
    The development environment to use (dev, staging, prod).
    
.EXAMPLE
    .\cloud_code_dev_setup.ps1 -ProjectId "yourl-cloud" -Environment "dev"
    
.NOTES
    Requires Google Cloud CLI and Docker to be installed and configured.
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-west1",
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("dev", "staging", "prod")]
    [string]$Environment = "dev"
)

# Set error action preference
$ErrorActionPreference = "Stop"

Write-Host "🚀 Yourl.Cloud Cloud Code Development Setup" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow

# Check if gcloud is installed
try {
    $gcloudVersion = gcloud --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Google Cloud CLI not found"
    }
    Write-Host "✅ Google Cloud CLI: $(($gcloudVersion | Select-Object -First 1))" -ForegroundColor Green
} catch {
    Write-Host "❌ Google Cloud CLI not found. Please install from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Red
    exit 1
}

# Check if Docker is running
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not found or not running"
    }
    Write-Host "✅ Docker: $(($dockerVersion | Select-Object -First 1))" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found or not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check if Python is available
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "✅ Python: $(($pythonVersion | Select-Object -First 1))" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.11+." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Authenticate with Google Cloud
Write-Host "🔐 Authenticating with Google Cloud..." -ForegroundColor Yellow
try {
    gcloud auth list --filter=status:ACTIVE --format="value(account)" | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  No active Google Cloud authentication found. Please run 'gcloud auth login'" -ForegroundColor Yellow
        gcloud auth login
    } else {
        $activeAccount = gcloud auth list --filter=status:ACTIVE --format="value(account)"
        Write-Host "✅ Authenticated as: $activeAccount" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Authentication failed. Please check your Google Cloud credentials." -ForegroundColor Red
    exit 1
}

# Set project and region
Write-Host "⚙️  Configuring Google Cloud project and region..." -ForegroundColor Yellow
try {
    gcloud config set project $ProjectId
    gcloud config set run/region $Region
    Write-Host "✅ Project set to: $ProjectId" -ForegroundColor Green
    Write-Host "✅ Region set to: $Region" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to set project or region. Please check your permissions." -ForegroundColor Red
    exit 1
}

# Enable required APIs
Write-Host "🔌 Enabling required Google Cloud APIs..." -ForegroundColor Yellow
$requiredApis = @(
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "secretmanager.googleapis.com",
    "sql-component.googleapis.com"
)

foreach ($api in $requiredApis) {
    try {
        Write-Host "  Enabling $api..." -ForegroundColor Gray
        gcloud services enable $api --quiet
        Write-Host "  ✅ $api enabled" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Failed to enable $api" -ForegroundColor Red
    }
}

Write-Host ""

# Initialize Cloud Code development environment
Write-Host "🚀 Initializing Cloud Code development environment..." -ForegroundColor Yellow
try {
    # Check if .cloudcode directory exists
    if (Test-Path ".cloudcode") {
        Write-Host "✅ Cloud Code configuration already exists" -ForegroundColor Green
    } else {
        Write-Host "  Creating Cloud Code configuration..." -ForegroundColor Gray
        gcloud beta code dev init --quiet
        Write-Host "  ✅ Cloud Code environment initialized" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Failed to initialize Cloud Code environment. Please check your permissions." -ForegroundColor Red
    exit 1
}

# Create environment-specific configuration
Write-Host "📝 Creating environment-specific configuration..." -ForegroundColor Yellow
try {
    $configDir = ".cloudcode"
    if (!(Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    }
    
    # Copy the main configuration
    if (Test-Path ".cloudcode\cloudcode.yaml") {
        Write-Host "✅ Main Cloud Code configuration exists" -ForegroundColor Green
    } else {
        Write-Host "❌ Main Cloud Code configuration not found. Please ensure .cloudcode/cloudcode.yaml exists." -ForegroundColor Red
        exit 1
    }
    
    # Create environment-specific config
    $envConfig = @"
apiVersion: cloudcode.dev/v1
kind: DevEnvironment
metadata:
  name: yourl-cloud-$Environment
  description: "Yourl.Cloud $Environment Environment"
spec:
  services:
    - name: yourl-cloud
      source: .
      port: 8080
      env:
        - name: FLASK_ENV
          value: "$Environment"
        - name: FLASK_DEBUG
          value: "$(if ($Environment -eq 'dev') { 'true' } else { 'false' })"
        - name: GOOGLE_CLOUD_PROJECT
          value: "$ProjectId"
        - name: LOG_LEVEL
          value: "$(if ($Environment -eq 'dev') { 'DEBUG' } else { 'INFO' })"
        - name: PORT
          value: "8080"
      build:
        dockerfile: Dockerfile
        context: .
      run:
        command: ["python", "app_simple.py"]
        args: []
"@
    
    $envConfig | Out-File -FilePath ".cloudcode\$Environment.yaml" -Encoding UTF8
    Write-Host "✅ Environment configuration created: .cloudcode\$Environment.yaml" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Failed to create environment configuration." -ForegroundColor Red
    exit 1
}

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
try {
    if (Test-Path "requirements.txt") {
        pip install -r requirements.txt
        Write-Host "✅ Python dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "⚠️  No requirements.txt found. Skipping dependency installation." -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Failed to install Python dependencies." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Display next steps
Write-Host "🎯 Setup Complete! Next Steps:" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green
Write-Host ""
Write-Host "1. 🚀 Start development environment:" -ForegroundColor Cyan
Write-Host "   gcloud beta code dev up --config .cloudcode\$Environment.yaml" -ForegroundColor White
Write-Host ""
Write-Host "2. 📊 View logs:" -ForegroundColor Cyan
Write-Host "   gcloud beta code dev logs --follow" -ForegroundColor White
Write-Host ""
Write-Host "3. 🧪 Run tests:" -ForegroundColor Cyan
Write-Host "   gcloud beta code dev test --all" -ForegroundColor White
Write-Host ""
Write-Host "4. 🛑 Stop development environment:" -ForegroundColor Cyan
Write-Host "   gcloud beta code dev down" -ForegroundColor White
Write-Host ""
Write-Host "5. 📚 View documentation:" -ForegroundColor Cyan
Write-Host "   docs/GCLOUD_CODE_DEV_GUIDE.md" -ForegroundColor White
Write-Host ""

# Create a quick start script
$quickStartScript = @"
#!/usr/bin/env pwsh
# Quick start script for Yourl.Cloud development

Write-Host "🚀 Starting Yourl.Cloud development environment..." -ForegroundColor Green
gcloud beta code dev up --config .cloudcode\$Environment.yaml

Write-Host "📊 Development environment started!" -ForegroundColor Green
Write-Host "🌐 Your application will be available at the Cloud Run URL shown above" -ForegroundColor Green
Write-Host "📝 View logs with: gcloud beta code dev logs --follow" -ForegroundColor Cyan
"@

$quickStartScript | Out-File -FilePath "start-dev.ps1" -Encoding UTF8
Write-Host "✅ Quick start script created: start-dev.ps1" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Yourl.Cloud Cloud Code development environment is ready!" -ForegroundColor Green
Write-Host "Happy coding! 🚀" -ForegroundColor Green
