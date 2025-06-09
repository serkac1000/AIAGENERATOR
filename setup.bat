@echo off
echo MIT App Inventor AIA Generator - Setup
echo =====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or later from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found. Installing required packages...
echo.

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install required packages
pip install google-generativeai pillow pyinstaller

REM Check installation
echo.
echo Checking installation...
python -c "import google.generativeai; import PIL; print('All packages installed successfully!')"

if errorlevel 1 (
    echo.
    echo ERROR: Package installation failed
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
echo.
echo You can now run the application with:
echo python main.py
echo.
echo Or build an executable with:
echo build.bat
echo.
pause
