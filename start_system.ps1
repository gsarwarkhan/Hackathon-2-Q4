$host.ui.RawUI.WindowTitle = "Evolution of Todo - System Launcher"

Write-Host "🌌 SUPER-CHARGING SYSTEM..." -ForegroundColor Cyan
Write-Host "   [1/3] Initializing Neural Backend (Port 8000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "uvicorn backend.main:app --reload --port 8000" -WindowStyle Minimized

Write-Host "   [2/3] Engaging Holographic Frontend (Port 3000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "cd frontend; npm run dev" -WindowStyle Minimized

Write-Host "   [3/3] Opening Strategic Interface..." -ForegroundColor Green
Start-Sleep -Seconds 5
Start-Process "http://localhost:3000"

Write-Host "✅ SYSTEM ACTIVE. WELCOME, GOVERNOR." -ForegroundColor Magenta
Write-Host "   > Backend is running in background (Port 8000)"
Write-Host "   > Frontend is running in background (Port 3000)"
Write-Host "   > Press Enter to exit this launcher..."
Read-Host
