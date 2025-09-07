#!/usr/bin/env python3
"""
Flask API for Circle Detection Service
Author: Tanatpon D
"""

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import cv2 as cv
import numpy as np
from circle_detector import CircleDetector
import base64
from io import BytesIO
from PIL import Image
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Initialize circle detector
detector = CircleDetector()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """API health check"""
    return jsonify({
        "status": "running",
        "service": "Circle Detection API",
        "version": "1.0.0",
        "endpoints": [
            "/detect - Detect circles in uploaded image",
            "/detect_base64 - Detect circles in base64 image",
            "/extract - Extract individual circles from image",
            "/info - Get API information"
        ]
    })


@app.route('/detect', methods=['POST'])
def detect_circles():
    """
    Detect circles in uploaded image
    
    Returns JSON with circle information and base64 encoded result image
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get parameters from request
        min_radius = request.form.get('min_radius', 10, type=int)
        max_radius = request.form.get('max_radius', 200, type=int)
        
        # Detect circles
        detector.min_radius = min_radius
        detector.max_radius = max_radius
        circles = detector.detect_circles(filepath)
        
        if circles is None:
            return jsonify({
                "success": False,
                "message": "No circles detected",
                "count": 0
            })
        
        # Get circle information
        info = detector.get_circle_info(circles)
        
        # Draw circles on image
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"result_{filename}")
        output_image = detector.draw_circles(filepath, circles, output_path)
        
        # Convert result to base64
        _, buffer = cv.imencode('.png', output_image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            "success": True,
            "message": f"Detected {info['count']} circles",
            "data": info,
            "result_image": f"data:image/png;base64,{image_base64}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/detect_base64', methods=['POST'])
def detect_circles_base64():
    """
    Detect circles in base64 encoded image
    """
    try:
        data = request.get_json()
        
        if 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'].split(',')[1] if ',' in data['image'] else data['image'])
        image = Image.open(BytesIO(image_data))
        
        # Save temporary file
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_image.png')
        image.save(temp_path)
        
        # Get parameters
        min_radius = data.get('min_radius', 10)
        max_radius = data.get('max_radius', 200)
        
        # Detect circles
        detector.min_radius = min_radius
        detector.max_radius = max_radius
        circles = detector.detect_circles(temp_path)
        
        if circles is None:
            os.remove(temp_path)
            return jsonify({
                "success": False,
                "message": "No circles detected",
                "count": 0
            })
        
        # Get circle information
        info = detector.get_circle_info(circles)
        
        # Draw circles on image
        output_image = detector.draw_circles(temp_path, circles)
        
        # Convert result to base64
        _, buffer = cv.imencode('.png', output_image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({
            "success": True,
            "message": f"Detected {info['count']} circles",
            "data": info,
            "result_image": f"data:image/png;base64,{image_base64}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/extract', methods=['POST'])
def extract_circles():
    """
    Extract individual circles as separate images
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Detect circles
        circles = detector.detect_circles(filepath)
        
        if circles is None:
            os.remove(filepath)
            return jsonify({
                "success": False,
                "message": "No circles detected",
                "count": 0
            })
        
        # Extract circles
        extracted_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'extracted')
        extracted_paths = detector.extract_circles(filepath, circles, extracted_dir)
        
        # Convert extracted circles to base64
        extracted_images = []
        for i, path in enumerate(extracted_paths):
            with open(path, 'rb') as f:
                img_base64 = base64.b64encode(f.read()).decode('utf-8')
                extracted_images.append({
                    "id": i + 1,
                    "radius": int(circles[i][2]),
                    "center": {"x": int(circles[i][0]), "y": int(circles[i][1])},
                    "image": f"data:image/png;base64,{img_base64}"
                })
        
        # Clean up
        os.remove(filepath)
        for path in extracted_paths:
            os.remove(path)
        
        return jsonify({
            "success": True,
            "message": f"Extracted {len(extracted_images)} circles",
            "count": len(extracted_images),
            "circles": extracted_images
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/info', methods=['GET'])
def api_info():
    """Get API information and usage examples"""
    return jsonify({
        "name": "Circle Detection API",
        "version": "1.0.0",
        "author": "Tanatpon D",
        "description": "API for detecting and extracting circles from images using OpenCV",
        "endpoints": {
            "/detect": {
                "method": "POST",
                "description": "Detect circles in uploaded image",
                "parameters": {
                    "image": "Image file (required)",
                    "min_radius": "Minimum circle radius (optional, default: 10)",
                    "max_radius": "Maximum circle radius (optional, default: 200)"
                },
                "returns": "JSON with circle information and base64 result image"
            },
            "/detect_base64": {
                "method": "POST",
                "description": "Detect circles in base64 encoded image",
                "body": {
                    "image": "Base64 encoded image (required)",
                    "min_radius": "Minimum circle radius (optional)",
                    "max_radius": "Maximum circle radius (optional)"
                },
                "returns": "JSON with circle information and base64 result image"
            },
            "/extract": {
                "method": "POST",
                "description": "Extract individual circles as separate images",
                "parameters": {
                    "image": "Image file (required)"
                },
                "returns": "JSON with extracted circle images in base64"
            }
        },
        "supported_formats": list(ALLOWED_EXTENSIONS)
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({"error": "File too large. Maximum size is 16MB"}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 error"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 error"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)