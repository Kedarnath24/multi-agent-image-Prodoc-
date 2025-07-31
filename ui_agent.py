import streamlit as st
from PIL import Image
from typing import Optional, Dict, Any
import json

class UIAgent:
    """Agent responsible for handling the Streamlit user interface."""
    
    def __init__(self):
        self.example_prompts = [
            "describe this image in detail",
            "what is happening in this image",
            "analyze the texts in this image, if any",
            "describe the scene and mood of this image",
            "what can you see in this picture",
        ]
    
    def setup_page(self):
        """Setup the main page configuration."""
        st.set_page_config(
            page_title="Multi-Agent Image Analysis System",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for better styling
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1rem;
        }
        .agent-status {
            padding: 0.5rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        .success-status {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .error-status {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .info-status {
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Render the main header."""
        st.markdown('<h1 class="main-header">🤖 Multi-Agent Image Analysis System</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <p style="font-size: 1.2rem; color: #666;">
                Upload an image and get detailed analysis using our intelligent multi-agent system!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self, model_agent, analysis_agent):
        """Render the sidebar with settings and controls."""

        model_status = model_agent.get_model_status()
        
        if model_status['is_loaded']:
            st.sidebar.markdown('<div class="agent-status success-status">✅ Model Loaded</div>', unsafe_allow_html=True)
            st.sidebar.text(f"Device: {model_status['device']}")
        else:
            st.sidebar.markdown('<div class="agent-status error-status">❌ Model Not Loaded</div>', unsafe_allow_html=True)
        
        # Analysis Settings
        st.sidebar.subheader("📝 Analysis Settings")
        
        default_prompt = st.sidebar.text_input(
            "Custom Prompt",
            value="a photography of",
            help="Enter a custom prompt to guide the image analysis"
        )
        
        max_tokens = st.sidebar.slider(
            "Maximum Tokens",
            min_value=10,
            max_value=100,
            value=50,
            help="Maximum number of tokens in the generated description"
        )






        
        # Quick Actions
        st.sidebar.subheader("QUICK ACTIONS")
        
        if st.sidebar.button("🔄 Refresh Model", help="Reload the model"):
            st.rerun()
        
        if st.sidebar.button("🗑️ Clear History", help="Clear analysis history"):
            analysis_agent.clear_history()
            st.rerun()
        
        if st.sidebar.button("🧹 Cleanup Resources", help="Free up memory"):
            model_agent.cleanup_resources()
            st.rerun()
        




        # System Info
        st.sidebar.subheader("ℹ️ System Info")
        if model_status['is_loaded']:
            model_info = model_agent.get_model_info()
            for key, value in model_info.items():
                if key != 'error':
                    st.sidebar.text(f"{key}: {value}")
        
        return default_prompt, max_tokens
    


    def render_upload_section(self, image_agent) -> tuple:
        st.header(" Upload Image")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📁 File Upload")
            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
                help="Upload an image to analyze"
            )
            
            if uploaded_file is not None:
                image, error = image_agent.load_image_from_file(uploaded_file)
                if image:
                    image = image_agent.preprocess_image(image)
                    st.image(image, caption="Uploaded Image", use_column_width=True)
                    
                    # Show image info
                    info = image_agent.get_image_info(image)
                    st.info(f" Image Info: {info['width']}x{info['height']} pixels, {info['mode']} mode")
                    
                    return image, None
                else:
                    st.error(f"❌ {error}")
                    return None, error
        
        with col2:
            st.subheader("🌐 URL Input")
            image_url = st.text_input(
                "Or enter image URL",
                placeholder="https://example.com/image.jpg",
                help="Alternatively, provide a direct URL to an image"
            )
            
            if image_url:
                image, error = image_agent.load_image_from_url(image_url)
                if image:
                    image = image_agent.preprocess_image(image)
                    st.image(image, caption="Image from URL", use_column_width=True)
                    
                    # Show image info
                    info = image_agent.get_image_info(image)
                    st.info(f" Image Info: {info['width']}x{info['height']} pixels, {info['mode']} mode")
                    
                    return image, None
                else:
                    st.error(f"❌ {error}")
                    return None, error
        
        return None, None
    
    def render_analysis_section(self, image, analysis_agent, default_prompt, max_tokens):
        """Render the analysis section."""
        st.header(" Analysis Results")
        
        if image is None:
            st.warning("⚠️ Please upload an image or provide an image URL first. ⚠️")
            return
        
        # Analysis button
        col1, col2 = st.columns([1, 3])
        
        with col1:
            if st.button("Analyze Image", type="primary", use_container_width=True):
                with st.spinner("Analyzing image..."):
                    result = analysis_agent.analyze_image(image, default_prompt, max_tokens)
                    self.display_analysis_result(result)
        
        with col2:
            if st.button("Multi-Prompt Analysis", use_container_width=True):
                with st.spinner("Running multi-prompt analysis..."):
                    result = analysis_agent.analyze_with_multiple_prompts(
                        image, 
                        self.example_prompts[:3], 
                        max_tokens
                    )
                    self.display_analysis_result(result)
        
        # Example prompts
        st.subheader("💡 Example Prompts")
        cols = st.columns(3)
        
        for i, prompt in enumerate(self.example_prompts):
            col_idx = i % 3
            with cols[col_idx]:
                if st.button(prompt, key=f"prompt_{i}", use_container_width=True):
                    st.session_state.custom_prompt = prompt
                    st.rerun()
    
    def display_analysis_result(self, result: Dict[str, Any]):
        """Display analysis results."""
        if result['success']:
            st.success("✅ Analysis Complete!")
            
            # Display caption
            st.subheader(" Generated Description:")
            st.markdown(f"**{result['caption']}**")
            
            # Display metadata
            with st.expander(" Analysis Details"):
                metadata = result['metadata']
                st.json({
                    "Processing Time": f"{result['processing_time']:.2f} seconds",
                    "Prompt Used": result['prompt'],
                    "Max Tokens": result['max_tokens'],
                    "Model": metadata['model_id'],
                    "Device": metadata['device'],
                    "Image Size": metadata['image_size'],
                    "Timestamp": metadata['timestamp']
                })
            
            # Copy button
            st.code(result['caption'], language="text")
            
        else:
            st.error(f"❌ Analysis Failed: {result['error']}")
    
    def render_history_section(self, analysis_agent):
        """Render the analysis history section."""
        st.header("📚 Analysis History")
        
        history = analysis_agent.get_analysis_history(limit=5)
        
        if not history:
            st.info("No analysis history available. Run some analyses to see history here!")
            return
        
        for i, result in enumerate(reversed(history)):
            with st.expander(f"Analysis {len(history) - i} - {result['metadata']['timestamp']}"):
                if result['success']:
                    st.markdown(f"**Caption:** {result['caption']}")
                    st.text(f"Prompt: {result['prompt']}")
                    st.text(f"Processing Time: {result['processing_time']:.2f}s")
                else:
                    st.error(f"Failed: {result['error']}")
    
    def render_statistics_section(self, analysis_agent):
        """Render the statistics section."""
        st.header(" Statistics")
        
        stats = analysis_agent.get_statistics()
        
        if 'message' in stats:
            st.info(stats['message'])
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Analyses", stats['total_analyses'])
        
        with col2:
            st.metric("Success Rate", f"{stats['success_rate']:.1f}%")
        
        with col3:
            st.metric("Avg Time", f"{stats['average_processing_time']:.2f}s")
        
        with col4:
            st.metric("Failed", stats['failed_analyses']) 