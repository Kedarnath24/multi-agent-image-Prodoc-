import torch
from PIL import Image
import io
import requests
import streamlit as st
from typing import Union, Optional, Tuple

class ImageProcessingAgent:
    #Agent responsible for image processing, loading, and validation.
    
    def __init__(self):
        self.supported_formats = ['png', 'jpg', 'jpeg', 'gif', 'bmp']
        self.max_image_size = 10 * 1024 * 1024  # 10MB limit
    
    def validate_image_format(self, filename: str) -> bool:
        """Validate if the image format is supported."""
        if not filename:
            return False
        
        file_extension = filename.lower().split('.')[-1]
        return file_extension in self.supported_formats
    
    def validate_image_size(self, file_size: int) -> bool:
        """Validate if the image size is within acceptable limits."""
        return file_size <= self.max_image_size
    
    def load_image_from_file(self, uploaded_file) -> Tuple[Optional[Image.Image], Optional[str]]:
        """Load image from uploaded file."""
        try:
            if uploaded_file is None:
                return None, "No file uploaded"
            
            # Validate file format
            if not self.validate_image_format(uploaded_file.name):
                return None, f"Unsupported file format. Supported formats: {', '.join(self.supported_formats)}"
            
            # Validate file size
            uploaded_file.seek(0, 2)  # Seek to end
            file_size = uploaded_file.tell()
            uploaded_file.seek(0)  # Reset to beginning
            
            if not self.validate_image_size(file_size):
                return None, f"File too large. Maximum size: {self.max_image_size // (1024*1024)}MB"
            
            # Load image
            image_data = uploaded_file.read()
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
            
            st.success("✅ Image loaded successfully!")
            return image, None
            
        except Exception as e:
            return None, f"Error loading image: {str(e)}"
    
    def load_image_from_url(self, url: str) -> Tuple[Optional[Image.Image], Optional[str]]:
        """Load image from URL."""
        try:
            if not url or not url.strip():
                return None, "No URL provided"
            
            # Validate URL format
            if not url.startswith(('http://', 'https://')):
                return None, "Invalid URL format. Must start with http:// or https://"
            
            # Download image
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Validate content type
            content_type = response.headers.get('content-type', '').lower()
            if not any(format_type in content_type for format_type in ['image/', 'jpeg', 'png', 'gif', 'bmp']):
                return None, "URL does not point to a valid image file"
            
            # Load image
            image = Image.open(io.BytesIO(response.content)).convert("RGB")
            
            st.success("✅ Image loaded from URL successfully!")
            return image, None
            
        except requests.exceptions.RequestException as e:
            return None, f"Error downloading image: {str(e)}"
        except Exception as e:
            return None, f"Error processing image from URL: {str(e)}"
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for analysis."""
        try:
            # Convert to RGB if not already
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too large (optional optimization)
            max_dimension = 1024
            if max(image.size) > max_dimension:
                ratio = max_dimension / max(image.size)
                new_size = tuple(int(dim * ratio) for dim in image.size)
                image = image.resize(new_size, Image.Resampling.LANCZOS)
                st.info(f"Image resized to {new_size} for optimal processing")
            
            return image
            
        except Exception as e:
            st.error(f"Error preprocessing image: {str(e)}")
            return image
    
    def get_image_info(self, image: Image.Image) -> dict:
        """Get basic information about the image."""
        return {
            'size': image.size,
            'mode': image.mode,
            'format': getattr(image, 'format', 'Unknown'),
            'width': image.width,
            'height': image.height
        } 