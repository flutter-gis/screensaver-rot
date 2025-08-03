@echo off
echo Installing ADHD Brain Rot Screen Savers...
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo Installation complete! 
echo You can now run start_screensaver.bat to launch the screen savers.
echo.
pause 