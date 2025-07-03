#!/usr/bin/env python3
"""
YouTube Uploader for Honest AI Slop Videos
Automatically uploads generated videos to YouTube
"""

import os
import json
import time
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import pickle

class YouTubeUploader:
    def __init__(self, credentials_file="client_secrets.json"):
        self.credentials_file = credentials_file
        self.youtube = None
        self.setup_youtube_api()
        
        # Default upload settings
        self.default_title_template = "Mind-Blowing Fact: {fact_title}"
        self.default_description_template = """
🔬 {fact}

💡 Did you know this incredible fact? Share your thoughts below!

#facts #education #mindblowing #science #knowledge #interesting #didyouknow #amazing #fact #learning

---
Generated with AI 🤖
        """.strip()
        
        self.default_tags = [
            "facts", "education", "mindblowing", "science", "knowledge", 
            "interesting", "didyouknow", "amazing", "fact", "learning",
            "psychedelic", "tantric", "mystical", "spiritual"
        ]
        
        self.default_category_id = "27"  # Education category
        self.default_privacy_status = "public"  # or "private", "unlisted"
    
    def setup_youtube_api(self):
        """Setup YouTube API with OAuth2 authentication"""
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        
        creds = None
        
        # Load existing credentials
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials available, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    print(f"❌ {self.credentials_file} not found!")
                    print("Please download your OAuth2 credentials from Google Cloud Console")
                    print("1. Go to https://console.cloud.google.com/")
                    print("2. Create a project and enable YouTube Data API v3")
                    print("3. Create OAuth2 credentials and download as client_secrets.json")
                    raise FileNotFoundError(f"{self.credentials_file} not found")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        self.youtube = build('youtube', 'v3', credentials=creds)
        print("✅ YouTube API authenticated successfully!")
    
    def upload_video(self, video_path, fact, category="science", custom_title=None, custom_description=None):
        """
        Upload a video to YouTube
        
        Args:
            video_path: Path to the video file
            fact: The fact text for title/description
            category: Fact category for better tagging
            custom_title: Custom title (optional)
            custom_description: Custom description (optional)
        """
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Create title from fact (first 50 characters)
        fact_title = fact[:50] + "..." if len(fact) > 50 else fact
        
        # Generate title and description
        title = custom_title or self.default_title_template.format(fact_title=fact_title)
        description = custom_description or self.default_description_template.format(fact=fact)
        
        # Add category-specific tags
        tags = self.default_tags.copy()
        tags.extend([category, "honest_ai_slop"])
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': self.default_category_id
            },
            'status': {
                'privacyStatus': self.default_privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Create media upload object
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        
        print(f"🎬 Uploading video: {title}")
        print(f"📁 File: {video_path}")
        print(f"📊 Size: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
        
        try:
            # Start upload
            request = self.youtube.videos().insert(
                part=",".join(body.keys()),
                body=body,
                media_body=media
            )
            
            # Monitor upload progress
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"📤 Uploaded {int(status.progress() * 100)}%")
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            print(f"✅ Video uploaded successfully!")
            print(f"🔗 URL: {video_url}")
            
            return {
                'video_id': video_id,
                'url': video_url,
                'title': title,
                'upload_time': datetime.now().isoformat()
            }
            
        except HttpError as e:
            print(f"❌ Upload failed: {e}")
            raise
    
    def upload_batch(self, video_data_list):
        """
        Upload multiple videos with delays to avoid rate limits
        
        Args:
            video_data_list: List of dicts with 'video_path', 'fact', 'category'
        """
        results = []
        
        for i, video_data in enumerate(video_data_list):
            print(f"\n--- Uploading video {i+1}/{len(video_data_list)} ---")
            
            try:
                result = self.upload_video(
                    video_path=video_data['video_path'],
                    fact=video_data['fact'],
                    category=video_data.get('category', 'science')
                )
                results.append(result)
                
                # Wait between uploads to avoid rate limits
                if i < len(video_data_list) - 1:
                    print("⏳ Waiting 30 seconds before next upload...")
                    time.sleep(30)
                    
            except Exception as e:
                print(f"❌ Failed to upload video {i+1}: {e}")
                results.append({'error': str(e)})
        
        return results

# Example usage
if __name__ == "__main__":
    # Test upload
    uploader = YouTubeUploader()
    
    # Example video data
    test_video_data = {
        'video_path': 'storage/tasks/example/final-1.mp4',
        'fact': 'A day on Venus is longer than its year. Venus takes 243 Earth days to rotate on its axis, but only 225 Earth days to orbit the Sun.',
        'category': 'science'
    }
    
    # Uncomment to test upload
    # result = uploader.upload_video(**test_video_data)
    # print(f"Upload result: {result}") 