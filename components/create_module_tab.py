"""
Create new module tab component for the Quantum Circuit Simulator.
"""
import streamlit as st
import io
import sys
from qiskit import QuantumCircuit
from utils.simulator import save_user_applications, run_with_simulator # Import the simulator function
from utils.ui import display_success_message, display_error_message, display_terminal_output

def render_create_module_tab(user_applications, templates):
    """Render the Create New Module tab"""
    st.markdown("<h2>QUANTUM MODULE CREATION INTERFACE</h2>", unsafe_allow_html=True)
    
    # Display different views based on whether we're editing or creating
    if st.session_state.editing_app:
        st.markdown(f"<h3>EDITING MODULE: {st.session_state.edit_app_name}</h3>", unsafe_allow_html=True)
        
        # Create futuristic form styling
        st.markdown("""
        <div style="background-color: #1a1a2e; border: 1px solid #00ffcc; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="width: 15px; height: 15px; background-color: #00ffcc; border-radius: 50%; margin-right: 10px;"></div>
                <span style="color: #00ffcc; font-family: 'Courier New', monospace;">MODULE PARAMETERS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        edit_name = st.text_input("MODULE IDENTIFIER", value=st.session_state.edit_app_name, key="edit_app_name_input")
        
        # Add futuristic separator
        st.markdown("""
        <div style="display: flex; align-items: center; margin: 20px 0;">
            <div style="flex-grow: 1; height: 1px; background-color: #00ffcc40;"></div>
            <div style="padding: 0 10px; color: #00ffcc; font-size: 0.8em;">QUANTUM CODE INTERFACE</div>
            <div style="flex-grow: 1; height: 1px; background-color: #00ffcc40;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        edit_code = st.text_area("MODULE SOURCE CODE", value=user_applications[st.session_state.edit_app_name]["code"], height=400, key="edit_app_code")
        
        # Create futuristic buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 SAVE MODULE", key="save_edit", help="Save changes to this module"):
                if edit_name != st.session_state.edit_app_name:
                    # If name was changed, create new entry and delete old one
                    user_applications[edit_name] = user_applications[st.session_state.edit_app_name].copy()
                    user_applications.pop(st.session_state.edit_app_name)
                    
                user_applications[edit_name]["code"] = edit_code
                user_applications[edit_name]["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                save_user_applications(user_applications)
                
                # Show success message with futuristic styling
                display_success_message(
                    "MODULE UPDATED SUCCESSFULLY",
                    "All changes have been saved to quantum storage"
                )
                
                st.session_state.editing_app = False
                st.experimental_rerun()
        with col2:
            if st.button("❌ CANCEL", key="cancel_edit", help="Discard changes"):
                st.session_state.editing_app = False
                st.experimental_rerun()
    else:
        # Create new module interface with futuristic styling
        st.markdown("<h3>INITIALIZE NEW QUANTUM MODULE</h3>", unsafe_allow_html=True)
        
        # Add pulsing animation to indicate "new" state
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="width: 12px; height: 12px; background-color: #00ffcc; border-radius: 50%; 
                  margin-right: 10px; animation: pulse 2s infinite;">
            </div>
            <span style="color: #00ffcc99;">SYSTEM READY FOR NEW MODULE CREATION</span>
        </div>
        <style>
            @keyframes pulse {
                0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.7); }
                70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 204, 0); }
                100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); }
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Module name input with futuristic styling
        new_app_name = st.text_input("MODULE IDENTIFIER", key="new_app_name", 
                                  placeholder="Enter a unique name for your quantum module...")
        
        # Template selection with futuristic cards
        st.markdown("<p style='color: #00ffcc; margin: 20px 0 10px 0;'>SELECT TEMPLATE CONFIGURATION:</p>", unsafe_allow_html=True)
        
        # Visually display templates as cards
        template_options = ["Blank"] + list(templates.keys())
        template_cols = st.columns(len(template_options))
        
        # Track selected template
        if 'selected_template' not in st.session_state:
            st.session_state.selected_template = "Blank"
        
        # Create clickable template cards
        for i, template_name in enumerate(template_options):
            with template_cols[i]:
                # Different card styling for selected template
                is_selected = st.session_state.selected_template == template_name
                card_bg = "#1a4a3a" if is_selected else "#1a1a2e"
                border = "2px solid #00ffcc" if is_selected else "1px solid #00ffcc80"
                
                template_card = f"""
                <div style="background-color: {card_bg}; border: {border}; 
                     border-radius: 8px; padding: 15px; text-align: center; cursor: pointer;
                     height: 100px; display: flex; flex-direction: column; justify-content: center;">
                    <h4 style="margin: 0; color: #00ffcc;">
                        {template_name}
                        {('<span style="font-size: 1.5em; display: block; margin-top: 5px;">✓</span>') if is_selected else ''}
                    </h4>
                </div>
                """
                st.markdown(template_card, unsafe_allow_html=True)
                
                # Button to select this template
                if st.button(f"SELECT", key=f"template_{template_name}", 
                           help=f"Use the {template_name} template"):
                    st.session_state.selected_template = template_name
                    # Initialize code with selected template
                    if template_name == "Blank":
                        st.session_state.new_app_code = """from qiskit import QuantumCircuit

# Create your quantum circuit
qc = QuantumCircuit(2, 2)

# Add your gates here

# Add measurements
qc.measure([0, 1], [0, 1])

# Run simulation
counts = run_with_simulator(qc)
print(counts)
"""
                    else:
                        st.session_state.new_app_code = templates[template_name]
                    st.experimental_rerun()
        
        # Add futuristic separator
        st.markdown("""
        <div style="display: flex; align-items: center; margin: 20px 0;">
            <div style="flex-grow: 1; height: 1px; background-color: #00ffcc40;"></div>
            <div style="padding: 0 10px; color: #00ffcc; font-size: 0.8em;">CODE INTERFACE</div>
            <div style="flex-grow: 1; height: 1px; background-color: #00ffcc40;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize code with selected template if needed
        if "new_app_code" not in st.session_state:
            st.session_state.new_app_code = """from qiskit import QuantumCircuit

# Create your quantum circuit
qc = QuantumCircuit(2, 2)

# Add your gates here

# Add measurements
qc.measure([0, 1], [0, 1])

# Run simulation
counts = run_with_simulator(qc)
print(counts)
"""
        
        # Code editor with syntax highlighting
        new_app_code = st.text_area("QUANTUM SOURCE CODE", value=st.session_state.new_app_code, 
                                 height=400, key="app_code_input")
        st.session_state.new_app_code = new_app_code
        
        # Action buttons with futuristic styling
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 SAVE MODULE", key="save_new_app", help="Save this quantum module"):
                if not new_app_name:
                    # Show error with futuristic styling
                    display_error_message(
                        "ERROR: MODULE IDENTIFIER REQUIRED",
                        "Please provide a name for your quantum module"
                    )
                elif new_app_name in user_applications:
                    display_error_message(
                        "ERROR: IDENTIFIER CONFLICT DETECTED",
                        f"A module with identifier '{new_app_name}' already exists"
                    )
                else:
                    user_applications[new_app_name] = {
                        "code": new_app_code,
                        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    save_result = save_user_applications(user_applications)
                    if save_result:
                        # Show success with futuristic styling
                        display_success_message(
                            "MODULE CREATION SUCCESSFUL",
                            "New quantum module has been saved to storage"
                        )
                        
                        # Clear the form
                        st.session_state.new_app_code = ""
                        st.session_state.selected_template = "Blank"
                        st.experimental_rerun()
        
        with col2:
            if st.button("▶ TEST EXECUTE", key="test_run", help="Execute this quantum module"):
                try:
                    # Redirect stdout to capture print output
                    old_stdout = sys.stdout
                    redirected_output = io.StringIO()
                    sys.stdout = redirected_output

                    # Execute the new application code
                    exec(new_app_code)

                    # Retrieve and display output
                    output = redirected_output.getvalue()
                    
                    # Show success with futuristic styling
                    display_success_message(
                        "TEST EXECUTION SUCCESSFUL",
                        "Module executed in test environment | Status: OPTIMAL"
                    )
                    
                    # Output in a terminal-like display
                    display_terminal_output(output)
                except Exception as e:
                    # Show error with futuristic styling
                    display_error_message("EXECUTION ERROR DETECTED", str(e))
                finally:
                    # Reset stdout
                    sys.stdout = old_stdout
