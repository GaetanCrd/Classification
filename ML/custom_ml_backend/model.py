"""
Custom Label Studio ML Backend that integrates SAM with metadata-based attribute pre-filling.

This backend:
1. Uses Segment Anything Model (SAM) to detect objects/feathers
2. Pre-fills attributes (colors, size, motif) from task metadata
3. Returns predictions with both bounding boxes AND attributes
"""

from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.utils import get_image_size, get_single_tag_keys, get_local_path
import os
import numpy as np
import time
from typing import List, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SAMWithMetadata(LabelStudioMLBase):
    """ML Backend that combines SAM detection with metadata-based attribute filling"""
    
    def __init__(self, **kwargs):
        super(SAMWithMetadata, self).__init__(**kwargs)
        
        # Import SAM dependencies
        try:
            from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
            from PIL import Image
            import torch
            
            self.Image = Image
            self.torch = torch
            self.sam_model_registry = sam_model_registry
            self.SamAutomaticMaskGenerator = SamAutomaticMaskGenerator
        except ImportError as e:
            logger.error(f"Failed to import SAM dependencies: {e}")
            raise
        
        # Load SAM model
        model_path = kwargs.get('model_path', 'models/sam_vit_b_01ec64.pth')
        
        # Handle relative paths - make them relative to this file's directory
        if not os.path.isabs(model_path):
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(backend_dir, model_path)
        
        if not os.path.exists(model_path):
            error_msg = f"Model file not found: {model_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        model_type = self._get_model_type(model_path)
        
        logger.info(f"Loading SAM model: {model_type} from {model_path}")
        
        device = "cuda" if self.torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        
        try:
            sam = self.sam_model_registry[model_type](checkpoint=model_path)
            sam.to(device=device)
        except Exception as e:
            logger.error(f"Failed to load SAM model: {e}")
            raise
        
        # Create mask generator optimized for feathers (not grid patterns)
        self.mask_generator = self.SamAutomaticMaskGenerator(
            model=sam,
            points_per_side=100,  # Reduced - fewer sample points to avoid grid detection
            pred_iou_thresh=0.60,  # Very high - only extremely confident detections
            stability_score_thresh=0.90,  # Very stable masks only
            crop_n_layers=0,  # Disable crop layers to reduce small region detection
            crop_n_points_downscale_factor=1,
            min_mask_region_area=500,  # Much larger - feathers are substantial objects, grid squares are small
            # box_nms_thresh=0.7,  # Remove overlapping boxes
        )
        
        # Get label configuration - extract only RectangleLabels
        try:
            # Filter for only RectangleLabels tags
            rectangle_configs = {k: v for k, v in self.parsed_label_config.items() 
                                if v.get('type') == 'RectangleLabels'}
            
            if len(rectangle_configs) == 1:
                config_name, config = list(rectangle_configs.items())[0]
                self.from_name = config_name
                self.to_name = config['to_name'][0]
                self.value = config['inputs'][0]['value']
                logger.info(f"Label config parsed: from_name={self.from_name}, to_name={self.to_name}, value={self.value}")
            else:
                raise ValueError(f"Expected 1 RectangleLabels config, found {len(rectangle_configs)}")
        except Exception as e:
            logger.warning(f"Could not parse label config automatically: {e}")
            # Fallback defaults
            self.from_name = 'feathers'
            self.to_name = 'image'
            self.value = 'image'
            logger.info(f"Using fallback defaults: from_name={self.from_name}, to_name={self.to_name}, value={self.value}")
    
    def _get_model_type(self, model_path: str) -> str:
        """Determine SAM model type from filename"""
        if 'vit_h' in model_path:
            return 'vit_h'
        elif 'vit_l' in model_path:
            return 'vit_l'
        elif 'vit_b' in model_path:
            return 'vit_b'
        else:
            logger.warning(f"Unknown model type in path: {model_path}, defaulting to vit_h")
            return 'vit_h'
    
    def _mask_to_bbox(self, mask: np.ndarray) -> tuple:
        """Convert binary mask to bounding box coordinates"""
        pos = np.where(mask)
        if len(pos[0]) == 0:
            return None
        
        y_min, y_max = pos[0].min(), pos[0].max()
        x_min, x_max = pos[1].min(), pos[1].max()
        
        return (x_min, y_min, x_max, y_max)
    
    def _extract_metadata_defaults(self, task: Dict) -> Dict[str, Any]:
        """Extract default attribute values from task metadata"""
        defaults = {
            'colors': [],
            'taille': None,
            'motif': None
        }
        
        # Check in task.meta
        if 'meta' in task:
            meta = task['meta']
            defaults['colors'] = meta.get('couleurs', [])
            tailles = meta.get('tailles', [])
            defaults['taille'] = tailles[0] if tailles else None
            motifs = meta.get('motifs', [])
            defaults['motif'] = motifs[0] if motifs else None
        
        # Also check in task.data
        if 'data' in task:
            data = task['data']
            if not defaults['colors']:
                defaults['colors'] = data.get('default_colors', [])
            if not defaults['taille']:
                defaults['taille'] = data.get('default_taille')
            if not defaults['motif']:
                defaults['motif'] = data.get('default_motif')
        
        return defaults
    
    def predict(self, tasks: List[Dict], **kwargs) -> List[Dict]:
        """Generate predictions with SAM + metadata defaults"""
        predictions = []
        
        for task in tasks:
            try:
                # Get image
                image_url = task['data'].get(self.value, task['data'].get('image'))
                
                # Handle local-files:// URLs directly
                if '/data/local-files/' in image_url:
                    # Extract path from local-files URL: /data/local-files/?d=images/...
                    # Parse the path after ?d=
                    import urllib.parse
                    parsed = urllib.parse.urlparse(image_url)
                    params = urllib.parse.parse_qs(parsed.query)
                    relative_path = params.get('d', [''])[0]
                    
                    # Construct full path - assume images are in parent directory
                    backend_dir = os.path.dirname(os.path.abspath(__file__))
                    project_root = os.path.dirname(backend_dir)
                    image_path = os.path.join(project_root, relative_path)
                    logger.info(f"Resolved local file: {image_url} -> {image_path}")
                else:
                    # Try using get_local_path for other URLs
                    project_dir = '/data'
                    if kwargs:
                        project_dir = kwargs.get('project_dir', 
                                               kwargs.get('context', {}).get('project_dir', '/data') if kwargs.get('context') else '/data')
                    
                    image_path = get_local_path(
                        image_url,
                        project_dir=project_dir,
                        hostname=kwargs.get('hostname', 'localhost') if kwargs else 'localhost',
                        access_token=kwargs.get('access_token') if kwargs else None
                    )
                
                if not os.path.exists(image_path):
                    logger.warning(f"Image not found: {image_path}")
                    predictions.append({'result': [], 'score': 0})
                    continue
                
                # Load image
                image = self.Image.open(image_path)
                image_np = np.array(image.convert('RGB'))
                img_height, img_width = image_np.shape[:2]
                
                # Get metadata defaults
                defaults = self._extract_metadata_defaults(task)
                logger.info(f"Using defaults: {defaults}")
                
                # Generate masks with SAM
                logger.info(f"Generating masks for {image_path}")
                masks = self.mask_generator.generate(image_np)
                logger.info(f"Generated {len(masks)} masks")
                
                # Convert masks to Label Studio format
                result = []
                
                # Filter masks by quality AND shape (to exclude grid squares)
                high_quality_masks = []
                for m in masks:
                    # Must have high IoU
                    if m.get('predicted_iou', 0) < 0.93:
                        continue
                    
                    # Get bbox to check aspect ratio
                    bbox_check = self._mask_to_bbox(m['segmentation'])
                    if bbox_check is None:
                        continue
                    
                    x_min_c, y_min_c, x_max_c, y_max_c = bbox_check
                    bbox_width = x_max_c - x_min_c
                    bbox_height = y_max_c - y_min_c
                    
                    # Calculate aspect ratio
                    if bbox_height == 0:
                        continue
                    aspect_ratio = bbox_width / bbox_height
                    
                    # Feathers are elongated (tall), not square
                    # Aspect ratio should be between 0.15 and 0.6 (much taller than wide)
                    # Grid squares have aspect ratio ~1.0
                    if 0.15 < aspect_ratio < 0.6:
                        high_quality_masks.append(m)
                
                logger.info(f"Filtered to {len(high_quality_masks)} feather-shaped masks (IoU >= 0.93, aspect ratio 0.15-0.6)")
                
                for i, mask_data in enumerate(high_quality_masks):
                    # Get bounding box from segmentation mask
                    bbox = self._mask_to_bbox(mask_data['segmentation'])
                    if bbox is None:
                        continue
                    
                    x_min, y_min, x_max, y_max = bbox
                    
                    # Convert to Label Studio percentages
                    x = (x_min / img_width) * 100
                    y = (y_min / img_height) * 100
                    width = ((x_max - x_min) / img_width) * 100
                    height = ((y_max - y_min) / img_height) * 100
                    
                    # Generate a unique ID for this region
                    region_id = f"region_{i}_{int(time.time() * 1000)}"
                    
                    # Create region (bounding box)
                    region = {
                        'id': region_id,
                        'from_name': self.from_name,
                        'to_name': self.to_name,
                        'type': 'rectanglelabels',
                        'value': {
                            'rectanglelabels': ['Plume'],
                            'x': float(x),
                            'y': float(y),
                            'width': float(width),
                            'height': float(height)
                        },
                        'score': float(mask_data.get('predicted_iou', 0.0)),
                        'readonly': False
                    }
                    
                    result.append(region)
                    
                    # Add per-region attributes linked to this specific region
                    # Colors (multi-select) - use default_colors from task data
                    if defaults['colors']:
                        result.append({
                            'id': f"{region_id}_colors",
                            'from_name': 'colors',
                            'to_name': self.to_name,
                            'type': 'choices',
                            'value': {
                                'choices': defaults['colors']
                            },
                            'readonly': False,
                            'origin': 'manual',
                            'parent_id': region_id  # Link to the region
                        })
                    
                    # Size - use default_taille from task data
                    if defaults['taille']:
                        result.append({
                            'id': f"{region_id}_taille",
                            'from_name': 'taille',
                            'to_name': self.to_name,
                            'type': 'choices',
                            'value': {
                                'choices': [defaults['taille']]
                            },
                            'readonly': False,
                            'origin': 'manual',
                            'parent_id': region_id  # Link to the region
                        })
                    
                    # Motif - use default_motif from task data
                    if defaults['motif']:
                        result.append({
                            'id': f"{region_id}_motif",
                            'from_name': 'motif',
                            'to_name': self.to_name,
                            'type': 'choices',
                            'value': {
                                'choices': [defaults['motif']]
                            },
                            'readonly': False,
                            'origin': 'manual',
                            'parent_id': region_id  # Link to the region
                        })
                
                # Calculate average confidence
                avg_score = sum(r.get('score', 0) for r in result if 'score' in r) / len(result) if result else 0
                
                predictions.append({
                    'result': result,
                    'score': float(avg_score),
                    'model_version': 'SAM-with-metadata-v1',
                    'meta': {
                        'num_detections': len([r for r in result if r.get('type') == 'rectanglelabels']),
                        'defaults_applied': defaults
                    }
                })
                
            except Exception as e:
                logger.error(f"Error processing task: {e}", exc_info=True)
                predictions.append({
                    'result': [],
                    'score': 0,
                    'error': str(e)
                })
        
        return predictions
    
    def fit(self, annotations, **kwargs):
        """
        Optional: Implement fine-tuning here if needed.
        For now, SAM is used as-is without training.
        """
        logger.info("Fit called - SAM is used without training")
        return {'status': 'SAM does not require training'}


# Export as NewModel for label-studio-ml compatibility
NewModel = SAMWithMetadata
