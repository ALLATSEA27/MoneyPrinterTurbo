#!/usr/bin/env python3
"""
FREE YouTube Pipeline for Honest AI Slop
Zero-cost automation using only free services and local resources
"""

import os
import json
import time
import random
import requests
from datetime import datetime, timedelta
from urllib.parse import urlparse
from honest_ai_slop_generator import HonestAISlopGenerator
from youtube_uploader import YouTubeUploader

# Helper to convert API video URL to local file path
def url_to_local_path(url):
    parsed = urlparse(url)
    if parsed.path.startswith('/tasks/'):
        return os.path.join('storage', parsed.path.lstrip('/'))
    return url  # fallback

class FreeYouTubePipeline:
    def __init__(self, base_url="http://localhost:8080"):
        self.generator = HonestAISlopGenerator(base_url)
        self.uploader = YouTubeUploader()
        self.upload_log_file = "upload_log.json"
        self.load_upload_log()
        
        # Free tier limits
        self.daily_upload_limit = 6  # YouTube API free tier: ~6 uploads/day
        self.uploads_today = self.count_uploads_today()
        
    def load_upload_log(self):
        """Load upload history to avoid duplicates"""
        if os.path.exists(self.upload_log_file):
            with open(self.upload_log_file, 'r') as f:
                self.upload_log = json.load(f)
        else:
            self.upload_log = []
    
    def save_upload_log(self):
        """Save upload history"""
        with open(self.upload_log_file, 'w') as f:
            json.dump(self.upload_log, f, indent=2)
    
    def count_uploads_today(self):
        """Count uploads made today"""
        today = datetime.now().date()
        count = 0
        for entry in self.upload_log:
            try:
                upload_date = datetime.fromisoformat(entry['timestamp']).date()
                if upload_date == today:
                    count += 1
            except:
                continue
        return count
    
    def check_daily_limit(self):
        """Check if we've hit the daily upload limit"""
        self.uploads_today = self.count_uploads_today()
        remaining = self.daily_upload_limit - self.uploads_today
        
        if remaining <= 0:
            print(f"⚠️  Daily upload limit reached ({self.daily_upload_limit} uploads)")
            print("🕐 Next uploads available tomorrow")
            return False
        
        print(f"📊 Daily uploads: {self.uploads_today}/{self.daily_upload_limit} (remaining: {remaining})")
        return True
    
    def generate_and_upload_video(self, fact=None, category=None):
        """
        Generate a single video and upload it to YouTube (FREE)
        """
        print("🎬 Starting FREE video generation and upload pipeline...")
        
        # Check daily limits
        if not self.check_daily_limit():
            return None
        
        # Step 1: Generate video (FREE - uses local Ollama)
        print("📹 Generating video (FREE - local AI)...")
        task_id, videos, fact_data = self.generator.generate_honest_video()
        
        if not task_id or not videos:
            print("❌ Failed to generate video")
            return None
        
        # Step 2: Convert video URL to local file path
        video_path = url_to_local_path(videos[0]) if videos else None
        
        if not video_path or not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return None
        
        # Step 3: Upload to YouTube (FREE - YouTube API free tier)
        print("📤 Uploading to YouTube (FREE tier)...")
        try:
            upload_result = self.uploader.upload_video(
                video_path=video_path,
                fact=fact_data['fact'],
                category=fact_data['category']
            )
            
            # Log the upload
            upload_log_entry = {
                'task_id': task_id,
                'video_path': video_path,
                'fact': fact_data['fact'],
                'category': fact_data['category'],
                'upload_result': upload_result,
                'timestamp': datetime.now().isoformat(),
                'cost': 'FREE'
            }
            
            self.upload_log.append(upload_log_entry)
            self.save_upload_log()
            
            print(f"✅ Successfully generated and uploaded video (FREE)!")
            print(f"🔗 YouTube URL: {upload_result['url']}")
            print(f"💰 Cost: $0.00")
            
            return upload_result
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return None
    
    def free_daily_automation(self, videos_per_day=2):
        """
        Run daily automation with FREE tier limits
        """
        print(f"📅 Starting FREE daily automation: {videos_per_day} videos per day")
        print(f"💰 Total cost: $0.00")
        print(f"📊 Using YouTube API free tier: {self.daily_upload_limit} uploads/day")
        
        # Adjust videos per day to stay within free limits
        if videos_per_day > self.daily_upload_limit:
            print(f"⚠️  Adjusting to {self.daily_upload_limit} videos/day (free tier limit)")
            videos_per_day = self.daily_upload_limit
        
        # Calculate delay between videos
        delay_hours = 24 // videos_per_day
        
        while True:
            try:
                print(f"\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("=" * 50)
                
                # Check if we can upload today
                if not self.check_daily_limit():
                    print("😴 Waiting until tomorrow for more uploads...")
                    # Wait until next day
                    next_run = datetime.now() + timedelta(days=1)
                    next_run = next_run.replace(hour=9, minute=0, second=0, microsecond=0)
                    
                    wait_seconds = (next_run - datetime.now()).total_seconds()
                    print(f"⏰ Next run scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                    time.sleep(wait_seconds)
                    continue
                
                # Generate and upload videos
                for i in range(videos_per_day):
                    if not self.check_daily_limit():
                        print("⚠️  Daily limit reached, stopping for today")
                        break
                    
                    print(f"\n--- Video {i+1}/{videos_per_day} ---")
                    result = self.generate_and_upload_video()
                    
                    if result and i < videos_per_day - 1:
                        print(f"⏳ Waiting {delay_hours} hours before next video...")
                        time.sleep(delay_hours * 3600)
                
                # Wait until next day
                next_run = datetime.now() + timedelta(days=1)
                next_run = next_run.replace(hour=9, minute=0, second=0, microsecond=0)
                
                wait_seconds = (next_run - datetime.now()).total_seconds()
                print(f"⏰ Next run scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"😴 Sleeping for {wait_seconds/3600:.1f} hours...")
                
                time.sleep(wait_seconds)
                
            except KeyboardInterrupt:
                print("\n⏹️ Automation stopped by user")
                break
            except Exception as e:
                print(f"❌ Automation error: {e}")
                print("🔄 Retrying in 1 hour...")
                time.sleep(3600)
    
    def get_free_stats(self):
        """Get statistics about free uploads"""
        if not self.upload_log:
            return {
                "total_uploads": 0, 
                "successful_uploads": 0, 
                "failed_uploads": 0,
                "total_cost": "$0.00",
                "uploads_today": 0,
                "daily_limit": self.daily_upload_limit
            }
        
        successful = len([entry for entry in self.upload_log if 'upload_result' in entry and 'error' not in entry['upload_result']])
        failed = len([entry for entry in self.upload_log if 'upload_result' in entry and 'error' in entry['upload_result']])
        
        return {
            "total_uploads": len(self.upload_log),
            "successful_uploads": successful,
            "failed_uploads": failed,
            "success_rate": f"{(successful/len(self.upload_log)*100):.1f}%",
            "total_cost": "$0.00",
            "uploads_today": self.count_uploads_today(),
            "daily_limit": self.daily_upload_limit,
            "remaining_today": max(0, self.daily_upload_limit - self.count_uploads_today())
        }

# Command line interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="FREE YouTube Pipeline for Honest AI Slop")
    parser.add_argument("--mode", choices=["single", "daily"], default="single",
                       help="Operation mode")
    parser.add_argument("--videos-per-day", type=int, default=2,
                       help="Videos per day (max 6 for free tier)")
    parser.add_argument("--fact", type=str,
                       help="Specific fact to use")
    parser.add_argument("--category", type=str,
                       help="Specific category to use")
    parser.add_argument("--stats", action="store_true",
                       help="Show upload statistics")
    
    args = parser.parse_args()
    
    pipeline = FreeYouTubePipeline()
    
    if args.stats:
        stats = pipeline.get_free_stats()
        print("📊 FREE Upload Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        exit(0)
    
    if args.mode == "single":
        pipeline.generate_and_upload_video(args.fact, args.category)
    elif args.mode == "daily":
        pipeline.free_daily_automation(args.videos_per_day) 