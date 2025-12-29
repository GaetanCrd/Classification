#!/usr/bin/env python3
"""
Convert Google Drive URLs in base-data.json to relative image paths.
Uses actual directory structure to match files.
"""

import json
import re
import os
from pathlib import Path

def extract_species_name(full_name):
    """
    Extract species scientific name from full species string.
    E.g., "Accipiter gentilis (Autour des palombes)" -> "Accipiter_gentilis"
    """
    match = re.match(r'^([A-Za-z]+\s+[a-z]+)', full_name)
    if match:
        scientific = match.group(1).strip()
        return scientific.replace(' ', '_')
    return None

def category_to_filename_part(category):
    """
    Convert category abbreviation to filename part.
    """
    if not category:
        return None
    
    category = category.strip().upper()
    
    # Handle ranges like P2-P9
    if category.startswith('P'):
        return 'Primaires'
    elif category.startswith('S'):
        return 'Secondaires'
    elif category.startswith('R'):
        return 'Rectrices'
    elif 'COUV' in category:
        if 'PRIMAIRE' in category:
            return 'Couvertures_primaires'
        elif 'SECONDAIRE' in category:
            return 'Couvertures_secondaires'
        else:
            return 'Couvertures'
    elif 'TECTR' in category:
        return 'Tectrices'
    elif 'SCAPUL' in category:
        return 'Scapulaires'
    elif 'RÉMIGE' in category:
        return 'Remiges'
    
    return None

def find_matching_directory(species_scientific, images_dir):
    """
    Find the actual directory that matches the species scientific name.
    """
    for dir_name in os.listdir(images_dir):
        dir_path = os.path.join(images_dir, dir_name)
        if os.path.isdir(dir_path):
            # Check if directory starts with the scientific name
            if dir_name.startswith(species_scientific):
                return dir_name
    return None

def find_image_file(species_full, category, images_dir='images'):
    """
    Find the actual image file path based on species and category.
    """
    species_scientific = extract_species_name(species_full)
    if not species_scientific:
        return None
    
    filename_part = category_to_filename_part(category)
    if not filename_part:
        return None
    
    # Find the matching directory
    dir_name = find_matching_directory(species_scientific, images_dir)
    if not dir_name:
        return None
    
    # Build the expected filename
    filename = f"{species_scientific}_{filename_part}.jpg"
    
    # Check if file exists
    full_path = os.path.join(images_dir, dir_name, filename)
    if os.path.exists(full_path):
        return f"{images_dir}/{dir_name}/{filename}"
    
    return None

def main():
    # Load the JSON file
    with open('base-data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    values = data.get('values', [])
    
    if len(values) < 3:
        print("Error: Not enough rows in data")
        return
    
    # Find the "Apercu" column index from header row 2
    header_row = values[1]
    apercu_col_index = None
    for i, header in enumerate(header_row):
        if header and header.lower().strip() == 'apercu':
            apercu_col_index = i
            break
    
    if apercu_col_index is None:
        print("Error: Could not find 'Apercu' column")
        return
    
    print(f"Found 'Apercu' column at index {apercu_col_index}")
    
    # Process data rows (starting from row 3, index 2)
    converted_count = 0
    skipped_count = 0
    
    for row_idx in range(2, len(values)):
        row = values[row_idx]
        
        # Ensure row has enough columns
        while len(row) <= apercu_col_index:
            row.append(None)
        
        current_url = row[apercu_col_index]
        
        # Skip if not a Google Drive URL
        if not current_url or 'drive.google.com' not in str(current_url):
            continue
        
        # Get species name (column 0) and category (column 3)
        species_full = row[0] if len(row) > 0 else None
        category = row[3] if len(row) > 3 else None
        
        if not species_full or not category:
            print(f"Row {row_idx}: Missing species or category, skipping")
            skipped_count += 1
            continue
        
        # Find the actual image file
        relative_path = find_image_file(species_full, category)
        
        if relative_path:
            row[apercu_col_index] = relative_path
            converted_count += 1
            print(f"✓ Row {row_idx}: {species_full} ({category}) -> {relative_path}")
        else:
            print(f"✗ Row {row_idx}: Could not find image for {species_full} ({category})")
            skipped_count += 1
    
    # Save the updated JSON
    with open('base-data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nConversion complete!")
    print(f"Converted: {converted_count} URLs")
    print(f"Skipped: {skipped_count} rows")
    print(f"Updated file: base-data.json")

if __name__ == '__main__':
    main()
