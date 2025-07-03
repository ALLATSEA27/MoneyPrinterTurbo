#!/usr/bin/env python3
"""
Honest AI Slop Generator
Creates videos with factual, educational content over psychedelic backgrounds
"""

import requests
import json
import time
import random
import glob
import os
from typing import List, Dict

class HonestAISlopGenerator:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        
        # Load facts from database
        try:
            with open("fact_database.json") as f:
                data = json.load(f)
                self.facts = data["facts"]
                print(f"Loaded {len(self.facts)} facts from database")
        except FileNotFoundError:
            print("fact_database.json not found. Please create it first.")
            raise
        
        # Track used facts to avoid repetition
        self.used_facts = set()
        self.used_facts_file = "used_facts.json"
        self.load_used_facts()
        
        # Tantric/Psychedelic search terms for video generation
        self.tantric_terms = [
            "tantric",
            "psychedelic",
            "mandala",
            "sacred geometry",
            "chakra",
            "meditation",
            "spiritual",
            "mystical",
            "cosmic",
            "aurora",
            "fractal",
            "kaleidoscope",
            "neon lights",
            "liquid art",
            "flowing colors",
            "morphing shapes",
            "sacred symbols",
            "energy patterns",
            "vibrant colors",
            "mystical art"
        ]
        
        print(f"Using {len(self.tantric_terms)} tantric/psychedelic search terms")
        print(f"Already used {len(self.used_facts)} facts")
        
        # Voice options for variety (Edge TTS)
        self.voice_options = [
            "en-US-JennyNeural",  # Female
            "en-US-GuyNeural",    # Male
            "en-US-AriaNeural",   # Female
            "en-US-DavisNeural",  # Male
            "en-US-ChristopherNeural",  # Male
            "en-US-SaraNeural"    # Female
        ]
    
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
    
    def generate_honest_video(self, voice: str = None):
        """
        Generate a video with factual content over psychedelic background
        """
        
        # Pick unused fact and tantric search term
        fact = self.get_unused_fact()
        tantric_term = random.choice(self.tantric_terms)
        selected_voice = voice or random.choice(self.voice_options)
        
        print(f"\n--- Generating Honest AI Slop Video ---")
        print(f"Fact: {fact['fact']}")
        print(f"Category: {fact['category']} - {fact['subcategory']}")
        print(f"Tantric theme: {tantric_term}")
        print(f"Voice: {selected_voice}")
        
        # Step 1: Create the task
        task_data = {
            "video_subject": fact["fact"],
            "video_script": fact["fact"],  # Use the fact as both subject and script
            "video_aspect": "9:16",
            "video_concat_mode": "random",
            "video_transition_mode": "FadeIn",
            "max_clip_duration": 4,
            "video_count": 1,
            "subtitle_provider": "edge",
            "voice_name": selected_voice,
            "voice_rate": 1.0,
            "voice_volume": 1.0,
            "bgm_type": "random",
            "bgm_volume": 0.2,
            "subtitle_enabled": True,
            "subtitle_position": "bottom",
            "subtitle_font_size": 60,
            "subtitle_font_color": "#FFFFFF",
            "subtitle_stroke_color": "#000000",
            "subtitle_stroke_width": 2,
            "video_source": "pexels",  # or "pixabay"
            "video_terms": tantric_term
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
        print(f"Created task: {task_id}")
        
        # Step 2: Monitor task progress
        while True:
            status_response = requests.get(f"{self.base_url}/api/v1/tasks/{task_id}")
            if status_response.status_code != 200:
                raise Exception(f"Failed to get task status: {status_response.text}")
            
            status_data = status_response.json()
            
            # Handle the actual API response structure
            if "data" in status_data:
                data = status_data["data"]
                state = data.get("state", 0)
                progress = data.get("progress", 0)
                videos = data.get("videos", [])
                
                print(f"State: {state}, Progress: {progress:.1f}%")
                
                # Check if task is completed (state 1 = completed)
                if state == 1 and progress >= 100:
                    print("✅ Task completed!")
                    for i, video in enumerate(videos):
                        print(f"✅ Video {i+1}: {video}")
                    return task_id, videos, fact
                
                # Check if task failed (state -1 = failed)
                elif state == -1:
                    error_msg = status_data.get("message", "Task failed")
                    print(f"❌ Task failed: {error_msg}")
                    raise Exception(f"Task failed: {error_msg}")
                
                # Task is still running
                else:
                    time.sleep(5)
                    continue
            else:
                print(f"⚠️ Unexpected response format: {status_data}")
                time.sleep(5)
                continue
            


    
    def generate_batch(self, count: int = 3):
        """
        Generate multiple honest AI slop videos
        """
        results = []
        
        for i in range(count):
            print(f"\n--- Generating video {i+1}/{count} ---")
            
            try:
                task_id, videos, fact = self.generate_honest_video()
                results.append({
                    "task_id": task_id,
                    "videos": videos
                })
            except Exception as e:
                print(f"❌ Failed to generate video {i+1}: {e}")
            
            # Wait between generations to avoid rate limits
            if i < count - 1:  # Don't wait after the last video
                print("Waiting 10 seconds before next generation...")
                time.sleep(10)
        
        return results
    
    def create_content_calendar(self, days: int = 7):
        """
        Create a content calendar for the week
        """
        from datetime import datetime, timedelta
        
        calendar = {}
        start_date = datetime.now()
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            
            # Pick an unused fact for each day
            fact = self.get_unused_fact()
            tantric_term = random.choice(self.tantric_terms)
            voice = random.choice(self.voice_options)
            
            calendar[date_str] = {
                "fact": fact["fact"],
                "category": fact["category"],
                "subcategory": fact["subcategory"],
                "tantric_theme": tantric_term,
                "voice": voice
            }
        
        return calendar

# Example usage
if __name__ == "__main__":
    try:
        generator = HonestAISlopGenerator()
        
        # Generate a single video
        print("🎬 Generating single honest AI slop video...")
        task_id, videos, fact = generator.generate_honest_video()
        
        # Uncomment to generate a batch
        # print("\n🎬 Generating batch of 3 videos...")
        # results = generator.generate_batch(3)
        
        # Uncomment to create content calendar
        # print("\n📅 Creating content calendar...")
        # calendar = generator.create_content_calendar(7)
        # print(json.dumps(calendar, indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure:")
        print("1. MoneyPrinterTurbo API is running (python main.py)")
        print("2. fact_database.json exists in the current directory")
        print("3. You have Pexels/Pixabay API keys configured in config.toml") 