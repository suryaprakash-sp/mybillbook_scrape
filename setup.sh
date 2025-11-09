#!/bin/bash
# Setup script for Mac/Linux

echo "=========================================="
echo "MyBillBook Scraper Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

echo "Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "IMPORTANT: Please edit .env and add your MyBillBook credentials!"
    echo ""
else
    echo "✓ .env file already exists"
fi

# Create output directory
mkdir -p output

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your credentials"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the scraper:"
echo "   - Basic: python scraper.py"
echo "   - Advanced: python cli.py --help"
echo ""
