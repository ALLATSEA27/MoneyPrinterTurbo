#!/bin/bash
# setup_high_quality_cron.sh
# Interactive setup for high-quality MoneyPrinterTurbo cron jobs

echo "🤖 Setting up automated HIGH-QUALITY MoneyPrinterTurbo pipeline..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WRAPPER_SCRIPT="$SCRIPT_DIR/run_pipeline.sh"

if [ ! -f "$WRAPPER_SCRIPT" ]; then
    echo "❌ Error: run_pipeline.sh not found in $SCRIPT_DIR"
    exit 1
fi

# Function to add cron job
add_cron_job() {
    local time="$1"
    local description="$2"
    # Remove any existing job for run_pipeline.sh
    crontab -l 2>/dev/null | grep -v "$WRAPPER_SCRIPT" > temp_cron || true
    # Add new job
    { cat temp_cron; echo "$time $WRAPPER_SCRIPT >> $SCRIPT_DIR/cron.log 2>&1"; } | crontab -
    rm -f temp_cron
    echo "✅ Added cron job for $description at $time"
}

echo ""
echo "Choose your automation schedule for HIGH-QUALITY pipeline:"
echo "1. Four times daily (9 AM, 11 AM, 1 PM, 3 PM)"
echo "2. Twice daily (9 AM and 9 PM)"
echo "3. Once daily (9 AM)"
echo "4. Custom schedule"
echo "5. View current cron jobs"
echo "6. Remove all cron jobs"

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        add_cron_job "0 9,11,13,15 * * *" "four times daily (9, 11, 13, 15)"
        ;;
    2)
        add_cron_job "0 9,21 * * *" "twice daily (9 AM and 9 PM)"
        ;;
    3)
        add_cron_job "0 9 * * *" "once daily (9 AM)"
        ;;
    4)
        echo "Enter cron schedule (e.g., '0 9 * * *' for daily at 9 AM):"
        echo "Format: minute hour day month weekday"
        read -p "Cron schedule: " custom_schedule
        add_cron_job "$custom_schedule" "custom schedule"
        ;;
    5)
        echo "📋 Current cron jobs:"
        crontab -l 2>/dev/null || echo "No cron jobs found"
        exit 0
        ;;
    6)
        echo "🗑️  Removing all cron jobs..."
        crontab -r 2>/dev/null
        echo "✅ All cron jobs removed"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Current cron jobs:"
crontab -l 2>/dev/null || echo "No cron jobs found"
echo ""
echo "📝 Logs will be saved to: $SCRIPT_DIR/cron.log"
echo ""
echo "🔧 Manual commands:"
echo "  Test single upload: $WRAPPER_SCRIPT"
echo "  Edit cron jobs: crontab -e"
echo "  View cron logs: tail -f $SCRIPT_DIR/cron.log" 