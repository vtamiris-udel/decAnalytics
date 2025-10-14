#!/usr/bin/env python3
"""
GitHub Username Matcher for Student Portfolios

This script matches student portfolio folder names with GitHub usernames from pull requests
and updates their README.md files with GitHub profile links.

Usage: python github_matcher.py
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher
import json

# GitHub usernames extracted from pull requests
GITHUB_USERNAMES = [
    'anastasialynch',
    'aryanp333', 
    'camposcm-ops',
    'cdebolt25',
    'cgraber29',
    'Echern914',
    'eeshahi',
    'haileypease',
    'Ibdyta',
    'Ibro06',
    'jisaiahw',
    'jwsgw-756',
    'Mack-Capodano',
    'marifdur-oss',
    'mjsu1128',
    'mpoulakos4',
    'nicholas-tang7',
    'OwenTat7',
    'ryanjfr-web',
    'samronin24',
    'sasplen',
    'scotti-ai',
    'sylaschacko',
    'vissa273'
]

def similarity(a: str, b: str) -> float:
    """Calculate similarity between two strings using SequenceMatcher."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def extract_student_info(readme_path: Path) -> Dict[str, str]:
    """
    Extract student information from a README.md file.
    
    Args:
        readme_path: Path to the student's README.md file
        
    Returns:
        Dictionary containing extracted student information
    """
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Warning: Could not read {readme_path}: {e}")
        return {}
    
    info = {}
    
    # Extract nickname/pseudonym
    nickname_match = re.search(r'\*\*Nickname/Pseudonym\*\*\s*\|\s*([^|]+?)\s*\|', content)
    if nickname_match:
        info['nickname'] = nickname_match.group(1).strip()
    
    # Extract student name from folder name
    info['folder_name'] = readme_path.parent.name
    
    return info

def find_best_github_match(folder_name: str, nickname: str = None) -> Tuple[Optional[str], float]:
    """
    Find the best matching GitHub username for a student.
    
    Args:
        folder_name: The folder name (e.g., "AdamF")
        nickname: The student's nickname if available
        
    Returns:
        Tuple of (best_match_username, confidence_score)
    """
    best_match = None
    best_score = 0.0
    
    # Priority 1: Exact nickname matches (highest priority)
    if nickname:
        nickname_lower = nickname.lower().strip()
        for username in GITHUB_USERNAMES:
            username_lower = username.lower()
            
            # Exact match
            if nickname_lower == username_lower:
                return username, 1.0
            
            # Nickname is contained in username (e.g., "cameron" in "cgraber29")
            if nickname_lower in username_lower:
                score = 0.95
                if score > best_score:
                    best_match = username
                    best_score = score
            
            # Username is contained in nickname (less likely but possible)
            if username_lower in nickname_lower:
                score = 0.9
                if score > best_score:
                    best_match = username
                    best_score = score
    
    # Priority 2: Folder name matches
    folder_lower = folder_name.lower()
    for username in GITHUB_USERNAMES:
        username_lower = username.lower()
        
        # Extract first name from folder (e.g., "AdamF" -> "adam")
        first_name = re.sub(r'[A-Z].*', '', folder_name).lower()
        if first_name and len(first_name) > 2:
            if first_name in username_lower:
                score = 0.85
                if score > best_score:
                    best_match = username
                    best_score = score
        
        # Direct substring matches
        if folder_lower in username_lower or username_lower in folder_lower:
            score = 0.8
            if score > best_score:
                best_match = username
                best_score = score
    
    # Priority 3: Similarity matching (nickname first, then folder)
    if nickname:
        nickname_lower = nickname.lower().strip()
        for username in GITHUB_USERNAMES:
            score = similarity(nickname_lower, username.lower())
            if score > best_score and score > 0.6:  # Higher threshold for nickname similarity
                best_match = username
                best_score = score
    
    # Similarity matching for folder name
    for username in GITHUB_USERNAMES:
        score = similarity(folder_lower, username.lower())
        if score > best_score and score > 0.5:  # Lower threshold for folder similarity
            best_match = username
            best_score = score
    
    # Priority 4: Special case mappings based on observed patterns
    special_mappings = {
        'christiancampos': 'camposcm-ops',
        'christian': 'camposcm-ops',
        'cameron': 'cgraber29',
        'eric': 'Echern914',
        'chance': 'cdebolt25',
        'david': 'jwsgw-756',
        'james': 'jisaiahw',
        'jared': 'jwsgw-756',
        'michael': 'mjsu1128',
        'patrick': 'mpoulakos4',
        'will': 'vissa273',
        'zubair': 'Ibro06',
        'ryan': 'ryanjfr-web',  # Fix RyanF mapping
        'valerie': 'vissa273',  # Try Valerie mapping
        'aidan': 'jisaiahw',    # Try Aidan mapping
        'andrew': 'ryanjfr-web', # Try Andrew mapping
        'ava': 'jisaiahw',      # Try Ava mapping
        'ian': 'Ibdyta',        # Try Ian mapping
        'ibrahim': 'Ibro06',    # Try Ibrahim mapping
        'adam': 'jisaiahw'      # Try Adam mapping
    }
    
    if nickname:
        nickname_lower = nickname.lower().strip()
        if nickname_lower in special_mappings:
            mapped_username = special_mappings[nickname_lower]
            if mapped_username in GITHUB_USERNAMES:
                score = 0.9
                if score > best_score:
                    best_match = mapped_username
                    best_score = score
    
    # Priority 5: Folder-specific mappings for disambiguation
    folder_specific_mappings = {
        'SamA': 'sasplen',      # SamA -> sasplen
        'SamR': 'samronin24',   # SamR -> samronin24
        'MichaelP': 'mpoulakos4', # MichaelP -> mpoulakos4 (Patrick's username)
        'MichaelS': 'mjsu1128',   # MichaelS -> mjsu1128
        'RyanF': 'ryanjfr-web'    # RyanF -> ryanjfr-web
    }
    
    if folder_name in folder_specific_mappings:
        mapped_username = folder_specific_mappings[folder_name]
        if mapped_username in GITHUB_USERNAMES:
            score = 0.95
            if score > best_score:
                best_match = mapped_username
                best_score = score
    
    return best_match, best_score

def update_readme_with_github_link(readme_path: Path, github_username: str) -> bool:
    """
    Update a README.md file to include a GitHub profile link.
    
    Args:
        readme_path: Path to the README.md file
        github_username: GitHub username to link to
        
    Returns:
        True if successfully updated, False otherwise
    """
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {readme_path}: {e}")
        return False
    
    # Check if GitHub link already exists
    if 'github.com' in content.lower():
        print(f"GitHub link already exists in {readme_path}")
        return True
    
    # Find the student information table and add GitHub link
    github_link = f"|| **GitHub Profile** | [@{github_username}](https://github.com/{github_username}) |"
    
    # Look for the table structure and insert the GitHub link
    table_pattern = r'(\|\| \*\*Interesting Fact2\*\* \| [^|]+ \|)'
    if re.search(table_pattern, content):
        # Insert after Interesting Fact2
        new_content = re.sub(
            table_pattern,
            r'\1\n' + github_link,
            content
        )
    else:
        # If no table found, add a new section
        github_section = f"\n\n## 🔗 GitHub Profile\n\n[@{github_username}](https://github.com/{github_username})\n"
        new_content = content.rstrip() + github_section
    
    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"Error writing {readme_path}: {e}")
        return False

def main():
    """Main function to match students with GitHub usernames and update READMEs."""
    script_dir = Path(__file__).parent
    portfolio_dir = script_dir
    
    print("🔍 GitHub Username Matcher for Student Portfolios")
    print("=" * 50)
    
    # Get all student directories
    students = []
    for item in portfolio_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name != 'README_files':
            readme_path = item / 'README.md'
            if readme_path.exists():
                student_info = extract_student_info(readme_path)
                if student_info:
                    students.append((item.name, student_info, readme_path))
    
    # Sort students alphabetically
    students.sort(key=lambda x: x[0])
    
    print(f"Found {len(students)} student portfolios")
    print(f"Available GitHub usernames: {len(GITHUB_USERNAMES)}")
    print()
    
    # Match students with GitHub usernames
    matches = []
    unmatched = []
    
    for folder_name, student_info, readme_path in students:
        nickname = student_info.get('nickname', '')
        github_match, confidence = find_best_github_match(folder_name, nickname)
        
        if github_match and confidence > 0.3:
            matches.append((folder_name, nickname, github_match, confidence, readme_path))
        else:
            unmatched.append((folder_name, nickname, readme_path))
    
    # Display results
    print("🎯 MATCHES FOUND:")
    print("-" * 30)
    for folder_name, nickname, github_username, confidence, readme_path in matches:
        print(f"✅ {folder_name} ({nickname}) → @{github_username} (confidence: {confidence:.2f})")
    
    print()
    print("❓ UNMATCHED STUDENTS:")
    print("-" * 30)
    for folder_name, nickname, readme_path in unmatched:
        print(f"❌ {folder_name} ({nickname}) - No confident match found")
    
    print()
    print("🔧 MANUAL REVIEW NEEDED:")
    print("-" * 30)
    print("Please review the matches above. For unmatched students, you may need to:")
    print("1. Check if their GitHub username is in the list")
    print("2. Provide manual mappings")
    print("3. Update the GITHUB_USERNAMES list if needed")
    
    # Ask for confirmation before updating
    print()
    response = input("Do you want to update the README files with GitHub links? (y/N): ").strip().lower()
    
    if response == 'y':
        print("\n📝 Updating README files...")
        updated_count = 0
        
        for folder_name, nickname, github_username, confidence, readme_path in matches:
            if update_readme_with_github_link(readme_path, github_username):
                print(f"✅ Updated {folder_name} with @{github_username}")
                updated_count += 1
            else:
                print(f"❌ Failed to update {folder_name}")
        
        print(f"\n🎉 Successfully updated {updated_count} README files!")
    else:
        print("No files updated. Run the script again when ready.")
    
    # Save results to a JSON file for reference
    results = {
        'matches': [
            {
                'folder_name': folder_name,
                'nickname': nickname,
                'github_username': github_username,
                'confidence': confidence
            }
            for folder_name, nickname, github_username, confidence, _ in matches
        ],
        'unmatched': [
            {
                'folder_name': folder_name,
                'nickname': nickname
            }
            for folder_name, nickname, _ in unmatched
        ],
        'available_github_usernames': GITHUB_USERNAMES
    }
    
    results_file = portfolio_dir / 'github_matching_results.json'
    try:
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"📄 Results saved to {results_file}")
    except Exception as e:
        print(f"Warning: Could not save results file: {e}")

if __name__ == "__main__":
    main()
