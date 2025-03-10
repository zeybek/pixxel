#!/usr/bin/env python3
"""
Generate example images for Pixxel
"""
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.image_processor.processor import ImageProcessor

def create_directory(path):
    """Create directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)

def generate_gradient_image(width=500, height=500):
    """Generate a gradient image"""
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    for y in range(height):
        r = int(255 * y / height)
        g = int(255 * (1 - y / height))
        b = int(255 * (0.5 + 0.5 * y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return image

def generate_geometric_image(width=500, height=500):
    """Generate an image with geometric shapes"""
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw rectangles
    draw.rectangle([(50, 50), (200, 200)], fill=(255, 0, 0))
    draw.rectangle([(250, 50), (400, 200)], fill=(0, 255, 0))
    
    # Draw circles
    draw.ellipse([(50, 250), (200, 400)], fill=(0, 0, 255))
    draw.ellipse([(250, 250), (400, 400)], fill=(255, 255, 0))
    
    # Draw lines
    for i in range(10):
        draw.line([(0, i*20), (width, height-i*20)], fill=(128, 0, 128), width=3)
    
    return image

def main():
    """Generate example images and their pixel art versions"""
    # Create assets directory
    assets_dir = Path(__file__).parent.parent.parent / "assets" / "examples"
    create_directory(assets_dir)
    
    # Generate gradient image
    gradient = generate_gradient_image()
    gradient_path = assets_dir / "gradient.png"
    gradient.save(gradient_path)
    
    # Generate geometric image
    geometric = generate_geometric_image()
    geometric_path = assets_dir / "geometric.png"
    geometric.save(geometric_path)
    
    # Create pixel art versions with different settings
    for img_path, name in [(gradient_path, "gradient"), (geometric_path, "geometric")]:
        img = Image.open(img_path)
        
        # Different pixel sizes
        for pixel_size in [4, 8, 16]:
            # Different color counts
            for color_count in [8, 16, 32]:
                pixel_art = ImageProcessor.convert_to_pixel_art(img, pixel_size, color_count)
                output_path = assets_dir / f"{name}_pixel_{pixel_size}px_{color_count}colors.png"
                pixel_art.save(output_path)
    
    print(f"Example images generated in {assets_dir}")

if __name__ == "__main__":
    main() 