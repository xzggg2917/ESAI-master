#!/bin/bash
# ESAI Build Script for Linux/macOS
# Builds a standalone executable with English interface

echo "========================================"
echo "ESAI Application Build Tool"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if PyInstaller is installed
echo "Checking PyInstaller..."
if ! python -m pip show pyinstaller > /dev/null 2>&1; then
    echo "Installing PyInstaller..."
    python -m pip install pyinstaller
fi

# Clean previous builds
echo ""
echo "Cleaning previous builds..."
rm -rf build dist

# Build the application
echo ""
echo "Building ESAI application..."
echo "This may take several minutes..."

# Set locale to English for build process
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Run PyInstaller
pyinstaller --clean \
    --name ESAI \
    --windowed \
    --onefile \
    --add-data "rj.png:." \
    --add-data "logo.ico:." \
    --add-data "save.png:." \
    --hidden-import PIL._tkinter_finder \
    --hidden-import tkinter \
    --hidden-import matplotlib.backends.backend_tkagg \
    run_esai.py

# Check if build was successful
if [ -f "dist/ESAI" ]; then
    echo ""
    echo "========================================"
    echo "Build Successful!"
    echo "========================================"
    echo ""
    echo "Executable location: dist/ESAI"
    echo ""
    echo "To run the application:"
    echo "  ./dist/ESAI"
else
    echo ""
    echo "Build FAILED!"
    echo "Check the output above for errors"
    exit 1
fi
