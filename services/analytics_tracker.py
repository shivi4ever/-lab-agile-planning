"""
Analytics Tracking Service
Monitors Pinterest performance and website traffic from Pinterest automation.
"""

import asyncio
import json
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import os
from dataclasses import dataclass
import aiohttp

@dataclass
class PinAnalytics:
    """Data class for pin analytics."""
    pin_id: str
    impressions: int
    saves: int
    clicks: int
    outbound_clicks: int
    engagement_rate: float
    date: str

@dataclass
class TrafficData:
    """Data class for website traffic data."""
    source: str
    sessions: int
    page_views: int
    bounce_rate: float
    avg_session_duration: float
    conversions: int
    date: str

class AnalyticsTracker:
    """Analytics tracking and reporting service."""
    
    def __init__(self, settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        if settings.DATABASE_URL.startswith('sqlite:///'):
            db_path = settings.DATABASE_URL.replace('sqlite:///', '')
            if db_path.startswith('./'):
                self.db_path = db_path.replace('.db', '_analytics.db')
            else:
                self.db_path = os.path.join('.', db_path.replace('.db', '_analytics.db'))
        else:
            self.db_path = os.path.join('./data', 'analytics.db')
        
        self._init_database()
        
        # Pinterest client reference (will be injected)
        self.pinterest_client = None
        
        # Google Analytics setup
        self.ga_property_id = settings.GOOGLE_ANALYTICS_ID
    
    def _init_database(self):
        """Initialize analytics database."""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Pin analytics table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS pin_analytics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pin_id TEXT NOT NULL,
                        strategy_id INTEGER,
                        impressions INTEGER DEFAULT 0,
                        saves INTEGER DEFAULT 0,
                        clicks INTEGER DEFAULT 0,
                        outbound_clicks INTEGER DEFAULT 0,
                        engagement_rate REAL DEFAULT 0,
                        ctr REAL DEFAULT 0,
                        save_rate REAL DEFAULT 0,
                        date TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Website traffic table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS website_traffic (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source TEXT NOT NULL,
                        medium TEXT,
                        campaign TEXT,
                        sessions INTEGER DEFAULT 0,
                        page_views INTEGER DEFAULT 0,
                        unique_page_views INTEGER DEFAULT 0,
                        bounce_rate REAL DEFAULT 0,
                        avg_session_duration REAL DEFAULT 0,
                        conversions INTEGER DEFAULT 0,
                        revenue REAL DEFAULT 0,
                        date TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Performance reports table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS performance_reports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        report_type TEXT NOT NULL,
                        report_data TEXT NOT NULL,
                        metrics TEXT NOT NULL,
                        date_range TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Content performance tracking
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS content_performance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        pin_id TEXT NOT NULL,
                        niche TEXT,
                        theme TEXT,
                        keywords TEXT,
                        board_name TEXT,
                        style TEXT,
                        total_impressions INTEGER DEFAULT 0,
                        total_saves INTEGER DEFAULT 0,
                        total_clicks INTEGER DEFAULT 0,
                        total_outbound_clicks INTEGER DEFAULT 0,
                        performance_score REAL DEFAULT 0,
                        roi_score REAL DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                self.logger.info("Analytics database initialized")
                
        except Exception as e:
            self.logger.error(f"Error initializing analytics database: {str(e)}")
    
    def set_pinterest_client(self, pinterest_client):
        """Set Pinterest client reference."""
        self.pinterest_client = pinterest_client
    
    async def track_post(self, pin_id: str, strategy: Dict[str, Any]) -> bool:
        """Track a new Pinterest post."""
        try:
            # Save initial tracking data
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Insert into content performance tracking
                cursor.execute('''
                    INSERT INTO content_performance 
                    (pin_id, niche, theme, keywords, board_name, style)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    pin_id,
                    strategy.get('niche'),
                    strategy.get('theme'),
                    json.dumps(strategy.get('keywords', [])),
                    strategy.get('board_name'),
                    strategy.get('style')
                ))
                
                # Initial analytics entry
                cursor.execute('''
                    INSERT INTO pin_analytics (pin_id, date)
                    VALUES (?, ?)
                ''', (pin_id, datetime.now().strftime('%Y-%m-%d')))
                
                conn.commit()
            
            self.logger.info(f"Started tracking pin: {pin_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error tracking post: {str(e)}")
            return False
    
    async def update_pin_analytics(self, pin_id: str) -> bool:
        """Update analytics data for a specific pin."""
        try:
            if not self.pinterest_client:
                self.logger.warning("Pinterest client not available for analytics update")
                return False
            
            # Get analytics from Pinterest API
            analytics_data = await self.pinterest_client.get_pin_analytics(pin_id)
            
            if not analytics_data:
                self.logger.warning(f"No analytics data received for pin: {pin_id}")
                return False
            
            # Parse Pinterest analytics response
            metrics = self._parse_pinterest_analytics(analytics_data)
            
            if not metrics:
                return False
            
            # Update database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Update pin analytics
                cursor.execute('''
                    UPDATE pin_analytics SET
                        impressions = ?,
                        saves = ?,
                        clicks = ?,
                        outbound_clicks = ?,
                        engagement_rate = ?,
                        ctr = ?,
                        save_rate = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE pin_id = ?
                ''', (
                    metrics['impressions'],
                    metrics['saves'],
                    metrics['clicks'],
                    metrics['outbound_clicks'],
                    metrics['engagement_rate'],
                    metrics['ctr'],
                    metrics['save_rate'],
                    pin_id
                ))
                
                # Update content performance
                cursor.execute('''
                    UPDATE content_performance SET
                        total_impressions = ?,
                        total_saves = ?,
                        total_clicks = ?,
                        total_outbound_clicks = ?,
                        performance_score = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE pin_id = ?
                ''', (
                    metrics['impressions'],
                    metrics['saves'],
                    metrics['clicks'],
                    metrics['outbound_clicks'],
                    self._calculate_performance_score(metrics),
                    pin_id
                ))
                
                conn.commit()
            
            self.logger.info(f"Updated analytics for pin: {pin_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating pin analytics: {str(e)}")
            return False
    
    async def update_all_pin_analytics(self) -> int:
        """Update analytics for all tracked pins."""
        try:
            # Get all pins that need updating (last 30 days)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT DISTINCT pin_id FROM pin_analytics
                    WHERE date > date('now', '-30 days')
                    ORDER BY updated_at ASC
                ''')
                
                pin_ids = [row[0] for row in cursor.fetchall()]
            
            updated_count = 0
            
            # Update each pin with rate limiting
            for i, pin_id in enumerate(pin_ids):
                if await self.update_pin_analytics(pin_id):
                    updated_count += 1
                
                # Rate limiting - don't overwhelm Pinterest API
                if i % 10 == 0 and i > 0:
                    await asyncio.sleep(60)  # Wait 1 minute every 10 requests
                else:
                    await asyncio.sleep(5)  # 5 second delay between requests
            
            self.logger.info(f"Updated analytics for {updated_count}/{len(pin_ids)} pins")
            return updated_count
            
        except Exception as e:
            self.logger.error(f"Error updating all pin analytics: {str(e)}")
            return 0
    
    async def track_website_traffic(self) -> bool:
        """Track website traffic from Pinterest (placeholder for Google Analytics integration)."""
        try:
            if not self.ga_property_id:
                self.logger.warning("Google Analytics not configured")
                return False
            
            # This would integrate with Google Analytics API
            # For now, we'll create sample data structure
            
            traffic_data = await self._get_pinterest_traffic_data()
            
            if traffic_data:
                # Save to database
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO website_traffic 
                        (source, medium, campaign, sessions, page_views, bounce_rate, 
                         avg_session_duration, conversions, date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        'pinterest',
                        'social',
                        'pinterest_automation',
                        traffic_data['sessions'],
                        traffic_data['page_views'],
                        traffic_data['bounce_rate'],
                        traffic_data['avg_session_duration'],
                        traffic_data['conversions'],
                        datetime.now().strftime('%Y-%m-%d')
                    ))
                    conn.commit()
                
                self.logger.info("Website traffic data updated")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error tracking website traffic: {str(e)}")
            return False
    
    async def generate_daily_report(self) -> Dict[str, Any]:
        """Generate daily performance report."""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Pin performance today
                cursor.execute('''
                    SELECT COUNT(*) as pins_posted,
                           SUM(impressions) as total_impressions,
                           SUM(saves) as total_saves,
                           SUM(clicks) as total_clicks,
                           SUM(outbound_clicks) as total_outbound_clicks,
                           AVG(engagement_rate) as avg_engagement
                    FROM pin_analytics
                    WHERE date = ?
                ''', (today,))
                
                today_stats = cursor.fetchone()
                
                # Compare with yesterday
                cursor.execute('''
                    SELECT COUNT(*) as pins_posted,
                           SUM(impressions) as total_impressions,
                           SUM(saves) as total_saves,
                           SUM(clicks) as total_clicks,
                           SUM(outbound_clicks) as total_outbound_clicks,
                           AVG(engagement_rate) as avg_engagement
                    FROM pin_analytics
                    WHERE date = ?
                ''', (yesterday,))
                
                yesterday_stats = cursor.fetchone()
                
                # Top performing content
                cursor.execute('''
                    SELECT cp.niche, cp.theme, cp.performance_score,
                           pa.impressions, pa.saves, pa.clicks
                    FROM content_performance cp
                    JOIN pin_analytics pa ON cp.pin_id = pa.pin_id
                    WHERE pa.date = ?
                    ORDER BY cp.performance_score DESC
                    LIMIT 5
                ''', (today,))
                
                top_content = cursor.fetchall()
                
                # Website traffic
                cursor.execute('''
                    SELECT sessions, page_views, bounce_rate, conversions
                    FROM website_traffic
                    WHERE source = 'pinterest' AND date = ?
                ''', (today,))
                
                traffic_stats = cursor.fetchone()
            
            # Build report
            report = {
                'date': today,
                'pinterest_stats': {
                    'pins_posted': today_stats[0] or 0,
                    'total_impressions': today_stats[1] or 0,
                    'total_saves': today_stats[2] or 0,
                    'total_clicks': today_stats[3] or 0,
                    'total_outbound_clicks': today_stats[4] or 0,
                    'avg_engagement_rate': round(today_stats[5] or 0, 2)
                },
                'comparison': {
                    'impressions_change': self._calculate_change(today_stats[1], yesterday_stats[1] if yesterday_stats else 0),
                    'saves_change': self._calculate_change(today_stats[2], yesterday_stats[2] if yesterday_stats else 0),
                    'clicks_change': self._calculate_change(today_stats[3], yesterday_stats[3] if yesterday_stats else 0)
                },
                'top_content': [
                    {
                        'niche': content[0],
                        'theme': content[1],
                        'performance_score': round(content[2], 2),
                        'impressions': content[3],
                        'saves': content[4],
                        'clicks': content[5]
                    } for content in top_content
                ],
                'website_traffic': {
                    'sessions': traffic_stats[0] if traffic_stats else 0,
                    'page_views': traffic_stats[1] if traffic_stats else 0,
                    'bounce_rate': round(traffic_stats[2], 2) if traffic_stats else 0,
                    'conversions': traffic_stats[3] if traffic_stats else 0
                } if traffic_stats else None
            }
            
            # Save report
            self._save_report('daily', report, today)
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating daily report: {str(e)}")
            return {}
    
    async def generate_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly performance report."""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            date_range = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Weekly Pinterest stats
                cursor.execute('''
                    SELECT COUNT(*) as pins_posted,
                           SUM(impressions) as total_impressions,
                           SUM(saves) as total_saves,
                           SUM(clicks) as total_clicks,
                           SUM(outbound_clicks) as total_outbound_clicks,
                           AVG(engagement_rate) as avg_engagement
                    FROM pin_analytics
                    WHERE date BETWEEN ? AND ?
                ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                
                week_stats = cursor.fetchone()
                
                # Best performing niches
                cursor.execute('''
                    SELECT cp.niche, 
                           COUNT(*) as pin_count,
                           AVG(cp.performance_score) as avg_score,
                           SUM(pa.impressions) as total_impressions,
                           SUM(pa.saves) as total_saves
                    FROM content_performance cp
                    JOIN pin_analytics pa ON cp.pin_id = pa.pin_id
                    WHERE pa.date BETWEEN ? AND ?
                    GROUP BY cp.niche
                    ORDER BY avg_score DESC
                ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                
                niche_performance = cursor.fetchall()
                
                # Daily breakdown
                cursor.execute('''
                    SELECT date,
                           COUNT(*) as pins,
                           SUM(impressions) as impressions,
                           SUM(saves) as saves,
                           SUM(clicks) as clicks
                    FROM pin_analytics
                    WHERE date BETWEEN ? AND ?
                    GROUP BY date
                    ORDER BY date
                ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                
                daily_breakdown = cursor.fetchall()
                
                # Website traffic summary
                cursor.execute('''
                    SELECT SUM(sessions) as total_sessions,
                           SUM(page_views) as total_page_views,
                           AVG(bounce_rate) as avg_bounce_rate,
                           SUM(conversions) as total_conversions
                    FROM website_traffic
                    WHERE source = 'pinterest' AND date BETWEEN ? AND ?
                ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                
                traffic_summary = cursor.fetchone()
            
            # Build comprehensive report
            report = {
                'date_range': date_range,
                'summary': {
                    'pins_posted': week_stats[0] or 0,
                    'total_impressions': week_stats[1] or 0,
                    'total_saves': week_stats[2] or 0,
                    'total_clicks': week_stats[3] or 0,
                    'total_outbound_clicks': week_stats[4] or 0,
                    'avg_engagement_rate': round(week_stats[5] or 0, 2),
                    'avg_pins_per_day': round((week_stats[0] or 0) / 7, 1)
                },
                'niche_performance': [
                    {
                        'niche': niche[0],
                        'pin_count': niche[1],
                        'avg_performance_score': round(niche[2], 2),
                        'total_impressions': niche[3],
                        'total_saves': niche[4]
                    } for niche in niche_performance
                ],
                'daily_breakdown': [
                    {
                        'date': day[0],
                        'pins': day[1],
                        'impressions': day[2],
                        'saves': day[3],
                        'clicks': day[4]
                    } for day in daily_breakdown
                ],
                'website_traffic': {
                    'total_sessions': traffic_summary[0] if traffic_summary else 0,
                    'total_page_views': traffic_summary[1] if traffic_summary else 0,
                    'avg_bounce_rate': round(traffic_summary[2], 2) if traffic_summary else 0,
                    'total_conversions': traffic_summary[3] if traffic_summary else 0
                } if traffic_summary else None,
                'recommendations': self._generate_recommendations(niche_performance, week_stats)
            }
            
            # Save report
            self._save_report('weekly', report, date_range)
            
            self.logger.info(f"Generated weekly report for {date_range}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating weekly report: {str(e)}")
            return {}
    
    def _parse_pinterest_analytics(self, analytics_data: Dict) -> Optional[Dict]:
        """Parse Pinterest analytics API response."""
        try:
            if not analytics_data or 'data' not in analytics_data:
                return None
            
            data = analytics_data['data']
            
            # Extract metrics (Pinterest API format may vary)
            impressions = 0
            saves = 0
            clicks = 0
            outbound_clicks = 0
            
            for metric in data:
                metric_type = metric.get('metric_type', '')
                value = sum(day.get('value', 0) for day in metric.get('daily_metrics', []))
                
                if metric_type == 'IMPRESSION':
                    impressions = value
                elif metric_type == 'SAVE':
                    saves = value
                elif metric_type == 'PIN_CLICK':
                    clicks = value
                elif metric_type == 'OUTBOUND_CLICK':
                    outbound_clicks = value
            
            # Calculate derived metrics
            engagement_rate = ((saves + clicks) / impressions * 100) if impressions > 0 else 0
            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            save_rate = (saves / impressions * 100) if impressions > 0 else 0
            
            return {
                'impressions': impressions,
                'saves': saves,
                'clicks': clicks,
                'outbound_clicks': outbound_clicks,
                'engagement_rate': engagement_rate,
                'ctr': ctr,
                'save_rate': save_rate
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing Pinterest analytics: {str(e)}")
            return None
    
    def _calculate_performance_score(self, metrics: Dict) -> float:
        """Calculate overall performance score for a pin."""
        try:
            impressions = metrics.get('impressions', 0)
            saves = metrics.get('saves', 0)
            clicks = metrics.get('clicks', 0)
            outbound_clicks = metrics.get('outbound_clicks', 0)
            
            if impressions == 0:
                return 0.0
            
            # Weighted scoring system
            save_weight = 0.4
            click_weight = 0.3
            outbound_weight = 0.3
            
            save_score = (saves / impressions) * 100 * save_weight
            click_score = (clicks / impressions) * 100 * click_weight
            outbound_score = (outbound_clicks / impressions) * 100 * outbound_weight
            
            total_score = save_score + click_score + outbound_score
            
            # Normalize to 0-100 scale
            return min(100.0, max(0.0, total_score))
            
        except Exception as e:
            self.logger.error(f"Error calculating performance score: {str(e)}")
            return 0.0
    
    def _calculate_change(self, current: Optional[int], previous: Optional[int]) -> Dict[str, Any]:
        """Calculate percentage change between two values."""
        current = current or 0
        previous = previous or 0
        
        if previous == 0:
            return {'value': current, 'change': 0, 'direction': 'neutral'}
        
        change_percent = ((current - previous) / previous) * 100
        direction = 'up' if change_percent > 0 else 'down' if change_percent < 0 else 'neutral'
        
        return {
            'value': current,
            'change': round(change_percent, 1),
            'direction': direction
        }
    
    async def _get_pinterest_traffic_data(self) -> Optional[Dict]:
        """Get Pinterest traffic data from Google Analytics (placeholder)."""
        try:
            # This would integrate with Google Analytics API
            # For now, return sample structure
            return {
                'sessions': 0,
                'page_views': 0,
                'bounce_rate': 0.0,
                'avg_session_duration': 0.0,
                'conversions': 0
            }
            
        except Exception as e:
            self.logger.error(f"Error getting Pinterest traffic data: {str(e)}")
            return None
    
    def _save_report(self, report_type: str, report_data: Dict, date_range: str):
        """Save report to database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO performance_reports (report_type, report_data, metrics, date_range)
                    VALUES (?, ?, ?, ?)
                ''', (
                    report_type,
                    json.dumps(report_data),
                    json.dumps(list(report_data.keys())),
                    date_range
                ))
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error saving report: {str(e)}")
    
    def _generate_recommendations(self, niche_performance: List, week_stats: Tuple) -> List[str]:
        """Generate actionable recommendations based on performance data."""
        recommendations = []
        
        try:
            if niche_performance:
                # Best performing niche
                best_niche = niche_performance[0]
                recommendations.append(f"Focus more on '{best_niche[0]}' content - it's your top performer this week")
                
                # Low performing niches
                if len(niche_performance) > 1:
                    worst_niche = niche_performance[-1]
                    if worst_niche[2] < 20:  # Low performance score
                        recommendations.append(f"Consider adjusting your '{worst_niche[0]}' content strategy")
            
            # Posting frequency
            pins_posted = week_stats[0] or 0
            if pins_posted < 7:
                recommendations.append("Increase posting frequency - aim for at least 1 pin per day")
            elif pins_posted > 21:
                recommendations.append("Consider reducing posting frequency to avoid overwhelming your audience")
            
            # Engagement rate
            avg_engagement = week_stats[5] or 0
            if avg_engagement < 2:
                recommendations.append("Work on improving engagement - try more eye-catching visuals and compelling titles")
            
            # General recommendations
            recommendations.append("Continue monitoring performance and adjust content strategy based on top-performing pins")
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
        
        return recommendations
    
    async def get_performance_insights(self, days: int = 30) -> Dict[str, Any]:
        """Get performance insights for the specified period."""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Overall metrics
                cursor.execute('''
                    SELECT AVG(performance_score) as avg_score,
                           COUNT(*) as total_pins,
                           SUM(total_impressions) as total_impressions,
                           SUM(total_saves) as total_saves,
                           SUM(total_clicks) as total_clicks
                    FROM content_performance
                    WHERE created_at BETWEEN ? AND ?
                ''', (start_date.isoformat(), end_date.isoformat()))
                
                overall_stats = cursor.fetchone()
                
                # Best performing content attributes
                cursor.execute('''
                    SELECT niche, AVG(performance_score) as avg_score
                    FROM content_performance
                    WHERE created_at BETWEEN ? AND ?
                    GROUP BY niche
                    ORDER BY avg_score DESC
                ''', (start_date.isoformat(), end_date.isoformat()))
                
                niche_insights = cursor.fetchall()
                
                cursor.execute('''
                    SELECT style, AVG(performance_score) as avg_score
                    FROM content_performance
                    WHERE created_at BETWEEN ? AND ?
                    GROUP BY style
                    ORDER BY avg_score DESC
                ''', (start_date.isoformat(), end_date.isoformat()))
                
                style_insights = cursor.fetchall()
            
            insights = {
                'period_days': days,
                'overall_performance': {
                    'avg_performance_score': round(overall_stats[0] or 0, 2),
                    'total_pins': overall_stats[1] or 0,
                    'total_impressions': overall_stats[2] or 0,
                    'total_saves': overall_stats[3] or 0,
                    'total_clicks': overall_stats[4] or 0
                },
                'best_niches': [{'niche': n[0], 'avg_score': round(n[1], 2)} for n in niche_insights[:5]],
                'best_styles': [{'style': s[0], 'avg_score': round(s[1], 2)} for s in style_insights[:5]]
            }
            
            return insights
            
        except Exception as e:
            self.logger.error(f"Error getting performance insights: {str(e)}")
            return {}
    
    async def cleanup_old_data(self, days_to_keep: int = 90):
        """Clean up old analytics data to keep database size manageable."""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime('%Y-%m-%d')
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clean up old pin analytics
                cursor.execute('DELETE FROM pin_analytics WHERE date < ?', (cutoff_date,))
                deleted_pins = cursor.rowcount
                
                # Clean up old traffic data
                cursor.execute('DELETE FROM website_traffic WHERE date < ?', (cutoff_date,))
                deleted_traffic = cursor.rowcount
                
                # Clean up old reports
                cursor.execute('DELETE FROM performance_reports WHERE created_at < ?', (cutoff_date,))
                deleted_reports = cursor.rowcount
                
                conn.commit()
            
            self.logger.info(f"Cleaned up old data: {deleted_pins} pin records, {deleted_traffic} traffic records, {deleted_reports} reports")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up old data: {str(e)}")
    
    async def export_analytics_data(self, start_date: str, end_date: str, format: str = 'json') -> Optional[str]:
        """Export analytics data for external analysis."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get comprehensive data
                cursor.execute('''
                    SELECT pa.*, cp.niche, cp.theme, cp.keywords, cp.board_name, cp.style
                    FROM pin_analytics pa
                    LEFT JOIN content_performance cp ON pa.pin_id = cp.pin_id
                    WHERE pa.date BETWEEN ? AND ?
                    ORDER BY pa.date DESC
                ''', (start_date, end_date))
                
                data = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                # Convert to list of dictionaries
                export_data = [dict(zip(columns, row)) for row in data]
            
            if format.lower() == 'json':
                export_content = json.dumps(export_data, indent=2, default=str)
                filename = f"pinterest_analytics_{start_date}_to_{end_date}.json"
            else:
                # CSV format
                import csv
                import io
                
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=columns)
                writer.writeheader()
                writer.writerows(export_data)
                export_content = output.getvalue()
                filename = f"pinterest_analytics_{start_date}_to_{end_date}.csv"
            
            # Save to file
            export_path = os.path.join(self.settings.CONTENT_STORAGE_PATH, filename)
            with open(export_path, 'w') as f:
                f.write(export_content)
            
            self.logger.info(f"Analytics data exported to: {export_path}")
            return export_path
            
        except Exception as e:
            self.logger.error(f"Error exporting analytics data: {str(e)}")
            return None