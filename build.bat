@echo off
chcp 65001 >nul 2>&1
setlocal

REM Yum Agent Company VSIX build launcher.
REM ASCII-only on purpose: avoids Windows console/codepage errors.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0build.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [FAILED] Build failed. Check the error message above.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [OK] Build completed.
pause
