"""
AI Image Generation Service
Supports OpenAI DALL-E and Stability AI for generating Pinterest-optimized images.
"""

import aiohttp
import asyncio
import base64
import io
import os
import uuid
from datetime import datetime
from typing import Dict, Optional, Tuple, Any
from PIL import Image, ImageEnhance, ImageFilter
import logging

class AIImageGenerator:
    """AI Image Generation service supporting multiple providers."""
    
    def __init__(self, settings):
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        
        # Validate API keys
        if settings.AI_PROVIDER == 'openai' and not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key is required when using OpenAI provider")
        elif settings.AI_PROVIDER == 'stability' and not settings.STABILITY_AI_KEY:
            raise ValueError("Stability AI API key is required when using Stability AI provider")
    
    async def generate_image(self, prompt: str, style: str = 'standard', 
                           dimensions: str = 'standard') -> Optional[Dict]:
        """Generate an AI image optimized for Pinterest."""
        try:
            self.logger.info(f"Generating image with prompt: {prompt[:100]}...")
            
            # Get image dimensions
            width, height = self.settings.IMAGE_DIMENSIONS[dimensions]
            
            # Enhance prompt for Pinterest optimization
            enhanced_prompt = self._enhance_prompt_for_pinterest(prompt, style)
            
            if self.settings.AI_PROVIDER == 'openai':
                image_data = await self._generate_with_openai(enhanced_prompt, width, height)
            elif self.settings.AI_PROVIDER == 'stability':
                image_data = await self._generate_with_stability(enhanced_prompt, width, height)
            else:
                raise ValueError(f"Unsupported AI provider: {self.settings.AI_PROVIDER}")
            
            if image_data:
                # Post-process image for Pinterest optimization
                processed_image = await self._post_process_image(image_data, style)
                return processed_image
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error generating image: {str(e)}")
            return None
    
    async def _generate_with_openai(self, prompt: str, width: int, height: int) -> Optional[Dict]:
        """Generate image using OpenAI DALL-E."""
        try:
            headers = {
                'Authorization': f'Bearer {self.settings.OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            # DALL-E 3 supports specific sizes
            size = self._get_dalle_size(width, height)
            
            payload = {
                'model': 'dall-e-3',
                'prompt': prompt,
                'size': size,
                'quality': 'hd',
                'n': 1,
                'response_format': 'b64_json'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://api.openai.com/v1/images/generations',
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        image_b64 = result['data'][0]['b64_json']
                        
                        # Save image
                        image_path = await self._save_image_from_b64(image_b64)
                        
                        return {
                            'path': image_path,
                            'provider': 'openai',
                            'prompt': prompt,
                            'dimensions': (width, height)
                        }
                    else:
                        error_text = await response.text()
                        self.logger.error(f"OpenAI API error: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            self.logger.error(f"Error with OpenAI generation: {str(e)}")
            return None
    
    async def _generate_with_stability(self, prompt: str, width: int, height: int) -> Optional[Dict]:
        """Generate image using Stability AI."""
        try:
            headers = {
                'Authorization': f'Bearer {self.settings.STABILITY_AI_KEY}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'text_prompts': [
                    {
                        'text': prompt,
                        'weight': 1
                    }
                ],
                'cfg_scale': 7,
                'height': height,
                'width': width,
                'samples': 1,
                'steps': 30,
                'style_preset': 'photographic'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image',
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        image_b64 = result['artifacts'][0]['base64']
                        
                        # Save image
                        image_path = await self._save_image_from_b64(image_b64)
                        
                        return {
                            'path': image_path,
                            'provider': 'stability',
                            'prompt': prompt,
                            'dimensions': (width, height)
                        }
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Stability AI error: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            self.logger.error(f"Error with Stability AI generation: {str(e)}")
            return None
    
    def _enhance_prompt_for_pinterest(self, prompt: str, style: str) -> str:
        """Enhance prompt for Pinterest optimization."""
        pinterest_enhancements = {
            'standard': 'high quality, professional photography, pinterest style, clean composition',
            'lifestyle': 'lifestyle photography, bright and airy, instagram worthy, pinterest aesthetic',
            'artistic': 'artistic composition, creative design, visually striking, pinterest trending',
            'minimal': 'minimalist design, clean aesthetic, simple composition, modern style'
        }
        
        enhancement = pinterest_enhancements.get(style, pinterest_enhancements['standard'])
        
        # Add Pinterest-specific styling
        enhanced_prompt = f"{prompt}, {enhancement}, vertical composition, eye-catching, shareable content"
        
        return enhanced_prompt
    
    async def _post_process_image(self, image_data: Dict, style: str) -> Dict:
        """Post-process image for Pinterest optimization."""
        try:
            image_path = image_data['path']
            
            # Open and process image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Apply style-specific enhancements
                if style == 'bright':
                    # Increase brightness and contrast
                    enhancer = ImageEnhance.Brightness(img)
                    img = enhancer.enhance(1.1)
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(1.05)
                elif style == 'vibrant':
                    # Increase saturation
                    enhancer = ImageEnhance.Color(img)
                    img = enhancer.enhance(1.2)
                elif style == 'soft':
                    # Apply slight blur for soft effect
                    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
                
                # Ensure Pinterest optimal dimensions
                target_width, target_height = image_data['dimensions']
                if img.size != (target_width, target_height):
                    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                
                # Save processed image
                processed_path = image_path.replace('.png', '_processed.png')
                img.save(processed_path, 'PNG', quality=95, optimize=True)
                
                # Update image data
                image_data['path'] = processed_path
                image_data['processed'] = True
                
                return image_data
                
        except Exception as e:
            self.logger.error(f"Error post-processing image: {str(e)}")
            return image_data
    
    async def _save_image_from_b64(self, image_b64: str) -> str:
        """Save base64 image to file."""
        try:
            # Decode base64
            image_data = base64.b64decode(image_b64)
            
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"ai_image_{timestamp}_{uuid.uuid4().hex[:8]}.png"
            filepath = os.path.join(self.settings.CONTENT_STORAGE_PATH, filename)
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            self.logger.info(f"Image saved to: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error saving image: {str(e)}")
            raise
    
    def _get_dalle_size(self, width: int, height: int) -> str:
        """Get the closest DALL-E supported size."""
        # DALL-E 3 supported sizes
        supported_sizes = {
            (1024, 1024): '1024x1024',
            (1792, 1024): '1792x1024',
            (1024, 1792): '1024x1792'
        }
        
        # Find closest supported size
        aspect_ratio = width / height
        
        if aspect_ratio > 1.5:  # Wide image
            return '1792x1024'
        elif aspect_ratio < 0.7:  # Tall image (Pinterest optimal)
            return '1024x1792'
        else:  # Square-ish image
            return '1024x1024'
    
    async def generate_batch_images(self, prompts: list, style: str = 'standard') -> list:
        """Generate multiple images in batch."""
        tasks = []
        for prompt in prompts:
            task = self.generate_image(prompt, style)
            tasks.append(task)
        
        # Execute with rate limiting
        results = []
        batch_size = 3  # Limit concurrent requests
        
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]
            batch_results = await asyncio.gather(*batch, return_exceptions=True)
            results.extend(batch_results)
            
            # Rate limiting delay
            if i + batch_size < len(tasks):
                await asyncio.sleep(2)
        
        return [r for r in results if r and not isinstance(r, Exception)]