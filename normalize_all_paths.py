#!/usr/bin/env python3
"""
Script to normalize ALL paths:
- Remove spaces, parentheses, accents
- Convert everything to lowercase
- Update both filesystem and base-data.json
"""
import os
import json
import unicodedata
import re
from pathlib import Path

def normalize_path(name):
    """
    Normalize a path component:
    - Remove accents using Unicode normalization
    - Remove parentheses
    - Replace spaces with underscores
    - Convert to lowercase
    """
    # Remove accents using Unicode NFD normalization
    nfd = unicodedata.normalize('NFD', name)
    without_accents = ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')
    
    # Additional replacements for special characters
    replacements = {
        'ç': 'c', 'Ç': 'C',
        'œ': 'oe', 'Œ': 'OE',
        'æ': 'ae', 'Æ': 'AE',
        'ñ': 'n', 'Ñ': 'N',
    }
    
    result = without_accents
    for accented, plain in replacements.items():
        result = result.replace(accented, plain)
    
    # Remove parentheses
    result = result.replace('(', '').replace(')', '')
    
    # Replace spaces with underscores
    result = result.replace(' ', '_')
    
    # Replace multiple underscores with single
    result = re.sub(r'_+', '_', result)
    
    # Convert to lowercase
    result = result.lower()
    
    # Remove leading/trailing underscores
    result = result.strip('_')
    
    return result

def rename_all_paths():
    """Rename all directories and files in images/ with normalized names."""
    images_dir = Path('images')
    
    if not images_dir.exists():
        print("Error: images directory not found")
        return {}
    
    renamed_map = {}  # Maps old relative path to new relative path
    
    # Get all paths (files and directories) sorted by depth (deepest first)
    all_paths = []
    for item in images_dir.rglob('*'):
        all_paths.append(item)
    
    all_paths.sort(key=lambda x: len(x.parts), reverse=True)
    
    print(f"Found {len(all_paths)} items to check\n")
    
    for old_path in all_paths:
        old_name = old_path.name
        new_name = normalize_path(old_name)
        
        if old_name != new_name:
            new_path = old_path.parent / new_name
            
            if new_path.exists() and new_path != old_path:
                print(f"Warning: {new_path} already exists, skipping {old_path}")
                continue
            
            print(f"Renaming:")
            print(f"  From: {old_path}")
            print(f"  To:   {new_path}")
            
            # Store the old relative path before renaming
            old_rel = str(old_path.relative_to(Path('.')))
            
            try:
                # Rename
                old_path.rename(new_path)
                
                # Store the new relative path after renaming
                new_rel = str(new_path.relative_to(Path('.')))
                renamed_map[old_rel] = new_rel
                
            except Exception as e:
                print(f"  Error: {e}")
    
    return renamed_map

def update_base_data(renamed_map):
    """Update base-data.json to reflect all renamed paths - ONLY update paths, not text content."""
    json_file = Path('base-data.json')
    
    if not json_file.exists():
        print("Error: base-data.json not found")
        return
    
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    changes_made = 0
    
    # Sort renamed_map by length (longest first) to handle nested paths correctly
    sorted_renames = sorted(renamed_map.items(), key=lambda x: len(x[0]), reverse=True)
    
    # Update the values
    if 'values' in data:
        for row_idx, row in enumerate(data['values']):
            for col_idx, cell in enumerate(row):
                if cell and isinstance(cell, str):
                    # ONLY update if this is an image path (starts with 'images/')
                    if cell.startswith('images/'):
                        original_cell = cell
                        updated_cell = cell
                        
                        # Replace paths based on renamed_map
                        for old_path, new_path in sorted_renames:
                            if old_path in updated_cell:
                                updated_cell = updated_cell.replace(old_path, new_path)
                        
                        if updated_cell != original_cell:
                            row[col_idx] = updated_cell
                            changes_made += 1
                            if changes_made <= 20:  # Show first 20 changes
                                print(f"Row {row_idx}, Col {col_idx}:")
                                print(f"  '{original_cell}'")
                                print(f"  -> '{updated_cell}'")
    
    # Write back the updated JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal changes made to base-data.json: {changes_made}")
    return changes_made

def main():
    print("=" * 70)
    print("NORMALIZING ALL PATHS")
    print("- Removing accents, spaces, parentheses")
    print("- Converting to lowercase")
    print("=" * 70)
    print()
    
    response = input("This will rename ALL directories and files. Continue? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("Aborted.")
        return
    
    print("\n" + "=" * 70)
    print("Step 1: Renaming directories and files")
    print("=" * 70)
    print()
    
    # Rename all paths
    renamed_map = rename_all_paths()
    
    if renamed_map:
        print(f"\n{'=' * 70}")
        print(f"Renamed {len(renamed_map)} items")
        print(f"{'=' * 70}\n")
        
        print("Step 2: Updating base-data.json")
        print("=" * 70)
        print()
        
        changes = update_base_data(renamed_map)
        
        if changes > 20:
            print(f"... and {changes - 20} more changes")
    else:
        print("\nNo items needed renaming")
        print("\nBut still checking base-data.json for normalization...\n")
        update_base_data({})
    
    print("\n" + "=" * 70)
    print("Done! All paths have been normalized.")
    print("=" * 70)

if __name__ == '__main__':
    main()
