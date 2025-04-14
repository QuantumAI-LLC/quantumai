"""
Quantum Circuit Simulator - Main Application
"""
import streamlit as st

# Import utility modules
from utils.simulator import load_user_applications
from utils.ui import configure_page_style, render_app_header

# Import component modules
from components.predefined_tab import render_predefined_tab
from components.user_modules_tab import render_user_modules_tab
from components.create_module_tab import render_create_module_tab

# Import examples and templates
from examples.examples import examples
from templates.templates import templates

def main():
    """Main application entry point"""
    # Configure page styling
    configure_page_style()
    
    # Display application header with robot animation
    render_app_header()
    
    # Initialize session state for application state management
    if 'creating_new_app' not in st.session_state:
        st.session_state.creating_new_app = False
    if 'editing_app' not in st.session_state:
        st.session_state.editing_app = False
    if 'edit_app_name' not in st.session_state:
        st.session_state.edit_app_name = ""
    
    # Load user-defined applications
    user_applications = load_user_applications()
    
    # Create tabs for different sections with custom styling
    st.markdown("<div class='tabs-container'>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs([
        "🔬 PREDEFINED MODULES", 
        "💾 USER MODULES", 
        "🔧 CREATE NEW MODULE"
    ])
    
    # Render each tab with its component
    with tab1:
        render_predefined_tab(examples)
    
    with tab2:
        render_user_modules_tab(user_applications)
    
    with tab3:
        render_create_module_tab(user_applications, templates)

if __name__ == "__main__":
    main()
