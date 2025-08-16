Write-Host "🚀 Committing and pushing GitHub Actions workflow fixes..." -ForegroundColor Green
Write-Host ""

Write-Host "📝 Adding workflow changes..." -ForegroundColor Yellow
git add .github/workflows/

Write-Host ""
Write-Host "💾 Committing changes..." -ForegroundColor Yellow
git commit -m "Fix GitHub Actions wiki sync - handle case where wiki repository already exists during creation"

Write-Host ""
Write-Host "🚀 Pushing to trigger new workflow..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "✅ Done! The new workflow should now run with improved error handling." -ForegroundColor Green
Write-Host "📋 Check GitHub Actions to see the improved workflow in action." -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

