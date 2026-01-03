#!/usr/bin/env python3
"""
Script to replace accented characters in ALL directory names (including subdirectories)
and update base-data.json accordingly. Handles Unicode normalization properly.
"""
import os
import json
import unicodedata
from pathlib import Path

def normalize_name(name):
    """Replace accented characters with plain equivalents using Unicode normalization."""
    # First normalize Unicode to decomposed form (NFD), then remove combining characters
    nfd = unicodedata.normalize('NFD', name)
    # Remove combining characters (category 'Mn' = Nonspacing_Mark)
    without_accents = ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')
    
    # Additional replacements for any precomposed characters that might remain
    replacements = {
        'ç': 'c', 'Ç': 'C',
        'œ': 'oe', 'Œ': 'OE',
        'æ': 'ae', 'Æ': 'AE',
        'ñ': 'n', 'Ñ': 'N',
    }
    
    result = without_accents
    for accented, plain in replacements.items():
        result = result.replace(accented, plain)
    
    return result

def rename_all_directories():
    """Rename all directories (including subdirectories) in images/ that contain accented characters."""
    images_dir = Path('images')
    
    if not images_dir.exists():
        print("Error: images directory not found")
        return {}
    
    renamed_map = {}  # Maps old full path to new full path
    
    # Get all directories and sort by depth (deepest first) to avoid conflicts
    all_dirs = [d for d in images_dir.rglob('*') if d.is_dir()]
    all_dirs.sort(key=lambda x: len(x.parts), reverse=True)
    
    print(f"Found {len(all_dirs)} total directories to check\n")
    
    for old_path in all_dirs:
        old_name = old_path.name
        new_name = normalize_name(old_name)
        
        if old_name != new_name:
            new_path = old_path.parent / new_name
            
            if new_path.exists():
                print(f"Warning: {new_path} already exists, skipping {old_path}")
                continue
            
            print(f"Renaming directory:")
            print(f"  From: {old_path}")
            print(f"  To:   {new_path}")
            
            # Store the old path before renaming
            old_rel = str(old_path.relative_to(images_dir))
            
            # Rename the directory
            old_path.rename(new_path)
            
            # Store the new path after renaming
            new_rel = str(new_path.relative_to(images_dir))
            renamed_map[old_rel] = new_rel
    
    return renamed_map

def update_base_data(renamed_map):
    """Update base-data.json to reflect ALL renamed directories and normalize text."""
    json_file = Path('base-data.json')
    
    if not json_file.exists():
        print("Error: base-data.json not found")
        return
    
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    changes_made = 0
    path_changes = 0
    
    # Update the values
    if 'values' in data:
        for row_idx, row in enumerate(data['values']):
            for col_idx, cell in enumerate(row):
                if cell and isinstance(cell, str):
                    original_cell = cell
                    updated_cell = cell
                    
                    # First, replace any paths that match renamed directories
                    for old_path, new_path in renamed_map.items():
                        if old_path in updated_cell:
                            updated_cell = updated_cell.replace(old_path, new_path)
                            path_changes += 1
                            print(f"Updated path in row {row_idx}, col {col_idx}:")
                            print(f"  {old_path} -> {new_path}")
                    
                    # Then normalize any remaining accented characters in the text
                    normalized_cell = normalize_name(updated_cell)
                    
                    if normalized_cell != original_cell:
                        row[col_idx] = normalized_cell
                        changes_made += 1
    
    # Write back the updated JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal changes made to base-data.json: {changes_made}")
    print(f"  - Path updates: {path_changes}")

def main():
    print("=" * 70)
    print("Starting comprehensive directory renaming process...")
    print("=" * 70)
    print()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Rename all directories (including subdirectories)
    renamed_map = rename_all_directories()
    
    if renamed_map:
        print(f"\n{'=' * 70}")
        print(f"Renamed {len(renamed_map)} directories")
        print(f"{'=' * 70}\n")
        
        print("Updating base-data.json...\n")
        update_base_data(renamed_map)
    else:
        print("\nNo directories needed renaming")
    
    print("\n" + "=" * 70)
    print("Done!")
    print("=" * 70)

if __name__ == '__main__':
    main()
