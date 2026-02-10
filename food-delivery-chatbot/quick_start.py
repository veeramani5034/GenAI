"""
Quick start script to verify setup and run the chatbot
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.9+"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    return True

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Run: copy .env.example .env")
        print("   Then add your OpenAI API key")
        return False
    print("✅ .env file exists")
    return True

def check_api_key():
    """Check if OpenAI API key is configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("❌ OpenAI API key not configured")
        print("   Edit .env and add your API key")
        return False
    print("✅ OpenAI API key configured")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required = ['openai', 'langchain', 'streamlit', 'dotenv']
    missing = []
    
    for package in required:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def check_data_files():
    """Check if data files exist"""
    files = ['data/orders.json', 'data/restaurants.json']
    all_exist = True
    
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            all_exist = False
    
    return all_exist

def main():
    print("=" * 60)
    print("Food Delivery Chatbot - Quick Start")
    print("=" * 60)
    
    print("\n📋 Checking Prerequisites...\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("OpenAI API Key", check_api_key),
        ("Dependencies", check_dependencies),
        ("Data Files", check_data_files),
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n{name}:")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("\n✅ All checks passed! You're ready to go!\n")
        print("Choose how to run the chatbot:\n")
        print("1. Command Line: python chatbot.py")
        print("2. Web Interface: streamlit run app.py")
        print("\nRecommended: Web Interface (option 2)\n")
        
        choice = input("Run web interface now? (y/n): ").strip().lower()
        
        if choice == 'y':
            print("\n🚀 Starting web interface...")
            print("Opening browser at http://localhost:8501\n")
            subprocess.run(['streamlit', 'run', 'app.py'])
        else:
            print("\n👋 Run 'streamlit run app.py' when ready!")
    else:
        print("\n❌ Some checks failed. Please fix the issues above.\n")
        print("Quick fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Create .env: copy .env.example .env")
        print("3. Add OpenAI API key to .env file")
        print("\nSee SETUP_GUIDE.md for detailed instructions.\n")

if __name__ == "__main__":
    main()
