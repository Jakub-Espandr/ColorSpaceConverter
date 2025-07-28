<p align="center">
  <a href="https://i.ibb.co/d4qL04RC/icon.png">
    <img src="https://i.ibb.co/d4qL04RC/icon.png" alt="ColorSpace Converter Logo" width="250"/>
  </a>
</p>

<h1 align="center">ColorSpace Converter</h1>
<p align="center"><em>(by Jakub Ešpandr)</em></p>

## Overview
A modern desktop application for analyzing and converting images between different color spaces. Developed as a tool for visualizing and analyzing color channels in RGB, CIELab, and HSV color spaces. The application provides an intuitive interface for loading images, switching between color channels, and saving conversion results.

---

## ✨ Features

- **RGB Analysis**
  - Load and display RGB images
  - Switch between individual channels (R, G, B) and complete RGB display
  - Real-time display of RGB values, hex code, and pixel position on mouse hover
  - Save modified images

- **CIELab Conversion**
  - Convert RGB → CIELab color space
  - Display individual channels (L, a, b) or complete CIELab image
  - Toggle between "RGB View" (converted back for display) and "Raw Data" (original CIELab values)
  - Save in original CIELab format or converted back to RGB

- **HSV Conversion**
  - Convert RGB → HSV color space
  - Display individual channels (H, S, V) or complete HSV image
  - Toggle between "RGB View" (converted back for display) and "Raw Data" (original HSV values)
  - Save in original HSV format or converted back to RGB

- **Modern GUI**
  - Tab-based interface for organized function display
  - Responsive design with minimum window size 800x600
  - Centered images in all tabs for consistent display
  - Intuitive controls with radio buttons for channel selection
  - Custom fonts (fccTYPO) for professional appearance
  - Platform-specific application icons (PNG, ICO, ICNS)

- **Analytical Tools**
  - Real-time color value display on mouse hover
  - Hex color code for precise identification
  - Pixel position for detailed analysis
  - Comparison between different color spaces

---

## 📦 Requirements

- Python 3.7+
- [OpenCV](https://opencv.org/) >= 4.5.0 – Computer vision and image processing
- [NumPy](https://numpy.org/) >= 1.21.0 – Numerical computations
- [Pillow](https://pillow.readthedocs.io/) >= 8.3.0 – Image processing
- [Matplotlib](https://matplotlib.org/) >= 3.5.0 – Visualization (optional)
- Tkinter (part of Python standard library)

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/Jakub-Espandr/ColorSpaceConverter.git
cd ColorSpaceConverter

# Install dependencies
pip install -r requirements.txt

# Start the application
python main.py
```

---

## 🛠️ Usage

### RGB Preview Tab
1. Click "📁 Load Image" to load an image
2. Use radio buttons to switch between channels:
   - **All**: Shows complete RGB image
   - **R**: Shows only red channel (grayscale)
   - **G**: Shows only green channel (grayscale)
   - **B**: Shows only blue channel (grayscale)
3. Hover over the image to see RGB values, hex code, and pixel position
4. Click "💾 Save Image" to save

### CIELab Conversion Tab
1. First load an image in the RGB Preview tab
2. Click "🔄 Convert to CIELab" to convert
3. Select channel using radio buttons:
   - **All**: Shows all CIELab channels
   - **L**: Shows lightness channel (0-100)
   - **a**: Shows green-red chromaticity channel (-128 to 127)
   - **b**: Shows blue-yellow chromaticity channel (-128 to 127)
4. Toggle display mode:
   - **RGB View**: Shows channels converted back to RGB for normal viewing
   - **Raw Data**: Shows original CIELab values (may look unusual)
5. Click "💾 Save CIELab" to save

### HSV Conversion Tab
1. First load an image in the RGB Preview tab
2. Click "🔄 Convert to HSV" to convert
3. Select channel using radio buttons:
   - **All**: Shows all HSV channels
   - **H**: Shows hue channel (0-179)
   - **S**: Shows saturation channel (0-255)
   - **V**: Shows value/brightness channel (0-255)
4. Toggle display mode:
   - **RGB View**: Shows channels converted back to RGB for normal viewing
   - **Raw Data**: Shows original HSV values (may look unusual)
5. Click "💾 Save HSV" to save

---

## 📁 Project Structure

```
testApp/
├── main.py                  # Main application - ColorSpace Converter
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── CHANGELOG.md            # Change history
└── assets/                 # Custom fonts and icons
    ├── fonts/
    │   ├── fccTYPO-Regular.ttf
    │   └── fccTYPO-Bold.ttf
    └── icons/
        ├── icon.png
        ├── icon.ico
        └── icon.icns
```

---

## 🎨 Color Spaces

### RGB (Red, Green, Blue)
- Standard color space for digital images
- Each pixel has three values representing red, green, and blue intensity
- Values typically range from 0-255

### CIELab (L*a*b*)
- Device-independent color space
- **L**: Lightness (0 = black, 100 = white)
- **a**: Green-red chromaticity (-128 = green, +127 = red)
- **b**: Blue-yellow chromaticity (-128 = blue, +127 = yellow)
- Better for color analysis and processing

### HSV (Hue, Saturation, Value)
- Intuitive color space based on human perception
- **H**: Hue (0-179 in OpenCV, represents color angle)
- **S**: Saturation (0-255, 0 = grayscale, 255 = full color)
- **V**: Value/Brightness (0-255, 0 = black, 255 = brightest)
- Useful for color segmentation and filtering

---

## 🎨 Custom Styling

The application uses custom fonts and icons for a professional appearance:

### Fonts
- **fccTYPO-Regular.ttf**: Regular weight font for general text
- **fccTYPO-Bold.ttf**: Bold weight font for titles and emphasis
- Fallback to Arial if custom fonts cannot be loaded

### Icons
- **icon.png**: PNG icon for macOS and Linux
- **icon.ico**: ICO icon for Windows
- **icon.icns**: ICNS icon for macOS (alternative)
- Platform-specific icon loading with automatic fallback

---

## 🔐 License

This project is licensed under the **Non-Commercial Public License (NCPL v1.0)**  
© 2025 Jakub Ešpandr - Born4Flight, FlyCamCzech  
See the [LICENSE](https://github.com/Jakub-Espandr/ColorSpaceConverter/raw/main/LICENSE) file for full terms.

---

## 🙏 Acknowledgments

- Built with ❤️ for color space analysis and visualization
- Powered by modern image processing libraries and GUI frameworks 