#!/usr/bin/env python3
"""
Pinterest Automation Bot Setup Script
Helps users initialize and configure the bot for first-time use.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    """Print setup banner."""
    print("=" * 60)
    print("🎨 Pinterest Automation Bot Setup")
    print("=" * 60)
    print("This script will help you set up your Pinterest automation bot.")
    print()

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print("✅ Python version check passed")

def create_directories():
    """Create necessary directories."""
    directories = [
        'content',
        'logs',
        'data',
        'config',
        'services',
        'utils',
        'scripts'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")

def install_dependencies():
    """Install required Python packages."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies. Please install manually using:")
        print("   pip install -r requirements.txt")
        return False
    return True

def create_env_file():
    """Create .env file from template."""
    if os.path.exists('.env'):
        response = input("\n.env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Skipping .env file creation")
            return
    
    if os.path.exists('.env.example'):
        with open('.env.example', 'r') as f:
            content = f.read()
        
        with open('.env', 'w') as f:
            f.write(content)
        
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your actual API keys and configuration")
    else:
        print("❌ .env.example file not found")

def setup_pinterest_oauth():
    """Guide user through Pinterest OAuth setup."""
    print("\n🔑 Pinterest API Setup")
    print("To use this bot, you need to set up Pinterest API access:")
    print()
    print("1. Go to https://developers.pinterest.com/")
    print("2. Create a new app")
    print("3. Get your App ID and App Secret")
    print("4. Set up OAuth redirect URI: http://localhost:5000/auth/pinterest/callback")
    print("5. Generate access token")
    print()
    print("Add these credentials to your .env file:")
    print("- PINTEREST_APP_ID")
    print("- PINTEREST_APP_SECRET") 
    print("- PINTEREST_ACCESS_TOKEN")
    print("- PINTEREST_REFRESH_TOKEN")

def setup_ai_providers():
    """Guide user through AI provider setup."""
    print("\n🤖 AI Image Generation Setup")
    print("Choose your AI image generation provider:")
    print()
    print("Option 1: OpenAI DALL-E")
    print("- Go to https://platform.openai.com/api-keys")
    print("- Create an API key")
    print("- Add OPENAI_API_KEY to your .env file")
    print()
    print("Option 2: Stability AI")
    print("- Go to https://platform.stability.ai/account/keys")
    print("- Create an API key")
    print("- Add STABILITY_AI_KEY to your .env file")
    print()
    print("You can use both providers and switch between them using AI_PROVIDER setting")

def create_sample_config():
    """Create sample configuration files."""
    # Create sample content strategy config
    sample_strategy = {
        "custom_niches": [
            "your_custom_niche_1",
            "your_custom_niche_2"
        ],
        "custom_keywords": [
            "your_brand_keywords",
            "your_industry_terms"
        ],
        "posting_schedule": {
            "monday": ["09:00", "15:00", "20:00"],
            "tuesday": ["09:00", "15:00", "20:00"],
            "wednesday": ["09:00", "15:00", "20:00"],
            "thursday": ["09:00", "15:00", "20:00"],
            "friday": ["09:00", "15:00", "20:00"],
            "saturday": ["10:00", "16:00"],
            "sunday": ["10:00", "16:00"]
        }
    }
    
    with open('config/custom_strategy.json', 'w') as f:
        json.dump(sample_strategy, f, indent=2)
    
    print("✅ Created sample configuration files")

def run_initial_test():
    """Run initial test to verify setup."""
    print("\n🧪 Running initial test...")
    
    try:
        # Test imports
        from config.settings import Settings
        from services.content_strategy import ContentStrategy
        
        # Test basic initialization
        settings = Settings()
        print("✅ Configuration loaded successfully")
        
        # Test database initialization
        content_strategy = ContentStrategy(settings)
        print("✅ Database initialization successful")
        
        print("✅ Initial test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Initial test failed: {str(e)}")
        print("Please check your configuration and try again")
        return False

def print_next_steps():
    """Print next steps for the user."""
    print("\n🚀 Setup Complete!")
    print("=" * 60)
    print("Next steps:")
    print()
    print("1. Edit the .env file with your API keys:")
    print("   - Pinterest API credentials")
    print("   - AI provider API key (OpenAI or Stability AI)")
    print("   - Your website URL")
    print()
    print("2. Customize your content strategy in config/custom_strategy.json")
    print()
    print("3. Test the bot:")
    print("   python -m pinterest_bot.main --test")
    print()
    print("4. Run the bot:")
    print("   python -m pinterest_bot.main")
    print()
    print("5. Monitor logs in the logs/ directory")
    print()
    print("For more information, check the README.md file")
    print("=" * 60)

def main():
    """Main setup function."""
    print_banner()
    
    # Check requirements
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create configuration files
    create_env_file()
    create_sample_config()
    
    # Provide setup guidance
    setup_pinterest_oauth()
    setup_ai_providers()
    
    # Run initial test
    if run_initial_test():
        print_next_steps()
    else:
        print("\n❌ Setup completed with errors. Please review the configuration.")

if __name__ == "__main__":
    main()