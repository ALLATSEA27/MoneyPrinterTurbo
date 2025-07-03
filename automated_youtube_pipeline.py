#!/usr/bin/env python3
"""
Automated YouTube Pipeline for Honest AI Slop
Generates videos and uploads them to YouTube automatically
"""

import os
import json
import time
import random
import requests
from datetime import datetime, timedelta
from honest_ai_slop_generator import HonestAISlopGenerator
from youtube_uploader import YouTubeUploader

class AutomatedYouTubePipeline:
    def __init__(self, config_file="config.toml", fact_database="fact_database.json"):
        self.generator = HonestAISlopGenerator(config_file, fact_database)
        self.uploader = YouTubeUploader()
        self.upload_log_file = "upload_log.json"
        self.load_upload_log()
    
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
    
    def generate_and_upload_video(self, fact=None, category=None):
        """
        Generate a single video and upload it to YouTube
        
        Args:
            fact: Specific fact to use (optional)
            category: Specific category to use (optional)
        """
        print("🎬 Starting video generation and upload pipeline...")
        
        # Step 1: Generate video
        print("📹 Generating video...")
        task_id = self.generator.generate_single_video(fact, category)
        
        if not task_id:
            print("❌ Failed to generate video")
            return None
        
        # Step 2: Wait for video completion
        print("⏳ Waiting for video generation to complete...")
        video_path = self.generator.wait_for_completion(task_id)
        
        if not video_path:
            print("❌ Video generation failed or timed out")
            return None
        
        # Step 3: Upload to YouTube
        print("📤 Uploading to YouTube...")
        try:
            # Get fact details for upload
            fact_data = self.generator.get_last_used_fact()
            
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
                'timestamp': datetime.now().isoformat()
            }
            
            self.upload_log.append(upload_log_entry)
            self.save_upload_log()
            
            print(f"✅ Successfully generated and uploaded video!")
            print(f"🔗 YouTube URL: {upload_result['url']}")
            
            return upload_result
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return None
    
    def generate_and_upload_batch(self, count=2, delay_hours=12):
        """
        Generate and upload multiple videos with delays
        
        Args:
            count: Number of videos to generate
            delay_hours: Hours to wait between videos
        """
        print(f"🚀 Starting batch generation: {count} videos")
        print(f"⏰ Delay between videos: {delay_hours} hours")
        
        results = []
        
        for i in range(count):
            print(f"\n--- Video {i+1}/{count} ---")
            
            result = self.generate_and_upload_video()
            results.append(result)
            
            if result and i < count - 1:
                print(f"⏳ Waiting {delay_hours} hours before next video...")
                time.sleep(delay_hours * 3600)  # Convert hours to seconds
        
        print(f"\n🎉 Batch complete! Generated and uploaded {len([r for r in results if r])} videos")
        return results
    
    def daily_automation(self, videos_per_day=2):
        """
        Run daily automation - generates specified number of videos per day
        """
        print(f"📅 Starting daily automation: {videos_per_day} videos per day")
        
        # Calculate delay between videos
        delay_hours = 24 // videos_per_day
        
        while True:
            try:
                print(f"\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("=" * 50)
                
                # Generate and upload videos
                self.generate_and_upload_batch(
                    count=videos_per_day,
                    delay_hours=delay_hours
                )
                
                # Wait until next day
                next_run = datetime.now() + timedelta(days=1)
                next_run = next_run.replace(hour=9, minute=0, second=0, microsecond=0)  # 9 AM
                
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
    
    def get_upload_stats(self):
        """Get statistics about uploaded videos"""
        if not self.upload_log:
            return {"total_uploads": 0, "successful_uploads": 0, "failed_uploads": 0}
        
        successful = len([entry for entry in self.upload_log if 'upload_result' in entry and 'error' not in entry['upload_result']])
        failed = len([entry for entry in self.upload_log if 'upload_result' in entry and 'error' in entry['upload_result']])
        
        return {
            "total_uploads": len(self.upload_log),
            "successful_uploads": successful,
            "failed_uploads": failed,
            "success_rate": f"{(successful/len(self.upload_log)*100):.1f}%"
        }

# Command line interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated YouTube Pipeline for Honest AI Slop")
    parser.add_argument("--mode", choices=["single", "batch", "daily"], default="single",
                       help="Operation mode")
    parser.add_argument("--count", type=int, default=1,
                       help="Number of videos to generate (for batch mode)")
    parser.add_argument("--delay", type=int, default=12,
                       help="Hours between videos (for batch mode)")
    parser.add_argument("--videos-per-day", type=int, default=2,
                       help="Videos per day (for daily mode)")
    parser.add_argument("--fact", type=str,
                       help="Specific fact to use")
    parser.add_argument("--category", type=str,
                       help="Specific category to use")
    parser.add_argument("--stats", action="store_true",
                       help="Show upload statistics")
    
    args = parser.parse_args()
    
    pipeline = AutomatedYouTubePipeline()
    
    if args.stats:
        stats = pipeline.get_upload_stats()
        print("📊 Upload Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        exit(0)
    
    if args.mode == "single":
        pipeline.generate_and_upload_video(args.fact, args.category)
    elif args.mode == "batch":
        pipeline.generate_and_upload_batch(args.count, args.delay)
    elif args.mode == "daily":
        pipeline.daily_automation(args.videos_per_day) 