"""
Prepare data for Label Studio with pre-filled attributes from base-data.json
"""
import json
import os
from pathlib import Path
from urllib.parse import quote

# Configuration
BASE_DATA_FILE = "base-data.json"
IMAGES_DIR = "images"
OUTPUT_FILE = "label_studio_import.json"

# Column indices from your data
COL_ESPECE = 0
COL_AGE = 1
COL_SEXE = 2
COL_CATEGORIE = 3
COL_TAILLE = 4
COL_NOIR = 5
COL_BLANC = 6
COL_MARRON = 7
COL_GRIS = 8
COL_BLEU = 9
COL_JAUNE = 10
COL_VERT = 11
COL_VIOLET = 12
COL_MOTIF = 13
COL_APERCU = 14

def load_base_data():
    """Load existing data from JSON"""
    with open(BASE_DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Skip header rows (first 2 rows)
    return data['values'][2:]

def extract_colors(row):
    """Extract selected colors from row"""
    colors = []
    color_cols = [
        (COL_NOIR, "Noir"),
        (COL_BLANC, "Blanc"),
        (COL_MARRON, "Marron"),
        (COL_GRIS, "Gris"),
        (COL_BLEU, "Bleu"),
        (COL_JAUNE, "Jaune"),
        (COL_VERT, "Vert"),
        (COL_VIOLET, "Violet")
    ]
    
    for col_idx, color_name in color_cols:
        if row[col_idx] == 'X':
            colors.append(color_name)
    
    return colors

def find_image_for_row(row):
    """Find local image file matching the row data"""
    espece = row[COL_ESPECE]
    if not espece:
        return None
    
    # Normalize species name to match renamed directories (spaces replaced with underscores)
    normalized_espece = espece.replace(' ', '_')
    
    # Try to find matching directory
    images_path = Path(IMAGES_DIR)
    if not images_path.exists():
        return None
    
    # Look for species folder
    for species_dir in images_path.iterdir():
        if not species_dir.is_dir():
            continue
        
        # Check if directory name starts with the species name (before parenthesis)
        species_prefix = normalized_espece.split('(')[0].strip('_')
        if species_dir.name.startswith(species_prefix):
            # Found species folder, now find matching image
            categorie = row[COL_CATEGORIE] or ""
            
            # Map category to image type
            if categorie.startswith('P'):
                img_type = 'primaires'
            elif categorie.startswith('S'):
                img_type = 'secondaires'
            elif categorie.startswith('R'):
                img_type = 'rectrices'
            else:
                continue
            
            # Find matching image file
            for img_file in species_dir.glob('*.jpg'):
                if img_type.lower() in img_file.name.lower():
                    return str(img_file.relative_to('.'))
            
            # Also check .JPG, .jpeg, .JPEG, .png, .PNG
            for ext in ['JPG', 'jpeg', 'JPEG', 'png', 'PNG']:
                for img_file in species_dir.glob(f'*.{ext}'):
                    if img_type.lower() in img_file.name.lower():
                        return str(img_file.relative_to('.'))
    
    return None

def create_label_studio_task(row, image_path):
    """Create a Label Studio task with pre-annotations"""
    
    espece = row[COL_ESPECE] or ""
    age = row[COL_AGE] or ""
    sexe = row[COL_SEXE] or ""
    categorie = row[COL_CATEGORIE] or ""
    taille = row[COL_TAILLE] or ""
    motif = row[COL_MOTIF] or ""
    colors = extract_colors(row)
    
    # Build metadata display string
    metadata_parts = []
    if espece:
        metadata_parts.append(f"Espèce: {espece}")
    if age:
        metadata_parts.append(f"Age: {age}")
    if sexe:
        metadata_parts.append(f"Sexe: {sexe}")
    if categorie:
        metadata_parts.append(f"Catégorie: {categorie}")
    if taille:
        metadata_parts.append(f"Taille: {taille}")
    if colors:
        metadata_parts.append(f"Couleurs: {', '.join(colors)}")
    if motif:
        metadata_parts.append(f"Motif: {motif}")
    
    task = {
        "data": {
            "image": f"/data/local-files/?d={image_path}",
            "metadata": "\n".join(metadata_parts)
        },
        "predictions": [{
            "result": [],
            "model_version": "pre-filled-data"
        }],
        "meta": {
            "espece": espece,
            "age": age,
            "sexe": sexe,
            "categorie": categorie,
            "taille": taille,
            "couleurs": colors,
            "motif": motif
        }
    }
    
    return task

def main():
    print("Loading base data...")
    rows = load_base_data()
    print(f"Loaded {len(rows)} rows")
    
    tasks = []
    images_found = 0
    images_not_found = 0
    
    # Group rows by image (multiple rows can reference same image)
    image_to_rows = {}
    
    for row in rows:
        image_path = find_image_for_row(row)
        if image_path:
            if image_path not in image_to_rows:
                image_to_rows[image_path] = []
            image_to_rows[image_path].append(row)
            images_found += 1
        else:
            images_not_found += 1
    
    print(f"\nFound {len(image_to_rows)} unique images")
    print(f"Matched: {images_found} rows")
    print(f"Not matched: {images_not_found} rows")
    
    # Create tasks (one per unique image, combining metadata from all rows)
    for image_path, image_rows in image_to_rows.items():
        # Use first row for base data, but aggregate info if needed
        primary_row = image_rows[0]
        
        # Combine metadata from all rows for this image
        all_categories = set(row[COL_CATEGORIE] for row in image_rows if row[COL_CATEGORIE])
        all_tailles = set(row[COL_TAILLE] for row in image_rows if row[COL_TAILLE])
        all_motifs = set(row[COL_MOTIF] for row in image_rows if row[COL_MOTIF])
        all_colors = set()
        for row in image_rows:
            all_colors.update(extract_colors(row))
        
        # Build combined metadata
        espece = primary_row[COL_ESPECE] or ""
        age = primary_row[COL_AGE] or ""
        sexe = primary_row[COL_SEXE] or ""
        
        metadata_parts = []
        if espece:
            metadata_parts.append(f"📋 Espèce: {espece}")
        if age:
            metadata_parts.append(f"🕐 Age: {age}")
        if sexe:
            metadata_parts.append(f"⚥ Sexe: {sexe}")
        if all_categories:
            metadata_parts.append(f"🪶 Catégories: {', '.join(sorted(all_categories))}")
        if all_tailles:
            metadata_parts.append(f"📏 Tailles: {', '.join(sorted(all_tailles))}")
        if all_colors:
            metadata_parts.append(f"🎨 Couleurs: {', '.join(sorted(all_colors))}")
        if all_motifs:
            metadata_parts.append(f"✨ Motifs: {', '.join(sorted(all_motifs))}")
        
        # Create default predictions with pre-filled attributes
        # These will be the default values when user creates bounding boxes
        default_predictions = []
        
        # If we have known attributes, create a template prediction
        # This will pre-fill colors, size, and motif for new regions
        if all_colors or all_tailles or all_motifs:
            # Note: We don't create actual bounding boxes (no x,y,width,height)
            # Just store the default values in meta for reference
            # Label Studio will use these when ML backend creates boxes
            pass
        
        # Use path relative to project root for local file serving
        # LOCAL_FILES_DOCUMENT_ROOT is set to /Users/pierrebastiani/Classification
        # So we just need the relative path from there
        
        task = {
            "data": {
                "image": f"/data/local-files/?d={image_path}",
                "metadata": "\n".join(metadata_parts),
                # Add default values that can be used by the UI
                "default_colors": list(all_colors),
                "default_taille": list(all_tailles)[0] if all_tailles else None,
                "default_motif": list(all_motifs)[0] if all_motifs else None
            },
            "predictions": [{
                "result": [],  # Empty - ML backend will fill this
                "model_version": "metadata-defaults",
                # Store defaults in prediction meta
                "meta": {
                    "default_colors": list(all_colors),
                    "default_taille": list(all_tailles)[0] if all_tailles else None,
                    "default_motif": list(all_motifs)[0] if all_motifs else None
                }
            }],
            "meta": {
                "espece": espece,
                "age": age,
                "sexe": sexe,
                "categories": list(all_categories),
                "tailles": list(all_tailles),
                "couleurs": list(all_colors),
                "motifs": list(all_motifs),
                "num_rows": len(image_rows)
            }
        }
        
        tasks.append(task)
    
    # Save to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Created {len(tasks)} tasks")
    print(f"💾 Saved to: {OUTPUT_FILE}")
    print("\nNext steps:")
    print("1. Install Label Studio: pip install label-studio")
    print("2. Start Label Studio: label-studio start")
    print("3. Create a new project")
    print("4. Go to Settings > Cloud Storage > Add Source Storage > Local files")
    print(f"5. Set path to: {os.path.abspath(IMAGES_DIR)}")
    print(f"6. Import {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
