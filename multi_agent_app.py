import streamlit as st
from PIL import Image
import sys
import os

# Add the agents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))

# Import all agents
from agents.image_processing_agent import ImageProcessingAgent
from agents.model_management_agent import ModelManagementAgent
from agents.analysis_agent import AnalysisAgent
from agents.ui_agent import UIAgent
from agents.coordinator_agent import CoordinatorAgent

def main():
    """Main application function that orchestrates the multi-agent system."""
    
    # Initialize the coordinator
    coordinator = CoordinatorAgent()
    
    # Initialize all agents
    image_agent = ImageProcessingAgent()
    model_agent = ModelManagementAgent()
    analysis_agent = AnalysisAgent(model_agent)
    ui_agent = UIAgent()
    
    # Register all agents with the coordinator
    coordinator.register_agent('image_processing', image_agent)
    coordinator.register_agent('model_management', model_agent)
    coordinator.register_agent('analysis', analysis_agent)
    coordinator.register_agent('ui', ui_agent)
    
    # Setup the UI
    ui_agent.setup_page()
    ui_agent.render_header()
    
    # Initialize the system
    if not coordinator.system_status['initialized']:
        if coordinator.initialize_system():
            st.success("🎉 Multi-Agent System is ready!")
        else:
            st.error("❌ Failed to initialize the system. Please check the logs.")
            return
    
    # Render sidebar and get settings
    default_prompt, max_tokens = ui_agent.render_sidebar(model_agent, analysis_agent)
    
    # Handle custom prompt from session state
    if 'custom_prompt' in st.session_state:
        default_prompt = st.session_state.custom_prompt
        del st.session_state.custom_prompt
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload & Analyze", "📊 Dashboard", "📚 History", "ℹ️ About"])
    
    with tab1:
        # Render upload section
        image, error = ui_agent.render_upload_section(image_agent)
        
        # Render analysis section
        ui_agent.render_analysis_section(image, analysis_agent, default_prompt, max_tokens)
    
    with tab2:
        # Render system dashboard
        coordinator.display_system_dashboard()
        
        # Render statistics
        ui_agent.render_statistics_section(analysis_agent)
    
    with tab3:
        # Render history section
        ui_agent.render_history_section(analysis_agent)
    
    with tab4:
        # About section
        st.header("🤖 About Multi-Agent Image Analysis System")
        
        st.markdown("""
        This is a sophisticated multi-agent system for image analysis built using Streamlit and the BLIP model.
        
        ### 🏗️ System Architecture
        
        The system consists of five specialized agents:
        
        **1. Image Processing Agent** 
        - Handles image loading, validation, and preprocessing
        - Supports multiple image formats and URL inputs
        - Performs image optimization and format conversion
        
        **2. Model Management Agent** 
        - Manages the BLIP model loading and caching
        - Handles device selection (CPU/GPU)
        - Provides model status and resource management
        
        **3. Analysis Agent** 
        - Performs the actual image analysis using the BLIP model
        - Supports multiple prompts and analysis strategies
        - Maintains analysis history and statistics
        
        **4. UI Agent** 
        - Handles all user interface components
        - Manages user interactions and display logic
        - Provides a modern, responsive interface
        
        **5. Coordinator Agent** 
        - Orchestrates communication between all agents
        - Manages system workflow and error handling
        - Provides system health monitoring and status reporting
        
        ### 🚀 Features
        
        - **Multi-Agent Architecture**: Modular, scalable design
        - **Real-time Analysis**: Fast image processing and caption generation
        - **Multiple Input Methods**: File upload and URL input support
        - **Custom Prompts**: Flexible prompt customization
        - **Analysis History**: Track and review previous analyses
        - **System Monitoring**: Real-time system health and performance metrics
        - **Resource Management**: Efficient memory and GPU utilization
        
        ### 🛠️ Technical Stack
        
        - **Frontend**: Streamlit
        - **AI Model**: BLIP (Bootstrapping Language-Image Pre-training)
        - **Image Processing**: PIL (Python Imaging Library)
        - **Deep Learning**: PyTorch, Transformers
        - **Architecture**: Multi-Agent System Design Pattern
        
        ### 📈 Performance
        
        - **GPU Acceleration**: Automatic GPU detection and utilization
        - **Caching**: Intelligent model and result caching
        - **Optimization**: Image preprocessing for optimal performance
        - **Memory Management**: Efficient resource cleanup and management
        
        ### 🔧 Usage
        
        1. **Upload an Image**: Use the file uploader or provide an image URL
        2. **Configure Settings**: Adjust prompt and token settings in the sidebar
        3. **Run Analysis**: Click "Analyze Image" or "Multi-Prompt Analysis"
        4. **View Results**: See generated captions and detailed metadata
        5. **Monitor System**: Check the dashboard for system status and statistics
        
        ### 🎯 Use Cases
        
        - **Content Analysis**: Analyze images for content description
        - **Accessibility**: Generate alt-text for images
        - **Research**: Study image understanding capabilities
        - **Education**: Learn about computer vision and NLP
        - **Prototyping**: Test image analysis workflows
        
        ### 🔮 Future Enhancements
        
        - Support for video analysis
        - Multiple model selection
        - Batch processing capabilities
        - Advanced prompt engineering
        - Export and sharing features
        - API integration capabilities
        """)
        
        # System information
        st.subheader("📋 System Information")
        
        system_info = coordinator.get_system_status()
        st.json(system_info)

if __name__ == "__main__":
    main() 