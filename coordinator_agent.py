import streamlit as st
from typing import Optional, Dict, Any
import time

class CoordinatorAgent:
    """Agent responsible for orchestrating communication between all other agents."""
    
    def __init__(self):
        self.agents = {}
        self.system_status = {
            'initialized': False,
            'last_activity': None,
            'total_operations': 0
        }
    
    def register_agent(self, agent_name: str, agent_instance):
        """Register an agent with the coordinator."""
        self.agents[agent_name] = agent_instance
        st.success(f"✅ {agent_name} registered successfully!")
    
    def get_agent(self, agent_name: str):
        """Get a registered agent by name."""
        return self.agents.get(agent_name)
    
    def initialize_system(self) -> bool:
        """Initialize the entire multi-agent system."""
        try:
            st.info("🚀 Initializing Multi-Agent System...")
            
            # Check if all required agents are registered
            required_agents = ['model_management', 'image_processing', 'analysis', 'ui']
            missing_agents = [agent for agent in required_agents if agent not in self.agents]
            
            if missing_agents:
                st.error(f"❌ Missing agents: {', '.join(missing_agents)}")
                return False
            
            # Initialize model management agent
            model_agent = self.agents['model_management']
            success, error = model_agent.initialize_model()
            
            if not success:
                st.error(f"❌ Model initialization failed: {error}")
                return False
            
            self.system_status['initialized'] = True
            self.system_status['last_activity'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            st.success("✅ Multi-Agent System initialized successfully!")
            return True
            
        except Exception as e:
            st.error(f"❌ System initialization failed: {str(e)}")
            return False
    
    def process_image_analysis(self, image, prompt: str = "a photography of", 
                             max_tokens: int = 50) -> Dict[str, Any]:
        """
        Coordinate the complete image analysis workflow.
        
        Args:
            image: PIL Image object
            prompt: Analysis prompt
            max_tokens: Maximum tokens for generation
            
        Returns:
            Dictionary containing analysis results and workflow metadata
        """
        try:
            self.system_status['total_operations'] += 1
            start_time = time.time()
            
            # Step 1: Validate system status
            if not self.system_status['initialized']:
                return {
                    'success': False,
                    'error': 'System not initialized',
                    'workflow_metadata': {}
                }
            
            # Step 2: Preprocess image using image processing agent
            image_agent = self.agents['image_processing']
            processed_image = image_agent.preprocess_image(image)
            
            # Step 3: Perform analysis using analysis agent
            analysis_agent = self.agents['analysis']
            analysis_result = analysis_agent.analyze_image(
                processed_image, 
                prompt, 
                max_tokens
            )
            
            # Step 4: Update system status
            self.system_status['last_activity'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            # Step 5: Add workflow metadata
            end_time = time.time()
            workflow_metadata = {
                'total_processing_time': end_time - start_time,
                'system_operation_count': self.system_status['total_operations'],
                'agents_involved': list(self.agents.keys()),
                'timestamp': self.system_status['last_activity']
            }
            
            analysis_result['workflow_metadata'] = workflow_metadata
            
            return analysis_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Workflow coordination failed: {str(e)}',
                'workflow_metadata': {}
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        status = {
            'system_initialized': self.system_status['initialized'],
            'total_operations': self.system_status['total_operations'],
            'last_activity': self.system_status['last_activity'],
            'registered_agents': list(self.agents.keys()),
            'agent_count': len(self.agents)
        }
        
        # Get individual agent statuses
        agent_statuses = {}
        for agent_name, agent in self.agents.items():
            if hasattr(agent, 'get_model_status'):
                agent_statuses[agent_name] = agent.get_model_status()
            elif hasattr(agent, 'get_statistics'):
                agent_statuses[agent_name] = agent.get_statistics()
            else:
                agent_statuses[agent_name] = {'status': 'active'}
        
        status['agent_statuses'] = agent_statuses
        
        return status
    
    def run_health_check(self) -> Dict[str, Any]:
        """Run a comprehensive health check of all agents."""
        health_report = {
            'overall_health': 'healthy',
            'issues': [],
            'warnings': [],
            'agent_health': {}
        }
        
        for agent_name, agent in self.agents.items():
            agent_health = {'status': 'unknown', 'issues': []}
            
            try:
                # Check if agent has required methods
                if hasattr(agent, 'get_model_status'):
                    status = agent.get_model_status()
                    if not status.get('is_loaded', True):
                        agent_health['status'] = 'warning'
                        agent_health['issues'].append('Model not loaded')
                    else:
                        agent_health['status'] = 'healthy'
                
                elif hasattr(agent, 'get_statistics'):
                    stats = agent.get_statistics()
                    if 'message' in stats:
                        agent_health['status'] = 'info'
                        agent_health['issues'].append(stats['message'])
                    else:
                        agent_health['status'] = 'healthy'
                
                else:
                    agent_health['status'] = 'healthy'
                
            except Exception as e:
                agent_health['status'] = 'error'
                agent_health['issues'].append(f'Exception: {str(e)}')
            
            health_report['agent_health'][agent_name] = agent_health
            
            # Update overall health
            if agent_health['status'] == 'error':
                health_report['overall_health'] = 'unhealthy'
                health_report['issues'].append(f'{agent_name}: {", ".join(agent_health["issues"])}')
            elif agent_health['status'] == 'warning':
                health_report['warnings'].append(f'{agent_name}: {", ".join(agent_health["issues"])}')
        
        return health_report
    
    def cleanup_system(self):
        """Clean up system resources."""
        try:
            st.info("🧹 Cleaning up system resources...")
            
            # Clean up model resources
            if 'model_management' in self.agents:
                self.agents['model_management'].cleanup_resources()
            
            # Clear analysis history
            if 'analysis' in self.agents:
                self.agents['analysis'].clear_history()
            
            # Reset system status
            self.system_status['initialized'] = False
            self.system_status['total_operations'] = 0
            
            st.success("✅ System cleanup completed!")
            
        except Exception as e:
            st.error(f"❌ Cleanup failed: {str(e)}")
    
    def display_system_dashboard(self):
        """Display a comprehensive system dashboard."""
        st.header(" System Dashboard")
        
        # System Status
        status = self.get_system_status()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("System Status", "✅ Active" if status['system_initialized'] else "❌ Inactive")
        
        with col2:
            st.metric("Total Operations", status['total_operations'])
        
        with col3:
            st.metric("Active Agents", status['agent_count'])
        
        with col4:
            st.metric("Last Activity", status['last_activity'] or "Never")
        
        # Health Check
        st.subheader(" System Health")
        health_report = self.run_health_check()
        
        if health_report['overall_health'] == 'healthy':
            st.success("✅ System is healthy")
        elif health_report['overall_health'] == 'unhealthy':
            st.error("❌ System has issues")
        else:
            st.warning("⚠️ System has warnings")
        
        # Display issues and warnings
        if health_report['issues']:
            with st.expander("❌ Issues"):
                for issue in health_report['issues']:
                    st.error(issue)
        
        if health_report['warnings']:
            with st.expander("⚠️ Warnings"):
                for warning in health_report['warnings']:
                    st.warning(warning)
        
        # Agent Status
        st.subheader("🤖 Agent Status")
        for agent_name, agent_health in health_report['agent_health'].items():
            status_emoji = {
                'healthy': '✅',
                'warning': '⚠️',
                'error': '❌',
                'info': 'ℹ️',
                'unknown': '❓'
            }
            
            st.text(f"{status_emoji.get(agent_health['status'], '❓')} {agent_name}: {agent_health['status']}")
            
            if agent_health['issues']:
                for issue in agent_health['issues']:
                    st.text(f"  - {issue}") 