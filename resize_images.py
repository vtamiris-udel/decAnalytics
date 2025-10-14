#!/usr/bin/env python3
"""
Script to resize large PNG images to make them more manageable for GitHub.
"""

from PIL import Image
import os

def resize_image(input_path, output_path, max_width=800, max_height=600, quality=85):
    """
    Resize an image while maintaining aspect ratio.
    
    Args:
        input_path: Path to input image
        output_path: Path to output image
        max_width: Maximum width in pixels
        max_height: Maximum height in pixels
        quality: JPEG quality (1-100) for output
    """
    try:
        # Open the image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (PNG might have transparency)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create a white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Calculate new dimensions while maintaining aspect ratio
            width, height = img.size
            ratio = min(max_width / width, max_height / height)
            
            if ratio < 1:  # Only resize if image is larger than max dimensions
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save as JPEG with specified quality
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            # Get file sizes
            original_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)
            
            print(f"✓ Resized {input_path}")
            print(f"  Original: {original_size / (1024*1024):.1f} MB")
            print(f"  New: {new_size / (1024*1024):.1f} MB")
            print(f"  Reduction: {((original_size - new_size) / original_size * 100):.1f}%")
            print()
            
    except Exception as e:
        print(f"✗ Error processing {input_path}: {e}")

def main():
    # Define the images to resize
    images = [
        "student-portfolios/SamR/IMG_00633.png",
        "student-portfolios/SamR/IMG_2206.png"
    ]
    
    print("Resizing images for GitHub compatibility...")
    print("=" * 50)
    
    for img_path in images:
        if os.path.exists(img_path):
            # Create output path (change extension to .jpg)
            output_path = img_path.replace('.png', '_resized.jpg')
            
            # Resize the image
            resize_image(img_path, output_path, max_width=800, max_height=600, quality=85)
        else:
            print(f"✗ Image not found: {img_path}")
    
    print("=" * 50)
    print("Resizing complete! You can now:")
    print("1. Review the resized images")
    print("2. Replace the original PNG files with the resized JPG files")
    print("3. Update your git commit to use the smaller files")
    print("4. Push to GitHub successfully!")

if __name__ == "__main__":
    main()
