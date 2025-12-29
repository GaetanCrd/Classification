# Semi-Automated Labeling Setup with Label Studio

This guide explains how to set up semi-automated labeling with Label Studio using ML backends to pre-label your feather images.

## 🎯 Overview

Semi-automated labeling combines:

1. **Pre-trained ML models** that generate initial bounding boxes and labels
2. **Human review** to correct and refine the predictions
3. **Active learning** where the model improves as you label

## 📋 Prerequisites

✅ You already have:

- Label Studio installed and configured
- 102 images with metadata
- Custom labeling interface (`label_studio_config.xml`)

## 🔧 Setup Options

### Option 1: Segment Anything Model (SAM) - Recommended for Object Detection

SAM is excellent for detecting and segmenting feathers in images without training.

#### Install ML Backend

```bash
# 1. Install the Label Studio ML backend
pip install label-studio-ml

# 2. Install SAM backend
git clone https://github.com/HumanSignal/label-studio-ml-backend.git
cd label-studio-ml-backend/label_studio_ml/examples/segment_anything_model

# 3. Install dependencies
pip install -r requirements.txt
pip install segment-anything
```

#### Download SAM Model

```bash
# Create models directory
mkdir -p models

# Download a SAM checkpoint (choose one):
# - ViT-H (largest, most accurate, ~2.5GB)
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -P models/

# - ViT-L (medium, ~1.2GB)
# wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth -P models/

# - ViT-B (smallest, fastest, ~375MB)
# wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -P models/
```

#### Start SAM ML Backend

```bash
# Start the ML backend server
label-studio-ml start label_studio_ml/examples/segment_anything_model \
  --with model_path=models/sam_vit_h_4b8939.pth \
  --port 9090
```

### Option 2: YOLO (if you have a pre-trained model)

If you already have a trained YOLO model for feather detection:

#### Install YOLO Backend

```bash
cd label-studio-ml-backend/label_studio_ml/examples/yolo
pip install -r requirements.txt
```

#### Configure YOLO Backend

Create `config.json`:

```json
{
  "model_path": "/path/to/your/yolo/model.pt",
  "confidence_threshold": 0.25,
  "label_map": {
    "0": "Plume"
  }
}
```

#### Start YOLO Backend

```bash
label-studio-ml start . --port 9090
```

### Option 3: GroundingDINO - Text-Prompted Object Detection

GroundingDINO can detect objects based on text descriptions (e.g., "feather").

#### Install GroundingDINO

```bash
cd label-studio-ml-backend/label_studio_ml/examples/grounding_dino
pip install -r requirements.txt
```

#### Start GroundingDINO Backend

```bash
label-studio-ml start . --port 9090
```

## 🔗 Connect ML Backend to Label Studio

### 1. In Label Studio UI

1. Open your project: "Feather Classification YOLO"
2. Go to **Settings** → **Model**
3. Click **Add Model**
4. Configure:

   - **Name**: `SAM Feather Detector` (or your model name)
   - **Backend URL**: `http://localhost:9090`
   - **Enable**: Check "Use for interactive preannotations"
   - **Enable**: Check "Start model training on annotation submit"

5. Click **Validate and Save**

### 2. Verify Connection

You should see:

- ✅ "Connected" status
- Model version information

## 🚀 Using Semi-Automated Labeling

### Pre-labeling Workflow

#### 1. Batch Pre-labeling

To generate predictions for all unlabeled tasks:

1. Go to your project dashboard
2. Select tasks you want to pre-label (or select all)
3. Click **Actions** → **Retrieve predictions**
4. The ML backend will process images and generate bounding boxes

#### 2. Interactive Labeling

When labeling individual images:

1. Open a task
2. ML model predictions appear automatically as suggested bounding boxes
3. Review and adjust:

   - ✅ **Accept**: Click the prediction to accept it
   - ✏️ **Edit**: Drag corners to adjust
   - ❌ **Delete**: Select and press Delete
   - ➕ **Add**: Draw new boxes for missed feathers

4. Add attributes (colors, size, motif) to each box
5. Submit

### Model Training (Optional)

If you want the model to learn from your corrections:

1. Enable "Start model training on annotation submit" in Model settings
2. As you label, the model will retrain automatically
3. Predictions improve over time based on your corrections

## 📊 Expected Performance

### SAM (Segment Anything)

- **Pros**:
  - No training needed
  - Excellent at finding object boundaries
  - Works well with varied feather shapes
- **Cons**:
  - May over-segment (find too many regions)
  - Needs manual selection of which segments are feathers

### YOLO (if pre-trained)

- **Pros**:
  - Fast predictions
  - Specific to your use case if trained
- **Cons**:
  - Needs training data first
  - Less flexible than SAM

### GroundingDINO

- **Pros**:
  - Text-prompted ("find feathers")
  - No specific training needed
- **Cons**:
  - May need fine-tuning for best results

## 🛠️ Custom ML Backend (Advanced)

If you want to create your own model:

### 1. Create Custom Backend Structure

```bash
mkdir custom_feather_detector
cd custom_feather_detector
```

### 2. Create `model.py`

```python
from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.utils import get_image_size, get_single_tag_keys
import torch
from ultralytics import YOLO

class FeatherDetector(LabelStudioMLBase):
    def __init__(self, **kwargs):
        super(FeatherDetector, self).__init__(**kwargs)

        # Load your model
        self.model = YOLO('path/to/your/model.pt')

        # Get label configuration
        self.from_name, self.to_name, self.value = get_single_tag_keys(
            self.parsed_label_config, 'RectangleLabels', 'Image'
        )

    def predict(self, tasks, **kwargs):
        predictions = []

        for task in tasks:
            # Get image
            image_url = task['data'][self.value]
            image_path = self.get_local_path(image_url)

            # Run inference
            results = self.model.predict(image_path, conf=0.25)

            # Convert to Label Studio format
            result = []
            for box in results[0].boxes:
                x, y, x2, y2 = box.xyxy[0].tolist()
                conf = box.conf[0].item()

                # Convert to percentages
                img_width, img_height = get_image_size(image_path)

                result.append({
                    'from_name': self.from_name,
                    'to_name': self.to_name,
                    'type': 'rectanglelabels',
                    'value': {
                        'rectanglelabels': ['Plume'],
                        'x': x / img_width * 100,
                        'y': y / img_height * 100,
                        'width': (x2 - x) / img_width * 100,
                        'height': (y2 - y) / img_height * 100
                    },
                    'score': conf
                })

            predictions.append({
                'result': result,
                'score': sum(r['score'] for r in result) / len(result) if result else 0,
                'model_version': 'custom-feather-v1'
            })

        return predictions

    def fit(self, annotations, **kwargs):
        # Optional: implement training
        pass
```

### 3. Create `requirements.txt`

```txt
label-studio-ml>=1.0.9
ultralytics
torch
torchvision
Pillow
```

### 4. Start Custom Backend

```bash
label-studio-ml start . --port 9090
```

## 🔄 Complete Workflow

```
1. Start Label Studio
   └─> ./start_label_studio.sh

2. Start ML Backend (separate terminal)
   └─> label-studio-ml start [backend] --port 9090

3. Connect Backend to Project
   └─> Settings → Model → Add Model

4. Pre-label Batch
   └─> Select Tasks → Actions → Retrieve Predictions

5. Review & Correct
   └─> Open task → Adjust boxes → Add attributes → Submit

6. Export for YOLO
   └─> Export → YOLO format
```

## 💡 Best Practices

### 1. Start Small

- Pre-label 10-20 images first
- Review quality before batch processing all 102

### 2. Set Confidence Thresholds

- Start with low threshold (0.15) to catch all feathers
- Better to have false positives than miss feathers

### 3. Active Learning

- Label diverse examples first (different species, colors)
- Model learns patterns faster with varied training data

### 4. Quality Control

- Review predictions before accepting
- Ensure bounding boxes are tight around feathers
- Double-check attribute labels

### 5. Batch Operations

- Use filters to select unlabeled tasks
- Pre-label in batches of 20-30
- Submit all corrections before starting new batch

## 🐛 Troubleshooting

### ML Backend Won't Connect

```bash
# Check backend is running
curl http://localhost:9090/health

# Check Label Studio can reach it
# Make sure both are on same network/localhost
```

### Out of Memory Errors

```bash
# For SAM, use smaller model (ViT-B instead of ViT-H)
# Or process fewer images at once
```

### Predictions Not Appearing

1. Check Model settings - ensure "Use for predictions" is enabled
2. Verify backend URL is correct
3. Check backend logs for errors

### Poor Quality Predictions

1. Adjust confidence threshold
2. Try different model (SAM vs YOLO vs GroundingDINO)
3. Provide more training examples

## 📚 Resources

- [Label Studio ML Backend Docs](https://labelstud.io/guide/ml.html)
- [SAM GitHub](https://github.com/facebookresearch/segment-anything)
- [GroundingDINO](https://github.com/IDEA-Research/GroundingDINO)
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)

## ⏭️ Next Steps

After semi-automated labeling:

1. Export labeled data in YOLO format
2. Train your own YOLO model on labeled data
3. Use trained model as ML backend for even better predictions
4. Iterate: label more → train → improve → repeat
