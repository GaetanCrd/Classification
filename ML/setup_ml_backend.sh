#!/bin/bash
# Setup ML Backend for Label Studio Semi-Automated Labeling

#lsof -ti:9090 | xargs kill
set -e

echo "🤖 Label Studio ML Backend Setup"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run from the Classification directory."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

echo "📦 Installing Label Studio ML Backend..."
pip install label-studio-ml

echo ""
echo "📥 Cloning Label Studio ML Backend repository..."
if [ ! -d "label-studio-ml-backend" ]; then
    git clone https://github.com/HumanSignal/label-studio-ml-backend.git
else
    echo "⚠️  Repository already exists, skipping clone"
fi

echo ""
echo "🎯 Choose ML Backend to setup:"
echo "1. SAM (Segment Anything Model) - Basic object detection"
echo "2. Custom SAM with Metadata - Recommended! (SAM + auto-fill attributes)"
echo "3. GroundingDINO - Text-prompted detection"
echo "4. Skip backend installation (manual setup later)"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "📦 Setting up Segment Anything Model (SAM)..."
        cd label-studio-ml-backend/label_studio_ml/examples/segment_anything_model
        
        echo "Installing dependencies (fixing version conflicts)..."
        # Install segment-anything first (it will get compatible onnxruntime)
        pip install segment-anything
        # Then install other requirements, allowing newer onnxruntime
        pip install -r requirements.txt --upgrade
        
        echo ""
        echo "📥 Choose SAM model size:"
        echo "1. ViT-B (smallest, fastest, 375MB)"
        echo "2. ViT-L (medium, 1.2GB)"
        echo "3. ViT-H (largest, most accurate, 2.5GB)"
        echo ""
        read -p "Enter choice (1-3): " model_choice
        
        mkdir -p models
        
        case $model_choice in
            1)
                echo "Downloading ViT-B model..."
                curl -L https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -o models/sam_vit_b_01ec64.pth
                MODEL_PATH="models/sam_vit_b_01ec64.pth"
                ;;
            2)
                echo "Downloading ViT-L model..."
                curl -L https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth -o models/sam_vit_l_0b3195.pth
                MODEL_PATH="models/sam_vit_l_0b3195.pth"
                ;;
            3)
                echo "Downloading ViT-H model..."
                curl -L https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -o models/sam_vit_h_4b8939.pth
                MODEL_PATH="models/sam_vit_h_4b8939.pth"
                ;;
            *)
                echo "Invalid choice. Defaulting to ViT-B"
                curl -L https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -o models/sam_vit_b_01ec64.pth
                MODEL_PATH="models/sam_vit_b_01ec64.pth"
                ;;
        esac
        
        cd ../../../..        echo ""
        echo "✅ SAM backend setup complete!"
        echo ""
        echo "To start the ML backend, run:"
        echo "cd label-studio-ml-backend/label_studio_ml/examples/segment_anything_model"
        echo "label-studio-ml start . --with model_path=$MODEL_PATH --port 9090"
        ;;
    
    2)
        echo ""
        echo "📦 Setting up Custom SAM with Metadata Pre-filling..."
        echo "This combines SAM detection with automatic attribute filling!"
        echo ""
        
        # Custom backend is already in custom_ml_backend/
        cd custom_ml_backend
        
        echo "Installing dependencies..."
        pip install -r requirements.txt
        
        echo ""
        echo "📥 Choose SAM model size:"
        echo "1. ViT-B (smallest, fastest, 375MB) - Recommended"
        echo "2. ViT-L (medium, 1.2GB)"
        echo "3. ViT-H (largest, most accurate, 2.5GB)"
        echo ""
        read -p "Enter choice (1-3): " model_choice
        
        mkdir -p models
        
        case $model_choice in
            1)
                echo "Downloading ViT-B model..."
                curl -L https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -o models/sam_vit_b_01ec64.pth
                MODEL_PATH="models/sam_vit_b_01ec64.pth"
                ;;
            2)
                echo "Downloading ViT-L model..."
                curl -L https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth -o models/sam_vit_l_0b3195.pth
                MODEL_PATH="models/sam_vit_l_0b3195.pth"
                ;;
            3)
                echo "Downloading ViT-H model..."
                curl -L https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -o models/sam_vit_h_4b8939.pth
                MODEL_PATH="models/sam_vit_h_4b8939.pth"
                ;;
            *)
                echo "Invalid choice. Defaulting to ViT-B"
                curl -L https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -o models/sam_vit_b_01ec64.pth
                MODEL_PATH="models/sam_vit_b_01ec64.pth"
                ;;
        esac
        
        cd ..
        
        echo ""
        echo "✅ Custom SAM backend with metadata pre-filling setup complete!"
        echo ""
        echo "🎉 This backend will:"
        echo "  ✓ Detect feathers automatically (SAM)"
        echo "  ✓ Pre-fill colors, size, motif from metadata"
        echo "  ✓ Save you even more time!"
        echo ""
        echo "To start the ML backend, run:"
        echo "cd custom_ml_backend"
        echo "label-studio-ml start . --with model_path=$MODEL_PATH --port 9090"
        ;;
        
    3)
        echo ""
        echo "📦 Setting up GroundingDINO..."
        cd label-studio-ml-backend/label_studio_ml/examples/grounding_dino
        
        echo "Installing dependencies..."
        pip install -r requirements.txt
        
        cd ../../../..
        
        echo ""
        echo "✅ GroundingDINO backend setup complete!"
        echo ""
        echo "To start the ML backend, run:"
        echo "cd label-studio-ml-backend/label_studio_ml/examples/grounding_dino"
        echo "label-studio-ml start . --port 9090"
        ;;
        
    4)
        echo "Skipping backend installation"
        ;;
        
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "📖 Next steps:"
echo "1. Start Label Studio (in one terminal):"
echo "   ./start_label_studio.sh"
echo ""
echo "2. Start ML Backend (in another terminal):"
echo "   See the command above for your chosen backend"
echo ""
echo "3. Connect backend to Label Studio:"
echo "   - Open your project"
echo "   - Settings → Model → Add Model"
echo "   - URL: http://localhost:9090"
echo ""
echo "4. See docs/ML_BACKEND_SETUP.md for detailed usage instructions"
echo ""
echo "✨ Setup complete!"
