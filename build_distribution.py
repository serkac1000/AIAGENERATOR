"""
Build distribution package for Windows deployment
Creates a complete package with executable and all necessary files
"""

import os
import shutil
import zipfile
import subprocess
import sys
from pathlib import Path

def create_distribution():
    """Create complete distribution package"""
    print("Creating MIT App Inventor AIA Generator distribution...")
    
    # Create distribution directory
    dist_dir = "AIA_Generator_Windows"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    # Copy source files
    source_files = [
        "main.py", "gui.py", "ai_agent.py", "aia_generator.py", 
        "config.py", "utils.py", "README.md", "test_app.py", "create_sample_aia.py"
    ]
    
    for file in source_files:
        if os.path.exists(file):
            shutil.copy2(file, dist_dir)
            print(f"Copied {file}")
    
    # Create requirements file
    requirements_content = """google-generativeai>=0.8.0
pillow>=10.0.0
pyinstaller>=6.0.0"""
    
    with open(os.path.join(dist_dir, "requirements.txt"), "w") as f:
        f.write(requirements_content)
    
    # Copy batch files
    batch_files = ["setup.bat", "build.bat"]
    for file in batch_files:
        if os.path.exists(file):
            shutil.copy2(file, dist_dir)
            print(f"Copied {file}")
    
    # Create run.bat for easy execution
    run_bat_content = """@echo off
echo Starting MIT App Inventor AIA Generator...
python main.py
if errorlevel 1 (
    echo.
    echo Error running the application.
    echo Please run setup.bat first to install dependencies.
    pause
)"""
    
    with open(os.path.join(dist_dir, "run.bat"), "w") as f:
        f.write(run_bat_content)
    
    # Create output directory
    os.makedirs(os.path.join(dist_dir, "output"), exist_ok=True)
    
    # Create install instructions
    install_instructions = """# MIT App Inventor AIA Generator - Installation Guide

## Quick Start (Windows)

1. **Install Python 3.8+**
   - Download from: https://www.python.org/downloads/
   - IMPORTANT: Check "Add Python to PATH" during installation

2. **Install Dependencies**
   - Double-click `setup.bat`
   - Wait for installation to complete

3. **Run Application**
   - Double-click `run.bat` OR
   - Double-click `main.py` OR
   - Open command prompt and run: `python main.py`

4. **Get Google AI API Key**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in and create API key
   - Paste into application

## Building Executable (Optional)

1. Run `setup.bat` first
2. Run `build.bat` to create standalone .exe file
3. Executable will be in `dist` folder

## Troubleshooting

- If app won't start: Check Python installation and run setup.bat
- If API errors: Verify your Google AI API key
- Check app.log file for detailed error information
"""
    
    with open(os.path.join(dist_dir, "INSTALL.md"), "w") as f:
        f.write(install_instructions)
    
    print(f"\nDistribution created in '{dist_dir}' folder")
    
    # Create ZIP file
    zip_filename = f"{dist_dir}.zip"
    print(f"Creating ZIP file: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, ".")
                zipf.write(file_path, arc_name)
    
    print(f"\nComplete! Distribution package: {zip_filename}")
    print("\nContents:")
    print("- Source code files")
    print("- Setup and run scripts")
    print("- Installation instructions")
    print("- Requirements file")
    print("- Empty output folder")
    
    return zip_filename

if __name__ == "__main__":
    create_distribution()