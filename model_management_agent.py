import torch
import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from typing import Tuple, Optional
import gc

class ModelManagementAgent:
    """Agent responsible for model loading, caching, and device management."""
    
    def __init__(self):
        self.model_id = "Salesforce/blip-image-captioning-large"
        self.model = None
        self.processor = None
        self.device = None
        self.is_loaded = False
    
    def get_device_info(self) -> str:
        """Determine the best available device for model execution."""
        if torch.cuda.is_available():
            device = "cuda"
            # Get GPU info
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            st.info(f"🚀 Using GPU: {gpu_name} ({gpu_memory:.1f}GB)")
        else:
            device = "cpu"
            st.info("💻 Using CPU for inference")
        
        return device
    
    @staticmethod
    @st.cache_resource
    def _load_processor_cached(model_id: str):
        """Load the BLIP processor with caching (no UI elements)."""
        try:
            processor = BlipProcessor.from_pretrained(model_id)
            return processor, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    @st.cache_resource
    def _load_model_cached(model_id: str, device: str):
        """Load the BLIP model with caching (no UI elements)."""
        try:
            model = BlipForConditionalGeneration.from_pretrained(model_id).to(device)
            return model, None
        except Exception as e:
            return None, str(e)
    
    def load_processor(self):
        """Load the BLIP processor with UI feedback."""
        with st.spinner("Loading model processor..."):
            processor, error = self._load_processor_cached(self.model_id)
        
        if processor is not None:
            st.success("✅ Processor loaded successfully!")
        else:
            st.error(f"❌ Error loading processor: {error}")
        
        return processor
    
    def load_model(self, device: str):
        """Load the BLIP model with UI feedback."""
        with st.spinner("Loading model... (This may take a while on first run)"):
            model, error = self._load_model_cached(self.model_id, device)
        
        if model is not None:
            st.success("✅ Model loaded successfully!")
        else:
            st.error(f"❌ Error loading model: {error}")
        
        return model
    
    def initialize_model(self) -> Tuple[bool, Optional[str]]:
        """Initialize the model and processor."""
        try:
            # Get device
            self.device = self.get_device_info()
            
            # Load processor
            self.processor = self.load_processor()
            if self.processor is None:
                return False, "Failed to load processor"
            
            # Load model
            self.model = self.load_model(self.device)
            if self.model is None:
                return False, "Failed to load model"
            
            self.is_loaded = True
            return True, None
            
        except Exception as e:
            return False, f"Error initializing model: {str(e)}"
    
    def get_model_status(self) -> dict:
        """Get current model status."""
        return {
            'is_loaded': self.is_loaded,
            'device': self.device,
            'model_id': self.model_id,
            'has_model': self.model is not None,
            'has_processor': self.processor is not None
        }
    
    def cleanup_resources(self):
        """Clean up model resources to free memory."""
        try:
            if self.model is not None:
                del self.model
                self.model = None
            
            if self.processor is not None:
                del self.processor
                self.processor = None
            
            # Clear cache
            st.cache_resource.clear()
            
            # Force garbage collection
            gc.collect()
            
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            self.is_loaded = False
            st.success("✅ Resources cleaned up successfully!")
            
        except Exception as e:
            st.error(f"❌ Error cleaning up resources: {str(e)}")
    
    def get_model_info(self) -> dict:
        """Get detailed information about the loaded model."""
        if not self.is_loaded:
            return {"error": "Model not loaded"}
        
        info = {
            'model_id': self.model_id,
            'device': self.device,
            'model_type': type(self.model).__name__,
            'processor_type': type(self.processor).__name__,
        }
        
        if torch.cuda.is_available():
            info.update({
                'gpu_name': torch.cuda.get_device_name(0),
                'gpu_memory_allocated': f"{torch.cuda.memory_allocated(0) / (1024**3):.2f}GB",
                'gpu_memory_cached': f"{torch.cuda.memory_reserved(0) / (1024**3):.2f}GB"
            })
        
        return info 