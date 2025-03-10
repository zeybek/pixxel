from PIL import Image

class ImageProcessor:
    @staticmethod
    def convert_to_pixel_art(image, pixel_size, color_count):
        """
        Convert an image to pixel art style.
        
        Args:
            image (PIL.Image): The source image
            pixel_size (int): Size of pixels in the output
            color_count (int): Number of colors in the output
            
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
        
        # Calculate new dimensions
        width = max(1, image.width // pixel_size)
        height = max(1, image.height // pixel_size)
        
        # Resize image to smaller size
        small = image.resize((width, height), Image.Resampling.LANCZOS)
        
        # Reduce color count
        small = small.convert('P', palette=Image.Palette.ADAPTIVE, colors=color_count)
        
        # Resize back to original size
        processed = small.resize(
            (width * pixel_size, height * pixel_size),
            Image.Resampling.NEAREST
        )
        
        return processed

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