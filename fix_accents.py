#!/usr/bin/env python3
"""
Script to replace special French characters (â, é, è, ê, à) with 'a' or 'e' in directory names
and update base-data.json accordingly.
"""
import os
import json
import shutil
from pathlib import Path

def normalize_name(name):
    """Replace accented characters with plain equivalents."""
    replacements = {
        'â': 'a',
        'à': 'a',
        'é': 'e',
        'è': 'e',
        'ê': 'e',
        'î': 'i',
        'ï': 'i',
        'ô': 'o',
        'ù': 'u',
        'û': 'u',
        'ç': 'c'
    }
    
    result = name
    for accented, plain in replacements.items():
        result = result.replace(accented, plain)
    
    return result

def rename_directories():
    """Rename all directories in images/ that contain accented characters."""
    images_dir = Path('images')
    
    if not images_dir.exists():
        print("Error: images directory not found")
        return {}
    
    renamed_dirs = {}
    
    # Get all directories and sort by depth (deepest first) to avoid conflicts
    dirs = sorted([d for d in images_dir.rglob('*') if d.is_dir()], 
                  key=lambda x: len(x.parts), reverse=True)
    
    for old_path in dirs:
        old_name = old_path.name
        new_name = normalize_name(old_name)
        
        if old_name != new_name:
            new_path = old_path.parent / new_name
            
            if new_path.exists():
                print(f"Warning: {new_path} already exists, skipping {old_path}")
                continue
            
            print(f"Renaming: {old_path} -> {new_path}")
            old_path.rename(new_path)
            
            # Store the mapping with relative paths
            old_rel = str(old_path.relative_to(images_dir))
            new_rel = str(new_path.relative_to(images_dir))
            renamed_dirs[old_rel] = new_rel
    
    return renamed_dirs

def update_base_data(renamed_dirs):
    """Update base-data.json to reflect renamed directories."""
    json_file = Path('base-data.json')
    
    if not json_file.exists():
        print("Error: base-data.json not found")
        return
    
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    changes_made = 0
    
    # Update the values
    if 'values' in data:
        for row in data['values']:
            for i, cell in enumerate(row):
                if cell and isinstance(cell, str):
                    # Check if this cell contains any species name that needs updating
                    original_cell = cell
                    
                    # Replace accented characters in the cell content
                    for old_dir, new_dir in renamed_dirs.items():
                        # Extract species name from directory path
                        old_species = old_dir.split('/')[0] if '/' in old_dir else old_dir
                        new_species = new_dir.split('/')[0] if '/' in new_dir else new_dir
                        
                        if old_species in cell:
                            cell = cell.replace(old_species, new_species)
                    
                    # Also normalize any remaining accented characters
                    normalized_cell = normalize_name(cell)
                    
                    if normalized_cell != original_cell:
                        row[i] = normalized_cell
                        changes_made += 1
                        print(f"Updated: '{original_cell}' -> '{normalized_cell}'")
    
    # Write back the updated JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal changes made to base-data.json: {changes_made}")

def main():
    print("Starting directory renaming process...\n")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Rename directories
    renamed_dirs = rename_directories()
    
    if renamed_dirs:
        print(f"\nRenamed {len(renamed_dirs)} directories")
        print("\nUpdating base-data.json...\n")
        update_base_data(renamed_dirs)
    else:
        print("\nNo directories needed renaming")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
