# Quick Start: Semi-Automated Labeling

## 🚀 Getting Started in 3 Steps

### Step 1: Install ML Backend (One-time setup)

```bash
./setup_ml_backend.sh
```

**Choose option 1 (SAM)** when prompted - it's the best for detecting feathers without training.

**Model size recommendation:**

- If you have good internet & disk space: Choose **ViT-H** (most accurate)
- If you want faster processing: Choose **ViT-B** (smallest, fastest)

This will:

- Install Label Studio ML backend
- Download Segment Anything Model
- Configure everything automatically

⏱️ **Time:** ~10-15 minutes (depending on model size)

---

### Step 2: Start Both Servers

You need **TWO terminals**:

**Terminal 1 - Label Studio:**

```bash
./start_label_studio.sh
```

→ Opens at http://localhost:8080

**Terminal 2 - ML Backend:**

```bash
./start_ml_backend.sh
```

→ Runs at http://localhost:9090

Keep both running!

---

### Step 3: Connect & Use in Label Studio

#### A. Connect ML Backend (First time only)

1. Open http://localhost:8080
2. Open your project: "Feather Classification YOLO"
3. Go to **Settings** (⚙️) → **Model**
4. Click **Add Model**
5. Fill in:
   - **Name:** `SAM Feather Detector`
   - **Backend URL:** `http://localhost:9090`
   - ✅ Check: "Use for interactive preannotations"
6. Click **Validate and Save**

You should see ✅ **Connected**

#### B. Pre-label Your Images

**Option 1: Batch Pre-labeling** (recommended)

1. Go to your project dashboard
2. Select **all tasks** (checkbox at top)
3. Click **Actions** → **Retrieve Predictions**
4. Wait for processing (~30 seconds for 102 images)
5. All images now have bounding box predictions! 🎉

**Option 2: Interactive Labeling**

1. Open any task
2. ML predictions appear automatically
3. Review and adjust each box
4. Add attributes (colors, size, motif)
5. Submit

---

## 📝 Labeling Workflow

For each image:

1. **Review pre-labeled boxes**

   - SAM will have detected potential feathers
   - Some may be over/under-detected

2. **Adjust bounding boxes**

   - ✅ Keep good detections
   - ✏️ Resize boxes by dragging corners
   - ❌ Delete false positives (Delete key)
   - ➕ Add missed feathers (draw new boxes)

3. **Add attributes** to each box:

   - **Colors** (multi-select): Noir, Blanc, Marron, etc.
   - **Taille**: <10cm, [10-20cm[, [20-35cm[, [35-60cm[
   - **Motif**: Aucun, Rayé, Tâché, Liseré, etc.

4. **Submit** (or press Space)

---

## 💡 Tips for Best Results

### ✨ SAM Usage Tips

- **SAM finds ALL objects** - it will detect feathers but also other objects
- **Use it as a starting point** - expect to delete some false positives
- **SAM is excellent at boundaries** - boxes will be very precise
- **Add missed feathers manually** - SAM might miss small/overlapping feathers

### ⚡ Speed Tips

- **Pre-label in batches of 20-30** - easier to manage
- **Use keyboard shortcuts:**
  - `Space` - Submit task
  - `Ctrl+Z` - Undo
  - `Delete/Backspace` - Delete selected box
  - `Ctrl+Enter` - Accept all and submit
- **Filter tasks** - Use filters to show only unlabeled/predicted tasks

### 🎯 Quality Tips

- **Tight bounding boxes** - Box should hug the feather edges
- **One feather per box** - Don't box multiple feathers together
- **Check metadata reference** - Pre-filled metadata shows expected colors/sizes
- **Consistent labeling** - Use same standards across all images

---

## 🔍 Quality Control

After pre-labeling a batch:

1. Randomly check 5-10 images
2. Verify box quality
3. Check if important feathers are missed
4. Adjust confidence threshold if needed (in ML backend settings)

---

## 📤 Export for YOLO Training

When all images are labeled:

1. Click **Export** button
2. Select **YOLO** format
3. Download the zip file

Contains:

- `classes.txt` - Your class labels
- `images/` - Your images
- `labels/` - YOLO format annotations (.txt files)
- One `.txt` per image with bounding box coordinates

---

## 🐛 Troubleshooting

### ML Backend not connecting?

```bash
# Check backend is running
curl http://localhost:9090/health

# Should return: {"status": "UP"}
```

### No predictions appearing?

1. Check Model settings - "Use for interactive preannotations" enabled?
2. Click "Retrieve Predictions" manually
3. Check ML backend terminal for errors

### Predictions are poor quality?

- SAM detects everything - this is normal
- Focus on **correcting** rather than expecting perfect results
- Delete false positives, add missed feathers
- The goal is to **speed up** labeling, not eliminate manual work

### Out of memory?

- SAM ViT-H is large (2.5GB)
- If crashing, use ViT-B instead (smaller, faster)
- Re-run `./setup_ml_backend.sh` and choose option 1 (ViT-B)

---

## 📊 Expected Time Savings

**Without ML backend:**

- ~5-8 minutes per image (6-10 feathers)
- **Total:** ~8-13 hours for 102 images

**With ML backend:**

- ~2-4 minutes per image (review + corrections)
- **Total:** ~3-6 hours for 102 images

**Time saved:** ~50-60% faster! 🎉

---

## 📚 More Information

- **Detailed setup:** See `docs/ML_BACKEND_SETUP.md`
- **Label Studio basics:** See `docs/LABEL_STUDIO_GUIDE.md`
- **Project roadmap:** See `docs/TODO.md`

---

## 🆘 Need Help?

Common issues and solutions in `docs/ML_BACKEND_SETUP.md` - Troubleshooting section
