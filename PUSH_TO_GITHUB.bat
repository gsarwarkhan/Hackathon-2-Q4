@echo off
echo ========================================================
echo   Evolution Todo - Professional Deployment Automation
echo ========================================================
echo.
echo [1/3] Staging all files...
git add .
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git command failed. Please ensure Git is installed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Committing changes...
git commit -m "feat: Final Professional Refactor v2.0"

echo.
echo [3/3] Pushing to GitHub...
git push origin master
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Push failed. Check your internet connection or credentials.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [SUCCESS] Code pushed to GitHub! 
echo Vercel should now automatically deploy your project.
echo.
echo Please visit: https://evolution-todo-orpin.vercel.app/
echo.
pause
