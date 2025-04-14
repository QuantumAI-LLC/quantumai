"""
User modules tab component for the Quantum Circuit Simulator.
"""
import streamlit as st
import io
import sys
from datetime import datetime
from utils.ui import display_success_message, display_error_message, display_terminal_output
from utils.simulator import save_user_applications

def render_user_modules_tab(user_applications):
    """Render the User Modules tab"""
    st.markdown("<h2>USER QUANTUM MODULES DATABASE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00ffcc99;'>Access and manage your quantum computing modules</p>", unsafe_allow_html=True)
    
    if user_applications:
        # Create a visual grid of user application cards
        st.markdown("<div class='user-modules-grid'>", unsafe_allow_html=True)
        
        # Create a 2-column layout for the cards
        cols = st.columns(2)
        
        # Track selected user app
        if 'selected_user_app' not in st.session_state:
            st.session_state.selected_user_app = None
        
        # Display applications as cards
        for i, (app_name, app_data) in enumerate(user_applications.items()):
            col_idx = i % 2
            with cols[col_idx]:
                # Create timestamp display
                created_date = app_data.get('created', 'Unknown')
                modified_date = app_data.get('last_modified', '')
                timestamp_info = f"CREATED: {created_date}"
                if modified_date:
                    timestamp_info += f" | UPDATED: {modified_date}"
                
                # Create a card with hover effect and futuristic styling
                card_html = f"""
                <div class="quantum-card">
                    <h3 style="margin-top:0; display: flex; align-items: center;">
                        <span style="display: inline-block; width: 20px; height: 20px; 
                              background-color: #00ffcc; border-radius: 50%; margin-right: 10px;"></span>
                        {app_name}
                    </h3>
                    <p style="color: #00ffcc99; font-size: 0.8em;">{timestamp_info}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="width: 70px; height: 8px; background: linear-gradient(90deg, #00ffcc, transparent); border-radius: 4px;"></div>
                        <div style="font-size: 0.8em; color: #00ffcc80;">USER MODULE #{i+1}</div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Button to select this application
                if st.button(f"SELECT MODULE", key=f"select_user_app_{i}"):
                    st.session_state.selected_user_app = app_name
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display selected application details
        if st.session_state.selected_user_app:
            selected_user_app = st.session_state.selected_user_app
            
            st.markdown("<hr style='border-color: #00ffcc40; margin: 30px 0;'>", unsafe_allow_html=True)
            st.markdown(f"<h3>USER MODULE: {selected_user_app}</h3>", unsafe_allow_html=True)
            
            # Create action buttons with futuristic styling
            actions_col1, actions_col2, actions_col3 = st.columns(3)
            
            with actions_col1:
                if st.button("▶ EXECUTE", key="run_user_app", help="Run this quantum module"):
                    try:
                        # Redirect stdout to capture print output
                        old_stdout = sys.stdout
                        redirected_output = io.StringIO()
                        sys.stdout = redirected_output

                        # Execute the selected user application
                        exec(user_applications[selected_user_app]["code"])

                        # Retrieve and display output
                        output = redirected_output.getvalue()
                        
                        # Display success with robotic styling
                        display_success_message(
                            "EXECUTION SUCCESSFUL", 
                            f"Module executed at {datetime.now().strftime('%H:%M:%S')} | Runtime: OPTIMAL"
                        )
                        
                        # Output in a terminal-like display
                        display_terminal_output(output)
                    except Exception as e:
                        display_error_message("EXECUTION ERROR DETECTED", str(e))
                    finally:
                        # Reset stdout
                        sys.stdout = old_stdout
            
            with actions_col2:
                if st.button("✏️ MODIFY", key="edit_user_app", help="Edit this quantum module"):
                    st.session_state.editing_app = True
                    st.session_state.edit_app_name = selected_user_app
                    st.experimental_rerun()
            
            with actions_col3:
                if st.button("❌ DELETE", key="delete_user_app", help="Delete this quantum module"):
                    st.markdown("""
                    <div style="background-color: #4a1a1a; color: #ff5555; padding: 10px; 
                         border-radius: 5px; border: 1px solid #ff5555; margin: 10px 0;">
                        <h4 style="margin: 0;">WARNING: MODULE DELETION INITIATED</h4>
                        <p>Confirm deletion of the selected quantum module?</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("CONFIRM DELETE", key="confirm_delete"):
                            user_applications.pop(selected_user_app)
                            save_user_applications(user_applications)
                            st.session_state.selected_user_app = None
                            st.success(f"Module '{selected_user_app}' deleted successfully!")
                            st.experimental_rerun()
                    with confirm_col2:
                        if st.button("CANCEL", key="cancel_delete"):
                            st.experimental_rerun()
            
            # Display code in a futuristic terminal-like area
            st.markdown("<h4>MODULE SOURCE CODE</h4>", unsafe_allow_html=True)
            st.code(user_applications[selected_user_app]["code"], language="python")
            
            # Add metadata display with futuristic styling
            metadata_html = f"""
            <div style="background-color: #1a1a2e; padding: 10px; border-radius: 5px; 
                border-left: 3px solid #00ffcc; margin-top: 20px;">
                <p style="margin: 0; font-family: 'Courier New', monospace; font-size: 0.9em; color: #00ffcc;">
                    <span style="color: #00ffcc80;">MODULE ID:</span> {hash(selected_user_app) % 10000:04d} | 
                    <span style="color: #00ffcc80;">CREATED:</span> {user_applications[selected_user_app]['created']} 
                    {f"| <span style='color: #00ffcc80;'>LAST MODIFIED:</span> {user_applications[selected_user_app]['last_modified']}" if 'last_modified' in user_applications[selected_user_app] else ""}
                </p>
            </div>
            """
            st.markdown(metadata_html, unsafe_allow_html=True)
            
    else:
        # Display futuristic empty state
        st.markdown("""
        <div style="text-align: center; padding: 50px 20px; background-color: #1a1a2e; 
             border: 1px dashed #00ffcc; border-radius: 10px; margin: 20px 0;">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin: 0 auto;">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z" 
                      fill="#00ffcc" opacity="0.7"></path>
            </svg>
            <h3 style="color: #00ffcc; margin-top: 20px;">NO USER MODULES DETECTED</h3>
            <p style="color: #00ffcc99;">Navigate to the "CREATE NEW MODULE" interface to develop your first quantum application</p>
            <button onclick="window.location.href='#'" style="background-color: #222244; color: #00ffcc; border: 1px solid #00ffcc; 
                    padding: 8px 16px; border-radius: 5px; cursor: pointer; margin-top: 10px;">
                INITIALIZE NEW MODULE
            </button>
        </div>
        """, unsafe_allow_html=True)
