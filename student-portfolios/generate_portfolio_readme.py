
#!/usr/bin/env python3
"""
Student Portfolio README Generator

This script automatically generates a README.md file for the student-portfolios folder
by scanning subdirectories and extracting information from each student's README.md file.

Usage: python generate_portfolio_readme.py
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional


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
    
    # Extract interesting facts
    fact1_match = re.search(r'\*\*Interesting Fact\*\*\s*\|\s*([^|]+?)\s*\|', content)
    if fact1_match:
        info['fact1'] = fact1_match.group(1).strip()
    
    fact2_match = re.search(r'\*\*Interesting Fact2\*\*\s*\|\s*([^|]+?)\s*\|', content)
    if fact2_match:
        info['fact2'] = fact2_match.group(1).strip()
    
    # Extract student name from folder name
    info['folder_name'] = readme_path.parent.name
    
    # Extract image information
    images = []
    # Look for markdown image syntax: ![alt text](filename)
    image_matches = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
    
    for alt_text, filename in image_matches:
        # Handle both local files and external URLs
        if filename.startswith('http'):
            # External URL - include as is
            images.append({
                'alt': alt_text.strip(),
                'filename': filename,
                'path': None,
                'is_external': True
            })
        else:
            # Local file - check if it exists
            image_path = readme_path.parent / filename
            if image_path.exists():
                images.append({
                    'alt': alt_text.strip(),
                    'filename': filename,
                    'path': image_path,
                    'is_external': False
                })
    
    info['images'] = images[:2]  # Limit to first 2 images
    
    return info


# Removed thumbnail generation function - using simple HTML sizing instead


def load_github_mappings(portfolio_dir: Path) -> Dict[str, str]:
    """
    Load GitHub username mappings from the JSON file.
    
    Args:
        portfolio_dir: Path to the student-portfolios directory
        
    Returns:
        Dictionary mapping folder names to GitHub usernames
    """
    mapping_file = portfolio_dir / 'student_github_mapping.json'
    github_mappings = {}
    
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            mappings = json.load(f)
        
        for mapping in mappings:
            folder_name = mapping.get('folder_name')
            github_username = mapping.get('github_username')
            if folder_name and github_username and github_username != 'MANUAL_MAPPING_NEEDED':
                github_mappings[folder_name] = github_username
                
    except FileNotFoundError:
        print(f"Warning: GitHub mapping file not found at {mapping_file}")
    except json.JSONDecodeError as e:
        print(f"Warning: Error parsing GitHub mapping file: {e}")
    except Exception as e:
        print(f"Warning: Error loading GitHub mappings: {e}")
    
    return github_mappings


def generate_portfolio_readme(portfolio_dir: Path) -> str:
    """
    Generate the main portfolio README.md content.
    
    Args:
        portfolio_dir: Path to the student-portfolios directory
        
    Returns:
        String content for the README.md file
    """
    students = []
    
    # Load GitHub mappings
    github_mappings = load_github_mappings(portfolio_dir)
    
    # Scan for student directories
    for item in portfolio_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            readme_path = item / 'README.md'
            if readme_path.exists():
                student_info = extract_student_info(readme_path)
                if student_info:
                    students.append(student_info)
    
    # Sort students alphabetically by folder name
    students.sort(key=lambda x: x['folder_name'])
    
    # Generate the README content
    content = """# 👨‍🎓 Student Portfolios

Welcome to the Decision Analytics Student Portfolio Collection!

This README is automatically generated and updated when changes are made to student portfolios.

## 📊 Current Students

| Student | Nickname | Interesting Facts | Portfolio | GitHub | Thumbnails |
|---------|----------|-------------------|-----------|--------|------------|
"""
    
    for student in students:
        nickname = student.get('nickname', 'N/A')
        fact1 = student.get('fact1', 'N/A')
        fact2 = student.get('fact2', 'N/A')
        folder_name = student['folder_name']
        
        # Truncate facts if they're too long
        fact1_short = fact1[:50] + "..." if len(fact1) > 50 else fact1
        fact2_short = fact2[:50] + "..." if len(fact2) > 50 else fact2
        
        # Combine facts for display
        facts_display = f"{fact1_short}<br>{fact2_short}"
        
        # Generate GitHub link
        github_username = github_mappings.get(folder_name)
        if github_username:
            github_link = f"[@{github_username}](https://github.com/{github_username})"
        else:
            github_link = "N/A"
        
        # Generate thumbnail HTML
        thumbnails_html = ""
        if 'images' in student and student['images']:
            for img in student['images']:
                if img.get('is_external', False):
                    # External URL - use the full URL with size parameters
                    # GitHub doesn't support resizing external URLs, so we'll use inline styles
                    thumbnails_html += f'<img src="{img["filename"]}" alt="{img["alt"]}" title="{img["alt"]}" width="150" style="max-height: 85px; object-fit: contain; margin: 2px;">'
                else:
                    # Local file - use original image with width only to preserve aspect ratio
                    # GitHub will respect the width attribute and auto-adjust height
                    thumbnails_html += f'<img src="{folder_name}/{img["filename"]}" alt="{img["alt"]}" title="{img["alt"]}" width="150">'
        
        if not thumbnails_html:
            thumbnails_html = "No images"
        
        content += f"| {folder_name} | {nickname} | {facts_display} | [View Portfolio]({folder_name}/README.md) | {github_link} | {thumbnails_html} |\n"
    
    content += f"""
## 🆕 How to Add Your Portfolio

1. Create a new folder with your name (e.g., `YourName`)
2. Add a `README.md` file with your information following this format:

```markdown
# 👨‍🎓 Student Portfolio - Your Name

---

## 📋 Student Information

| **Field** | **Details** |
|-----------|-------------|
| **Nickname/Pseudonym** | Your Nickname |
| **Interesting Fact** | An interesting fact about you |
| **Interesting Fact2** | Another interesting fact about you |

---

## 🖼️ Portfolio Images

### Image Title
![Description](image_filename.jpg)
```

3. Include portfolio images in your folder
4. Commit and push your changes

## 🔄 Auto-Generation

This README is automatically updated via GitHub Actions whenever any `README.md` file in the student-portfolios folder (or its subfolders) is modified.

---
*Last updated: {os.popen('git log -1 --format="%Y-%m-%d %H:%M:%S" -- .').read().strip() or 'Unknown'}*
"""
    
    return content


def main():
    """Main function to generate the portfolio README."""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    portfolio_dir = script_dir
    
    print(f"Scanning student portfolios in: {portfolio_dir}")
    
    # Generate the README content
    readme_content = generate_portfolio_readme(portfolio_dir)
    
    # Write the README.md file
    readme_path = portfolio_dir / 'README.md'
    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"Successfully generated {readme_path}")
        # Count students by counting lines that contain "View Portfolio"
        student_count = readme_content.count('[View Portfolio]')
        print(f"Found {student_count} student portfolios")
    except Exception as e:
        print(f"Error writing README.md: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
