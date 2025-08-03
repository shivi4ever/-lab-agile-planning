# 🎨 Pinterest Automation Bot

A comprehensive Pinterest automation bot that generates AI-powered images, posts daily content, and drives traffic to your website. Built with Python, featuring intelligent content strategy, analytics tracking, and scalable deployment options.

## ✨ Features

### 🤖 AI-Powered Content Generation
- **Multiple AI Providers**: Support for OpenAI DALL-E and Stability AI
- **Pinterest-Optimized Images**: Automatically generates images in optimal Pinterest dimensions (2:3 ratio)
- **Style Variations**: Multiple artistic styles (minimalist, vibrant, cozy, elegant, etc.)
- **Smart Prompting**: Context-aware prompts optimized for Pinterest engagement

### 📈 Intelligent Content Strategy
- **10+ Niche Categories**: Lifestyle, home decor, wellness, fashion, food, travel, and more
- **Seasonal Adaptation**: Content automatically adapts to seasonal themes and trends
- **Performance-Based Optimization**: AI learns from top-performing content to improve future posts
- **Keyword Optimization**: SEO-optimized titles, descriptions, and hashtags
- **Board Management**: Automatic board creation and intelligent board selection

### ⏰ Advanced Scheduling
- **Optimal Timing**: Posts at Pinterest's peak engagement times
- **Multi-Post Support**: Up to 25 pins per day with smart distribution
- **Weekend Scheduling**: Configurable weekend posting options
- **Batch Content Generation**: Pre-generates content for consistent posting

### 📊 Comprehensive Analytics
- **Pinterest Metrics**: Impressions, saves, clicks, and engagement rates
- **Website Traffic Tracking**: UTM-tagged links for traffic attribution
- **Performance Reports**: Daily and weekly automated reports
- **Content Insights**: Identifies top-performing niches, styles, and themes
- **ROI Tracking**: Measures traffic and conversion impact

### 🔗 Traffic Generation
- **Smart Link Building**: Every pin links back to your website with UTM tracking
- **Call-to-Action Optimization**: Compelling descriptions that drive clicks
- **Landing Page Optimization**: UTM parameters for detailed traffic analysis
- **Conversion Tracking**: Monitor how Pinterest traffic converts on your site

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Pinterest Developer Account
- OpenAI API key OR Stability AI key
- Your website URL

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/pinterest-automation-bot.git
cd pinterest-automation-bot
python scripts/setup.py
```

### 2. Configure Environment
Copy `.env.example` to `.env` and fill in your credentials:

```bash
# Pinterest API
PINTEREST_APP_ID=your_app_id
PINTEREST_APP_SECRET=your_app_secret
PINTEREST_ACCESS_TOKEN=your_access_token

# AI Provider (choose one)
OPENAI_API_KEY=your_openai_key
# OR
STABILITY_AI_KEY=your_stability_key

# Website
WEBSITE_URL=https://yourwebsite.com
```

### 3. Run the Bot
```bash
# Test configuration
python -m pinterest_bot.main --test

# Start automation
python -m pinterest_bot.main
```

## 📋 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PINTEREST_APP_ID` | Pinterest App ID | ✅ |
| `PINTEREST_APP_SECRET` | Pinterest App Secret | ✅ |
| `PINTEREST_ACCESS_TOKEN` | Pinterest Access Token | ✅ |
| `OPENAI_API_KEY` | OpenAI API Key | ⚠️ |
| `STABILITY_AI_KEY` | Stability AI Key | ⚠️ |
| `WEBSITE_URL` | Your website URL | ✅ |
| `POSTS_PER_DAY` | Number of posts per day (1-25) | ❌ |
| `SKIP_WEEKENDS` | Skip posting on weekends | ❌ |

⚠️ At least one AI provider key is required.

### Content Strategy Customization

Edit `config/custom_strategy.json` to customize:
- Target niches
- Custom keywords
- Posting schedule
- Content themes

```json
{
  "custom_niches": ["your_niche"],
  "custom_keywords": ["your_keywords"],
  "posting_schedule": {
    "monday": ["09:00", "15:00", "20:00"]
  }
}
```

## 🐳 Docker Deployment

### Quick Deploy
```bash
docker-compose up -d
```

### Production Deploy
```bash
# With PostgreSQL and monitoring
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 📊 Analytics & Monitoring

### Built-in Analytics
- **Daily Reports**: Automated daily performance summaries
- **Weekly Reports**: Comprehensive weekly analytics with recommendations
- **Performance Insights**: Identify top-performing content attributes
- **Traffic Attribution**: Track website traffic from Pinterest

### Accessing Reports
```python
from services.analytics_tracker import AnalyticsTracker

analytics = AnalyticsTracker(settings)
daily_report = await analytics.generate_daily_report()
weekly_report = await analytics.generate_weekly_report()
```

### Export Data
```bash
# Export analytics data
python -m pinterest_bot.analytics --export --start-date 2024-01-01 --end-date 2024-01-31
```

## 🎯 Content Strategy

### Supported Niches
1. **Lifestyle** - Minimalist living, daily routines, self-care
2. **Home Decor** - Interior design, DIY projects, organization
3. **Wellness** - Mental health, fitness, mindfulness
4. **Fashion** - Style tips, outfit ideas, sustainable fashion
5. **Food** - Recipes, meal prep, healthy eating
6. **Travel** - Destinations, travel tips, wanderlust
7. **Productivity** - Organization, time management, workspace
8. **DIY** - Craft projects, upcycling, handmade items
9. **Inspiration** - Motivational quotes, personal growth
10. **Quotes** - Daily motivation, life lessons, wisdom

### AI Image Styles
- **Minimalist**: Clean, simple compositions
- **Cozy**: Warm, comfortable atmospheres
- **Vibrant**: Bold, colorful designs
- **Elegant**: Sophisticated, premium aesthetics
- **Natural**: Organic, earthy elements
- **Modern**: Contemporary, sleek designs

## 🔧 Advanced Features

### Custom AI Prompts
Create custom image generation prompts:

```python
custom_prompts = {
    "your_niche": [
        "Custom prompt template for {theme}",
        "Another prompt variation for {theme}"
    ]
}
```

### Webhook Integration
Set up webhooks for real-time notifications:

```python
# In config/settings.py
WEBHOOK_URL = "https://your-webhook-url.com"
WEBHOOK_EVENTS = ["pin_created", "analytics_updated"]
```

### API Integration
Use the bot programmatically:

```python
from pinterest_bot.main import PinterestBot

bot = PinterestBot()
result = await bot.generate_and_post_content()
```

## 📈 Performance Optimization

### Best Practices
1. **Consistent Posting**: Maintain regular posting schedule
2. **Quality Images**: Use high-resolution, Pinterest-optimized images
3. **Keyword Research**: Use trending keywords in your niche
4. **Engagement**: Monitor and respond to comments on your pins
5. **Analytics**: Regularly review performance and adjust strategy

### Scaling Tips
- Use multiple Pinterest accounts (within Pinterest's terms)
- Implement content recycling for evergreen topics
- A/B test different posting times and frequencies
- Monitor competitor strategies and trends

## 🛠️ Development

### Setup Development Environment
```bash
git clone https://github.com/yourusername/pinterest-automation-bot.git
cd pinterest-automation-bot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black .
flake8 .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This bot is designed to help automate Pinterest marketing while respecting Pinterest's terms of service. Users are responsible for:
- Complying with Pinterest's API terms and community guidelines
- Ensuring content quality and originality
- Monitoring bot activity and performance
- Respecting rate limits and platform policies

## 🆘 Support

- **Documentation**: Check the [Wiki](https://github.com/yourusername/pinterest-automation-bot/wiki)
- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/yourusername/pinterest-automation-bot/issues)
- **Discussions**: Join the community in [GitHub Discussions](https://github.com/yourusername/pinterest-automation-bot/discussions)

## 🙏 Acknowledgments

- Pinterest API for platform integration
- OpenAI and Stability AI for image generation capabilities
- The open-source community for inspiration and tools

---

**Made with ❤️ for Pinterest marketers and content creators**
