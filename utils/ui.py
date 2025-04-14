"""
UI styling and theming components for the Quantum Circuit Simulator
"""
import streamlit as st

def configure_page_style():
    """Configure the page style and layout with the robotic/futuristic theme"""
    # Set page configuration
    st.set_page_config(
        page_title="Quantum AI Circuit Interface",
        page_icon="⚛️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply custom CSS for robotic/futuristic styling
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

def get_robot_animation():
    """Return the robot SVG animation HTML"""
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

def render_app_header():
    """Render the application header with robot animation"""
    # Display robot animation
    st.markdown(get_robot_animation(), unsafe_allow_html=True)
    
    # Display title and subtitle
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>QUANTUM AI CIRCUIT INTERFACE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 30px; color: #00ffcc99;'>SELECT QUANTUM MODULE TO INITIATE SIMULATION SEQUENCE</p>", unsafe_allow_html=True)

def display_success_message(message, details=None):
    """Display a futuristic success message"""
    details_html = ""
    if details:
        details_html = f"<p style='font-family: 'Courier New', monospace; margin: 5px 0 0 0; font-size: 0.8em;'>{details}</p>"
    
    st.markdown(f"""
    <div style="background-color: #1a4a1a; color: #00ffcc; padding: 10px; 
         border-radius: 5px; border-left: 5px solid #00ffcc; margin: 10px 0;">
        <h4 style="margin: 0;">{message}</h4>
        {details_html}
    </div>
    """, unsafe_allow_html=True)

def display_error_message(message, details=None):
    """Display a futuristic error message"""
    details_html = ""
    if details:
        details_html = f"<p style='font-family: 'Courier New', monospace; margin: 5px 0 0 0;'>{details}</p>"
    
    st.markdown(f"""
    <div style="background-color: #4a1a1a; color: #ff5555; padding: 10px; 
         border-radius: 5px; border-left: 5px solid #ff5555; margin: 10px 0;">
        <h4 style="margin: 0;">{message}</h4>
        {details_html}
    </div>
    """, unsafe_allow_html=True)

def display_terminal_output(output):
    """Display output in a terminal-like container"""
    st.markdown("<h4>QUANTUM OUTPUT DATA</h4>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background-color: #1a1a2e; color: #00ffcc; font-family: 'Courier New', monospace; 
         padding: 15px; border-radius: 5px; border: 1px solid #00ffcc; height: 200px; overflow-y: auto;">
        <pre>{output}</pre>
    </div>
    """, unsafe_allow_html=True)
