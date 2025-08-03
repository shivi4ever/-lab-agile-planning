#!/usr/bin/env python3
"""
Pinterest Automation Bot - Main Entry Point
Generates AI images, posts to Pinterest daily, and drives traffic to your site.
"""

import asyncio
import logging
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from config.settings import Settings
from services.ai_image_generator import AIImageGenerator
from services.pinterest_client import PinterestClient
from services.content_strategy import ContentStrategy
from services.analytics_tracker import AnalyticsTracker
from utils.logger import setup_logger

class PinterestBot:
    """Main Pinterest automation bot class."""
    
    def __init__(self):
        self.settings = Settings()
        self.logger = setup_logger(__name__)
        
        # Initialize services
        self.ai_generator = AIImageGenerator(self.settings)
        self.pinterest_client = PinterestClient(self.settings)
        self.content_strategy = ContentStrategy(self.settings)
        self.analytics = AnalyticsTracker(self.settings)
        
        self.logger.info("Pinterest Bot initialized successfully")
    
    async def generate_and_post_content(self) -> Dict:
        """Generate AI image and post to Pinterest with optimized content."""
        try:
            self.logger.info("Starting daily content generation and posting...")
            
            # Get content strategy for today
            strategy = await self.content_strategy.get_daily_strategy()
            self.logger.info(f"Content strategy: {strategy['theme']} - {strategy['keywords']}")
            
            # Generate AI image
            image_data = await self.ai_generator.generate_image(
                prompt=strategy['prompt'],
                style=strategy['style'],
                dimensions=strategy['dimensions']
            )
            
            if not image_data:
                raise Exception("Failed to generate AI image")
            
            # Create Pinterest post
            post_data = {
                'title': strategy['title'],
                'description': strategy['description'],
                'board_id': strategy['board_id'],
                'link': strategy['website_link'],
                'alt_text': strategy['alt_text']
            }
            
            # Post to Pinterest
            pin_result = await self.pinterest_client.create_pin(
                image_path=image_data['path'],
                **post_data
            )
            
            if pin_result['success']:
                # Track analytics
                await self.analytics.track_post(pin_result['pin_id'], strategy)
                
                self.logger.info(f"Successfully posted pin: {pin_result['pin_id']}")
                return {
                    'success': True,
                    'pin_id': pin_result['pin_id'],
                    'strategy': strategy
                }
            else:
                raise Exception(f"Failed to post to Pinterest: {pin_result['error']}")
                
        except Exception as e:
            self.logger.error(f"Error in content generation/posting: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def run_daily_automation(self):
        """Run the daily automation workflow."""
        self.logger.info("Running daily Pinterest automation...")
        
        # Check if we should post today
        if not await self.content_strategy.should_post_today():
            self.logger.info("Skipping post today based on content strategy")
            return
        
        # Generate and post content
        result = await self.generate_and_post_content()
        
        if result['success']:
            self.logger.info("Daily automation completed successfully")
            
            # Optional: Generate additional content for later posting
            if self.settings.GENERATE_BATCH_CONTENT:
                await self.generate_batch_content()
        else:
            self.logger.error(f"Daily automation failed: {result.get('error', 'Unknown error')}")
    
    async def generate_batch_content(self):
        """Generate multiple pieces of content for future posting."""
        self.logger.info("Generating batch content for future posts...")
        
        try:
            batch_size = self.settings.BATCH_CONTENT_SIZE
            strategies = await self.content_strategy.get_batch_strategies(batch_size)
            
            for i, strategy in enumerate(strategies):
                self.logger.info(f"Generating batch content {i+1}/{batch_size}")
                
                # Generate image
                image_data = await self.ai_generator.generate_image(
                    prompt=strategy['prompt'],
                    style=strategy['style'],
                    dimensions=strategy['dimensions']
                )
                
                if image_data:
                    # Save for future posting
                    await self.content_strategy.save_prepared_content(strategy, image_data)
                    
        except Exception as e:
            self.logger.error(f"Error generating batch content: {str(e)}")
    
    def setup_scheduler(self):
        """Set up the posting schedule."""
        posting_times = self.settings.POSTING_TIMES
        
        for posting_time in posting_times:
            schedule.every().day.at(posting_time).do(
                lambda: asyncio.run(self.run_daily_automation())
            )
            self.logger.info(f"Scheduled daily posting at {posting_time}")
        
        # Weekly analytics report
        schedule.every().monday.at("09:00").do(
            lambda: asyncio.run(self.analytics.generate_weekly_report())
        )
    
    def run(self):
        """Start the bot with scheduling."""
        self.logger.info("Starting Pinterest Automation Bot...")
        
        # Setup scheduler
        self.setup_scheduler()
        
        # Run initial post if configured
        if self.settings.RUN_INITIAL_POST:
            asyncio.run(self.run_daily_automation())
        
        # Keep the bot running
        self.logger.info("Bot is running. Press Ctrl+C to stop.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user")

if __name__ == "__main__":
    bot = PinterestBot()
    bot.run()