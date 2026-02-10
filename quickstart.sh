#!/bin/bash
# Quick Start Script for Student Review System

echo "=========================================="
echo "Student Review System - Quick Start"
echo "=========================================="
echo ""

# Check Python installation
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found: $PYTHON_VERSION"
else
    echo "✗ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    echo "  Try: pip3 install -r requirements.txt"
    exit 1
fi

echo ""

# Check if CSV exists
if [ -f "data/student_reviews.csv" ]; then
    echo "✓ Student data file found"
else
    echo "✗ student_reviews.csv not found in data/"
    echo "  Please add your student data CSV file"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application, run:"
echo "  streamlit run app.py"
echo ""
echo "Demo Credentials:"
echo "  Parent - username: parent1, password: pass1234"
echo "  Teacher - username: teacher, password: admin1234"
echo ""
