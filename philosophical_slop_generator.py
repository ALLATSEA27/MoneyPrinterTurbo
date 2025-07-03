#!/usr/bin/env python3
"""
Philosophical Slop Generator
Creates videos with philosophical subtitles over unrelated footage
"""

import requests
import json
import time
from typing import List, Dict

class PhilosophicalSlopGenerator:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        
        # Philosophical questions that work well
        self.philosophical_topics = [
            "What is consciousness?",
            "Why do we exist?",
            "Is reality real?",
            "What is the meaning of life?",
            "Are we just atoms arranged in a way that thinks?",
            "What if nothing matters?",
            "Why do we seek validation?",
            "Is happiness just a chemical reaction?",
            "What is time?",
            "Are we alone in the universe?",
            "Why do we work?",
            "What is love?",
            "Is free will real?",
            "What happens after death?",
            "Why do we dream?"
        ]
        
        # Video themes that are completely unrelated
        self.video_themes = [
            "luxury cars",
            "beach waves",
            "city streets",
            "people walking",
            "nature landscapes",
            "technology",
            "abstract patterns",
            "architecture",
            "food cooking",
            "fashion",
            "sports",
            "animals",
            "space",
            "underwater",
            "forest"
        ]
        
        # Voice options for variety
        self.voice_options = [
            "en-US-JennyNeural",  # Female
            "en-US-GuyNeural",    # Male
            "en-US-AriaNeural",   # Female
            "en-US-DavisNeural"   # Male
        ]
    
    def generate_philosophical_video(self, topic: str, video_theme: str, voice: str = None):
        """
        Generate a video with philosophical subtitles over unrelated footage
        """
        
        # Step 1: Create the task
        task_data = {
            "video_subject": topic,
            "video_script": "",  # Let AI generate this
            "video_terms": video_theme,  # Force unrelated video content
            "video_aspect": "9:16",
            "video_concat_mode": "random",
            "video_transition_mode": "FadeIn",
            "max_clip_duration": 4,
            "video_count": 1,
            "subtitle_provider": "edge",
            "voice_name": voice or "en-US-JennyNeural",
            "voice_rate": 1.0,
            "voice_volume": 1.0,
            "bgm_type": "random",
            "bgm_volume": 0.2,
            "subtitle_enabled": True,
            "subtitle_position": "bottom",
            "subtitle_font_size": 60,
            "subtitle_font_color": "#FFFFFF",
            "subtitle_stroke_color": "#000000",
            "subtitle_stroke_width": 2
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
        print(f"Topic: {topic}")
        print(f"Video theme: {video_theme}")
        
        # Step 2: Monitor task progress
        while True:
            status_response = requests.get(f"{self.base_url}/api/v1/tasks/{task_id}")
            if status_response.status_code != 200:
                raise Exception(f"Failed to get task status: {status_response.text}")
            
            status_data = status_response.json()
            status = status_data["status"]
            
            print(f"Status: {status}")
            
            if status == "completed":
                # Get video download links
                videos = status_data.get("videos", [])
                for i, video in enumerate(videos):
                    video_url = f"{self.base_url}/tasks/{task_id}/{video}"
                    print(f"Video {i+1}: {video_url}")
                return task_id, videos
            
            elif status == "failed":
                raise Exception(f"Task failed: {status_data.get('error', 'Unknown error')}")
            
            time.sleep(5)  # Wait 5 seconds before checking again
    
    def generate_batch(self, count: int = 5):
        """
        Generate multiple philosophical videos
        """
        import random
        
        results = []
        
        for i in range(count):
            # Randomly select topic and video theme
            topic = random.choice(self.philosophical_topics)
            video_theme = random.choice(self.video_themes)
            voice = random.choice(self.voice_options)
            
            print(f"\n--- Generating video {i+1}/{count} ---")
            
            try:
                task_id, videos = self.generate_philosophical_video(topic, video_theme, voice)
                results.append({
                    "task_id": task_id,
                    "topic": topic,
                    "video_theme": video_theme,
                    "voice": voice,
                    "videos": videos
                })
            except Exception as e:
                print(f"Failed to generate video {i+1}: {e}")
            
            # Wait between generations to avoid rate limits
            time.sleep(10)
        
        return results
    
    def create_content_calendar(self, days: int = 7):
        """
        Create a content calendar for the week
        """
        import random
        from datetime import datetime, timedelta
        
        calendar = {}
        start_date = datetime.now()
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            
            # Different themes for different days
            if i == 0:  # Monday - Existential
                topics = ["What is consciousness?", "Why do we exist?", "Is reality real?"]
            elif i == 1:  # Tuesday - Social
                topics = ["Why do we seek validation?", "What is love?", "Why do we work?"]
            elif i == 2:  # Wednesday - Reality
                topics = ["Is free will real?", "What is time?", "Are we alone?"]
            elif i == 3:  # Thursday - Meaning
                topics = ["What is the meaning of life?", "What if nothing matters?", "Why do we dream?"]
            elif i == 4:  # Friday - Science
                topics = ["Are we just atoms?", "Is happiness chemical?", "What happens after death?"]
            else:  # Weekend - Random
                topics = self.philosophical_topics
            
            calendar[date_str] = {
                "topic": random.choice(topics),
                "video_theme": random.choice(self.video_themes),
                "voice": random.choice(self.voice_options)
            }
        
        return calendar

# Example usage
if __name__ == "__main__":
    generator = PhilosophicalSlopGenerator()
    
    # Generate a single video
    print("Generating single philosophical video...")
    task_id, videos = generator.generate_philosophical_video(
        topic="What is consciousness?",
        video_theme="luxury cars",
        voice="en-US-JennyNeural"
    )
    
    # Generate a batch
    print("\nGenerating batch of 3 videos...")
    results = generator.generate_batch(3)
    
    # Create content calendar
    print("\nCreating content calendar...")
    calendar = generator.create_content_calendar(7)
    print(json.dumps(calendar, indent=2)) 