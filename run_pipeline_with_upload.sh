#!/bin/bash
cd "/Users/admin/Development/moneyprinter/MoneyPrinterTurbo"
source venv/bin/activate

# Log the start time
echo "$(date): Starting SIMPLE HIGH-QUALITY pipeline with YouTube upload..." >> cron.log

# Run the simple high-quality generator
python3 simple_high_quality_generator.py

# Upload the latest video to YouTube
echo "$(date): Uploading latest video to YouTube..." >> cron.log
python3 upload_latest_video.py

# Log the completion
echo "$(date): SIMPLE HIGH-QUALITY pipeline with YouTube upload completed" >> cron.log 