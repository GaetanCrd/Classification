# Label Studio Setup Guide

## 🚨 Common Issues We Encountered (and How to Fix Them)

### Issue 1: XML Syntax Error with `<` character

**Error:** `Unescaped '<' not allowed in attributes values, line 41`
**Fix:** Replace `<10 cm` with `&lt;10 cm` in the XML config

### Issue 2: Local File Serving Disabled

**Error:** `Serving local files can be dangerous, so it's disabled by default`
**Fix:** Must start Label Studio with environment variables set (use `start_label_studio.sh`)

### Issue 3: Cloud Storage Path Validation

**Error:** `Path must start with LOCAL_FILES_DOCUMENT_ROOT and must be a child`
**Fix:** Skip cloud storage setup entirely - use JSON import instead!

### Issue 4: Relative Paths Don't Work

**Error:** `404 Not Found` for `/data/local-files/?d=images/...`
**Fix:** Script now uses absolute paths automatically

---

## ✅ What's Ready

- ✅ Label Studio installed
- ✅ Import file created: `label_studio_import.json` (102 images with pre-filled metadata)
- ✅ Custom labeling template: `label_studio_config.xml`

## 🚀 Quick Start

### 1. Start Label Studio

```bash
./start_label_studio.sh
```

This will open Label Studio in your browser (usually http://localhost:8080)

**Note:** This script enables local file serving which is required to view your images. Keep this terminal running!

### 2. Create Account

- First time: create a login/password (stored locally)

### 3. Create New Project

- Click "Create Project"
- Name: "Feather Classification YOLO"

### 4. Configure Labeling Interface

- Go to **Settings** > **Labeling Interface**
- Click **Code** (top right)
- Copy/paste content from `label_studio_config.xml`
- Click **Save**

### 5. Import Pre-filled Data (RECOMMENDED - Skip Cloud Storage!)

- Go back to project main page
- Click **Import** button
- Upload `label_studio_import.json`
- You should see 102 tasks imported with images showing!

**Note:** You DON'T need to setup cloud storage if using the import file. The import file already has absolute paths configured.

## 📋 How to Label

### For Each Image:

1. **Review pre-filled metadata** (shown at top with emojis)

   - Shows existing data: species, colors, size, motif
   - This is your reference - no need to Ctrl+F!

2. **Draw bounding boxes** around each feather (6-10 per image)

   - Click and drag on the image
   - Each feather = 1 box

3. **Label each box** with attributes:

   - **Colors**: Select all that apply (multiple)
   - **Taille**: Select one size category
   - **Motif**: Select one pattern

4. **Submit** when done with the image

## ⌨️ Keyboard Shortcuts

- **Space**: Submit task
- **Ctrl+Z**: Undo
- **Backspace/Delete**: Delete selected region

## 📤 Export for YOLO

When labeling is complete:

1. Go to **Export** button
2. Select **YOLO** format
3. Download the annotations

The export will include:

- `classes.txt` - list of your classes
- `.txt` files - one per image with bounding boxes
- Format: `<class_id> <x_center> <y_center> <width> <height>`

## 💡 Tips

- The metadata box shows ALL info from your existing data
- You can see multiple categories/sizes/motifs if the image has multiple feather types
- `num_rows` in metadata tells you how many entries from your Excel reference this image

## 🔧 Stopping Label Studio

```bash
# Press Ctrl+C in the terminal
# Or close the terminal window
# Data is auto-saved
```

## 📝 Notes

- 102 images found and matched with existing data
- 45 rows couldn't be matched (likely Google Drive links or missing images)
- Your work is saved automatically in Label Studio's database
