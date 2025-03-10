# Pixxel

A simple Pixel Art conversion tool that allows you to convert normal images to Pixel Art style.

## Use Cases

- **Game Development**: Create retro-style sprites and textures for 2D games
- **Pixel Art Creation**: Convert photographs or digital art into pixel art without manual pixel-by-pixel editing
- **Social Media**: Create unique, retro-styled profile pictures or post images
- **Web Design**: Generate pixel art assets for retro-themed websites or UI elements
- **Educational**: Learn about pixel art principles and color reduction techniques
- **Artistic Projects**: Create unique artistic effects by experimenting with different pixel sizes and color counts

## Features

- Convert images to Pixel Art style
- Adjust pixel size
- Reduce color count
- Save converted images in various formats (PNG, JPEG)
- User-friendly interface with modern theme
- Error handling and validation
- **Advanced Features**:
  - Dithering options (None, Floyd-Steinberg)
  - Predefined color palettes (Grayscale, Gameboy, CGA, NES)
  - Image filters (Grayscale, Sepia, Invert)
  - Batch processing for multiple images

## Project Structure

```
pixxel/
├── src/                    # Source code
│   ├── image_processor/    # Image processing functionality
│   │   └── processor.py    # Core image processing logic
│   ├── ui/                 # User interface components
│   │   └── app_window.py   # Main application window
│   ├── utils/              # Utility scripts
│   │   └── generate_examples.py # Script to generate example images
│   └── main.py             # Application entry point
├── assets/                 # Example images and resources
│   └── examples/           # Example images with different settings
├── tests/                  # Unit tests
│   └── test_processor.py   # Tests for the image processor
├── requirements.txt        # Python dependencies
├── run.py                  # Launcher script
└── README.md               # This file
```

## Installation

1. Python 3.8 or higher is required.
2. Clone the repository:
   ```bash
   git clone https://github.com/zeybek/pixxel.git
   cd pixxel
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

There are two ways to run the application:

### Option 1: Using the launcher script (recommended)

```bash
python run.py
```

### Option 2: Running directly from the source directory

```bash
python src/main.py
```

### Using the Application

#### Basic Features

1. Click "Select Image" button to choose an image
2. Adjust Pixel Size and Color Count
3. Click "Convert" button
4. If you like the result, save it using the "Save" button

#### Advanced Features

1. Switch to the "Advanced" tab to access additional options
2. Choose a dithering method to create different pixel patterns
3. Select a predefined color palette for retro styles
4. Apply filters to the converted image
5. Use batch processing to convert multiple images at once

## Settings

### Basic Settings

- **Pixel Size**: Larger values create larger pixels (Default: 8)
- **Color Count**: Lower values provide a more retro look (Default: 32)

### Advanced Settings

- **Dithering**: Technique to create the illusion of more colors
  - None: No dithering
  - Floyd-Steinberg: Creates a pattern of dots to simulate more colors
- **Color Palettes**: Predefined color sets for specific retro looks
  - Grayscale: Black and white with gray tones
  - Gameboy: Classic 4-color Gameboy palette
  - CGA: 16-color Computer Graphics Adapter palette
  - NES: Nintendo Entertainment System palette
- **Filters**: Post-processing effects
  - Grayscale: Converts the image to black and white
  - Sepia: Adds a vintage brownish tone
  - Invert: Inverts all colors

## Tips for Best Results

- For classic 8-bit style art, try using 16-32 colors
- For more detailed pixel art, start with a larger Color Count (64-128) and gradually reduce
- Experiment with different Pixel Sizes:
  - Small (4-8): Good for detailed pixel art
  - Medium (12-16): Suitable for icons and small sprites
  - Large (24-32): Creates a more dramatic pixelation effect
- Try different dithering methods with low color counts to create interesting textures
- Use the Gameboy palette with a Pixel Size of 8 for authentic Gameboy-style graphics

## Testing

Run the unit tests to verify the functionality:

```bash
python -m unittest discover tests
```

## Generating Example Images

To generate example images with different settings:

```bash
python src/utils/generate_examples.py
```

This will create sample images in the `assets/examples` directory.

## Troubleshooting

- **ImportError**: Make sure you're running the application from the correct directory
- **ModuleNotFoundError**: Ensure all dependencies are installed correctly
- **Image Loading Issues**: The application supports PNG, JPEG, GIF, and BMP formats
- **Performance Issues**: Processing very large images may take time, especially with dithering enabled

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
