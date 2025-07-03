#!/usr/bin/env python3
"""
Simple YouTube API Authentication Test
"""

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

def test_auth():
    print("🔍 Testing YouTube API Authentication...")
    
    # Check if credentials file exists
    if not os.path.exists("client_secrets.json"):
        print("❌ client_secrets.json not found!")
        print("Please download OAuth2 credentials from Google Cloud Console")
        return False
    
    print("✅ client_secrets.json found")
    
    # OAuth2 scopes
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    creds = None
    
    # Load existing token
    if os.path.exists('token.pickle'):
        print("📁 Found existing token.pickle")
        try:
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
            print("✅ Loaded existing credentials")
        except Exception as e:
            print(f"❌ Error loading token: {e}")
            creds = None
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired credentials...")
            try:
                creds.refresh(Request())
                print("✅ Credentials refreshed")
            except Exception as e:
                print(f"❌ Failed to refresh: {e}")
                creds = None
        
        if not creds:
            print("🔐 Starting OAuth2 authentication...")
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secrets.json", SCOPES)
                
                print("🌐 Opening browser for authentication...")
                print("📝 Please log in with your Google account and grant permissions")
                
                creds = flow.run_local_server(port=0)
                print("✅ Authentication successful!")
                
                # Save credentials
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
                print("💾 Credentials saved to token.pickle")
                
            except Exception as e:
                print(f"❌ Authentication failed: {e}")
                return False
    
    # Test API connection
    try:
        print("🔗 Testing YouTube API connection...")
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Test with a simple API call
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )
        response = request.execute()
        
        if 'items' in response:
            channel = response['items'][0]
            print(f"✅ Connected to YouTube channel: {channel['snippet']['title']}")
            return True
        else:
            print("❌ No channels found")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_auth()
    if success:
        print("\n🎉 Authentication test passed! You're ready to upload videos.")
    else:
        print("\n❌ Authentication test failed. Please check the setup.") 