#!/usr/bin/env python3
"""
Convert all remaining Google Drive URLs to relative paths with fuzzy matching.
"""

import json
import os
import re

def normalize_for_comparison(text):
    """Normalize text for fuzzy comparison."""
    return text.lower().replace('_', '').replace(' ', '').replace('-', '').replace("'", '').replace('(', '').replace(')', '')

def get_all_image_files():
    """Get all image files mapped by normalized species name."""
    files_map = {}
    images_dir = 'images'
    
    for species_dir in os.listdir(images_dir):
        dir_path = os.path.join(images_dir, species_dir)
        if os.path.isdir(dir_path):
            # Check direct files
            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)
                if os.path.isfile(file_path) and filename.lower().endswith(('.jpg', '.jpeg')):
                    rel_path = f"{images_dir}/{species_dir}/{filename}"
                    normalized = normalize_for_comparison(rel_path)
                    files_map[normalized] = rel_path
                # Also check subdirectories (like "femelle", "male")
                elif os.path.isdir(file_path):
                    for subfile in os.listdir(file_path):
                        if subfile.lower().endswith(('.jpg', '.jpeg')):
                            rel_path = f"{images_dir}/{species_dir}/{filename}/{subfile}"
                            normalized = normalize_for_comparison(rel_path)
                            files_map[normalized] = rel_path
    
    return files_map

def extract_species_name(full_name):
    """Extract species scientific name."""
    match = re.match(r'^([A-Za-z]+\s+[a-z]+)', full_name)
    if match:
        scientific = match.group(1).strip()
        return scientific
    return None

def find_matching_file(species_full, category, files_map):
    """Find matching file using fuzzy logic."""
    species_sci = extract_species_name(species_full)
    if not species_sci:
        return None
    
    # Handle special spelling variations
    species_variants = [species_sci]
    if 'bradyryncha' in species_sci.lower():
        # Add variant with extra 'h'
        species_variants.append(species_sci.replace('bradyryncha', 'brachyrhyncha'))
        species_variants.append(species_sci.replace('Bradyryncha', 'Brachyrhyncha'))
    
    # Normalize category to keywords
    category_upper = category.strip().upper()
    category_keywords = []
    
    if category_upper.startswith('P'):
        category_keywords = ['primaire', 'primary', 'pimaire']  # including typo
    elif category_upper.startswith('S'):
        category_keywords = ['secondaire', 'secondary']
    elif category_upper.startswith('R'):
        category_keywords = ['rectrice', 'rectrices']
    
    # Try all species variants
    for species_variant in species_variants:
        species_normalized = normalize_for_comparison(species_variant)
        
        # Search through all files
        candidates = []
        for normalized_path, actual_path in files_map.items():
            # Check if species is in path
            if species_normalized in normalized_path:
                # Check if category matches
                for keyword in category_keywords:
                    if keyword in normalized_path:
                        candidates.append(actual_path)
                        break
        
        if candidates:
            # Prefer files without special suffixes like "1", "2", "bis", "FB", "FN"
            simple_files = [f for f in candidates if not re.search(r'[_\(](1|2|3|bis|fb|fn|fondnoir|male|femelle)', f.lower())]
            if simple_files:
                return simple_files[0]
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
    
    if apercu_col_index is None:
        print("Error: Could not find 'Apercu' column")
        return
    
    print(f"Found 'Apercu' column at index {apercu_col_index}")
    print("Loading all local image files...")
    
    files_map = get_all_image_files()
    print(f"Found {len(files_map)} local image files\n")
    
    # Process data rows
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
        
        # Get species name and category
        species_full = row[0] if len(row) > 0 else None
        category = row[3] if len(row) > 3 else None
        
        if not species_full or not category:
            print(f"Row {row_idx}: Missing species or category, skipping")
            skipped_count += 1
            continue
        
        # Find matching file
        matched_file = find_matching_file(species_full, category, files_map)
        
        if matched_file:
            row[apercu_col_index] = matched_file
            converted_count += 1
            print(f"✓ Row {row_idx}: {species_full} ({category}) -> {matched_file}")
        else:
            print(f"✗ Row {row_idx}: No match for {species_full} ({category})")
            skipped_count += 1
    
    # Save the updated JSON
    if converted_count > 0:
        with open('base-data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\nConversion complete!")
        print(f"Converted: {converted_count} URLs")
        print(f"Skipped: {skipped_count} rows")
        print(f"Updated file: base-data.json")
    else:
        print(f"\nNo URLs were converted.")
        print(f"Skipped: {skipped_count} rows")

if __name__ == '__main__':
    main()
