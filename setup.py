#!/usr/bin/env python3
"""
Setup script for OCR Camera App
This script helps users configure the application easily.
"""

import os
import sys

def create_config_file():
    """Create config.py file if it doesn't exist"""
    config_content = '''# Configuration for OCR Camera App

# DeepSeek API Configuration
# Sign up at https://platform.deepseek.com to get your API key
# For testing, you can use any string as the API key
DEEPSEEK_API_KEY = "sk-your-api-key-here"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# OCR Configuration
OCR_LANGUAGES = ['en', 'id']  # English and Indonesian
OCR_CONFIDENCE_THRESHOLD = 0.3

# Flask Configuration
SECRET_KEY = 'your-secret-key-here-change-this-in-production'
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
'''
    
    with open('config.py', 'w') as f:
        f.write(config_content)
    print("✅ Created config.py file")

def check_dependencies():
    """Check if required packages are installed"""
    import importlib
    
    package_mapping = {
        'opencv-python': 'cv2',
        'pillow': 'PIL',
        'flask': 'flask',
        'easyocr': 'easyocr',
        'numpy': 'numpy',
        'openai': 'openai'
    }
    
    missing_packages = []
    
    for package, import_name in package_mapping.items():
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed")
        return True

def main():
    print("🚀 OCR Camera App Setup")
    print("=" * 30)
    
    # Check if config.py exists
    if not os.path.exists('config.py'):
        print("📝 Creating configuration file...")
        create_config_file()
    else:
        print("✅ config.py already exists")
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    deps_ok = check_dependencies()
    
    if not deps_ok:
        sys.exit(1)
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit config.py to add your DeepSeek API key (optional)")
    print("2. Run: python app.py")
    print("3. Open your browser to http://localhost:5000")
    print("\nNote: The app will work without a real API key for basic functionality.")

if __name__ == "__main__":
    main()
