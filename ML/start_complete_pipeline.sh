#!/bin/bash
# Complete overnight prediction pipeline
# This script:
# 1. Starts Label Studio (if not running)
# 2. Ensures ML Backend is running
# 3. Runs batch predictions

echo "🌙 Overnight Batch Prediction Setup"
echo "=" * 60

# Check if Label Studio is running
if ! curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "📊 Starting Label Studio..."
    ./start_label_studio.sh > label_studio.log 2>&1 &
    LS_PID=$!
    echo "   Label Studio PID: $LS_PID"
    
    # Wait for Label Studio to be ready
    echo "   Waiting for Label Studio to start..."
    for i in {1..30}; do
        if curl -s http://localhost:8080/health > /dev/null 2>&1; then
            echo "   ✅ Label Studio is ready!"
            break
        fi
        sleep 2
        echo -n "."
    done
    echo ""
else
    echo "✅ Label Studio already running"
fi

# Check if ML Backend is running
if ! curl -s http://localhost:9090/health > /dev/null 2>&1; then
    echo "🤖 Starting ML Backend..."
    cd custom_ml_backend
    ../.venv/bin/python _wsgi.py > ../ml_backend.log 2>&1 &
    ML_PID=$!
    cd ..
    echo "   ML Backend PID: $ML_PID"
    
    # Wait for ML Backend to be ready
    echo "   Waiting for ML Backend to start..."
    for i in {1..10}; do
        if curl -s http://localhost:9090/health > /dev/null 2>&1; then
            echo "   ✅ ML Backend is ready!"
            break
        fi
        sleep 1
        echo -n "."
    done
    echo ""
else
    echo "✅ ML Backend already running"
fi

# Verify both services are up
echo ""
echo "🔍 Verifying services..."
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "   ✅ Label Studio: UP"
else
    echo "   ❌ Label Studio: DOWN"
    echo "   Cannot proceed without Label Studio!"
    exit 1
fi

if curl -s http://localhost:9090/health > /dev/null 2>&1; then
    echo "   ✅ ML Backend: UP"
else
    echo "   ❌ ML Backend: DOWN"
    echo "   Cannot proceed without ML Backend!"
    exit 1
fi

echo ""
echo "🚀 All services ready! Starting batch predictions..."
echo "=" * 60
echo ""

# Activate virtual environment
source .venv/bin/activate

# Run batch predictions
./run_predictions_overnight.sh

echo ""
echo "✅ Batch processing complete!"
echo "Check prediction_progress.json for results"
