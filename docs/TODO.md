# YOLO Training Project TODO

## Phase 1: Data Labeling

### Option A: Use Label Studio ✅ SETUP COMPLETE

- [x] Install Label Studio
- [x] Create import file with pre-filled metadata (102 images)
- [x] Configure labeling template (colors, size, motif)
- [ ] **Setup ML Backend for Semi-Automated Labeling** (RECOMMENDED)
  - [ ] Run `./setup_ml_backend.sh` to install SAM or GroundingDINO
  - [ ] Start ML backend: `./start_ml_backend.sh` (separate terminal)
  - [ ] Connect backend to Label Studio project
  - [ ] Pre-label batch of images automatically
  - See `docs/ML_BACKEND_SETUP.md` for detailed guide
- [ ] Start Label Studio: `./start_label_studio.sh`
- [ ] Create project and configure (see `docs/LABEL_STUDIO_GUIDE.md`)
- [ ] Label all images (review pre-labels + draw additional boxes + add attributes)
- [ ] Export to YOLO format

### Option B: Build custom tool

- [ ] Build labeling tool for multi-object images (6-10 items per image)
  - [ ] Integrate existing partial labels (color, size, motif)
  - [ ] Support 8 colors classification
  - [ ] Support 4 size categories (< 10cm, 10-20cm, 20-35cm, 35-60cm)
  - [ ] Support 7 motif types
  - [ ] Add bounding box drawing functionality
  - [ ] Export to YOLO format (txt annotations)
- [ ] Create efficient labeling workflow
  - [ ] Pre-fill known attributes per image
  - [ ] Batch processing interface
  - [ ] Keyboard shortcuts for speed
- [ ] Label complete dataset

## Phase 2: Training on M2 MacBook

- [ ] Setup YOLO training environment
  - [ ] Install PyTorch with MPS (Metal Performance Shaders) support
  - [ ] Configure for Mac M2 (no dedicated GPU)
  - [ ] Optimize batch size for memory constraints
- [ ] Prepare dataset
  - [ ] Split train/val/test sets
  - [ ] Create data.yaml configuration
- [ ] Train model
  - [ ] Start with YOLOv8-nano for speed
  - [ ] Monitor training metrics
  - [ ] Evaluate performance

## Phase 3: Web Deployment (Client-side)

- [ ] Research WebAssembly YOLO implementations
  - [ ] Check ONNX Runtime Web
  - [ ] Explore TensorFlow.js alternatives
- [ ] Convert trained model
  - [ ] Export to ONNX format
  - [ ] Optimize for web (quantization)
- [ ] Build web inference
  - [ ] Integrate WebAssembly runtime
  - [ ] Create browser-based detection UI
  - [ ] Test performance on client devices

## Resources

- Existing data: `base-data.json` (partial labels)
- Current UI: `index.html`
