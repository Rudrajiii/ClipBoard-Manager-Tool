@echo off
echo.
echo ========================================
echo    Clipboard History Cleanup Tool
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if the test script exists
if not exist "__tests__\__sql_command_for_data_removal__.py" (
    echo ❌ Test script not found: __tests__\__sql_command_for_data_removal__.py
    pause
    exit /b 1
)

REM Check if database file exists
if not exist "clipboard_history.db" (
    echo ⚠️  Warning: clipboard_history.db not found in current directory
    echo    The script will still run but may fail if database doesn't exist
    echo.
)

echo 🔄 Running cleanup script...
echo.

REM Run the cleanup script
python "__tests__\__sql_command_for_data_removal__.py"

echo.
echo ========================================
if errorlevel 1 (
    echo ❌ Script execution failed
) else (
    echo ✅ Script execution completed
)
echo ========================================
echo.
pause