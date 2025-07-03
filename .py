import requests
import json
import time
import random
import glob
import os

class HonestAISlopGenerator:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        # Load facts from your database
        with open("fact_database.json") as f:
            self.facts = json.load(f)["facts"]
        # Find all psychedelic images/videos in your local folder
        self.psychedelic_files = glob.glob("resource/psychedelic/*")
        if not self.psychedelic_files:
            raise Exception("No psychedelic files found in resource/psychedelic/")
        # Voice options (customize as needed)
        self.voice_options = [
            "en-US-JennyNeural", "en-US-GuyNeural", "en-US-AriaNeural", "en-US-DavisNeural"
        ]

    def generate_honest_video(self, voice: str = None):
        fact = random.choice(self.facts)
        background = random.choice(self.psychedelic_files)
        task_data = {
            "video_subject": fact["fact"],
            "video_script": fact["fact"],
            "video_aspect": "9:16",
            "video_concat_mode": "random",
            "video_transition_mode": "FadeIn",
            "max_clip_duration": 4,
            "video_count": 1,
            "subtitle_provider": "edge",
            "voice_name": voice or random.choice(self.voice_options),
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
            "video_source": "local",
            "video_materials": [
                {
                    "provider": "local",
                    "url": os.path.abspath(background)
                }
            ]
        }
        response = requests.post(f"{self.base_url}/api/v1/videos", json=task_data)
        print("API response:", response.text)
        if response.status_code != 200:
            raise Exception(f"Failed to create task: {response.text}")
        data = response.json()
        task_id = data["data"]["task_id"]
        print(f"Created task: {task_id}")
        # Monitor task status
        while True:
            status_response = requests.get(f"{self.base_url}/api/v1/tasks/{task_id}")
            status_data = status_response.json()
            status = status_data["status"]
            print(f"Status: {status}")
            if status == "completed":
                videos = status_data.get("videos", [])
                for i, video in enumerate(videos):
                    video_url = f"{self.base_url}/tasks/{task_id}/{video}"
                    print(f"Video {i+1}: {video_url}")
                return task_id, videos
            elif status == "failed":
                raise Exception(f"Task failed: {status_data.get('error', 'Unknown error')}")
            time.sleep(5)

if __name__ == "__main__":
    generator = HonestAISlopGenerator()
    generator.generate_honest_video()