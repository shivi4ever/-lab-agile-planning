"""
Pinterest API Client Service
Handles Pinterest API integration for automated posting and board management.
"""

import aiohttp
import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode, parse_qs, urlparse
import os

class PinterestClient:
    """Pinterest API client for automated posting."""
    
    def __init__(self, settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        
        self.base_url = "https://api.pinterest.com/v5"
        self.access_token = settings.PINTEREST_ACCESS_TOKEN
        
        # Rate limiting
        self.rate_limit_remaining = settings.API_RATE_LIMIT
        self.rate_limit_reset = time.time() + 3600  # Reset every hour
        
        # Board cache
        self._boards_cache = {}
        self._cache_expiry = time.time()
    
    async def authenticate(self) -> bool:
        """Authenticate with Pinterest API and refresh token if needed."""
        try:
            if not self.access_token:
                self.logger.error("No access token available")
                return False
            
            # Test the token with a simple API call
            headers = self._get_headers()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/user_account",
                    headers=headers
                ) as response:
                    
                    if response.status == 200:
                        user_data = await response.json()
                        self.logger.info(f"Authenticated as: {user_data.get('username', 'Unknown')}")
                        return True
                    elif response.status == 401:
                        # Token expired, try to refresh
                        return await self._refresh_access_token()
                    else:
                        self.logger.error(f"Authentication failed: {response.status}")
                        return False
                        
        except Exception as e:
            self.logger.error(f"Authentication error: {str(e)}")
            return False
    
    async def create_pin(self, image_path: str, title: str, description: str, 
                        board_id: str, link: str, alt_text: str = "") -> Dict:
        """Create a new pin on Pinterest."""
        try:
            if not await self._check_rate_limit():
                return {'success': False, 'error': 'Rate limit exceeded'}
            
            # Upload image first
            media_id = await self._upload_image(image_path)
            if not media_id:
                return {'success': False, 'error': 'Failed to upload image'}
            
            # Create pin data
            pin_data = {
                'board_id': board_id,
                'title': title[:100],  # Pinterest title limit
                'description': description[:500],  # Pinterest description limit
                'media_source': {
                    'source_type': 'image_upload',
                    'media_id': media_id
                },
                'link': link
            }
            
            if alt_text:
                pin_data['alt_text'] = alt_text[:500]
            
            headers = self._get_headers()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/pins",
                    headers=headers,
                    json=pin_data
                ) as response:
                    
                    if response.status == 201:
                        result = await response.json()
                        pin_id = result.get('id')
                        
                        self.logger.info(f"Pin created successfully: {pin_id}")
                        self._update_rate_limit(response.headers)
                        
                        return {
                            'success': True,
                            'pin_id': pin_id,
                            'pin_url': f"https://pinterest.com/pin/{pin_id}",
                            'board_id': board_id
                        }
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Pin creation failed: {response.status} - {error_text}")
                        return {'success': False, 'error': f"API error: {response.status}"}
                        
        except Exception as e:
            self.logger.error(f"Error creating pin: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def get_boards(self, force_refresh: bool = False) -> List[Dict]:
        """Get user's Pinterest boards."""
        try:
            # Check cache
            if not force_refresh and self._boards_cache and time.time() < self._cache_expiry:
                return list(self._boards_cache.values())
            
            headers = self._get_headers()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/boards",
                    headers=headers,
                    params={'page_size': 100}
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        boards = result.get('items', [])
                        
                        # Update cache
                        self._boards_cache = {board['id']: board for board in boards}
                        self._cache_expiry = time.time() + 3600  # Cache for 1 hour
                        
                        self.logger.info(f"Retrieved {len(boards)} boards")
                        return boards
                    else:
                        self.logger.error(f"Failed to get boards: {response.status}")
                        return []
                        
        except Exception as e:
            self.logger.error(f"Error getting boards: {str(e)}")
            return []
    
    async def create_board(self, name: str, description: str = "", privacy: str = "PUBLIC") -> Optional[str]:
        """Create a new Pinterest board."""
        try:
            board_data = {
                'name': name,
                'description': description,
                'privacy': privacy
            }
            
            headers = self._get_headers()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/boards",
                    headers=headers,
                    json=board_data
                ) as response:
                    
                    if response.status == 201:
                        result = await response.json()
                        board_id = result.get('id')
                        
                        self.logger.info(f"Board created: {name} (ID: {board_id})")
                        
                        # Clear cache to force refresh
                        self._boards_cache = {}
                        
                        return board_id
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Board creation failed: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            self.logger.error(f"Error creating board: {str(e)}")
            return None
    
    async def get_board_by_name(self, board_name: str) -> Optional[Dict]:
        """Get board by name."""
        boards = await self.get_boards()
        
        for board in boards:
            if board.get('name', '').lower() == board_name.lower():
                return board
        
        return None
    
    async def ensure_boards_exist(self) -> Dict[str, str]:
        """Ensure default boards exist, create if they don't."""
        board_ids = {}
        
        for board_config in self.settings.DEFAULT_BOARDS:
            board_name = board_config['name']
            board_description = board_config['description']
            
            # Check if board exists
            board = await self.get_board_by_name(board_name)
            
            if board:
                board_ids[board_name] = board['id']
                self.logger.info(f"Board exists: {board_name}")
            else:
                # Create board
                board_id = await self.create_board(board_name, board_description)
                if board_id:
                    board_ids[board_name] = board_id
                    self.logger.info(f"Board created: {board_name}")
                else:
                    self.logger.error(f"Failed to create board: {board_name}")
        
        return board_ids
    
    async def _upload_image(self, image_path: str) -> Optional[str]:
        """Upload image to Pinterest and return media ID."""
        try:
            if not os.path.exists(image_path):
                self.logger.error(f"Image file not found: {image_path}")
                return None
            
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            # Read image file
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            
            # Create form data
            data = aiohttp.FormData()
            data.add_field('file', image_data, filename=os.path.basename(image_path))
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/media",
                    headers=headers,
                    data=data
                ) as response:
                    
                    if response.status == 201:
                        result = await response.json()
                        media_id = result.get('media_id')
                        
                        self.logger.info(f"Image uploaded successfully: {media_id}")
                        return media_id
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Image upload failed: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            self.logger.error(f"Error uploading image: {str(e)}")
            return None
    
    async def _refresh_access_token(self) -> bool:
        """Refresh the access token using refresh token."""
        try:
            if not self.settings.PINTEREST_REFRESH_TOKEN:
                self.logger.error("No refresh token available")
                return False
            
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': self.settings.PINTEREST_REFRESH_TOKEN,
                'client_id': self.settings.PINTEREST_APP_ID,
                'client_secret': self.settings.PINTEREST_APP_SECRET
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://api.pinterest.com/v5/oauth/token',
                    data=data
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        self.access_token = result.get('access_token')
                        
                        # Update environment variable or save to config
                        self.logger.info("Access token refreshed successfully")
                        return True
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Token refresh failed: {response.status} - {error_text}")
                        return False
                        
        except Exception as e:
            self.logger.error(f"Error refreshing token: {str(e)}")
            return False
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Pinterest API requests."""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Pinterest-Bot/1.0'
        }
    
    async def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits."""
        current_time = time.time()
        
        # Reset rate limit if hour has passed
        if current_time >= self.rate_limit_reset:
            self.rate_limit_remaining = self.settings.API_RATE_LIMIT
            self.rate_limit_reset = current_time + 3600
        
        if self.rate_limit_remaining <= 0:
            self.logger.warning("Rate limit exceeded, waiting...")
            wait_time = self.rate_limit_reset - current_time
            if wait_time > 0:
                await asyncio.sleep(min(wait_time, 300))  # Wait max 5 minutes
            return False
        
        return True
    
    def _update_rate_limit(self, headers: Dict):
        """Update rate limit info from response headers."""
        try:
            if 'X-RateLimit-Remaining' in headers:
                self.rate_limit_remaining = int(headers['X-RateLimit-Remaining'])
            
            if 'X-RateLimit-Reset' in headers:
                self.rate_limit_reset = int(headers['X-RateLimit-Reset'])
                
        except (ValueError, KeyError):
            # Fallback: assume one request used
            self.rate_limit_remaining = max(0, self.rate_limit_remaining - 1)
    
    async def get_pin_analytics(self, pin_id: str) -> Dict:
        """Get analytics data for a specific pin."""
        try:
            headers = self._get_headers()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/pins/{pin_id}/analytics",
                    headers=headers,
                    params={
                        'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                        'end_date': datetime.now().strftime('%Y-%m-%d'),
                        'metric_types': 'IMPRESSION,SAVE,PIN_CLICK,OUTBOUND_CLICK'
                    }
                ) as response:
                    
                    if response.status == 200:
                        return await response.json()
                    else:
                        self.logger.error(f"Failed to get pin analytics: {response.status}")
                        return {}
                        
        except Exception as e:
            self.logger.error(f"Error getting pin analytics: {str(e)}")
            return {}
    
    async def bulk_create_pins(self, pins_data: List[Dict]) -> List[Dict]:
        """Create multiple pins with rate limiting."""
        results = []
        
        for i, pin_data in enumerate(pins_data):
            if not await self._check_rate_limit():
                self.logger.warning(f"Rate limit hit, stopping bulk creation at pin {i}")
                break
            
            result = await self.create_pin(**pin_data)
            results.append(result)
            
            # Small delay between requests
            await asyncio.sleep(1)
        
        return results