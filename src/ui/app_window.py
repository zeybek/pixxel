import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Add parent directory to path to make imports work
sys.path.append(str(Path(__file__).parent.parent))
from image_processor.processor import ImageProcessor

class AppWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixxel")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Image variables
        self.original_image = None
        self.processed_image = None
        self.original_photo = None
        self.processed_photo = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the main UI components"""
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self._setup_controls()
        self._setup_image_area()
    
    def _setup_controls(self):
        """Setup control buttons and settings"""
        # Select file button
        self.select_btn = ttk.Button(self.main_frame, text="Select Image", command=self._select_image)
        self.select_btn.grid(row=0, column=0, pady=5)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(self.main_frame, text="Settings", padding="5")
        settings_frame.grid(row=0, column=1, pady=5, padx=10, sticky="ew")
        
        # Pixel size setting
        ttk.Label(settings_frame, text="Pixel Size:").grid(row=0, column=0)
        self.pixel_size = tk.StringVar(value="8")
        pixel_entry = ttk.Entry(settings_frame, textvariable=self.pixel_size, width=5)
        pixel_entry.grid(row=0, column=1, padx=5)
        
        # Color count setting
        ttk.Label(settings_frame, text="Color Count:").grid(row=0, column=2, padx=5)
        self.color_count = tk.StringVar(value="32")
        color_entry = ttk.Entry(settings_frame, textvariable=self.color_count, width=5)
        color_entry.grid(row=0, column=3)
        
        # Convert button
        self.convert_btn = ttk.Button(settings_frame, text="Convert", command=self._convert_image)
        self.convert_btn.grid(row=0, column=4, padx=10)
        
        # Save button
        self.save_btn = ttk.Button(settings_frame, text="Save", command=self._save_image)
        self.save_btn.grid(row=0, column=5)
    
    def _setup_image_area(self):
        """Setup the image display area"""
        self.image_frame = ttk.Frame(self.main_frame)
        self.image_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.original_label = ttk.Label(self.image_frame, text="Original Image")
        self.original_label.grid(row=0, column=0, padx=5)
        
        self.processed_label = ttk.Label(self.image_frame, text="Pixel Art")
        self.processed_label.grid(row=0, column=1, padx=5)
    
    def _select_image(self):
        """Handle image selection"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.original_image = Image.open(file_path)
            self._display_images(self.original_image, None)
    
    def _convert_image(self):
        """Convert the selected image to pixel art"""
        if self.original_image is None:
            tk.messagebox.showinfo("No Image", "Please select an image first.")
            return
        
        try:
            pixel_size = int(self.pixel_size.get())
            if pixel_size <= 0:
                raise ValueError("Pixel size must be positive")
                
            color_count = int(self.color_count.get())
            if color_count <= 0 or color_count > 256:
                raise ValueError("Color count must be between 1 and 256")
            
            self.processed_image = ImageProcessor.convert_to_pixel_art(
                self.original_image,
                pixel_size,
                color_count
            )
            
            self._display_images(self.original_image, self.processed_image)
        except ValueError as e:
            tk.messagebox.showerror("Invalid Input", str(e) or "Please enter valid numbers for Pixel Size and Color Count.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def _save_image(self):
        """Save the processed image"""
        if self.processed_image is None:
            messagebox.showinfo("No Image", "Please convert an image first.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.processed_image.save(file_path)
                messagebox.showinfo("Success", f"Image saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def _display_images(self, original, processed):
        """Display both original and processed images"""
        display_size = (350, 350)
        
        if original:
            original_resized = ImageProcessor.resize_with_aspect_ratio(original, display_size)
            self.original_photo = ImageTk.PhotoImage(original_resized)
            self.original_label.configure(image=self.original_photo)
        
        if processed:
            processed_resized = ImageProcessor.resize_with_aspect_ratio(processed, display_size)
            self.processed_photo = ImageTk.PhotoImage(processed_resized)
            self.processed_label.configure(image=self.processed_photo) 