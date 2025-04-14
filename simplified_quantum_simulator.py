import streamlit as st

# Ensure Streamlit is imported at the very top of the file
st.set_page_config(
    page_title="Quantum Circuit Simulator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"  # Changed to expanded for better navigation
)

# Import necessary libraries and modules
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import io
import sys
import json
import os
import base64
import numpy as np
from datetime import datetime

# Import tab components
from components.predefined_tab import render_predefined_tab
from components.user_modules_tab import render_user_modules_tab
from components.create_module_tab import render_create_module_tab
from components.visualization_3d import render_3d_visualization_tab

# Import examples and utilities
from examples.examples import examples
from utils.simulator import load_user_applications, save_user_applications, run_with_simulator
from utils.ui import display_success_message, display_error_message, display_terminal_output
from utils.simulator import global_simulator
from templates.templates import templates

# Custom CSS for simplified but still attractive styling
st.markdown("""
<style>
    /* Main background and text colors */
    .stApp {
        background-color: #0a0a1a;
        color: #00ffcc;
    }
    
    /* Header styling - simplified */
    h1, h2, h3 {
        color: #00ffcc !important;
        font-family: 'Arial', sans-serif; /* Simplified font */
        text-shadow: 0 0 5px #00ffcc80; /* Reduced shadow effect */
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Button styling - larger size, more contrast */
    .stButton button {
        background-color: #222244 !important;
        color: #00ffcc !important;
        border: 2px solid #00ffcc !important;
        border-radius: 5px !important;
        box-shadow: 0 0 5px #00ffcc80 !important; /* Reduced shadow */
        transition: all 0.2s !important;
        font-size: 1rem !important; /* Larger font */
        padding: 0.5rem 1rem !important; /* More padding */
        margin: 0.5rem 0 !important;
        width: 100%; /* Full width buttons */
    }
    
    .stButton button:hover {
        background-color: #00ffcc !important;
        color: #222244 !important;
    }
    
    /* Input fields - simplified */
    .stTextInput input, .stTextArea textarea, .stSelectbox, .stMultiselect {
        background-color: #222244 !important;
        color: #00ffcc !important;
        border: 1px solid #00ffcc !important;
        border-radius: 5px !important;
        font-size: 1rem !important;
    }
    
    /* Card styling - simplified with clear labeling */
    .quantum-card {
        background-color: #222244;
        border: 1px solid #00ffcc;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0; /* More margin */
        box-shadow: 0 0 5px #00ffcc80;
    }
    
    /* Make cards more obviously clickable */
    .quantum-card:hover {
        border: 2px solid #00ffcc;
        cursor: pointer;
    }
    
    /* Make the module title more prominent */
    .module-title {
        font-size: 1.3rem !important;
        font-weight: bold !important;
        margin-bottom: 10px !important;
        text-align: center !important;
    }
    
    /* Code area - improved readability */
    .stCodeBlock {
        background-color: #1a1a2e !important;
        border: 1px solid #00ffcc !important;
        padding: 10px !important;
        font-size: 0.9rem !important;
    }
    
    /* Tab styling - larger and more obvious */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #222244;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        border: 1px solid #00ffcc;
        font-size: 1.1rem; /* Larger font */
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00ffcc;
        color: #222244;
        font-weight: bold;
    }
    
    /* Error message styling - more prominent */
    .error-message {
        background-color: rgba(255, 50, 50, 0.2);
        border: 1px solid #ff3232;
        color: #ff6666;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-weight: bold;
    }
    
    /* Navigation menu */
    .nav-menu {
        position: fixed;
        top: 10px;
        right: 10px;
        background-color: #222244;
        border: 1px solid #00ffcc;
        border-radius: 5px;
        padding: 10px;
        z-index: 999;
    }
    
    .nav-item {
        display: block;
        padding: 5px 10px;
        color: #00ffcc;
        text-decoration: none;
        margin: 5px 0;
        border-radius: 3px;
    }
    
    .nav-item:hover {
        background-color: #00ffcc;
        color: #222244;
    }
    
    /* Add more whitespace and improve readability */
    .content-section {
        margin: 20px 0;
        padding: 15px;
    }
    
    /* Simple tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #00ffcc;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #222244;
        color: #00ffcc;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        border: 1px solid #00ffcc;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Adding section dividers */
    .section-divider {
        border-bottom: 1px solid #00ffcc80;
        margin: 30px 0;
    }
</style>

<link href="https://fonts.googleapis.com/css2?family=Arial:wght@400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Simple navigation menu HTML
nav_menu = """
<div class="nav-menu">
    <a class="nav-item" href="#predefined">Predefined Modules</a>
    <a class="nav-item" href="#user">User Modules</a>
    <a class="nav-item" href="#create">Create Module</a>
    <a class="nav-item" href="#help">Help</a>
</div>
"""

st.markdown(nav_menu, unsafe_allow_html=True)

# Helper function to add simplified robot icon
def get_robot_icon():
    # Simpler robot icon SVG
    robot_svg = '''
    <svg width="80" height="80" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <rect x="30" y="20" width="40" height="30" rx="5" fill="#222244" stroke="#00ffcc" stroke-width="2" />
      <circle cx="40" cy="35" r="5" fill="#00ffcc" />
      <circle cx="60" cy="35" r="5" fill="#00ffcc" />
      <rect x="42" y="50" width="16" height="3" fill="#00ffcc" />
      <rect x="20" y="50" width="60" height="20" rx="5" fill="#222244" stroke="#00ffcc" stroke-width="2" />
    </svg>
    '''
    return f'<div style="display: flex; justify-content: center; margin-bottom: 10px;">{robot_svg}</div>'

# Simplified title with robot icon
st.markdown(get_robot_icon(), unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>QUANTUM CIRCUIT SIMULATOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 20px; color: #00ffcc;'>A simplified interface for quantum computing simulations</p>", unsafe_allow_html=True)

# Quick help section
with st.expander("📚 How to use this simulator"):
    st.markdown("""
    ### Quick Start Guide:
    1. **Select a Module**: Choose a predefined quantum module from the list below
    2. **Click the SELECT MODULE button**: This loads the module into the editor
    3. **Execute the Module**: Click the EXECUTE button to run the simulation
    4. **View Results**: See the results displayed in the output area
    
    Need help? Click the Help nav item for more detailed instructions.
    """)

# Initialize session state
if 'creating_new_app' not in st.session_state:
    st.session_state.creating_new_app = False
if 'editing_app' not in st.session_state:
    st.session_state.editing_app = False
if 'edit_app_name' not in st.session_state:
    st.session_state.edit_app_name = ""
if 'selected_module' not in st.session_state:
    st.session_state.selected_module = None

# Load user-defined applications
user_applications = load_user_applications()

# Main application layout with tabs - simplified labels
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Predefined Modules", 
    "💾 My Modules", 
    "✏️ Create Module",
    "🔮 3D View" 
])

with tab1:
    st.markdown("<div id='predefined'></div>", unsafe_allow_html=True)
    st.markdown("### Available Quantum Modules")
    st.markdown("Select a module below to get started:")
    
    # Call the render function with a simplified=True parameter
    # (You'll need to modify this function in the predefined_tab.py)
    render_predefined_tab(examples)

with tab2:
    st.markdown("<div id='user'></div>", unsafe_allow_html=True)
    st.markdown("### Your Saved Modules")
    
    # Add a simple filter/search box for user modules
    search_term = st.text_input("Filter modules:", "")
    
    render_user_modules_tab(user_applications)

with tab3:
    st.markdown("<div id='create'></div>", unsafe_allow_html=True)
    st.markdown("### Create a New Module")
    
    # Add template selection at the top for easier access
    template_options = ["Basic Circuit", "Algorithm Implementation", "Quantum Machine Learning", "Start from Scratch"]
    selected_template = st.selectbox("Start with a template:", template_options)
    
    render_create_module_tab(user_applications, templates)

with tab4:
    st.markdown("<div id='visualization'></div>", unsafe_allow_html=True)
    st.markdown("### 3D Quantum Circuit Visualization")
    
    render_3d_visualization_tab(examples, user_applications)

# Help section
st.markdown("<div id='help'></div>", unsafe_allow_html=True)
with st.expander("Detailed Help & Documentation"):
    st.markdown("""
    ## How to Use This Quantum Circuit Simulator

    ### Basic Navigation:
    - Use the tabs at the top to switch between different sections
    - The floating menu at the top-right provides quick access to main areas

    ### Working with Predefined Modules:
    1. Browse the available modules in the "Predefined Modules" tab
    2. Click on a module card or its SELECT button
    3. The module will load in the editor area
    4. Click EXECUTE to run the simulation
    5. View the results in the output panel

    ### Common Errors:
    - Import errors: Make sure you're using the proper import statements
    - Measurement errors: Ensure qubits are properly measured before reading results
    - Execution errors: Check that your quantum circuit is properly defined

    ### Tips:
    - Hover over buttons and options to see tooltips with additional information
    - Use the search box to find specific modules
    - Save your work regularly when creating new modules
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #00ffcc80;'>Quantum Circuit Simulator v1.1 | Simplified Interface</p>", unsafe_allow_html=True)
