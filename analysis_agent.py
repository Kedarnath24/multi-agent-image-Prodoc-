import torch
from PIL import Image
import streamlit as st
from typing import Optional, Dict, Any
import time

class AnalysisAgent:
    """Agent responsible for performing image analysis using the BLIP model."""
    
    def __init__(self, model_management_agent):
        self.model_agent = model_management_agent
        self.analysis_history = []
    
    def analyze_image(self, image: Image.Image, prompt: str = "Describe the image", 
                     max_tokens: int = 50) -> Dict[str, Any]:
        
        try:
            # Check if model is loaded
            if not self.model_agent.is_loaded:
                return {
                    'success': False,
                    'error': 'Model not loaded. Please initialize the model first.',
                    'caption': None,
                    'metadata': {}
                }
            
            start_time = time.time()
            
            # Prepare inputs for the model
            inputs = self.model_agent.processor(
                image, 
                text=prompt, 
                return_tensors="pt"
            ).to(self.model_agent.device)
            
            # Generate caption
            with st.spinner("🤖 Generating caption..."):
                with torch.no_grad():  # Disable gradient computation for inference
                    outputs = self.model_agent.model.generate(
                        **inputs, 
                        max_new_tokens=max_tokens,
                        do_sample=True,
                        temperature=0.7,
                        top_p=0.9
                    )
            
            # Decode the generated tokens
            caption = self.model_agent.processor.decode(
                outputs[0], 
                skip_special_tokens=True
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Create result
            result = {
                'success': True,
                'caption': caption,
                'prompt': prompt,
                'max_tokens': max_tokens,
                'processing_time': processing_time,
                'metadata': {
                    'model_id': self.model_agent.model_id,
                    'device': self.model_agent.device,
                    'image_size': image.size,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            
            # Store in history
            self.analysis_history.append(result)
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Analysis failed: {str(e)}",
                'caption': None,
                'metadata': {}
            }
    
    def analyze_with_multiple_prompts(self, image: Image.Image, 
        prompts: list, 
        max_tokens: int = 50) -> Dict[str, Any]:
        """
        Analyze an image with multiple prompts and return the best result.
        
        Args:
            image: PIL Image object
            prompts: List of prompts to try
            max_tokens: Maximum number of tokens in the generated description
            
        Returns:
            Dictionary containing the best analysis result
        """
        results = []
        
        for i, prompt in enumerate(prompts):
            st.info(f"Trying prompt {i+1}/{len(prompts)}: '{prompt}'")
            
            result = self.analyze_image(image, prompt, max_tokens)
            results.append(result)
            
            if result['success']:
                st.success(f"✅ Generated: {result['caption']}")
            else:
                st.error(f"❌ Failed: {result['error']}")
        
        # Return the first successful result, or the last result if all failed
        for result in results:
            if result['success']:
                return result
        
        return results[-1] if results else {
            'success': False,
            'error': 'All analysis attempts failed',
            'caption': None,
            'metadata': {}
        }
    
    def get_analysis_history(self, limit: int = 10) -> list:
        """Get recent analysis history."""
        return self.analysis_history[-limit:] if self.analysis_history else []
    
    def clear_history(self):
        """Clear analysis history."""
        self.analysis_history.clear()
        st.toast("✅ Analysis history cleared!", icon="✅")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get analysis statistics."""
        if not self.analysis_history:
            return {"message": "No analysis history available"}
        
        successful_analyses = [r for r in self.analysis_history if r['success']]
        failed_analyses = [r for r in self.analysis_history if not r['success']]
        
        total_time = sum(r.get('processing_time', 0) for r in successful_analyses)
        avg_time = total_time / len(successful_analyses) if successful_analyses else 0
        
        return {
            'total_analyses': len(self.analysis_history),
            'successful_analyses': len(successful_analyses),
            'failed_analyses': len(failed_analyses),
            'success_rate': len(successful_analyses) / len(self.analysis_history) * 100,
            'average_processing_time': avg_time,
            'total_processing_time': total_time
        } 