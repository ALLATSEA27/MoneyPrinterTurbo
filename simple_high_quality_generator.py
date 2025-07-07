#!/usr/bin/env python3
"""
Simple High-Quality Generator
Creates high-quality videos with factual content - simplified and reliable
"""

import requests
import json
import time
import random
import os
from typing import List, Dict
from enum import Enum

class VideoQuality(Enum):
    STANDARD = "standard"
    HIGH = "high"
    PREMIUM = "premium"

class SimpleHighQualityGenerator:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        
        # Load facts from database
        try:
            with open("fact_database.json") as f:
                data = json.load(f)
                # Handle both direct array and nested structure
                if isinstance(data, dict) and "facts" in data:
                    self.facts = data["facts"]
                elif isinstance(data, list):
                    self.facts = data
                else:
                    print(f"Unexpected fact database format: {type(data)}")
                    self.facts = []
                print(f"Loaded {len(self.facts)} facts from database")
        except FileNotFoundError:
            print("fact_database.json not found. Please create it first.")
            raise
        
        # Track used facts to avoid repetition
        self.used_facts = set()
        self.used_facts_file = "used_facts_high_quality.json"
        self.load_used_facts()
        
        # High-quality video themes that work well for shorts
        self.video_themes = [
            "nature landscapes", "city timelapse", "ocean waves", "forest scenes",
            "mountain views", "sunset sky", "abstract patterns", "geometric shapes",
            "colorful gradients", "minimalist design", "modern architecture",
            "aerial footage", "macro photography", "light trails", "water reflections",
            "space", "technology", "futuristic", "neon lights", "liquid art"
        ]
        
        # Premium voice options for better quality
        self.voice_options = [
            "en-US-JennyNeural",      # Clear, professional female
            "en-US-GuyNeural",        # Clear, professional male
            "en-US-AriaNeural",       # Warm, engaging female
            "en-US-DavisNeural",      # Warm, engaging male
            "en-US-SaraNeural",       # Friendly, approachable female
            "en-US-TonyNeural",       # Friendly, approachable male
        ]
        
        print(f"Using {len(self.video_themes)} high-quality video themes")
        print(f"Already used {len(self.used_facts)} facts")
    
    def load_used_facts(self):
        """Load previously used facts from file"""
        try:
            if os.path.exists(self.used_facts_file):
                with open(self.used_facts_file, 'r') as f:
                    self.used_facts = set(json.load(f))
        except Exception as e:
            print(f"Warning: Could not load used facts: {e}")
            self.used_facts = set()
    
    def save_used_facts(self):
        """Save used facts to file"""
        try:
            with open(self.used_facts_file, 'w') as f:
                json.dump(list(self.used_facts), f)
        except Exception as e:
            print(f"Warning: Could not save used facts: {e}")
    
    def get_unused_fact(self):
        """Get a random fact that hasn't been used yet"""
        unused_facts = [f for f in self.facts if f['id'] not in self.used_facts]
        
        if not unused_facts:
            print("⚠️ All facts have been used! Resetting used facts list.")
            self.used_facts.clear()
            unused_facts = self.facts
        
        fact = random.choice(unused_facts)
        self.used_facts.add(fact['id'])
        self.save_used_facts()
        return fact
    
    def optimize_script_for_shorts(self, fact: str) -> str:
        """Optimize script for short-form content"""
        # Keep it concise and engaging
        max_length = 150  # Optimal for 15-30 second shorts
        
        if len(fact) <= max_length:
            return fact
        
        # Try to find a natural break point
        sentences = fact.split('. ')
        optimized = ""
        
        for sentence in sentences:
            if len(optimized + sentence) <= max_length:
                optimized += sentence + ". "
            else:
                break
        
        return optimized.strip() or fact[:max_length] + "..."
    
    def select_optimal_video_theme(self, fact: str) -> str:
        """Select the best video theme based on content"""
        # Simple keyword matching for theme selection
        fact_lower = fact.lower()
        
        if any(word in fact_lower for word in ['nature', 'earth', 'planet', 'environment']):
            return random.choice(['nature landscapes', 'forest scenes', 'mountain views'])
        elif any(word in fact_lower for word in ['space', 'universe', 'stars', 'galaxy']):
            return random.choice(['space', 'abstract patterns', 'colorful gradients'])
        elif any(word in fact_lower for word in ['ocean', 'sea', 'water', 'marine']):
            return random.choice(['ocean waves', 'water reflections'])
        elif any(word in fact_lower for word in ['city', 'urban', 'building', 'architecture']):
            return random.choice(['city timelapse', 'modern architecture', 'aerial footage'])
        elif any(word in fact_lower for word in ['technology', 'computer', 'ai', 'robot']):
            return random.choice(['technology', 'futuristic', 'neon lights'])
        else:
            return random.choice(self.video_themes)
    
    def get_quality_settings(self, quality: VideoQuality):
        """Get quality-specific settings"""
        if quality == VideoQuality.STANDARD:
            return {
                "clip_duration": 4,
                "font_size": 60,
                "stroke_width": 2,
                "bgm_volume": 0.2,
                "voice_volume": 1.0,
                "threads": 2
            }
        elif quality == VideoQuality.HIGH:
            return {
                "clip_duration": 3,
                "font_size": 70,
                "stroke_width": 2.5,
                "bgm_volume": 0.15,
                "voice_volume": 1.0,
                "threads": 4
            }
        else:  # PREMIUM
            return {
                "clip_duration": 2,
                "font_size": 80,
                "stroke_width": 3,
                "bgm_volume": 0.1,
                "voice_volume": 1.0,
                "threads": 6
            }
    
    def generate_high_quality_video(self, quality: VideoQuality = VideoQuality.HIGH, voice: str = None):
        """
        Generate a high-quality video with factual content
        """
        
        # Pick unused fact and theme
        fact = self.get_unused_fact()
        video_theme = self.select_optimal_video_theme(fact["fact"])
        selected_voice = voice or random.choice(self.voice_options)
        settings = self.get_quality_settings(quality)
        
        # Optimize script for shorts
        optimized_script = self.optimize_script_for_shorts(fact["fact"])
        
        print(f"\n🎬 Generating High-Quality Video ({quality.value})")
        print(f"📝 Fact: {optimized_script}")
        print(f"🎨 Theme: {video_theme}")
        print(f"🎤 Voice: {selected_voice}")
        print(f"⚙️ Quality: {quality.value}")
        
        # Create task with optimized settings
        task_data = {
            "video_subject": fact["fact"],
            "video_script": optimized_script,
            "video_aspect": "9:16",  # Perfect for shorts
            "video_concat_mode": "random",
            "video_transition_mode": "FadeIn",
            "video_clip_duration": settings["clip_duration"],
            "video_count": 1,
            "subtitle_provider": "edge",
            "voice_name": selected_voice,
            "voice_rate": 1.0,
            "voice_volume": settings["voice_volume"],
            "bgm_type": "random",
            "bgm_volume": settings["bgm_volume"],
            "subtitle_enabled": True,
            "subtitle_position": "bottom",
            "font_size": settings["font_size"],
            "text_fore_color": "#FFFFFF",
            "stroke_color": "#000000",
            "stroke_width": settings["stroke_width"],
            "video_source": "pexels",
            "video_terms": video_theme,
            "n_threads": settings["threads"]
        }
        
        # Create task
        response = requests.post(f"{self.base_url}/api/v1/videos", json=task_data)
        print("API response:", response.text)
        
        if response.status_code != 200:
            raise Exception(f"Failed to create task: {response.text}")
        
        data = response.json()
        if "data" not in data or "task_id" not in data["data"]:
            raise Exception(f"API did not return a task_id: {data}")
        
        task_id = data["data"]["task_id"]
        print(f"✅ Created task: {task_id}")
        
        # Monitor task progress
        return self.monitor_task(task_id, fact, optimized_script)
    
    def monitor_task(self, task_id: str, fact: Dict, script: str) -> tuple:
        """Monitor task progress with detailed status updates"""
        start_time = time.time()
        
        while True:
            status_response = requests.get(f"{self.base_url}/api/v1/tasks/{task_id}")
            if status_response.status_code != 200:
                raise Exception(f"Failed to get task status: {status_response.text}")
            
            status_data = status_response.json()
            
            if "data" in status_data:
                data = status_data["data"]
                state = data.get("state", 0)
                progress = data.get("progress", 0)
                videos = data.get("videos", [])
                
                elapsed = time.time() - start_time
                print(f"⏱️ Progress: {progress:.1f}% | Time: {elapsed:.0f}s | State: {state}")
                
                # Task completed
                if state == 1 and progress >= 100:
                    print("🎉 Task completed successfully!")
                    for i, video in enumerate(videos):
                        print(f"📹 Video {i+1}: {video}")
                    return task_id, videos, fact, script
                
                # Task failed
                elif state == -1:
                    error_msg = status_data.get("message", "Task failed")
                    print(f"❌ Task failed: {error_msg}")
                    if "error" in status_data:
                        print(f"Error details: {status_data['error']}")
                    raise Exception(f"Task failed: {error_msg}")
                
                # Still running
                else:
                    time.sleep(3)
                    continue
            else:
                print(f"⚠️ Unexpected response format: {status_data}")
                time.sleep(3)
                continue
    
    def generate_batch(self, count: int = 3, quality: VideoQuality = VideoQuality.HIGH) -> List[Dict]:
        """
        Generate multiple high-quality videos
        """
        results = []
        
        for i in range(count):
            print(f"\n{'='*50}")
            print(f"🎬 Generating video {i+1}/{count}")
            print(f"{'='*50}")
            
            try:
                task_id, videos, fact, script = self.generate_high_quality_video(quality)
                results.append({
                    "task_id": task_id,
                    "videos": videos,
                    "fact": fact,
                    "script": script,
                    "quality": quality.value
                })
                print(f"✅ Video {i+1} completed successfully!")
            except Exception as e:
                print(f"❌ Failed to generate video {i+1}: {e}")
            
            # Wait between generations
            if i < count - 1:
                wait_time = 15 if quality == VideoQuality.PREMIUM else 10
                print(f"⏳ Waiting {wait_time} seconds before next generation...")
                time.sleep(wait_time)
        
        return results

def main():
    """Main function to demonstrate the simple high-quality generator"""
    try:
        generator = SimpleHighQualityGenerator()
        
        print("🎬 Simple High-Quality Generator")
        print("=" * 40)
        
        # Generate a single high-quality video
        print("\n1️⃣ Generating single high-quality video...")
        task_id, videos, fact, script = generator.generate_high_quality_video(VideoQuality.HIGH)
        
        # Uncomment to generate a batch
        # print("\n2️⃣ Generating batch of 3 high-quality videos...")
        # results = generator.generate_batch(3, VideoQuality.HIGH)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure:")
        print("1. MoneyPrinterTurbo API is running (python main.py)")
        print("2. fact_database.json exists in the current directory")
        print("3. You have Pexels/Pixabay API keys configured in config.toml")

if __name__ == "__main__":
    main() 