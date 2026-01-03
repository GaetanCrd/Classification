# Bird Feather Classification - YOLO Training Project

A semi-automated image labeling and object detection project for classifying bird feathers using YOLO.

## 📁 Project Overview

This project helps you label and train a YOLO model to detect and classify bird feathers with multiple attributes:

- **Species:** 45+ bird species
- **Colors:** 8 color categories (multi-select)
- **Size:** 4 size ranges (<10cm to 35-60cm)
- **Patterns:** 7 motif types (striped, spotted, gradient, etc.)

**Dataset:** 102 feather images with pre-filled metadata from existing research.

## 🚀 Quick Start

### Prerequisites

- macOS (M2 MacBook)
- Python 3.8+ (virtual environment already set up in `.venv`)
- Git

### Option 1: Semi-Automated Labeling with Attribute Pre-filling (⭐ BEST!)

Use AI to pre-label images **AND** automatically fill in colors, size, and motif from your metadata:

```bash
# 1. Setup ML backend (one-time, ~10-15 min)
./setup_ml_backend.sh
# Choose option 2: "Custom SAM with Metadata"

# 2. Regenerate import file with metadata defaults
source .venv/bin/activate
python prepare_label_studio.py

# 3. Start Label Studio (terminal 1)
./start_label_studio.sh

# 4. Start ML Backend (terminal 2)
./start_ml_backend.sh
```

Then follow: **[docs/PREFILLED_ATTRIBUTES.md](docs/PREFILLED_ATTRIBUTES.md)** 🎉

**Benefits:**

- 🤖 AI detects feathers automatically
- 🎨 Colors auto-selected from metadata
- 📏 Size auto-selected from metadata
- ✨ Motif auto-selected from metadata
- ⏱️ **80% faster than manual labeling!**

### Option 2: Semi-Automated Labeling (Standard)

Use AI to pre-label images, then manually add attributes:

```bash
# 1. Setup ML backend (one-time, ~10-15 min)
./setup_ml_backend.sh
# Choose option 1: "SAM"

# 2. Start Label Studio (terminal 1)
./start_label_studio.sh

# 3. Start ML Backend (terminal 2)
./start_ml_backend.sh
```

Then follow: **[docs/QUICK_START_ML.md](docs/QUICK_START_ML.md)**

**Time saving:** ~50-60% faster than manual labeling

### Option 3: Manual Labeling

```bash
# Start Label Studio only
./start_label_studio.sh
```

Then follow: **[docs/LABEL_STUDIO_GUIDE.md](docs/LABEL_STUDIO_GUIDE.md)**

## 📚 Documentation

| Document                                                    | Description                                |
| ----------------------------------------------------------- | ------------------------------------------ |
| **[PREFILLED_ATTRIBUTES.md](docs/PREFILLED_ATTRIBUTES.md)** | 🌟 NEW! Auto-fill attributes from metadata |
| **[QUICK_START_ML.md](docs/QUICK_START_ML.md)**             | Quick start for semi-automated labeling    |
| **[ML_BACKEND_SETUP.md](docs/ML_BACKEND_SETUP.md)**         | Detailed ML backend configuration guide    |
| **[LABEL_STUDIO_GUIDE.md](docs/LABEL_STUDIO_GUIDE.md)**     | Label Studio setup and usage               |
| **[COMPARISON.md](docs/COMPARISON.md)**                     | Manual vs semi-automated comparison        |
| **[TODO.md](docs/TODO.md)**                                 | Project roadmap and tasks                  |

## 🛠️ Project Structure

```
Classification/
├── docs/                          # Documentation
│   ├── QUICK_START_ML.md         # Quick start for ML-assisted labeling
│   ├── ML_BACKEND_SETUP.md       # Detailed ML backend guide
│   ├── LABEL_STUDIO_GUIDE.md     # Label Studio manual
│   └── TODO.md                   # Project roadmap
│
├── images/                        # Bird feather images (102 images)
│   ├── Accipiter_gentilis_(Autour_des_palombes)/
│   ├── Falco_peregrinus_(Faucon_pélerin)/
│   └── ... (45+ species)
│
├── base-data.json                # Pre-filled metadata (colors, sizes, patterns)
├── label_studio_import.json      # Generated import file for Label Studio
├── label_studio_config.xml       # Labeling interface configuration
│
├── setup_ml_backend.sh           # 🚀 Setup ML backend (run first)
├── start_label_studio.sh         # Start Label Studio server
├── start_ml_backend.sh           # Start ML backend server
├── prepare_label_studio.py       # Script to generate import file
│
└── .venv/                        # Python virtual environment
```

## 🎯 Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. Setup ML Backend (one-time)                             │
│     ./setup_ml_backend.sh                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. Start Servers (two terminals)                           │
│     Terminal 1: ./start_label_studio.sh                     │
│     Terminal 2: ./start_ml_backend.sh                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. Configure in Label Studio                               │
│     - Create project                                        │
│     - Import label_studio_config.xml                        │
│     - Connect ML backend (http://localhost:9090)            │
│     - Import label_studio_import.json                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. Pre-label Images                                        │
│     - Select all tasks                                      │
│     - Actions → Retrieve Predictions                        │
│     - ML backend generates bounding boxes                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  5. Review & Correct Labels                                 │
│     - Review pre-labeled boxes                              │
│     - Adjust/delete/add boxes as needed                     │
│     - Add attributes (colors, size, motif)                  │
│     - Submit each image                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  6. Export for YOLO Training                                │
│     - Export → YOLO format                                  │
│     - Get annotated dataset                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  7. Train YOLO Model (Future)                               │
│     - Train on M2 MacBook with MPS                          │
│     - Deploy as WebAssembly for browser inference           │
└─────────────────────────────────────────────────────────────┘
```

## 🤖 ML Backend Options

### Custom SAM with Metadata - ⭐⭐⭐ RECOMMENDED

**Best for:** Maximum automation - detects feathers AND pre-fills attributes

**Pros:**

- Auto-detects feathers (SAM)
- Auto-fills colors from metadata
- Auto-fills size from metadata
- Auto-fills motif from metadata
- 80% faster than manual!

**Cons:**

- Requires metadata in import file
- Attributes are defaults (may need adjustment for individual feathers)

**Setup:** `./setup_ml_backend.sh` → Choose option 2

**Guide:** [docs/PREFILLED_ATTRIBUTES.md](docs/PREFILLED_ATTRIBUTES.md)

### Segment Anything Model (SAM) - ⭐⭐ Great

**Best for:** General object detection without training

**Pros:**

- No training needed
- Excellent at finding object boundaries
- Works well with varied feather shapes

**Cons:**

- Detects all objects (not just feathers)
- Requires manual attribute selection

**Setup:** `./setup_ml_backend.sh` → Choose option 1

### GroundingDINO - ⭐ Good

**Best for:** Text-prompted detection ("find feathers")

**Pros:**

- Natural language prompts
- More specific than SAM

**Setup:** `./setup_ml_backend.sh` → Choose option 3

### Custom YOLO (Advanced)

**Best for:** After initial labeling, train your own model

See [ML_BACKEND_SETUP.md](docs/ML_BACKEND_SETUP.md) for custom backend setup.

## 📊 Dataset Details

- **Total images:** 102
- **Species covered:** 45+
- **Images per species:** 1-4 (primaires, secondaires, rectrices)
- **Feathers per image:** 6-10 (average)
- **Total expected bounding boxes:** ~600-1000

### Pre-filled Metadata

Each image includes:

- Species name (scientific + French)
- Age (adult/juvenile) where applicable
- Sex (♂/♀) where applicable
- Feather category (P1-P10, S1-S19, R1-R6)
- Expected colors, sizes, and patterns

## 🎨 Label Classes

### Colors (multi-select)

- Noir (Black)
- Blanc (White)
- Marron (Brown)
- Gris (Gray)
- Bleu (Blue)
- Jaune (Yellow)
- Vert (Green)
- Violet (Purple)

### Size Categories

- `<10 cm`
- `[10-20 cm[`
- `[20-35 cm[`
- `[35-60 cm[`

### Motif (Pattern)

- Aucun (None)
- Rayé (Striped)
- Tâché (Spotted)
- Liseré (Bordered)
- Dégradé (Gradient)
- Irisé (Iridescent)
- Autre (Other)

## 🔧 Troubleshooting

### Label Studio won't start?

```bash
# Check if port 8080 is already in use
lsof -i :8080

# Kill the process if needed
kill -9 <PID>
```

### ML Backend not connecting?

```bash
# Verify backend is running
curl http://localhost:9090/health

# Should return: {"status": "UP"}
```

### Images not showing?

- Ensure `./start_label_studio.sh` is used (sets local file serving)
- Check that images exist in `images/` directory
- Verify import file uses correct paths

More troubleshooting: [LABEL_STUDIO_GUIDE.md](docs/LABEL_STUDIO_GUIDE.md) and [ML_BACKEND_SETUP.md](docs/ML_BACKEND_SETUP.md)

## 📈 Next Steps

After labeling (see [TODO.md](docs/TODO.md)):

1. **Export labeled data** in YOLO format
2. **Train YOLOv8 model** on M2 MacBook
3. **Optimize model** for web deployment
4. **Convert to ONNX/WebAssembly** for browser inference
5. **Build web interface** for real-time feather classification

## 🤝 Contributing

This is a research project. If you have suggestions or improvements:

1. Create feature branch
2. Make changes
3. Submit pull request

## 📝 License

Research/Educational use

## 🙏 Acknowledgments

- Label Studio for the annotation platform
- Meta AI for Segment Anything Model
- Existing feather research data in `base-data.json`

---

**Ready to start?** → Go to [docs/QUICK_START_ML.md](docs/QUICK_START_ML.md) 🚀
