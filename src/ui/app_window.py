import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Add parent directory to path to make imports work
sys.path.append(str(Path(__file__).parent.parent))
from image_processor.processor import ImageProcessor
from ui.dark_messagebox import patch_messagebox

class AppWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixxel")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Set dark theme
        self._set_dark_theme()
        
        # Patch messagebox to use dark theme
        patch_messagebox(self.root)
        
        # Configure file dialog colors if possible
        try:
            self.root.tk.call('tk_getOpenFile', '-background', '#2e2e2e')
            self.root.tk.call('tk_getOpenFile', '-foreground', '#e0e0e0')
        except:
            pass
        
        # Image variables
        self.original_image = None
        self.processed_image = None
        self.original_photo = None
        self.processed_photo = None
        
        self._setup_ui()
    
    def _set_dark_theme(self):
        """Set up a dark theme for the application"""
        # Configure colors
        bg_color = "#2e2e2e"  # Dark background
        fg_color = "#e0e0e0"  # Light text
        accent_color = "#4a6ea9"  # Blue accent
        frame_bg = "#3a3a3a"  # Slightly lighter background for frames
        
        # Configure styles
        style = ttk.Style()
        
        # Configure main elements
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10), background=accent_color)
        
        # Configure labelframes - make them more compact
        style.configure("TLabelframe", background=bg_color, foreground=fg_color, font=("Arial", 10, "bold"))
        style.configure("TLabelframe.Label", background=bg_color, foreground=fg_color, font=("Arial", 10, "bold"))
        
        # Configure notebook (tabs) - make them more compact
        style.configure("TNotebook", background=bg_color, foreground=fg_color, tabmargins=[2, 2, 2, 0])
        style.configure("TNotebook.Tab", background=frame_bg, foreground=fg_color, padding=[8, 1])
        style.map("TNotebook.Tab", 
                 background=[("selected", accent_color)],
                 foreground=[("selected", "#ffffff")])
        
        # Configure entry fields
        style.configure("TEntry", fieldbackground=frame_bg, foreground=fg_color)
        
        # Configure combobox
        style.configure("TCombobox", fieldbackground=frame_bg, background=bg_color, foreground=fg_color)
        style.map("TCombobox", 
                 fieldbackground=[("readonly", frame_bg)],
                 selectbackground=[("readonly", accent_color)])
        
        # Set root background
        self.root.configure(background=bg_color)
        
        # Override system dialog colors if possible
        try:
            self.root.tk.call('tk_setPalette', bg_color)
        except:
            pass
    
    def _setup_ui(self):
        """Setup the main UI components"""
        # Main frame with reduced padding
        self.main_frame = ttk.Frame(self.root, padding="5")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, columnspan=2, sticky="ew", pady=2)
        
        # Basic settings tab
        self.basic_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.basic_tab, text="Basic")
        
        # Advanced settings tab
        self.advanced_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.advanced_tab, text="Advanced")
        
        # Setup controls in tabs
        self._setup_basic_controls()
        self._setup_advanced_controls()
        
        # Setup image area
        self._setup_image_area()
        
        # Setup status bar
        self._setup_status_bar()
    
    def _setup_basic_controls(self):
        """Setup basic control buttons and settings"""
        # Create a compact horizontal frame for all controls
        controls_frame = ttk.Frame(self.basic_tab)
        controls_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Select file button
        self.select_btn = ttk.Button(controls_frame, text="Select Image", command=self._select_image)
        self.select_btn.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Settings frame - more compact
        settings_frame = ttk.LabelFrame(controls_frame, text="Settings", padding="2")
        settings_frame.pack(side=tk.LEFT, padx=5, pady=2, fill=tk.X, expand=True)
        
        # Use grid layout for settings with reduced padding
        # Pixel size setting
        ttk.Label(settings_frame, text="Pixel Size:").grid(row=0, column=0, padx=2, pady=0)
        self.pixel_size = tk.StringVar(value="8")
        pixel_entry = ttk.Entry(settings_frame, textvariable=self.pixel_size, width=5)
        pixel_entry.grid(row=0, column=1, padx=2, pady=0)
        
        # Color count setting
        ttk.Label(settings_frame, text="Color Count:").grid(row=0, column=2, padx=2, pady=0)
        self.color_count = tk.StringVar(value="32")
        color_entry = ttk.Entry(settings_frame, textvariable=self.color_count, width=5)
        color_entry.grid(row=0, column=3, padx=2, pady=0)
        
        # Action buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(side=tk.RIGHT, padx=5, pady=2)
        
        # Convert button
        self.convert_btn = ttk.Button(button_frame, text="Convert", command=self._convert_image)
        self.convert_btn.pack(side=tk.LEFT, padx=2, pady=0)
        
        # Save button
        self.save_btn = ttk.Button(button_frame, text="Save", command=self._save_image)
        self.save_btn.pack(side=tk.LEFT, padx=2, pady=0)
    
    def _setup_advanced_controls(self):
        """Setup advanced control options"""
        # Create a main frame for advanced controls
        adv_controls_frame = ttk.Frame(self.advanced_tab)
        adv_controls_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # Create a horizontal layout for the first row
        row1_frame = ttk.Frame(adv_controls_frame)
        row1_frame.pack(fill=tk.X, pady=1)
        
        # Dithering options
        dither_frame = ttk.LabelFrame(row1_frame, text="Dithering", padding="2")
        dither_frame.pack(side=tk.LEFT, padx=2, pady=1, fill=tk.X, expand=True)
        
        ttk.Label(dither_frame, text="Method:").grid(row=0, column=0, padx=2, pady=0)
        self.dither_method = tk.StringVar(value="none")
        dither_combo = ttk.Combobox(dither_frame, textvariable=self.dither_method, width=15)
        dither_combo['values'] = list(ImageProcessor.DITHER_METHODS.keys())
        dither_combo.grid(row=0, column=1, padx=2, pady=0)
        dither_combo.state(['readonly'])
        
        # Color palette options
        palette_frame = ttk.LabelFrame(row1_frame, text="Color Palette", padding="2")
        palette_frame.pack(side=tk.LEFT, padx=2, pady=1, fill=tk.X, expand=True)
        
        ttk.Label(palette_frame, text="Palette:").grid(row=0, column=0, padx=2, pady=0)
        self.palette_name = tk.StringVar(value="")
        palette_combo = ttk.Combobox(palette_frame, textvariable=self.palette_name, width=15)
        palette_combo['values'] = [""] + list(ImageProcessor.PALETTES.keys())
        palette_combo.grid(row=0, column=1, padx=2, pady=0)
        palette_combo.state(['readonly'])
        
        # Create a horizontal layout for the second row
        row2_frame = ttk.Frame(adv_controls_frame)
        row2_frame.pack(fill=tk.X, pady=1)
        
        # Filter options
        filter_frame = ttk.LabelFrame(row2_frame, text="Filters", padding="2")
        filter_frame.pack(side=tk.LEFT, padx=2, pady=1, fill=tk.X, expand=True)
        
        ttk.Label(filter_frame, text="Filter:").grid(row=0, column=0, padx=2, pady=0)
        self.filter_type = tk.StringVar(value="none")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type, width=15)
        filter_combo['values'] = ["none", "grayscale", "sepia", "invert"]
        filter_combo.grid(row=0, column=1, padx=2, pady=0)
        filter_combo.state(['readonly'])
        
        # Apply filter button
        self.apply_filter_btn = ttk.Button(filter_frame, text="Apply Filter", command=self._apply_filter)
        self.apply_filter_btn.grid(row=0, column=2, padx=2, pady=0)
        
        # Batch processing
        batch_frame = ttk.LabelFrame(row2_frame, text="Batch Processing", padding="2")
        batch_frame.pack(side=tk.LEFT, padx=2, pady=1, fill=tk.X, expand=True)
        
        self.batch_btn = ttk.Button(batch_frame, text="Process Folder", command=self._batch_process)
        self.batch_btn.pack(padx=2, pady=0)
    
    def _setup_image_area(self):
        """Setup the image display area"""
        # Create a dark frame for the image area
        bg_color = "#2e2e2e"  # Dark background
        self.image_frame = ttk.Frame(self.main_frame)
        self.image_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Original image
        original_frame = ttk.LabelFrame(self.image_frame, text="Original Image")
        original_frame.grid(row=0, column=0, padx=5)
        
        # Create a dark canvas for the original image
        self.original_canvas = tk.Canvas(original_frame, bg=bg_color, width=400, height=400, highlightthickness=0)
        self.original_canvas.grid(row=0, column=0, padx=2, pady=2)
        
        # Processed image
        processed_frame = ttk.LabelFrame(self.image_frame, text="Pixel Art")
        processed_frame.grid(row=0, column=1, padx=5)
        
        # Create a dark canvas for the processed image
        self.processed_canvas = tk.Canvas(processed_frame, bg=bg_color, width=400, height=400, highlightthickness=0)
        self.processed_canvas.grid(row=0, column=0, padx=2, pady=2)
    
    def _setup_status_bar(self):
        """Setup status bar at the bottom of the window"""
        bg_color = "#2e2e2e"  # Dark background
        fg_color = "#e0e0e0"  # Light text
        
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W, 
                             bg=bg_color, fg=fg_color, 
                             bd=1, padx=5, pady=1)  # Reduced padding
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def _select_image(self):
        """Handle image selection"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self._display_images(self.original_image, None)
                self.status_var.set(f"Loaded image: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {str(e)}")
    
    def _convert_image(self):
        """Convert the selected image to pixel art"""
        if self.original_image is None:
            messagebox.showinfo("No Image", "Please select an image first.")
            return
        
        try:
            # Get basic settings
            pixel_size = int(self.pixel_size.get())
            if pixel_size <= 0:
                raise ValueError("Pixel size must be positive")
                
            color_count = int(self.color_count.get())
            if color_count <= 0 or color_count > 256:
                raise ValueError("Color count must be between 1 and 256")
            
            # Get advanced settings
            dither_method = self.dither_method.get()
            palette_name = self.palette_name.get() or None  # Convert empty string to None
            
            # Show processing status
            self.status_var.set("Processing image...")
            self.root.update()
            
            # Process the image
            self.processed_image = ImageProcessor.convert_to_pixel_art(
                self.original_image,
                pixel_size,
                color_count,
                dither_method,
                palette_name
            )
            
            # Apply filter if selected
            if self.filter_type.get() != "none":
                self.processed_image = self._apply_filter_to_image(self.processed_image)
            
            # Display the result
            self._display_images(self.original_image, self.processed_image)
            self.status_var.set("Conversion complete")
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e) or "Please enter valid numbers for Pixel Size and Color Count.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def _apply_filter(self):
        """Apply selected filter to the processed image"""
        if self.processed_image is None:
            messagebox.showinfo("No Image", "Please convert an image first.")
            return
        
        try:
            self.processed_image = self._apply_filter_to_image(self.processed_image)
            self._display_images(self.original_image, self.processed_image)
            self.status_var.set(f"Applied {self.filter_type.get()} filter")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply filter: {str(e)}")
    
    def _apply_filter_to_image(self, image):
        """Apply the selected filter to an image"""
        filter_type = self.filter_type.get()
        if filter_type == "none":
            return image
        
        return ImageProcessor.apply_filter(image, filter_type)
    
    def _batch_process(self):
        """Process multiple images in a folder"""
        input_dir = filedialog.askdirectory(title="Select Input Folder")
        if not input_dir:
            return
            
        output_dir = filedialog.askdirectory(title="Select Output Folder")
        if not output_dir:
            return
        
        try:
            # Get settings
            pixel_size = int(self.pixel_size.get())
            color_count = int(self.color_count.get())
            dither_method = self.dither_method.get()
            palette_name = self.palette_name.get() or None
            filter_type = self.filter_type.get()
            
            # Find all image files
            image_files = []
            for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
                image_files.extend(list(Path(input_dir).glob(f"*{ext}")))
                image_files.extend(list(Path(input_dir).glob(f"*{ext.upper()}")))
            
            if not image_files:
                messagebox.showinfo("No Images", "No image files found in the selected folder.")
                return
            
            # Process each image
            processed_count = 0
            for img_path in image_files:
                try:
                    # Update status
                    self.status_var.set(f"Processing {img_path.name}...")
                    self.root.update()
                    
                    # Open and process image
                    img = Image.open(img_path)
                    processed = ImageProcessor.convert_to_pixel_art(
                        img, pixel_size, color_count, dither_method, palette_name
                    )
                    
                    # Apply filter if selected
                    if filter_type != "none":
                        processed = ImageProcessor.apply_filter(processed, filter_type)
                    
                    # Save the processed image
                    output_path = Path(output_dir) / f"pixel_{img_path.name}"
                    processed.save(output_path)
                    processed_count += 1
                    
                except Exception as e:
                    print(f"Error processing {img_path.name}: {e}")
            
            # Show completion message
            self.status_var.set(f"Batch processing complete. Processed {processed_count} images.")
            messagebox.showinfo("Batch Complete", f"Successfully processed {processed_count} out of {len(image_files)} images.")
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
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
                self.status_var.set(f"Image saved to {os.path.basename(file_path)}")
                messagebox.showinfo("Success", f"Image saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
    
    def _display_images(self, original, processed):
        """Display both original and processed images"""
        display_size = (400, 400)
        bg_color = "#2e2e2e"  # Dark background
        
        # Clear canvases
        self.original_canvas.delete("all")
        self.processed_canvas.delete("all")
        
        if original:
            original_resized = ImageProcessor.resize_with_aspect_ratio(original, display_size)
            self.original_photo = ImageTk.PhotoImage(original_resized)
            
            # Calculate center position
            x = (400 - original_resized.width) // 2
            y = (400 - original_resized.height) // 2
            
            # Create image on canvas with dark background
            self.original_canvas.create_image(x, y, anchor=tk.NW, image=self.original_photo)
            
            # Show image dimensions in status bar
            self.status_var.set(f"Image dimensions: {original.width}x{original.height}")
        
        if processed:
            processed_resized = ImageProcessor.resize_with_aspect_ratio(processed, display_size)
            self.processed_photo = ImageTk.PhotoImage(processed_resized)
            
            # Calculate center position
            x = (400 - processed_resized.width) // 2
            y = (400 - processed_resized.height) // 2
            
            # Create image on canvas with dark background
            self.processed_canvas.create_image(x, y, anchor=tk.NW, image=self.processed_photo) 