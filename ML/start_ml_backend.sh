#!/bin/bash
# Start the Label Studio ML Backend server

# Kill any existing ML backend processes to avoid duplicates
echo "🔍 Checking for existing ML backend processes..."
pkill -f "_wsgi.py" 2>/dev/null && echo "✓ Stopped existing backend" || echo "✓ No existing backend found"
pkill -f "label-studio-ml start" 2>/dev/null
sleep 2

# Activate virtual environment
source /Users/pierrebastiani/Classification/.venv/bin/activate

echo "🤖 Starting Label Studio ML Backend..."
echo ""

# Check if backend directory exists
if [ ! -d "label-studio-ml-backend" ]; then
    echo "❌ ML Backend not set up yet!"
    echo "Please run: ./setup_ml_backend.sh first"
    exit 1
fi

# Detect which backend is set up
if [ -d "custom_ml_backend/models" ]; then
    echo "🎯 Detected Custom SAM backend with metadata pre-filling"
    cd custom_ml_backend
    
    # Find the model file
    MODEL_FILE=$(ls models/*.pth 2>/dev/null | head -n 1)
    
    if [ -z "$MODEL_FILE" ]; then
        echo "❌ No SAM model found in models/ directory"
        exit 1
    fi
    
    echo "📦 Using model: $MODEL_FILE"
    echo ""
    echo "✨ This backend will:"
    echo "  ✓ Detect feathers automatically"
    echo "  ✓ Pre-fill colors, size, motif from your metadata"
    echo ""
    echo "Starting server on http://localhost:9090"
    echo "Logs: custom_ml_backend/ml_backend.log"
    echo ""
    
    # Start using the label-studio-ml CLI with proper directory setup in background
    cd ..
    nohup label-studio-ml start custom_ml_backend --with model_path=custom_ml_backend/$MODEL_FILE --port 9090 > custom_ml_backend/ml_backend.log 2>&1 &
    
    # Wait a moment and check if it started
    sleep 3
    if curl -s http://localhost:9090/health > /dev/null 2>&1; then
        echo "✅ ML Backend started successfully!"
        echo "📊 Health check: http://localhost:9090/health"
    else
        echo "⚠️  Backend may still be starting... check logs with:"
        echo "   tail -f custom_ml_backend/ml_backend.log"
    fi

elif [ -d "label-studio-ml-backend/label_studio_ml/examples/segment_anything_model/models" ]; then
    echo "🎯 Detected SAM backend"
    cd label-studio-ml-backend/label_studio_ml/examples/segment_anything_model
    
    # Find the model file
    MODEL_FILE=$(ls models/*.pth 2>/dev/null | head -n 1)
    
    if [ -z "$MODEL_FILE" ]; then
        echo "❌ No SAM model found in models/ directory"
        exit 1
    fi
    
    echo "📦 Using model: $MODEL_FILE"
    echo ""
    echo "Starting server on http://localhost:9090"
    echo "Logs: ml_backend.log"
    echo ""
    
    nohup label-studio-ml start . --with model_path=$MODEL_FILE --port 9090 > ml_backend.log 2>&1 &
    
    # Wait a moment and check if it started
    sleep 3
    if curl -s http://localhost:9090/health > /dev/null 2>&1; then
        echo "✅ ML Backend started successfully!"
    else
        echo "⚠️  Backend may still be starting... check logs with: tail -f ml_backend.log"
    fi
    
elif [ -d "label-studio-ml-backend/label_studio_ml/examples/grounding_dino" ]; then
    echo "🎯 Using GroundingDINO backend"
    cd label-studio-ml-backend/label_studio_ml/examples/grounding_dino
    
    echo "Starting server on http://localhost:9090"
    echo "Logs: ml_backend.log"
    echo ""
    
    nohup label-studio-ml start . --port 9090 > ml_backend.log 2>&1 &
    
    # Wait a moment and check if it started
    sleep 3
    if curl -s http://localhost:9090/health > /dev/null 2>&1; then
        echo "✅ ML Backend started successfully!"
    else
        echo "⚠️  Backend may still be starting... check logs with: tail -f ml_backend.log"
    fi
else
    echo "❌ No ML backend configured!"
    echo "Please run: ./setup_ml_backend.sh first"
    exit 1
fi
