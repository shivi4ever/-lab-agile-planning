#!/usr/bin/env python3
"""
Pinterest Bot Runner Script
Simple script to run the Pinterest automation bot.
"""

import os
import sys
import subprocess

def main():
    """Run the Pinterest bot."""
    print("🎨 Starting Pinterest Automation Bot...")
    
    # Check if virtual environment exists
    venv_path = "./pinterest_bot_env"
    if not os.path.exists(venv_path):
        print("❌ Virtual environment not found. Please run setup first:")
        print("   python3 scripts/setup.py")
        return False
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("❌ .env file not found. Please copy .env.example to .env and configure it:")
        print("   cp .env.example .env")
        print("   # Then edit .env with your API keys")
        return False
    
    try:
        # Import and run the bot (assumes virtual environment is already activated)
        from pinterest_bot.main import PinterestBot
        
        bot = PinterestBot()
        print("🚀 Pinterest Bot initialized successfully!")
        print("📋 Bot will start posting according to your schedule...")
        
        # Run the bot
        bot.run()
        
    except KeyboardInterrupt:
        print("\n⏹️  Bot stopped by user")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure you're in the virtual environment:")
        print("   source pinterest_bot_env/bin/activate")
        return False
    except Exception as e:
        print(f"❌ Error running bot: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)