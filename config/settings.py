"""
Configuration settings for Pinterest Automation Bot
"""

import os
from typing import List, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Settings:
    """Configuration settings for the Pinterest bot."""
    
    # Pinterest API Configuration
    PINTEREST_APP_ID: str = os.getenv('PINTEREST_APP_ID', '')
    PINTEREST_APP_SECRET: str = os.getenv('PINTEREST_APP_SECRET', '')
    PINTEREST_ACCESS_TOKEN: str = os.getenv('PINTEREST_ACCESS_TOKEN', '')
    PINTEREST_REFRESH_TOKEN: str = os.getenv('PINTEREST_REFRESH_TOKEN', '')
    
    # AI Image Generation Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    STABILITY_AI_KEY: str = os.getenv('STABILITY_AI_KEY', '')
    AI_PROVIDER: str = os.getenv('AI_PROVIDER', 'openai')  # 'openai' or 'stability'
    
    # Website Configuration
    WEBSITE_URL: str = os.getenv('WEBSITE_URL', 'https://yourwebsite.com')
    WEBSITE_NAME: str = os.getenv('WEBSITE_NAME', 'Your Website')
    
    # Content Strategy Configuration
    TARGET_NICHES: List[str] = [
        'lifestyle', 'home decor', 'fashion', 'food', 'travel', 
        'wellness', 'productivity', 'diy', 'inspiration', 'quotes'
    ]
    
    # Posting Schedule Configuration
    POSTING_TIMES: List[str] = ['09:00', '15:00', '20:00']  # Optimal Pinterest times
    POSTS_PER_DAY: int = int(os.getenv('POSTS_PER_DAY', '3'))
    SKIP_WEEKENDS: bool = os.getenv('SKIP_WEEKENDS', 'false').lower() == 'true'
    
    # Content Generation Settings
    GENERATE_BATCH_CONTENT: bool = os.getenv('GENERATE_BATCH_CONTENT', 'true').lower() == 'true'
    BATCH_CONTENT_SIZE: int = int(os.getenv('BATCH_CONTENT_SIZE', '7'))
    RUN_INITIAL_POST: bool = os.getenv('RUN_INITIAL_POST', 'false').lower() == 'true'
    
    # Image Configuration
    IMAGE_DIMENSIONS: Dict[str, tuple] = {
        'standard': (1000, 1500),  # Pinterest optimal ratio 2:3
        'square': (1080, 1080),
        'story': (1080, 1920)
    }
    
    # Database Configuration
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///pinterest_bot.db')
    
    # Analytics Configuration
    GOOGLE_ANALYTICS_ID: str = os.getenv('GOOGLE_ANALYTICS_ID', '')
    TRACK_CLICKS: bool = True
    GENERATE_REPORTS: bool = True
    
    # Rate Limiting
    MAX_PINS_PER_DAY: int = int(os.getenv('MAX_PINS_PER_DAY', '25'))
    API_RATE_LIMIT: int = int(os.getenv('API_RATE_LIMIT', '200'))  # Per hour
    
    # File Paths
    CONTENT_STORAGE_PATH: str = os.getenv('CONTENT_STORAGE_PATH', './content')
    LOG_FILE_PATH: str = os.getenv('LOG_FILE_PATH', './logs/pinterest_bot.log')
    
    # Content Templates
    CONTENT_TEMPLATES: Dict[str, Dict[str, Any]] = {
        'lifestyle': {
            'prompt_templates': [
                "Minimalist {theme} inspiration, clean aesthetic, modern design",
                "Cozy {theme} vibes, warm lighting, comfortable atmosphere",
                "Elegant {theme} setup, sophisticated style, premium quality"
            ],
            'hashtags': ['#lifestyle', '#inspiration', '#aesthetic', '#modern', '#design'],
            'boards': ['Lifestyle Inspiration', 'Modern Living', 'Daily Inspiration']
        },
        'home_decor': {
            'prompt_templates': [
                "Beautiful {theme} interior, scandinavian style, natural light",
                "Modern {theme} design, contemporary furniture, stylish decor",
                "Cozy {theme} space, rustic elements, warm atmosphere"
            ],
            'hashtags': ['#homedecor', '#interiordesign', '#homedesign', '#decor', '#interior'],
            'boards': ['Home Decor Ideas', 'Interior Design', 'Home Inspiration']
        },
        'wellness': {
            'prompt_templates': [
                "Peaceful {theme} scene, zen atmosphere, natural elements",
                "Healthy {theme} lifestyle, wellness routine, self-care",
                "Mindful {theme} practice, meditation space, tranquil setting"
            ],
            'hashtags': ['#wellness', '#selfcare', '#mindfulness', '#health', '#zen'],
            'boards': ['Wellness Journey', 'Self Care', 'Mindful Living']
        }
    }
    
    # Pinterest Board Configuration
    DEFAULT_BOARDS: List[Dict[str, str]] = [
        {'name': 'AI Generated Art', 'description': 'Beautiful AI-generated artwork and designs'},
        {'name': 'Daily Inspiration', 'description': 'Daily dose of inspiration and motivation'},
        {'name': 'Lifestyle Ideas', 'description': 'Modern lifestyle inspiration and tips'},
        {'name': 'Creative Designs', 'description': 'Creative and artistic design inspiration'}
    ]
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.PINTEREST_APP_ID or not self.PINTEREST_APP_SECRET:
            raise ValueError("Pinterest API credentials are required")
        
        if not self.OPENAI_API_KEY and not self.STABILITY_AI_KEY:
            raise ValueError("At least one AI provider API key is required")
        
        if not self.WEBSITE_URL:
            raise ValueError("Website URL is required")
        
        # Create directories if they don't exist
        os.makedirs(self.CONTENT_STORAGE_PATH, exist_ok=True)
        os.makedirs(os.path.dirname(self.LOG_FILE_PATH), exist_ok=True)
    
    def get_niche_config(self, niche: str) -> Dict[str, Any]:
        """Get configuration for a specific niche."""
        return self.CONTENT_TEMPLATES.get(niche, self.CONTENT_TEMPLATES['lifestyle'])
    
    def get_optimal_posting_times(self) -> List[str]:
        """Get optimal posting times based on Pinterest best practices."""
        if self.SKIP_WEEKENDS:
            # Return weekday-only times
            return self.POSTING_TIMES
        return self.POSTING_TIMES
    
    @property
    def pinterest_redirect_uri(self) -> str:
        """Get Pinterest OAuth redirect URI."""
        return f"{self.WEBSITE_URL}/auth/pinterest/callback"