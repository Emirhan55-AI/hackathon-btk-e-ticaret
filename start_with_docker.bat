@echo off
REM Aura AI System - Docker Desktop Startup Helper
REM Automatically starts Docker Desktop and waits for it to be ready

echo ================================================================================
echo 🐳 Docker Desktop Startup Helper
echo Aura AI Complete System - BTK Hackathon 2025
echo ================================================================================
echo.

REM Check if Docker Desktop is already running
echo 🔍 Checking Docker Desktop status...
docker ps >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Docker Desktop is already running!
    goto :start_system
)

echo ❌ Docker Desktop is not running. Starting it now...

REM Try to start Docker Desktop
echo 🚀 Starting Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"

REM Wait for Docker Desktop to start
echo ⏳ Waiting for Docker Desktop to initialize...
echo    This may take 2-3 minutes for first startup...

:wait_loop
timeout /t 10 /nobreak >nul
docker ps >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo    ⌛ Still waiting for Docker Desktop...
    goto :wait_loop
)

echo ✅ Docker Desktop is now running!
echo.

:start_system
echo 🌟 Starting Aura AI Complete System...
echo.

REM Change to the correct directory
cd /d "%~dp0"

REM Start the Aura AI system
python run_aura.py

pause
