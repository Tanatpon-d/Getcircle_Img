# 🔵 GetCircle Image - Circle Detection Tool

Advanced circle detection in images using OpenCV's Hough Circle Transform. Perfect for computer vision projects, quality control, and image analysis.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Features

- **Circle Detection** - Detect circles in images using Hough Transform
- **Circle Extraction** - Extract individual circles as separate images
- **REST API** - Flask-based API for integration
- **Docker Support** - Easy deployment with Docker
- **Batch Processing** - Process multiple images
- **Adjustable Parameters** - Fine-tune detection sensitivity

## 📸 Examples

### Input Image
![Input](test.jpg)

### Detection Result
- Detected circles are marked with green outlines
- Circle centers marked in red
- Radius values displayed

## 🚀 Quick Start

### Method 1: Python Script

```bash
# Clone repository
git clone https://github.com/Tanatpon-d/Getcircle_Img.git
cd Getcircle_Img

# Install dependencies
pip install -r requirements.txt

# Run circle detection
python circle_detector.py test.jpg --show

# Extract individual circles
python circle_detector.py test.jpg --extract
```

### Method 2: Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# API will be available at http://localhost:5000
```

### Method 3: Flask API

```bash
# Start API server
python circle_api.py

# Test with curl
curl -X POST -F "image=@test.jpg" http://localhost:5000/detect
```

## 📖 Usage

### Command Line Interface

```bash
# Basic detection
python circle_detector.py image.jpg

# Save result with circles drawn
python circle_detector.py image.jpg -o output.jpg

# Extract individual circles
python circle_detector.py image.jpg --extract

# Adjust detection parameters
python circle_detector.py image.jpg --min-radius 20 --max-radius 100

# Show result window
python circle_detector.py image.jpg --show
```

### Python API

```python
from circle_detector import CircleDetector

# Initialize detector
detector = CircleDetector(min_radius=10, max_radius=200)

# Detect circles
circles = detector.detect_circles('image.jpg')

# Get circle information
info = detector.get_circle_info(circles)
print(f"Found {info['count']} circles")
print(f"Average radius: {info['average_radius']}")

# Draw circles on image
output = detector.draw_circles('image.jpg', circles, 'output.jpg')

# Extract individual circles
extracted = detector.extract_circles('image.jpg', circles)
```

### REST API Endpoints

#### 1. Detect Circles
```bash
POST /detect
Content-Type: multipart/form-data

Parameters:
- image: Image file
- min_radius: Minimum radius (optional)
- max_radius: Maximum radius (optional)

Response:
{
  "success": true,
  "message": "Detected 3 circles",
  "data": {
    "count": 3,
    "average_radius": 45.5,
    "circles": [...]
  },
  "result_image": "data:image/png;base64,..."
}
```

#### 2. Detect from Base64
```bash
POST /detect_base64
Content-Type: application/json

Body:
{
  "image": "data:image/png;base64,...",
  "min_radius": 10,
  "max_radius": 200
}
```

#### 3. Extract Circles
```bash
POST /extract
Content-Type: multipart/form-data

Parameters:
- image: Image file

Response:
{
  "success": true,
  "count": 3,
  "circles": [
    {
      "id": 1,
      "radius": 45,
      "center": {"x": 100, "y": 150},
      "image": "data:image/png;base64,..."
    }
  ]
}
```

## 🔧 Parameters

### Hough Circle Transform Parameters

| Parameter | Description | Default | Range |
|-----------|------------|---------|-------|
| `dp` | Inverse ratio of accumulator resolution | 1.2 | 1.0-2.0 |
| `minDist` | Minimum distance between circle centers | 100 | > 0 |
| `param1` | Upper threshold for Canny edge detector | 50 | > 0 |
| `param2` | Threshold for center detection | 30 | > 0 |
| `minRadius` | Minimum circle radius | 10 | > 0 |
| `maxRadius` | Maximum circle radius | 200 | > minRadius |

### Tips for Better Detection

1. **Preprocessing**
   - Apply blur to reduce noise
   - Adjust contrast if needed
   - Ensure good lighting in images

2. **Parameter Tuning**
   - Decrease `param2` to detect more circles
   - Increase `minDist` to avoid overlapping detections
   - Adjust radius range based on expected circle sizes

3. **Image Quality**
   - Use high-resolution images
   - Ensure circles are clearly visible
   - Avoid motion blur

## 🐳 Docker Deployment

### Development
```bash
docker-compose up --build
```

### Production
```bash
docker build -t circle-detector .
docker run -p 5000:5000 circle-detector
```

### Environment Variables
```bash
FLASK_ENV=production
FLASK_DEBUG=0
MAX_CONTENT_LENGTH=16777216  # 16MB
```

## 📁 Project Structure

```
Getcircle_Img/
│
├── circle_detector.py      # Core detection module
├── circle_api.py          # Flask REST API
├── test.py               # Test scripts
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── README.md           # Documentation
│
├── uploads/            # Temporary upload directory
├── outputs/            # Output directory
└── extracted_circles/  # Extracted circles directory
```

## 🧪 Testing

### Run Tests
```bash
# Test detection on sample images
python test.py

# Test API endpoints
python test_api.py
```

### Sample Images
- `test.jpg` - Sample image with multiple circles
- `test2.png` - Another test image
- `formalin400.png` - Medical/scientific image sample

## 📊 Use Cases

- **Quality Control** - Detect circular defects or verify circular products
- **Medical Imaging** - Identify circular structures in medical images
- **Industrial Inspection** - Check circular components
- **Scientific Analysis** - Analyze circular patterns in microscopy
- **Computer Vision** - Preprocessing for object detection
- **Game Development** - Detect circular game objects

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📝 Requirements

```txt
Flask==2.3.3
opencv-python==4.8.1
numpy==1.24.3
Pillow==10.0.0
requests==2.31.0
matplotlib==3.7.2
```

## ⚠️ Known Issues

- Very small circles (< 10px) may not be detected reliably
- Overlapping circles might be detected as single circle
- Performance decreases with very high resolution images (> 4K)

## 📄 License

MIT License - feel free to use in your projects!

## 👨‍💻 Author

**Tanatpon D**
- GitHub: [@Tanatpon-d](https://github.com/Tanatpon-d)
- Project: [Getcircle_Img](https://github.com/Tanatpon-d/Getcircle_Img)

## 🙏 Acknowledgments

- OpenCV community for Hough Circle Transform
- Flask team for excellent web framework
- Contributors and testers

---

⭐ Star this repository if you find it useful!