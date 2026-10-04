@echo off
title Cisco CLI Command Center
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
  echo [ERROR] Virtual environment not found.
  echo Create it with: python -m venv venv
  pause
  exit /b 1
)

start "Cisco CLI Backend" cmd /k "cd /d "%~dp0" && venv\Scripts\python.exe -m uvicorn backend.main:app --reload"
timeout /t 2 /nobreak >nul
start "Cisco CLI Dashboard" cmd /k "cd /d "%~dp0dashboard" && ..\venv\Scripts\python.exe -m http.server 8080"
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:8080"

echo.
echo Backend:   http://127.0.0.1:8000
 echo Dashboard: http://127.0.0.1:8080
pause
