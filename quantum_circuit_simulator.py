import streamlit as st

# Ensure Streamlit is imported at the very top of the file
st.set_page_config(
    page_title="Quantum AI Circuit Interface",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed"
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
from components.visualization_3d import render_3d_visualization_tab # Import the new 3D tab component

# Import examples and utilities
from examples.examples import examples
from utils.simulator import load_user_applications, save_user_applications, run_with_simulator # Ensure run_with_simulator is imported if needed globally or passed around
from utils.ui import display_success_message, display_error_message, display_terminal_output
from utils.simulator import global_simulator

# Custom CSS for robotic/futuristic styling
st.markdown("""
<style>
    /* Main background and text colors */
    .stApp {
        background-color: #0a0a1a;
        color: #00ffcc;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #00ffcc !important;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 10px #00ffcc80;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #222244 !important;
        color: #00ffcc !important;
        border: 2px solid #00ffcc !important;
        border-radius: 5px !important;
        box-shadow: 0 0 10px #00ffcc80 !important;
        transition: all 0.3s !important;
    }
    
    .stButton button:hover {
        background-color: #00ffcc !important;
        color: #222244 !important;
        box-shadow: 0 0 15px #00ffcc !important;
    }
    
    /* Input fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox, .stMultiselect {
        background-color: #222244 !important;
        color: #00ffcc !important;
        border: 1px solid #00ffcc !important;
        border-radius: 5px !important;
    }
    
    /* Card styling for examples */
    .quantum-card {
        background-color: #222244;
        border: 1px solid #00ffcc;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 10px #00ffcc80;
        transition: all 0.3s;
    }
    
    .quantum-card:hover {
        box-shadow: 0 0 20px #00ffcc;
        transform: scale(1.01);
    }
    
    /* Code area */
    .stCodeBlock {
        background-color: #1a1a2e !important;
        border: 1px solid #00ffcc !important;
    }
    
    /* Apply scrollbar to pre elements inside code blocks */
    pre {
        max-height: 500px !important;
        overflow-y: auto !important;
        display: block !important;
    }
    
    /* Left side code box styling - Applied globally now */
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #222244;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        border: 1px solid #00ffcc;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00ffcc;
        color: #222244;
    }
</style>

<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Helper function to add animated robot icon
def get_robot_animation():
    # Robot icon SVG animation
    robot_svg = '''
    <svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <rect x="30" y="20" width="40" height="30" rx="5" fill="#222244" stroke="#00ffcc" stroke-width="2">
        <animate attributeName="stroke-opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite" />
      </rect>
      <circle cx="40" cy="35" r="5" fill="#00ffcc">
        <animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite" />
      </circle>
      <circle cx="60" cy="35" r="5" fill="#00ffcc">
        <animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite" />
      </circle>
      <rect x="42" y="50" width="16" height="3" fill="#00ffcc">
        <animate attributeName="width" values="16;10;16" dur="2s" repeatCount="indefinite" />
        <animate attributeName="x" values="42;45;42" dur="2s" repeatCount="indefinite" />
      </rect>
      <rect x="20" y="50" width="60" height="20" rx="5" fill="#222244" stroke="#00ffcc" stroke-width="2" />
      <rect x="25" y="70" width="10" height="15" fill="#222244" stroke="#00ffcc" stroke-width="2" />
      <rect x="65" y="70" width="10" height="15" fill="#222244" stroke="#00ffcc" stroke-width="2" />
    </svg>
    '''
    return f'<div style="display: flex; justify-content: center;">{robot_svg}</div>'

# Title with robot animation
st.markdown(get_robot_animation(), unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>QUANTUM AI CIRCUIT INTERFACE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 30px; color: #00ffcc99;'>SELECT QUANTUM MODULE TO INITIATE SIMULATION SEQUENCE</p>", unsafe_allow_html=True)

# Initialize session state for new application creation
if 'creating_new_app' not in st.session_state:
    st.session_state.creating_new_app = False
if 'editing_app' not in st.session_state:
    st.session_state.editing_app = False
if 'edit_app_name' not in st.session_state:
    st.session_state.edit_app_name = ""

# Define application templates
templates = {
    "Basic Circuit": """
from qiskit import QuantumCircuit
# Initialize your quantum circuit here
qc = QuantumCircuit(2, 2)
# Add gates to your circuit
qc.h(0)
qc.cx(0, 1)
# Add measurements
qc.measure([0, 1], [0, 1])
# Run simulation
counts = run_with_simulator(qc)
print(counts)
""",
    "Algorithm Implementation": """
from qiskit import QuantumCircuit
# Define your quantum algorithm here
def my_algorithm(params):
    qc = QuantumCircuit(3, 3)
    # Implement algorithm steps
    qc.h(range(3))
    # Add application-specific gates
    # Add measurements
    qc.measure(range(3), range(3))
    return qc

# Run the algorithm with your parameters
circuit = my_algorithm([1.0, 0.5])
counts = run_with_simulator(circuit)
print(counts)
""",
    "Quantum Machine Learning": """
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.algorithms.optimizers import COBYLA
from qiskit_machine_learning.algorithms import VQC
from qiskit_machine_learning.datasets import ad_hoc_data

# Generate simple dataset
num_samples = 20
X, y = ad_hoc_data(num_samples, feature_dimension=2, noise=0.1)
feature_map = ZZFeatureMap(2)
ansatz = RealAmplitudes(2, reps=1)
vqc = VQC(
    feature_map=feature_map,
    ansatz=ansatz,
    optimizer=COBYLA(maxiter=100),
    quantum_instance=global_simulator
)

# Just print the setup (full training would be too intensive)
print(f"Created VQC with {num_samples} data points")
print(f"Feature map: {feature_map.name}")
print(f"Ansatz: {ansatz.name}")
"""
}

# Load user-defined applications
user_applications = load_user_applications()

# Main application layout with split view
st.markdown("<h2 style='text-align: center;'>QUANTUM CIRCUIT INTERFACE</h2>", unsafe_allow_html=True)

# Create a layout with a left side (3 columns) and a right side (for code display)
left_section, right_section = st.columns([1, 1.2])

# Apply the left-section class to the left column
st.markdown('<div class="left-section" id="left-section"></div>', unsafe_allow_html=True)

# Set up the session state variables for the interface
if 'selected_circuit' not in st.session_state:
    st.session_state.selected_circuit = None
if 'selected_circuit_type' not in st.session_state:
    st.session_state.selected_circuit_type = None
if 'circuit_results' not in st.session_state:
    st.session_state.circuit_results = None
if 'show_run_details' not in st.session_state:
    st.session_state.show_run_details = False

# Left side - Circuit selection boxes
with left_section:
    st.markdown("<h3>AVAILABLE QUANTUM CIRCUITS</h3>", unsafe_allow_html=True)
    
    # Create tabs for different circuit types
    circ_tab1, circ_tab2 = st.tabs(["PREDEFINED CIRCUITS", "USER CIRCUITS"])
    
    with circ_tab1:
        # Display predefined circuit boxes
        st.markdown("<p style='color: #00ffcc99;'>Click on a circuit to view and run it</p>", unsafe_allow_html=True)
        
        # Create 3 columns for the boxes
        if len(examples) > 0:
            # Calculate number of rows needed
            num_rows = (len(examples) + 2) // 3  # Ceiling division
            
            for row in range(num_rows):
                # Create 3 columns for each row
                cols = st.columns(3)
                
                # Add up to 3 cards per row
                for col_idx in range(3):
                    idx = row * 3 + col_idx
                    if idx < len(examples):
                        example_name = list(examples.keys())[idx]
                        example_code = examples[example_name]
                        
                        with cols[col_idx]:
                            # Create a card with a hover effect
                            card_html = f"""
                            <div class="quantum-card" style="margin-bottom: 10px; height: 100px;" id="card_{idx}">
                                <h3 style="margin-top:0; font-size: 1em;">{example_name}</h3>
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div style="width: 50px; height: 10px; background: linear-gradient(90deg, #00ffcc, transparent); border-radius: 5px;"></div>
                                    <div style="font-size: 0.8em; color: #00ffcc80;">COMPLEXITY: {'●' * min(5, (idx + 1) // 2)}{'○' * (5 - min(5, (idx + 1) // 2))}</div>
                                </div>
                            </div>
                            """
                            st.markdown(card_html, unsafe_allow_html=True)
                            
                            # Create a button that looks like part of the card
                            if st.button(f"SELECT", key=f"select_example_{idx}"):
                                st.session_state.selected_circuit = example_name
                                st.session_state.selected_circuit_type = "predefined"
                                st.session_state.show_run_details = False
                                st.session_state.circuit_results = None
                                st.rerun()
    
    with circ_tab2:
        # Display user circuit boxes
        st.markdown("<p style='color: #00ffcc99;'>Click on a circuit to view and run it</p>", unsafe_allow_html=True)
        if user_applications:
            # Calculate number of rows needed
            num_rows = (len(user_applications) + 2) // 3  # Ceiling division
            
            for row in range(num_rows):
                # Create 3 columns for each row
                cols = st.columns(3)
                
                # Add up to 3 cards per row
                for col_idx in range(3):
                    idx = row * 3 + col_idx
                    if idx < len(user_applications):
                        app_name = list(user_applications.keys())[idx]
                        app_data = user_applications[app_name]
                        
                        with cols[col_idx]:
                            # Create a card with a hover effect
                            card_html = f"""
                            <div class="quantum-card" style="margin-bottom: 10px; height: 100px;" id="user_card_{idx}">
                                <h3 style="margin-top:0; font-size: 1em;">{app_name}</h3>
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div style="width: 50px; height: 10px; background: linear-gradient(90deg, #00ffcc, transparent); border-radius: 5px;"></div>
                                    <div style="font-size: 0.8em; color: #00ffcc80;">USER CIRCUIT</div>
                                </div>
                            </div>
                            """
                            st.markdown(card_html, unsafe_allow_html=True)
                            
                            # Create a button that looks like part of the card
                            if st.button(f"SELECT", key=f"select_user_app_{idx}"):
                                st.session_state.selected_circuit = app_name
                                st.session_state.selected_circuit_type = "user"
                                st.session_state.show_run_details = False
                                st.session_state.circuit_results = None
                                st.rerun()
        else:
            st.info("No user circuits available. Create a new circuit from the menu below.")
    
    # Add option to create new circuit
    st.markdown("<hr style='border-color: #00ffcc40; margin: 20px 0;'>", unsafe_allow_html=True)
    if st.button("+ CREATE NEW CIRCUIT"):
        st.session_state.creating_new_app = True
        st.session_state.selected_circuit = None
        st.session_state.selected_circuit_type = None
        st.rerun()

# Right side - Code display and results
with right_section:
    if st.session_state.creating_new_app:
        # Show create module interface
        render_create_module_tab(user_applications, templates)
    elif st.session_state.selected_circuit:
        selected_name = st.session_state.selected_circuit
        circuit_type = st.session_state.selected_circuit_type
        
        st.markdown(f"<h3>CIRCUIT: {selected_name}</h3>", unsafe_allow_html=True)
        
        # Get the appropriate code based on the selected circuit type
        if circuit_type == "predefined":
            circuit_code = examples[selected_name]
        else:  # "user"
            circuit_code = user_applications[selected_name]["code"]
        
        # Display the code with a more pronounced highlight box
        st.markdown("""
        <div style="background-color: #1a1a2e; border: 1px solid #00ffcc; border-radius: 5px; padding: 5px; margin-bottom: 15px;">
            <h4 style="color: #00ffcc; margin-top: 0;">QUANTUM ALGORITHM CODE</h4>
        </div>
        """, unsafe_allow_html=True)
        st.code(circuit_code, language="python")
        
        # Add a run button with futuristic styling
        if st.button("▶ EXECUTE QUANTUM CIRCUIT", key="run_circuit"):
            try:
                # Prepare to execute the code
                from qiskit import transpile
                from qiskit_aer import AerSimulator
                from utils.simulator import global_simulator
                
                # Create a local namespace to execute the code
                local_namespace = {
                    'run_with_simulator': run_with_simulator,
                    'transpile': transpile,
                    'AerSimulator': AerSimulator,
                    'global_simulator': global_simulator
                }
                
                # Execute the code
                exec(circuit_code, globals(), local_namespace)
                
                # Get the result from the local namespace
                if 'counts' in local_namespace:
                    output = local_namespace['counts']
                elif 'result' in local_namespace:
                    result = local_namespace['result']
                    output = result.get_counts() if hasattr(result, 'get_counts') else str(result)
                elif 'circuit' in local_namespace:
                    circuit = local_namespace['circuit']
                    output = run_with_simulator(circuit)
                elif 'qc' in local_namespace:
                    qc = local_namespace['qc']
                    output = run_with_simulator(qc)
                else:
                    output = "Execution completed, but no result or circuit was returned."
                
                st.session_state.circuit_results = str(output)
                st.session_state.show_run_details = True
                
                display_success_message(
                    "EXECUTION SUCCESSFUL", 
                    f"Circuit executed at {datetime.now().strftime('%H:%M:%S')} | Status: OPTIMAL"
                )
                
                # Display the results
                st.markdown("<h4>EXECUTION RESULTS</h4>", unsafe_allow_html=True)
                display_terminal_output(str(output))
                
            except Exception as e:
                # Display error with robotic styling
                display_error_message("EXECUTION ERROR DETECTED", str(e))
        
        # Show previous results if available
        if st.session_state.show_run_details and st.session_state.circuit_results:
            st.markdown("<h4>PREVIOUS EXECUTION RESULTS</h4>", unsafe_allow_html=True)
            display_terminal_output(st.session_state.circuit_results)
    else:
        # Show default message when no circuit is selected
        st.markdown("""
        <div style='text-align: center; padding: 50px; color: #00ffcc80;'>
            <h3>QUANTUM INTERFACE READY</h3>
            <p>Select a circuit from the left panel to view and execute it</p>
            <div style='font-size: 50px; margin: 30px;'>⚛️</div>
        </div>
        """, unsafe_allow_html=True)

# Footer or other common elements can go here
st.markdown("---<br><p style='text-align: center; color: #00ffcc80;'>Quantum AI Interface v1.0 | System Status: Nominal</p>", unsafe_allow_html=True)
