from PIL import Image
import numpy as np

class ImageProcessor:
    # Predefined color palettes
    PALETTES = {
        "grayscale": [(i, i, i) for i in range(0, 256, 32)],
        "gameboy": [(15, 56, 15), (48, 98, 48), (139, 172, 15), (155, 188, 15)],
        "cga": [(0, 0, 0), (85, 85, 85), (170, 170, 170), (255, 255, 255),
                (0, 0, 170), (85, 85, 255), (0, 170, 0), (85, 255, 85),
                (0, 170, 170), (85, 255, 255), (170, 0, 0), (255, 85, 85),
                (170, 0, 170), (255, 85, 255), (170, 85, 0), (255, 255, 85)],
        "nes": [(124, 124, 124), (0, 0, 252), (0, 0, 188), (68, 40, 188),
                (148, 0, 132), (168, 0, 32), (168, 16, 0), (136, 20, 0),
                (80, 48, 0), (0, 120, 0), (0, 104, 0), (0, 88, 0),
                (0, 64, 88), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                (188, 188, 188), (0, 120, 248), (0, 88, 248), (104, 68, 252),
                (216, 0, 204), (228, 0, 88), (248, 56, 0), (228, 92, 16),
                (172, 124, 0), (0, 184, 0), (0, 168, 0), (0, 168, 68),
                (0, 136, 136), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                (248, 248, 248), (60, 188, 252), (104, 136, 252), (152, 120, 248),
                (248, 120, 248), (248, 88, 152), (248, 120, 88), (252, 160, 68),
                (248, 184, 0), (184, 248, 24), (88, 216, 84), (88, 248, 152),
                (0, 232, 216), (120, 120, 120), (0, 0, 0), (0, 0, 0),
                (252, 252, 252), (164, 228, 252), (184, 184, 248), (216, 184, 248),
                (248, 184, 248), (248, 164, 192), (240, 208, 176), (252, 224, 168),
                (248, 216, 120), (216, 248, 120), (184, 248, 184), (184, 248, 216),
                (0, 252, 252), (248, 216, 248), (0, 0, 0), (0, 0, 0)]
    }
    
    # Dithering methods
    DITHER_METHODS = {
        "none": Image.Dither.NONE,
        "floyd-steinberg": Image.Dither.FLOYDSTEINBERG
    }
    
    @staticmethod
    def convert_to_pixel_art(image, pixel_size, color_count, dither_method="none", palette_name=None):
        """
        Convert an image to pixel art style.
        
        Args:
            image (PIL.Image): The source image
            pixel_size (int): Size of pixels in the output
            color_count (int): Number of colors in the output
            dither_method (str): Dithering method to use (default: "none")
            palette_name (str): Name of predefined palette to use (default: None for adaptive)
            
        Returns:
            PIL.Image: The processed pixel art image
            
        Raises:
            ValueError: If input parameters are invalid
            TypeError: If image is not a PIL Image
        """
        # Validate inputs
        if not isinstance(image, Image.Image):
            raise TypeError("Expected a PIL Image object")
        
        if not isinstance(pixel_size, int) or pixel_size <= 0:
            raise ValueError("Pixel size must be a positive integer")
            
        if not isinstance(color_count, int) or color_count <= 0 or color_count > 256:
            raise ValueError("Color count must be an integer between 1 and 256")
        
        if dither_method not in ImageProcessor.DITHER_METHODS:
            raise ValueError(f"Dither method must be one of: {', '.join(ImageProcessor.DITHER_METHODS.keys())}")
        
        # Calculate new dimensions
        width = max(1, image.width // pixel_size)
        height = max(1, image.height // pixel_size)
        
        # Resize image to smaller size
        small = image.resize((width, height), Image.Resampling.LANCZOS)
        
        # Apply color reduction
        if palette_name:
            if palette_name not in ImageProcessor.PALETTES:
                raise ValueError(f"Palette name must be one of: {', '.join(ImageProcessor.PALETTES.keys())}")
            
            # Create a new image with the palette
            palette_img = Image.new('P', (1, 1))
            flat_palette = [c for color in ImageProcessor.PALETTES[palette_name] for c in color]
            palette_img.putpalette(flat_palette + [0] * (768 - len(flat_palette)))
            
            # Convert using the custom palette
            dither = ImageProcessor.DITHER_METHODS[dither_method]
            small = small.quantize(colors=min(color_count, len(ImageProcessor.PALETTES[palette_name])), 
                                  palette=palette_img, dither=dither)
        else:
            # Use adaptive palette
            dither = ImageProcessor.DITHER_METHODS[dither_method]
            small = small.quantize(colors=color_count, dither=dither)
        
        # Resize back to original size
        processed = small.resize(
            (width * pixel_size, height * pixel_size),
            Image.Resampling.NEAREST
        )
        
        return processed
    
    @staticmethod
    def apply_filter(image, filter_type):
        """
        Apply a filter to an image.
        
        Args:
            image (PIL.Image): The source image
            filter_type (str): Type of filter to apply
            
        Returns:
            PIL.Image: The filtered image
            
        Raises:
            ValueError: If filter_type is invalid
            TypeError: If image is not a PIL Image
        """
        if not isinstance(image, Image.Image):
            raise TypeError("Expected a PIL Image object")
        
        # Convert to numpy array for easier manipulation
        img_array = np.array(image)
        
        if filter_type == "invert":
            # Invert colors
            if image.mode == "RGB":
                img_array = 255 - img_array
            else:
                raise ValueError("Invert filter only works with RGB images")
        
        elif filter_type == "sepia":
            # Apply sepia tone
            if image.mode == "RGB":
                r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
                new_r = np.minimum(0.393 * r + 0.769 * g + 0.189 * b, 255).astype(np.uint8)
                new_g = np.minimum(0.349 * r + 0.686 * g + 0.168 * b, 255).astype(np.uint8)
                new_b = np.minimum(0.272 * r + 0.534 * g + 0.131 * b, 255).astype(np.uint8)
                img_array = np.stack((new_r, new_g, new_b), axis=2)
            else:
                raise ValueError("Sepia filter only works with RGB images")
        
        elif filter_type == "grayscale":
            # Convert to grayscale
            if image.mode == "RGB":
                r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
                gray = (0.2989 * r + 0.5870 * g + 0.1140 * b).astype(np.uint8)
                img_array = np.stack((gray, gray, gray), axis=2)
            else:
                raise ValueError("Grayscale filter only works with RGB images")
        
        else:
            raise ValueError(f"Unknown filter type: {filter_type}")
        
        # Convert back to PIL Image
        return Image.fromarray(img_array)
    
    @staticmethod
    def resize_with_aspect_ratio(image, target_size):
        """
        Resize image while preserving aspect ratio.
        
        Args:
            image (PIL.Image): The source image
            target_size (tuple): Target width and height
            
        Returns:
            PIL.Image: Resized image
            
        Raises:
            ValueError: If target_size is invalid
            TypeError: If image is not a PIL Image
        """
        if not isinstance(image, Image.Image):
            raise TypeError("Expected a PIL Image object")
            
        if not isinstance(target_size, tuple) or len(target_size) != 2:
            raise ValueError("Target size must be a tuple of (width, height)")
            
        if target_size[0] <= 0 or target_size[1] <= 0:
            raise ValueError("Target dimensions must be positive")
            
        ratio = min(target_size[0] / image.width, target_size[1] / image.height)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        return image.resize(new_size, Image.Resampling.LANCZOS) 