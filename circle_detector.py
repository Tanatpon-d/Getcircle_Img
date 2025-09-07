#!/usr/bin/env python3
"""
Circle Detection in Images using OpenCV
Author: Tanatpon D
"""

import cv2 as cv
import numpy as np
from typing import Optional, Tuple, List
import os
from pathlib import Path


class CircleDetector:
    """Class for detecting circles in images using Hough Circle Transform"""
    
    def __init__(self, min_radius: int = 10, max_radius: int = 200):
        """
        Initialize Circle Detector
        
        Args:
            min_radius: Minimum circle radius to detect
            max_radius: Maximum circle radius to detect
        """
        self.min_radius = min_radius
        self.max_radius = max_radius
    
    def detect_circles(self, 
                      image_path: str,
                      dp: float = 1.2,
                      min_dist: int = 100,
                      param1: int = 50,
                      param2: int = 30) -> Optional[np.ndarray]:
        """
        Detect circles in an image
        
        Args:
            image_path: Path to input image
            dp: Inverse ratio of accumulator resolution
            min_dist: Minimum distance between circle centers
            param1: Upper threshold for Canny edge detector
            param2: Threshold for center detection
            
        Returns:
            Array of circles (x, y, radius) or None if no circles found
        """
        # Read image
        image = cv.imread(image_path)
        if image is None:
            raise ValueError(f"Cannot read image from {image_path}")
        
        # Convert to grayscale
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        gray = cv.medianBlur(gray, 5)
        
        # Detect circles
        circles = cv.HoughCircles(
            gray,
            cv.HOUGH_GRADIENT,
            dp=dp,
            minDist=min_dist,
            param1=param1,
            param2=param2,
            minRadius=self.min_radius,
            maxRadius=self.max_radius
        )
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            return circles
        return None
    
    def draw_circles(self, 
                    image_path: str,
                    circles: np.ndarray,
                    output_path: Optional[str] = None) -> np.ndarray:
        """
        Draw detected circles on image
        
        Args:
            image_path: Path to original image
            circles: Array of circles to draw
            output_path: Optional path to save output image
            
        Returns:
            Image with circles drawn
        """
        image = cv.imread(image_path)
        output = image.copy()
        
        # Draw each circle
        for (x, y, r) in circles:
            # Draw circle outline
            cv.circle(output, (x, y), r, (0, 255, 0), 2)
            # Draw circle center
            cv.circle(output, (x, y), 3, (0, 0, 255), -1)
            # Add label with radius
            cv.putText(output, f"r={r}", (x-20, y-r-10),
                      cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Save output if path provided
        if output_path:
            cv.imwrite(output_path, output)
            print(f"Output saved to {output_path}")
        
        return output
    
    def extract_circles(self,
                       image_path: str,
                       circles: np.ndarray,
                       output_dir: str = "extracted_circles") -> List[str]:
        """
        Extract individual circles as separate images
        
        Args:
            image_path: Path to original image
            circles: Array of circles to extract
            output_dir: Directory to save extracted circles
            
        Returns:
            List of paths to extracted circle images
        """
        image = cv.imread(image_path)
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        extracted_paths = []
        
        for i, (x, y, r) in enumerate(circles):
            # Create mask for circle
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv.circle(mask, (x, y), r, 255, -1)
            
            # Extract circle region
            x1 = max(0, x - r)
            y1 = max(0, y - r)
            x2 = min(image.shape[1], x + r)
            y2 = min(image.shape[0], y + r)
            
            # Crop and apply mask
            cropped = image[y1:y2, x1:x2]
            mask_cropped = mask[y1:y2, x1:x2]
            
            # Create circular image
            result = cv.bitwise_and(cropped, cropped, mask=mask_cropped)
            
            # Save extracted circle
            output_path = os.path.join(output_dir, f"circle_{i+1}.png")
            cv.imwrite(output_path, result)
            extracted_paths.append(output_path)
            
        print(f"Extracted {len(extracted_paths)} circles to {output_dir}/")
        return extracted_paths
    
    def get_circle_info(self, circles: np.ndarray) -> dict:
        """
        Get statistical information about detected circles
        
        Args:
            circles: Array of detected circles
            
        Returns:
            Dictionary with circle statistics
        """
        if circles is None or len(circles) == 0:
            return {"count": 0}
        
        radii = circles[:, 2]
        
        return {
            "count": len(circles),
            "average_radius": float(np.mean(radii)),
            "min_radius": int(np.min(radii)),
            "max_radius": int(np.max(radii)),
            "std_radius": float(np.std(radii)),
            "circles": [
                {"x": int(x), "y": int(y), "radius": int(r)}
                for x, y, r in circles
            ]
        }


def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Detect circles in images")
    parser.add_argument("image", help="Path to input image")
    parser.add_argument("-o", "--output", help="Path to save output image")
    parser.add_argument("-e", "--extract", action="store_true",
                       help="Extract individual circles")
    parser.add_argument("--min-radius", type=int, default=10,
                       help="Minimum circle radius (default: 10)")
    parser.add_argument("--max-radius", type=int, default=200,
                       help="Maximum circle radius (default: 200)")
    parser.add_argument("--show", action="store_true",
                       help="Display result image")
    
    args = parser.parse_args()
    
    # Initialize detector
    detector = CircleDetector(
        min_radius=args.min_radius,
        max_radius=args.max_radius
    )
    
    # Detect circles
    print(f"Detecting circles in {args.image}...")
    circles = detector.detect_circles(args.image)
    
    if circles is None:
        print("No circles detected!")
        return
    
    # Get circle info
    info = detector.get_circle_info(circles)
    print(f"\nDetected {info['count']} circles:")
    print(f"  Average radius: {info['average_radius']:.1f}")
    print(f"  Radius range: {info['min_radius']} - {info['max_radius']}")
    
    # Draw circles on image
    output = detector.draw_circles(args.image, circles, args.output)
    
    # Extract individual circles
    if args.extract:
        detector.extract_circles(args.image, circles)
    
    # Show result
    if args.show:
        cv.imshow("Detected Circles", output)
        print("\nPress any key to close...")
        cv.waitKey(0)
        cv.destroyAllWindows()


if __name__ == "__main__":
    main()