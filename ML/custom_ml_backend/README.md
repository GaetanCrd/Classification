# Custom ML Backend with Metadata Pre-filling

This custom backend combines:

1. **SAM (Segment Anything Model)** for automatic feather detection
2. **Metadata-based attribute pre-filling** for colors, size, and motif

## Features

- ✅ Automatically detects feathers in images using SAM
- ✅ Pre-fills bounding box attributes from your existing metadata
- ✅ Colors, size, and motif are automatically set based on species data
- ✅ User can still edit/override any attribute

## Installation

```bash
cd custom_ml_backend

# Install dependencies
pip install -r requirements.txt

# Download SAM model (if not already downloaded)
mkdir -p models

# Choose one model (macOS compatible - uses curl):
# ViT-B (smallest, fastest, 375MB)
curl -L https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -o models/sam_vit_b_01ec64.pth

# OR ViT-L (medium, 1.2GB)
# curl -L https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth -o models/sam_vit_l_0b3195.pth

# OR ViT-H (largest, most accurate, 2.5GB)
# curl -L https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -o models/sam_vit_h_4b8939.pth
```

## Usage

### Start the backend

```bash
label-studio-ml start . \
  --with model_path=models/sam_vit_h_4b8939.pth \
  --port 9090
```

### Connect to Label Studio

1. In Label Studio: Settings → Model
2. Add Model:
   - URL: `http://localhost:9090`
   - Name: "SAM with Metadata"
3. Enable "Use for interactive preannotations"

### How it works

When you retrieve predictions:

1. **SAM detects feathers** → Creates bounding boxes
2. **Metadata is read** from `task.meta.couleurs`, `task.meta.tailles`, etc.
3. **Attributes are pre-filled** on each bounding box:
   - Colors: All colors from metadata
   - Taille: First size from metadata
   - Motif: First motif from metadata
4. **User reviews** and can modify any attribute

## Example

For an image with metadata:

```json
{
  "meta": {
    "couleurs": ["Noir", "Blanc", "Marron"],
    "tailles": ["[10-20 cm["],
    "motifs": ["Rayé"]
  }
}
```

Each detected feather will have:

- ✅ Bounding box (from SAM)
- ✅ Colors: Noir, Blanc, Marron (pre-selected)
- ✅ Taille: [10-20 cm[ (pre-selected)
- ✅ Motif: Rayé (pre-selected)

**You just need to verify and adjust if needed!**

## Model Selection

Choose SAM model based on your needs:

| Model | Size  | Speed   | Accuracy |
| ----- | ----- | ------- | -------- |
| ViT-B | 375MB | Fastest | Good     |
| ViT-L | 1.2GB | Medium  | Better   |
| ViT-H | 2.5GB | Slower  | Best     |

Update `model_path` parameter when starting.

## Troubleshooting

### Attributes not showing?

Check that:

1. `prepare_label_studio.py` was run with updated version
2. Import file has `meta.couleurs`, `meta.tailles`, `meta.motifs`
3. Backend logs show "Using defaults: {...}"

### Too many/few detections?

Adjust parameters in `model.py`:

```python
self.mask_generator = self.SamAutomaticMaskGenerator(
    model=sam,
    points_per_side=32,  # Increase for more detections
    pred_iou_thresh=0.86,  # Lower for more detections
    min_mask_region_area=100,  # Lower to detect smaller objects
)
```
