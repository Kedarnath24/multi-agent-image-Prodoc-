"""
Multi-Agent Image Analysis System

This package contains specialized agents for image analysis using the BLIP model.
Each agent has a specific responsibility in the overall system architecture.

Agents:
- ImageProcessingAgent: Handles image loading, validation, and preprocessing
- ModelManagementAgent: Manages model loading, caching, and device selection
- AnalysisAgent: Performs image analysis using the BLIP model
- UIAgent: Handles Streamlit interface and user interactions
- CoordinatorAgent: Orchestrates communication between all agents
"""

from .image_processing_agent import ImageProcessingAgent
from .model_management_agent import ModelManagementAgent
from .analysis_agent import AnalysisAgent
from .ui_agent import UIAgent
from .coordinator_agent import CoordinatorAgent

__all__ = [
    'ImageProcessingAgent',
    'ModelManagementAgent', 
    'AnalysisAgent',
    'UIAgent',
    'CoordinatorAgent'
]

__version__ = '1.0.0'
__author__ = 'Multi-Agent System Team'
__description__ = 'A sophisticated multi-agent system for image analysis using BLIP model' 