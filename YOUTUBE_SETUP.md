# YouTube API Setup Guide

This guide will help you set up automated YouTube uploading for your "Honest AI Slop" videos.

## Prerequisites

1. **Google Account**: You need a Google account with YouTube access
2. **Python Dependencies**: Install the required packages

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name your project (e.g., "Honest AI Slop Uploader")
4. Click "Create"

## Step 2: Enable YouTube Data API v3

1. In your project, go to "APIs & Services" → "Library"
2. Search for "YouTube Data API v3"
3. Click on it and press "Enable"

## Step 3: Create OAuth2 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Choose "Desktop application" as application type
4. Name it (e.g., "Honest AI Slop Desktop Client")
5. Click "Create"
6. Download the JSON file and rename it to `client_secrets.json`
7. Place it in your project root directory

## Step 4: First Authentication

Run the uploader script for the first time:

```bash
python youtube_uploader.py
```

This will:
- Open a browser window for Google authentication
- Ask you to log in to your Google account
- Request permission to upload to YouTube
- Save authentication tokens to `token.pickle`

## Step 5: Test Upload

Test with a single video:

```bash
python automated_youtube_pipeline.py --mode single
```

## Usage Examples

### Single Video Upload
```bash
python automated_youtube_pipeline.py --mode single
```

### Batch Upload (2 videos, 12 hours apart)
```bash
python automated_youtube_pipeline.py --mode batch --count 2 --delay 12
```

### Daily Automation (2 videos per day)
```bash
python automated_youtube_pipeline.py --mode daily --videos-per-day 2
```

### Upload Statistics
```bash
python automated_youtube_pipeline.py --stats
```

## Configuration Options

### Video Settings
- **Title Template**: "Mind-Blowing Fact: {fact_title}"
- **Description**: Includes fact text, hashtags, and AI disclaimer
- **Tags**: facts, education, mindblowing, science, knowledge, etc.
- **Category**: Education (ID: 27)
- **Privacy**: Public (can be changed to "private" or "unlisted")

### Customization
Edit `youtube_uploader.py` to modify:
- Title templates
- Description format
- Tags
- Privacy settings
- Upload delays

## Troubleshooting

### Authentication Issues
- Delete `token.pickle` and re-authenticate
- Ensure `client_secrets.json` is in the project root
- Check that YouTube Data API v3 is enabled

### Upload Failures
- Check internet connection
- Verify video file exists and is valid
- Check YouTube API quotas (10,000 units/day)
- Ensure video meets YouTube guidelines

### Rate Limiting
- Default delay: 30 seconds between uploads
- YouTube API limit: ~100 uploads per day
- Consider using "private" uploads for testing

## Security Notes

- Keep `client_secrets.json` and `token.pickle` secure
- Don't commit these files to version control
- Add them to `.gitignore`:

```
client_secrets.json
token.pickle
upload_log.json
```

## Advanced Features

### Custom Titles and Descriptions
```python
uploader.upload_video(
    video_path="video.mp4",
    fact="Your fact here",
    custom_title="Custom Title",
    custom_description="Custom description with links"
)
```

### Batch Processing
```python
videos = [
    {"video_path": "video1.mp4", "fact": "Fact 1", "category": "science"},
    {"video_path": "video2.mp4", "fact": "Fact 2", "category": "history"}
]
uploader.upload_batch(videos)
```

## Monitoring and Logs

The system creates `upload_log.json` with:
- Upload timestamps
- Video URLs
- Success/failure status
- Fact and category information

Use `--stats` to view upload statistics.

## Cost Considerations

- YouTube Data API: Free tier (10,000 units/day)
- Each upload: ~1,600 units
- Daily limit: ~6 uploads per day
- For more uploads, enable billing in Google Cloud Console

## Next Steps

1. Test with a single video first
2. Run batch uploads during off-peak hours
3. Monitor upload logs and statistics
4. Adjust timing and content based on performance
5. Consider monetization strategies once you have a following 