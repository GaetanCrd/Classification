#!/usr/bin/env python3
"""
Analyze remaining Google Drive URLs and find local files with fuzzy matching.
"""

import json
import os
import re
from difflib import get_close_matches

def normalize_name(name):
    """Normalize name for comparison."""
    return name.lower().replace('_', '').replace(' ', '').replace('-', '').replace("'", '')

def get_all_image_files():
    """Get all image files in the images directory."""
    image_files = []
    images_dir = 'images'
    
    for species_dir in os.listdir(images_dir):
        dir_path = os.path.join(images_dir, species_dir)
        if os.path.isdir(dir_path):
            for filename in os.listdir(dir_path):
                if filename.endswith('.jpg') or filename.endswith('.jpeg'):
                    rel_path = f"{images_dir}/{species_dir}/{filename}"
                    image_files.append(rel_path)
    
    return image_files

def extract_species_name(full_name):
    """Extract species scientific name."""
    match = re.match(r'^([A-Za-z]+\s+[a-z]+)', full_name)
    if match:
        scientific = match.group(1).strip()
        return scientific.replace(' ', '_')
    return None

def category_to_keywords(category):
    """Get possible keywords for a category."""
    if not category:
        return []
    
    category = category.strip().upper()
    
    if category.startswith('P'):
        return ['primaire', 'primary']
    elif category.startswith('S'):
        return ['secondaire', 'secondary']
    elif category.startswith('R'):
        return ['rectrice', 'rectrices']
    
    return []

def find_best_match(species_full, category, all_files):
    """Find the best matching file for a species and category."""
    species_sci = extract_species_name(species_full)
    if not species_sci:
        return None
    
    category_keywords = category_to_keywords(category)
    
    # Try to find files that match the species
    candidates = []
    species_normalized = normalize_name(species_sci)
    
    for filepath in all_files:
        filename = os.path.basename(filepath)
        filename_normalized = normalize_name(filename)
        
        # Check if species name is in the filename (fuzzy)
        if species_normalized in filename_normalized or \
           any(normalize_name(species_sci.split('_')[i]) in filename_normalized 
               for i in range(len(species_sci.split('_')))):
            
            # Check if category matches
            for keyword in category_keywords:
                if keyword in filename_normalized:
                    candidates.append(filepath)
                    break
    
    if candidates:
        return candidates[0]
    
    return None

def main():
    # Load the JSON file
    with open('base-data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    values = data.get('values', [])
    
    # Find the "Apercu" column
    header_row = values[1]
    apercu_col_index = None
    for i, header in enumerate(header_row):
        if header and header.lower().strip() == 'apercu':
            apercu_col_index = i
            break
    
    print(f"Loading all local image files...")
    all_files = get_all_image_files()
    print(f"Found {len(all_files)} local image files\n")
    
    print("Analyzing remaining Google Drive URLs:\n")
    
    unconverted = []
    for row_idx in range(2, len(values)):
        row = values[row_idx]
        
        if len(row) <= apercu_col_index:
            continue
        
        current_url = row[apercu_col_index]
        
        if not current_url or 'drive.google.com' not in str(current_url):
            continue
        
        species_full = row[0] if len(row) > 0 else None
        category = row[3] if len(row) > 3 else None
        
        if species_full and category:
            unconverted.append({
                'row': row_idx,
                'species': species_full,
                'category': category,
                'url': current_url
            })
    
    print(f"Found {len(unconverted)} unconverted URLs\n")
    print("="*80)
    
    # Group by species
    species_groups = {}
    for item in unconverted:
        species = item['species']
        if species not in species_groups:
            species_groups[species] = []
        species_groups[species].append(item)
    
    for species, items in sorted(species_groups.items()):
        print(f"\n{species}")
        print(f"  Categories: {', '.join(item['category'] for item in items)}")
        
        # Try to find matching files
        species_sci = extract_species_name(species)
        if species_sci:
            species_normalized = normalize_name(species_sci)
            matching_files = [f for f in all_files if species_normalized in normalize_name(f)]
            
            if matching_files:
                print(f"  Potential matches found:")
                for f in matching_files:
                    print(f"    - {f}")
            else:
                print(f"  No matching files found in images/")
        print("-"*80)

if __name__ == '__main__':
    main()
