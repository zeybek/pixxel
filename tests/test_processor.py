#!/usr/bin/env python3
"""
Tests for the ImageProcessor class.
"""
import unittest
import sys
import os
from pathlib import Path
from PIL import Image

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from src.image_processor.processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    """Test cases for the ImageProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a test image
        self.test_image = Image.new('RGB', (100, 100), color='white')
        
        # Draw some shapes on the test image
        from PIL import ImageDraw
        draw = ImageDraw.Draw(self.test_image)
        draw.rectangle([(10, 10), (40, 40)], fill=(255, 0, 0))
        draw.ellipse([(60, 60), (90, 90)], fill=(0, 0, 255))
    
    def test_convert_to_pixel_art_basic(self):
        """Test basic pixel art conversion."""
        pixel_art = ImageProcessor.convert_to_pixel_art(self.test_image, 10, 8)
        
        # Check that the output is an image
        self.assertIsInstance(pixel_art, Image.Image)
        
        # Check dimensions
        self.assertEqual(pixel_art.width, 100)
        self.assertEqual(pixel_art.height, 100)
    
    def test_convert_to_pixel_art_invalid_inputs(self):
        """Test error handling for invalid inputs."""
        # Test with invalid pixel size
        with self.assertRaises(ValueError):
            ImageProcessor.convert_to_pixel_art(self.test_image, 0, 8)
        
        # Test with invalid color count
        with self.assertRaises(ValueError):
            ImageProcessor.convert_to_pixel_art(self.test_image, 10, 0)
        
        with self.assertRaises(ValueError):
            ImageProcessor.convert_to_pixel_art(self.test_image, 10, 300)
        
        # Test with invalid image
        with self.assertRaises(TypeError):
            ImageProcessor.convert_to_pixel_art("not an image", 10, 8)
    
    def test_resize_with_aspect_ratio(self):
        """Test image resizing with aspect ratio preservation."""
        # Create a rectangular image
        rect_image = Image.new('RGB', (200, 100), color='white')
        
        # Resize to a square target
        resized = ImageProcessor.resize_with_aspect_ratio(rect_image, (50, 50))
        
        # Check that aspect ratio is preserved
        self.assertEqual(resized.width, 50)
        self.assertEqual(resized.height, 25)
    
    def test_resize_with_aspect_ratio_invalid_inputs(self):
        """Test error handling for invalid resize inputs."""
        # Test with invalid target size
        with self.assertRaises(ValueError):
            ImageProcessor.resize_with_aspect_ratio(self.test_image, (0, 50))
        
        with self.assertRaises(ValueError):
            ImageProcessor.resize_with_aspect_ratio(self.test_image, (50, 0))
        
        # Test with invalid image
        with self.assertRaises(TypeError):
            ImageProcessor.resize_with_aspect_ratio("not an image", (50, 50))

if __name__ == '__main__':
    unittest.main() 