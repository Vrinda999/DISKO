#!/bin/bash

echo "🔧 Starting setup for Disk Forensics Tool..."

# 1. Install system dependencies
echo "📦 Installing system tools (requires sudo)..."
sudo apt update
sudo apt install -y dcfldd sleuthkit binwalk

# 2. Set up Python virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Python packages
echo "📚 Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete! To start, run:"
echo "source .venv/bin/activate && python main.py"
