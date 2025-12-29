#!/bin/bash
# Run batch predictions overnight in background
# Note: Token will be read from .label_studio_token file (automatically refreshed by get_api_token.py)
# Usage: ./run_predictions_overnight.sh [--resume]
#   --resume: Keep previous progress and resume from where it left off

RESUME=false
if [ "$1" == "--resume" ]; then
    RESUME=true
fi

echo "🚀 Starting batch predictions in background..."
echo "📝 Logs: batch_predictions.log"
echo "📊 Progress: prediction_progress.json"
echo ""

# Clear previous prediction progress to start fresh (unless --resume flag is set)
if [ "$RESUME" = false ] && [ -f prediction_progress.json ]; then
    echo "🗑️  Clearing previous prediction progress..."
    rm prediction_progress.json
elif [ "$RESUME" = true ] && [ -f prediction_progress.json ]; then
    echo "♻️  Resuming from previous progress..."
fi

# Run in background with nohup (token will be read from .label_studio_token file)
nohup bash -c "
cd $(pwd)
./start_batch_predictions.sh < /dev/null
" > batch_predictions.log 2>&1 &

PID=$!
echo "✅ Started! Process ID: $PID"
echo ""
echo "Monitor progress with:"
echo "  tail -f batch_predictions.log"
echo ""
echo "Check predictions:"
echo "  cat prediction_progress.json"
echo ""
echo "Stop if needed:"
echo "  kill $PID"