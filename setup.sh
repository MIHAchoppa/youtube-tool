#!/bin/bash

# Viral Video Clip Generator - Setup Script

echo "🎬 Viral Video Clip Generator Setup"
echo "===================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"
echo ""

# Check for FFmpeg
echo "Checking for FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version 2>&1 | head -n1)
    echo "✅ $ffmpeg_version"
else
    echo "❌ FFmpeg not found!"
    echo "Please install FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo "  Windows: Download from https://ffmpeg.org/download.html"
    echo ""
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo ""

# Create directories
echo "Creating directories..."
mkdir -p uploads outputs
echo "✅ Created uploads/ and outputs/ directories"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your GROQ_API_KEY"
else
    echo "✅ .env file already exists"
fi
echo ""

# Run tests
echo "Running basic tests..."
python test_basic.py
echo ""

echo "===================================="
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GROQ_API_KEY"
echo "2. Run the web app: python app.py"
echo "3. Or use CLI: python cli.py --help"
echo ""
