@echo off
echo 🚀 Committing and pushing GitHub Actions workflow fixes...
echo.

echo 📝 Adding workflow changes...
git add .github/workflows/

echo.
echo 💾 Committing changes...
git commit -m "Fix GitHub Actions wiki sync - handle case where wiki repository already exists during creation"

echo.
echo 🚀 Pushing to trigger new workflow...
git push origin main

echo.
echo ✅ Done! The new workflow should now run with improved error handling.
echo 📋 Check GitHub Actions to see the improved workflow in action.
pause

