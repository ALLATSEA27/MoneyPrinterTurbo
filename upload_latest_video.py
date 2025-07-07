#!/usr/bin/env python3
"""
Upload Latest Video to YouTube
Uploads the most recently generated video to YouTube
"""

import os
import json
import glob
from datetime import datetime
from youtube_uploader import YouTubeUploader

def get_latest_video():
    """Get the most recently generated video"""
    video_pattern = "storage/tasks/*/final-1.mp4"
    videos = glob.glob(video_pattern)
    
    if not videos:
        raise FileNotFoundError("No videos found in storage/tasks/")
    
    # Get the most recent video
    latest_video = max(videos, key=os.path.getctime)
    return latest_video

def get_fact_for_video(video_path):
    """Try to get the fact used for this video from logs or generate a default"""
    # This is a simplified version - you might want to store fact data with videos
    return "Amazing fact about the universe and science!"

def main():
    try:
        print("🎬 YouTube Upload Script")
        print("=" * 40)
        
        # Get latest video
        video_path = get_latest_video()
        print(f"📹 Found video: {video_path}")
        print(f"📊 Size: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
        print(f"🕒 Created: {datetime.fromtimestamp(os.path.getctime(video_path))}")
        
        # Get fact (you might want to store this with the video)
        fact = get_fact_for_video(video_path)
        
        # Initialize uploader
        print("\n🔐 Setting up YouTube API...")
        uploader = YouTubeUploader()
        
        # Upload video
        print("\n📤 Uploading to YouTube...")
        result = uploader.upload_video(
            video_path=video_path,
            fact=fact,
            category="science"
        )
        
        print(f"\n✅ Upload successful!")
        print(f"🔗 YouTube URL: {result['url']}")
        print(f"📝 Title: {result['title']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure:")
        print("1. You have valid YouTube credentials (client_secrets.json)")
        print("2. You have generated videos in storage/tasks/")
        print("3. Your YouTube API quota is not exceeded")

if __name__ == "__main__":
    main() 