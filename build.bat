@echo off
echo Building AIA Generator executable...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt

REM Check if PyInstaller installed successfully
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller installation failed
    pause
    exit /b 1
)

REM Build executable
echo Building executable...
pyinstaller --onefile --windowed --name "AIA_Generator" --icon=app_icon.ico main.py

REM Check if build was successful
if exist "dist\AIA_Generator.exe" (
    echo Build completed successfully!
    echo Executable location: dist\AIA_Generator.exe
    
    REM Create distribution folder
    if not exist "AIA_Generator_Release" mkdir "AIA_Generator_Release"
    
    REM Copy executable and readme
    copy "dist\AIA_Generator.exe" "AIA_Generator_Release\"
    copy "README.md" "AIA_Generator_Release\"
    
    REM Create sample folder
    if not exist "AIA_Generator_Release\output" mkdir "AIA_Generator_Release\output"
    
    echo.
    echo Distribution files created in AIA_Generator_Release folder
    echo You can now distribute this folder to users
) else (
    echo Build failed!
    echo Check the console output above for errors
)

echo.
pause
