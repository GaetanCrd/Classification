#!/bin/bash
# Quick start script for batch predictions

echo "🚀 Starting batch prediction generation..."
echo ""

# Check if Label Studio is running
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "❌ Label Studio is not running on port 8080"
    echo "   Start it with: ./start_label_studio.sh"
    exit 1
fi

# Check if ML backend is running
if ! curl -s http://localhost:9090/health > /dev/null 2>&1; then
    echo "❌ ML Backend is not running on port 9090"
    echo "   Start it with: ./start_ml_backend.sh"
    exit 1
fi

echo "✅ Both services are running"
echo ""

# Activate virtual environment
source .venv/bin/activate

# Run the batch prediction script (will prompt for token)
python3 generate_predictions_batch.py

echo ""
echo "✅ Batch processing complete!"
