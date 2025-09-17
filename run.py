#!/usr/bin/env python3
"""
Voice AI Agent - Easy Startup Script
This script helps you set up and run the Voice AI Agent application.
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.7+"""
    if sys.version_info < (3, 7):
        print(" Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f" Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install required packages"""
    print("\n Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print(" Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print(" Failed to install dependencies!")
        sys.exit(1)

def check_env_file():
    """Check if .env file exists and has API keys"""
    if not os.path.exists('.env'):
        print("\n .env file not found!")
        print("Creating .env file from template...")
        
        with open('.env.example', 'r') as source, open('.env', 'w') as target:
            target.write(source.read())
        
        print(" .env file created!")
        print(" Please edit .env file and add your API keys before running the app.")
        return False
    
    # Check if API keys are set
    with open('.env', 'r') as f:
        content = f.read()
        if 'your_elevenlabs_api_key_here' in content:
            print("\n  Please update your ElevenLabs API key in .env file")
            return False
    
    print(" .env file configured!")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['templates', 'static', 'static/audio']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print(" Directories created!")

def run_app():
    """Run the Flask application"""
    print("\n Starting Voice AI Agent...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the application")
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError:
        print(" app.py not found! Make sure all files are in the correct location.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n Application stopped by user")
    except Exception as e:
        print(f" Error running application: {e}")

def main():
    """Main setup and run function"""
    print(" Voice AI Agent Setup")
    print("=" * 30)
    
    # Check Python version
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Install dependencies
    install_dependencies()
    
    # Check environment file
    env_ready = check_env_file()
    
    if not env_ready:
        print("\n Setup incomplete!")
        print("Please:")
        print("1. Edit .env file with your ElevenLabs API key")
        print("2. Run this script again")
        return
    
    print("\n Setup complete!")
    input("Press Enter to start the application...")
    
    # Run the application
    run_app()

if __name__ == "__main__":
    main()