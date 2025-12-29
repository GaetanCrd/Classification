#!/usr/bin/env python3
"""
Quick test to see how many objects SAM detects with current thresholds
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_ml_backend'))

from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
from PIL import Image
import numpy as np
import torch

# Load model
model_path = 'custom_ml_backend/models/sam_vit_b_01ec64.pth'
print(f"Loading SAM model from {model_path}...")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

sam = sam_model_registry['vit_b'](checkpoint=model_path)
sam.to(device=device)

# Current settings
print("\nCurrent SAM settings:")
print("  pred_iou_thresh: 0.86")
print("  stability_score_thresh: 0.85")
print("  min_mask_region_area: 100")

mask_generator = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side=32,
    pred_iou_thresh=0.86,
    stability_score_thresh=0.85,
    crop_n_layers=1,
    crop_n_points_downscale_factor=2,
    min_mask_region_area=100,
)

# Test on first image
test_image = 'images/Accipiter_gentilis_(Autour_des_palombes)/Accipiter_gentilis_Primaires.jpg'
print(f"\nTesting on: {test_image}")

image = Image.open(test_image)
image_np = np.array(image.convert('RGB'))
print(f"Image size: {image_np.shape}")

print("\nGenerating masks...")
masks = mask_generator.generate(image_np)
print(f"✅ Generated {len(masks)} masks")

if len(masks) == 0:
    print("\n⚠️  NO MASKS DETECTED!")
    print("This means the thresholds are too strict.")
    print("\nTry lowering:")
    print("  pred_iou_thresh: 0.86 → 0.70")
    print("  stability_score_thresh: 0.85 → 0.70")
else:
    print(f"\n✅ Success! Found {len(masks)} objects")
    print("\nMask areas (top 10):")
    sorted_masks = sorted(masks, key=lambda x: x['area'], reverse=True)
    for i, mask in enumerate(sorted_masks[:10]):
        print(f"  {i+1}. Area: {mask['area']:,} pixels, IoU: {mask['predicted_iou']:.3f}, Stability: {mask['stability_score']:.3f}")
