#!/bin/bash
# Setup cron jobs for automated YouTube video generation and upload

echo "🤖 Setting up automated YouTube pipeline..."

# Get the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/free_youtube_pipeline.py"

# Check if the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: free_youtube_pipeline.py not found in $SCRIPT_DIR"
    exit 1
fi

# Create a wrapper script that activates the virtual environment
WRAPPER_SCRIPT="$SCRIPT_DIR/run_pipeline.sh"
cat > "$WRAPPER_SCRIPT" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
source venv/bin/activate
python free_youtube_pipeline.py --mode single
EOF

chmod +x "$WRAPPER_SCRIPT"

echo "📝 Created wrapper script: $WRAPPER_SCRIPT"

# Function to add cron job
add_cron_job() {
    local time="$1"
    local description="$2"
    
    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "$PYTHON_SCRIPT"; then
        echo "⚠️  Cron job already exists for $description"
        return
    fi
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$time $WRAPPER_SCRIPT >> $SCRIPT_DIR/cron.log 2>&1") | crontab -
    echo "✅ Added cron job for $description at $time"
}

# Add different cron job options
echo ""
echo "Choose your automation schedule:"
echo "1. Twice daily (9 AM and 9 PM)"
echo "2. Once daily (9 AM)"
echo "3. Custom schedule"
echo "4. View current cron jobs"
echo "5. Remove all cron jobs"

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        add_cron_job "0 9,21 * * *" "twice daily (9 AM and 9 PM)"
        add_cron_job "0 21 * * *" "twice daily (9 AM and 9 PM)"
        ;;
    2)
        add_cron_job "0 9 * * *" "once daily (9 AM)"
        ;;
    3)
        echo "Enter cron schedule (e.g., '0 9 * * *' for daily at 9 AM):"
        echo "Format: minute hour day month weekday"
        echo "Examples:"
        echo "  '0 9 * * *'     - Daily at 9 AM"
        echo "  '0 9,21 * * *'  - Daily at 9 AM and 9 PM"
        echo "  '0 */6 * * *'   - Every 6 hours"
        read -p "Cron schedule: " custom_schedule
        add_cron_job "$custom_schedule" "custom schedule"
        ;;
    4)
        echo "📋 Current cron jobs:"
        crontab -l 2>/dev/null || echo "No cron jobs found"
        ;;
    5)
        echo "🗑️  Removing all cron jobs..."
        crontab -r 2>/dev/null
        echo "✅ All cron jobs removed"
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
echo "  Test single upload: python free_youtube_pipeline.py --mode single"
echo "  View stats: python free_youtube_pipeline.py --stats"
echo "  Edit cron jobs: crontab -e"
echo "  View cron logs: tail -f $SCRIPT_DIR/cron.log" 