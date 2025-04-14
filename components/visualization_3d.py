"""
3D Visualization component for the Quantum Circuit Simulator apps.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np

def create_3d_app_visualization(predefined_apps, user_apps):
    """
    Generates an interactive 3D scatter plot of available applications.

    Args:
        predefined_apps (dict): Dictionary of predefined example applications.
        user_apps (dict): Dictionary of user-created applications.

    Returns:
        plotly.graph_objects.Figure: A Plotly figure object for the 3D visualization.
    """
    app_names = []
    x_coords = []
    y_coords = []
    z_coords = []
    colors = []
    symbols = []
    texts = []

    # Process predefined apps
    for i, (name, _) in enumerate(predefined_apps.items()):
        app_names.append(name)
        # Simple positioning logic (can be made more sophisticated)
        x_coords.append(np.cos(i * np.pi / 6) * (i + 1))
        y_coords.append(np.sin(i * np.pi / 6) * (i + 1))
        z_coords.append(i * 0.5) # Spread them out vertically
        colors.append('#00ffcc') # Predefined color
        symbols.append('circle')
        texts.append(f"<b>{name}</b><br>Type: Predefined")

    # Process user apps
    offset = len(predefined_apps)
    for i, (name, data) in enumerate(user_apps.items()):
        app_names.append(name)
        # Position user apps differently
        x_coords.append(np.cos((i + offset) * np.pi / 4 + np.pi/2) * (i + 1) * 1.5)
        y_coords.append(np.sin((i + offset) * np.pi / 4 + np.pi/2) * (i + 1) * 1.5)
        z_coords.append((i + offset) * 0.6) # Slightly different vertical spread
        colors.append('#ff66ff') # User app color
        symbols.append('diamond')
        created = data.get('created', 'N/A')
        modified = data.get('last_modified', 'N/A')
        texts.append(f"<b>{name}</b><br>Type: User Module<br>Created: {created}<br>Modified: {modified}")

    # Create the 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=x_coords,
        y=y_coords,
        z=z_coords,
        mode='markers+text',
        marker=dict(
            size=10,
            color=colors,
            symbol=symbols,
            opacity=0.8,
            line=dict(color='rgba(255, 255, 255, 0.5)', width=1)
        ),
        text=[name.split('. ')[-1] if '. ' in name else name for name in app_names], # Display short names next to markers
        textposition='top center',
        hoverinfo='text',
        hovertext=texts,
        name='Quantum Apps'
    )])

    # Customize layout for the futuristic theme
    fig.update_layout(
        title=dict(
            text='3D Quantum Application Matrix',
            font=dict(color='#00ffcc', family='Orbitron, sans-serif', size=18),
            x=0.5 # Center title
        ),
        scene=dict(
            xaxis=dict(
                title='X Dimension',
                backgroundcolor="rgba(10, 10, 26, 0.8)", # Match app background
                gridcolor="rgba(0, 255, 204, 0.3)",
                showbackground=True,
                zerolinecolor="rgba(0, 255, 204, 0.5)",
                titlefont=dict(color='#00ffcc'),
                tickfont=dict(color='#00ffcc')
            ),
            yaxis=dict(
                title='Y Dimension',
                backgroundcolor="rgba(10, 10, 26, 0.8)",
                gridcolor="rgba(0, 255, 204, 0.3)",
                showbackground=True,
                zerolinecolor="rgba(0, 255, 204, 0.5)",
                titlefont=dict(color='#00ffcc'),
                tickfont=dict(color='#00ffcc')
            ),
            zaxis=dict(
                title='Complexity/Index',
                backgroundcolor="rgba(10, 10, 26, 0.8)",
                gridcolor="rgba(0, 255, 204, 0.3)",
                showbackground=True,
                zerolinecolor="rgba(0, 255, 204, 0.5)",
                titlefont=dict(color='#00ffcc'),
                tickfont=dict(color='#00ffcc')
            ),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.0) # Adjust camera angle
            )
        ),
        margin=dict(l=0, r=0, b=0, t=40), # Adjust margins
        paper_bgcolor='rgba(10, 10, 26, 0.9)', # Transparent background for the plot area
        plot_bgcolor='rgba(10, 10, 26, 0.9)', # Background for the plot itself
        legend=dict(font=dict(color='#00ffcc'))
    )

    return fig

def render_3d_visualization_tab(predefined_apps, user_apps):
    """Renders the 3D visualization tab content."""
    st.markdown("<h2>3D APPLICATION VISUALIZER</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00ffcc99;'>Explore available quantum modules in an interactive 3D space.</p>", unsafe_allow_html=True)

    if not predefined_apps and not user_apps:
        st.warning("No applications found to visualize.")
        return

    # Generate and display the plot
    fig = create_3d_app_visualization(predefined_apps, user_apps)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<p style='color: #00ffcc99; font-size: 0.9em;'>Hint: Rotate the view by dragging. Zoom with scroll. Hover over points for details. Colors differentiate types: <span style='color:#00ffcc;'>● Predefined</span>, <span style='color:#ff66ff;'>♦ User Module</span>.</p>", unsafe_allow_html=True)

