#!/usr/bin/env python3
"""
Pinterest Bot Demo Test Script
Demonstrates the bot functionality without requiring actual API keys.
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import Settings
from services.content_strategy import ContentStrategy
from services.analytics_tracker import AnalyticsTracker
from utils.logger import setup_logger

async def test_content_strategy():
    """Test content strategy generation."""
    print("🎯 Testing Content Strategy...")
    
    settings = Settings()
    content_strategy = ContentStrategy(settings)
    
    # Generate a sample strategy
    strategy = await content_strategy.get_daily_strategy()
    
    print(f"📝 Generated Strategy:")
    print(f"   • Niche: {strategy['niche']}")
    print(f"   • Theme: {strategy['theme']}")
    print(f"   • Keywords: {', '.join(strategy['keywords'][:3])}")
    print(f"   • Title: {strategy['title'][:50]}...")
    print(f"   • Style: {strategy['style']}")
    print(f"   • Dimensions: {strategy['dimensions']}")
    print(f"   • Board: {strategy['board_name']}")
    
    return strategy

async def test_analytics():
    """Test analytics initialization."""
    print("\n📊 Testing Analytics...")
    
    settings = Settings()
    analytics = AnalyticsTracker(settings)
    
    # Test performance insights
    insights = await analytics.get_performance_insights(30)
    print(f"📈 Performance Insights:")
    print(f"   • Period: {insights.get('period_days', 0)} days")
    print(f"   • Total Pins: {insights.get('overall_performance', {}).get('total_pins', 0)}")
    
    return analytics

def test_configuration():
    """Test configuration loading."""
    print("⚙️  Testing Configuration...")
    
    settings = Settings()
    
    print(f"🔧 Configuration Loaded:")
    print(f"   • Website: {settings.WEBSITE_URL}")
    print(f"   • AI Provider: {settings.AI_PROVIDER}")
    print(f"   • Posts per Day: {settings.POSTS_PER_DAY}")
    print(f"   • Target Niches: {len(settings.TARGET_NICHES)} niches")
    print(f"   • Content Templates: {len(settings.CONTENT_TEMPLATES)} templates")
    print(f"   • Default Boards: {len(settings.DEFAULT_BOARDS)} boards")
    
    return settings

async def simulate_daily_workflow():
    """Simulate a daily workflow without API calls."""
    print("\n🤖 Simulating Daily Workflow...")
    
    settings = Settings()
    content_strategy = ContentStrategy(settings)
    
    # Check if we should post today
    should_post = await content_strategy.should_post_today()
    print(f"📅 Should post today: {'Yes' if should_post else 'No'}")
    
    if should_post:
        # Generate content strategy
        strategy = await content_strategy.get_daily_strategy()
        print(f"✨ Generated content strategy for {strategy['niche']}")
        
        # Simulate image generation (without actual API call)
        print(f"🎨 Would generate image with prompt: '{strategy['prompt'][:60]}...'")
        
        # Simulate Pinterest posting (without actual API call)
        print(f"📌 Would post to Pinterest board: '{strategy['board_name']}'")
        print(f"🔗 Would link to: {strategy['website_link']}")
        
        # Track the simulated post
        analytics = AnalyticsTracker(settings)
        success = await analytics.track_post("demo_pin_123", strategy)
        print(f"📊 Analytics tracking: {'Success' if success else 'Failed'}")

async def main():
    """Main test function."""
    print("=" * 60)
    print("🎨 Pinterest Automation Bot - Demo Test")
    print("=" * 60)
    
    try:
        # Test configuration
        settings = test_configuration()
        
        # Test content strategy
        strategy = await test_content_strategy()
        
        # Test analytics
        analytics = await test_analytics()
        
        # Simulate daily workflow
        await simulate_daily_workflow()
        
        print("\n" + "=" * 60)
        print("✅ All Tests Passed Successfully!")
        print("=" * 60)
        print("\n📋 Next Steps:")
        print("1. Add your actual Pinterest API credentials to .env")
        print("2. Add your OpenAI or Stability AI API key to .env")
        print("3. Update WEBSITE_URL in .env to your actual website")
        print("4. Run: python pinterest_bot/main.py")
        print("\n💡 For production use:")
        print("- Set up Pinterest Developer Account")
        print("- Configure OAuth redirect URIs")
        print("- Set up Google Analytics (optional)")
        print("- Deploy using Docker: docker-compose up -d")
        
    except Exception as e:
        print(f"\n❌ Test Failed: {str(e)}")
        print("\nPlease check your configuration and try again.")
        return False
    
    return True

if __name__ == "__main__":
    # Run the test
    success = asyncio.run(main())
    sys.exit(0 if success else 1)