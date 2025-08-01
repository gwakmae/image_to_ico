# Image to ICO Converter

A simple yet powerful Python application for converting images to ICO format with an intuitive GUI interface.

## 🎯 Features

- **Multiple Format Support**: Convert PNG, JPEG, BMP, GIF, TIFF, WEBP, and ICO files
- **Smart Cropping**: Automatically removes whitespace and transparent areas
- **Multi-Size ICO Generation**: Create ICO files with multiple resolutions (16px to 256px)
- **Batch Processing**: Convert multiple files at once
- **High-Quality Resampling**: Uses LANCZOS algorithm for best image quality
- **User-Friendly GUI**: Clean Tkinter interface with progress tracking
- **Flexible Output**: Save to custom folder or alongside original files

## 🖼️ Screenshot
<img width="600" height="523" alt="image" src="https://github.com/user-attachments/assets/cdffcfa9-a3b2-45a0-84be-b03e5ebbc2e0" />



The application provides a clean interface with:
- File selection and management
- Customizable icon size options
- Real-time progress tracking
- Easy-to-use settings panel

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Install Dependencies

```bash
pip install numpy pillow
```

Or using the included requirements:

```bash
pip install -r requirements.txt
```

## 💻 Usage

### Running the Application

```bash
python main.py
```

### Basic Workflow

1. **Select Images**: Click "이미지 파일 선택" to choose your image files
2. **Configure Settings**: 
   - Enable/disable automatic cropping
   - Select desired icon sizes (16px, 24px, 32px, 48px, 64px, 96px, 128px, 256px)
   - Choose output directory
3. **Convert**: Click "변환 시작" to begin the conversion process
4. **Monitor Progress**: Watch the progress bar and status updates

### Advanced Features

- **Smart Cropping**: Automatically detects and removes unnecessary whitespace
- **Quality Control**: Uses LANCZOS resampling for optimal image quality
- **Batch Processing**: Handle multiple files simultaneously
- **Cancellation**: Stop conversion process at any time

## 📁 Project Structure

```
image_to_ico/
├── main.py           # Application entry point
├── gui.py            # GUI interface implementation
├── converter.py      # Image conversion logic
├── config.py         # Configuration and constants
├── pyproject.toml    # Project configuration
└── README.md         # This file
```

## ⚙️ Configuration

The application includes several configurable options in `config.py`:

- **Supported Formats**: Easily add new image formats
- **Default Sizes**: Customize default icon size selections
- **Quality Settings**: Adjust resampling methods and thresholds
- **UI Preferences**: Modify default application behavior

## 🔧 Technical Details

### Core Components

- **ImageConverter Class**: Handles all image processing operations
- **Smart Cropping Algorithm**: Uses numpy for efficient pixel analysis
- **Multi-threading**: Background processing prevents UI freezing
- **Error Handling**: Comprehensive error management and user feedback

### Image Processing Pipeline

1. **Load Image**: Open and validate input file
2. **Format Conversion**: Convert to RGBA for consistent processing
3. **Smart Cropping**: Remove transparent/white borders (optional)
4. **Multi-Size Generation**: Create icons at selected resolutions
5. **ICO Assembly**: Combine all sizes into single ICO file

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Clone the repository
2. Install dependencies: `pip install numpy pillow`
3. Run the application: `python main.py`

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Known Issues

- Large images may take longer to process
- Some very old ICO formats might not be fully supported
- Memory usage increases with batch processing of large files

## 🔮 Future Enhancements

- [ ] Additional output formats (PNG, JPEG)
- [ ] Custom icon size input
- [ ] Image preview functionality
- [ ] Command-line interface
- [ ] Drag-and-drop file support
- [ ] Advanced cropping options

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Include error messages and system information

---

**Made with ❤️ using Python, Tkinter, PIL, and NumPy**
