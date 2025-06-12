@echo off
echo Scanning for __pycache__ folders...
for /d /r %%d in (__pycache__) do (
    if exist "%%d" (
        echo Deleting: %%d
        rmdir /s /q "%%d"
    )
)
echo All __pycache__ folders removed.
pause
