#!/bin/bash

# OmniMerch ERP Setup Script
# This script helps you quickly set up the ERP system

echo "========================================="
echo "OmniMerch ERP System Setup"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.12 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found: $(pip3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install requirements
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo "⚠ Please update .env file with your settings before running the server"
else
    echo "✓ .env file already exists"
fi
echo ""

# Run migrations
echo "Running database migrations..."
python manage.py migrate
echo "✓ Migrations completed"
echo ""

# Prompt to create superuser
read -p "Do you want to create a superuser now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi
echo ""

echo "========================================="
echo "Setup completed successfully!"
echo "========================================="
echo ""
echo "To start the development server:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the server: python manage.py runserver"
echo ""
echo "To use Docker instead:"
echo "  1. Update docker-compose.yml with your settings"
echo "  2. Run: docker-compose up -d --build"
echo ""
echo "Access the application at:"
echo "  - API: http://localhost:8000/"
echo "  - Swagger Docs: http://localhost:8000/swagger/"
echo "  - Admin Panel: http://localhost:8000/admin/"
echo ""
echo "Happy coding! 🚀"
