"""
Predefined modules tab component for the Quantum Circuit Simulator.
"""
import streamlit as st
import io
import sys
from datetime import datetime
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ui import display_success_message, display_error_message, display_terminal_output
from utils.simulator import run_with_simulator

def render_predefined_tab(examples):
    """Render the Predefined Modules tab"""
    st.markdown("<h2>QUANTUM CIRCUITS DATABASE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00ffcc99;'>Select a quantum module to view specifications and initiate simulation</p>", unsafe_allow_html=True)
    
    # Create a visual grid of example cards
    cols = st.columns(2)
    
    # Track the selected example
    if 'selected_predefined_example' not in st.session_state:
        st.session_state.selected_predefined_example = None
    
    # Display examples as clickable cards in a 2-column grid
    for i, (example_name, example_code) in enumerate(examples.items()):
        col_idx = i % 2
        
        with cols[col_idx]:
            # Extract a short description based on the example name
            description = example_name.split(". ")[1] if ". " in example_name else example_name
            
            # Create a card with a hover effect
            card_html = f"""
            <div class="quantum-card" onclick="this.style.backgroundColor='#1a1a4a';" id="card_{i}">
                <h3 style="margin-top:0;">{example_name}</h3>
                <p style="color: #00ffcc99;">MODULE TYPE: {description}</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="width: 50px; height: 10px; background: linear-gradient(90deg, #00ffcc, transparent); border-radius: 5px;"></div>
                    <div style="font-size: 0.8em; color: #00ffcc80;">COMPLEXITY: {'●' * min(5, (i + 1) // 2)}{'○' * (5 - min(5, (i + 1) // 2))}</div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Create a button that looks like part of the card
            if st.button(f"SELECT MODULE {i+1}", key=f"select_example_{i}"):
                st.session_state.selected_predefined_example = example_name
    
    # Display selected example details if one is selected
    if st.session_state.selected_predefined_example:
        selected_example = st.session_state.selected_predefined_example
        
        st.markdown("<hr style='border-color: #00ffcc40; margin: 30px 0;'>", unsafe_allow_html=True)
        st.markdown(f"<h3>MODULE: {selected_example}</h3>", unsafe_allow_html=True)
        
        # Create two columns for code and visualization
        code_col, viz_col = st.columns([3, 2])
        
        with code_col:
            st.markdown("<h4>QUANTUM ALGORITHM SPECIFICATION</h4>", unsafe_allow_html=True)
            st.code(examples[selected_example], language="python")
        
        with viz_col:
            st.markdown("<h4>MODULE INTERFACE</h4>", unsafe_allow_html=True)
            
            # Add a futuristic circular loading animation
            st.markdown("""
            <div style="display: flex; justify-content: center; margin-bottom: 20px;">
                <div style="width: 100px; height: 100px; border-radius: 50%; border: 3px solid transparent; 
                     border-top-color: #00ffcc; animation: spin 1s linear infinite;"></div>
            </div>
            <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Add a run button with futuristic styling
            if st.button("▶ EXECUTE QUANTUM MODULE", key="run_predefined", 
                       help="Run the selected quantum circuit example"):
                try:
                    # Ensure compatibility with the latest Qiskit version
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
                    
                    # Execute the example code to generate the quantum circuit
                    exec(examples[selected_example], globals(), local_namespace)
                    
                    # Display the output captured during execution
                    
                    # Get the result from the local namespace (the example code should store its result there)
                    if 'counts' in local_namespace:
                        # Most examples store results directly in a 'counts' variable
                        output = local_namespace['counts']
                    elif 'result' in local_namespace:
                        result = local_namespace['result']
                        output = result.get_counts() if hasattr(result, 'get_counts') else str(result)
                    elif 'circuit' in local_namespace:
                        # If no result is present but a circuit is, run it with the simulator
                        circuit = local_namespace['circuit']
                        output = run_with_simulator(circuit)
                    elif 'qc' in local_namespace:
                        # If there's a quantum circuit called 'qc', run it
                        qc = local_namespace['qc']
                        output = run_with_simulator(qc)
                    else:
                        output = "Execution completed, but no result or circuit was returned."
                        
                    display_success_message(
                        "EXECUTION SUCCESSFUL", 
                        f"Module executed at {datetime.now().strftime('%H:%M:%S')} | System status: OPTIMAL"
                    )

                    # Output results in a terminal-like display
                    display_terminal_output(str(output))
                except Exception as e:
                    # Display error with robotic styling
                    display_error_message("EXECUTION ERROR DETECTED", str(e))
                finally:
                    # Save the current stdout before redirecting it
                    old_stdout = sys.stdout
