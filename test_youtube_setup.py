#!/usr/bin/env python3
"""
Test script to verify YouTube API setup
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        print("✅ All YouTube API modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_credentials_file():
    """Test if credentials file exists"""
    print("\n🔍 Testing credentials file...")
    
    if os.path.exists("client_secrets.json"):
        print("✅ client_secrets.json found")
        return True
    else:
        print("❌ client_secrets.json not found")
        print("📝 Please download OAuth2 credentials from Google Cloud Console")
        print("   and save as 'client_secrets.json' in the project root")
        return False

def test_authentication():
    """Test YouTube API authentication"""
    print("\n🔍 Testing authentication...")
    
    try:
        from youtube_uploader import YouTubeUploader
        
        # This will attempt to authenticate
        uploader = YouTubeUploader()
        print("✅ YouTube API authentication successful")
        return True
        
    except FileNotFoundError:
        print("❌ client_secrets.json not found")
        return False
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

def test_video_generation():
    """Test if video generation is working"""
    print("\n🔍 Testing video generation...")
    
    try:
        from honest_ai_slop_generator import HonestAISlopGenerator
        
        generator = HonestAISlopGenerator()
        print("✅ Video generator initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Video generation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 YouTube Automation Setup Test")
    print("=" * 40)
    
    tests = [
        ("Module Imports", test_imports),
        ("Credentials File", test_credentials_file),
        ("YouTube Authentication", test_authentication),
        ("Video Generation", test_video_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! You're ready to automate YouTube uploads.")
        print("\n📝 Next steps:")
        print("1. Test single upload: python automated_youtube_pipeline.py --mode single")
        print("2. Set up cron automation: ./setup_cron.sh")
        print("3. Monitor uploads: python automated_youtube_pipeline.py --stats")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before proceeding.")
        
        if not any(name == "Credentials File" and result for name, result in results):
            print("\n🔧 To fix credentials:")
            print("1. Go to https://console.cloud.google.com/")
            print("2. Create a project and enable YouTube Data API v3")
            print("3. Create OAuth2 credentials and download as client_secrets.json")

if __name__ == "__main__":
    main() 