"""
Theme Manager for FraudLens

This module provides color schemes and theme management functionality
for the FraudLens application, allowing users to personalize their
dashboard experience.
"""

import streamlit as st
from typing import Dict, Any, List, Tuple

# Define mood-based color palettes
COLOR_SCHEMES = {
    "professional": {
        "primary": "#4F8BF9",
        "secondary": "#1E2130",
        "background": "#0E1117",
        "text": "#FAFAFA",
        "success": "#00CC96",
        "warning": "#FFA500",
        "danger": "#FF4B4B",
        "chart_colors": ["#4F8BF9", "#00CC96", "#FFA500", "#FF4B4B", "#B6E880", "#FF97FF", "#FECB52"],
        "gradient": ["#4F8BF9", "#00CC96"]
    },
    "calm": {
        "primary": "#68B0AB",
        "secondary": "#2C3531",
        "background": "#F4F9F9",
        "text": "#2C3531",
        "success": "#8FC0A9",
        "warning": "#C8D5B9",
        "danger": "#D8B4A0",
        "chart_colors": ["#68B0AB", "#8FC0A9", "#C8D5B9", "#D8B4A0", "#FAF3DD", "#116466", "#4B644A"],
        "gradient": ["#68B0AB", "#8FC0A9"]
    },
    "energetic": {
        "primary": "#F05D5E",
        "secondary": "#0F7173",
        "background": "#F7F7FF",
        "text": "#272932",
        "success": "#78C0E0",
        "warning": "#E09F3E",
        "danger": "#E55934",
        "chart_colors": ["#F05D5E", "#0F7173", "#78C0E0", "#E09F3E", "#E55934", "#F0EFF4", "#9E2B25"],
        "gradient": ["#F05D5E", "#E09F3E"]
    },
    "dark": {
        "primary": "#BB86FC",
        "secondary": "#1F1B24",
        "background": "#121212",
        "text": "#E1E1E1",
        "success": "#03DAC5",
        "warning": "#FFB74D",
        "danger": "#CF6679",
        "chart_colors": ["#BB86FC", "#03DAC5", "#FFB74D", "#CF6679", "#A4C2F4", "#8F8F8F", "#D0BCFF"],
        "gradient": ["#BB86FC", "#03DAC5"]
    },
    "focus": {
        "primary": "#4056A1",
        "secondary": "#F13C20",
        "background": "#EFE2BA",
        "text": "#2E282A",
        "success": "#5FAD56",
        "warning": "#F5BB00",
        "danger": "#F13C20",
        "chart_colors": ["#4056A1", "#F13C20", "#5FAD56", "#F5BB00", "#F7CB15", "#D79922", "#2B4570"],
        "gradient": ["#4056A1", "#F13C20"]
    }
}

def load_theme_css(theme_name: str) -> str:
    """
    Generate CSS for the selected theme to be injected into the page.
    
    Parameters:
    -----------
    theme_name : str
        Name of the theme to load
        
    Returns:
    --------
    str
        CSS code to be injected
    """
    if theme_name not in COLOR_SCHEMES:
        theme_name = "professional"  # Default fallback
        
    theme = COLOR_SCHEMES[theme_name]
    
    return f"""
    <style>
        /* Theme colors */
        :root {{
            --primary-color: {theme['primary']};
            --secondary-color: {theme['secondary']};
            --background-color: {theme['background']};
            --text-color: {theme['text']};
            --success-color: {theme['success']};
            --warning-color: {theme['warning']};
            --danger-color: {theme['danger']};
        }}
        
        /* Main elements */
        .main {{
            background-color: {theme['background']};
            color: {theme['text']};
        }}
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {theme['primary']};
        }}
        
        /* Metrics */
        .metric-container {{
            background-color: {theme['secondary']};
            border-radius: 5px;
            padding: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
        }}
        
        .metric-value {{
            color: {theme['primary']};
            font-size: 1.8rem;
            font-weight: bold;
        }}
        
        .metric-label {{
            color: {theme['text']};
            font-size: 1rem;
        }}
        
        /* Risk levels styling */
        .risk-high {{
            color: {theme['danger']};
            font-weight: bold;
        }}
        
        .risk-medium {{
            color: {theme['warning']};
            font-weight: bold;
        }}
        
        .risk-low {{
            color: {theme['success']};
            font-weight: bold;
        }}
        
        /* Tags */
        .fraud-type-tag {{
            background-color: {theme['primary']};
            color: white;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.8rem;
            display: inline-block;
            margin: 2px;
        }}
        
        /* Cards */
        .card {{
            background-color: {theme['secondary']};
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
        }}
        
        /* Status indicators */
        .status-confirmed {{
            color: {theme['danger']};
        }}
        
        .status-progress {{
            color: {theme['warning']};
        }}
        
        .status-closed {{
            color: {theme['success']};
        }}
    </style>
    """

def apply_theme_to_charts(theme_name: str) -> Dict[str, Any]:
    """
    Get chart configuration options based on the selected theme
    
    Parameters:
    -----------
    theme_name : str
        Name of the theme to apply
        
    Returns:
    --------
    Dict
        Dictionary containing chart configuration options
    """
    if theme_name not in COLOR_SCHEMES:
        theme_name = "professional"  # Default fallback
        
    theme = COLOR_SCHEMES[theme_name]
    
    return {
        "colors": theme["chart_colors"],
        "background_color": theme["background"],
        "text_color": theme["text"],
        "grid_color": theme["secondary"],
        "colorscale": theme["gradient"]
    }

def get_theme_selection_widget():
    """
    Create a theme selection widget for the sidebar
    """
    # Create a container with styling
    st.sidebar.markdown("## Dashboard Theme")
    st.sidebar.markdown("Personalize your fraud analysis experience:")
    
    # Theme selector with descriptions
    theme_descriptions = {
        "professional": "Clean, focused interface for detailed analysis",
        "calm": "Soothing colors to reduce stress during investigation",
        "energetic": "Vibrant colors to maintain alertness during long sessions",
        "dark": "Reduced eye strain for extended use",
        "focus": "High contrast for important metrics and alerts"
    }
    
    # Create the selection widget
    selected_theme = st.sidebar.selectbox(
        "Color Scheme",
        options=list(COLOR_SCHEMES.keys()),
        format_func=lambda x: f"{x.title()} - {theme_descriptions[x]}"
    )
    
    # Apply theme immediately when changed
    if selected_theme:
        # Store in session state
        if 'theme' not in st.session_state or st.session_state.theme != selected_theme:
            st.session_state.theme = selected_theme
            # Force a rerun to apply the theme
            st.rerun()
            
    return st.session_state.get('theme', 'professional')

def initialize_theme():
    """
    Initialize theme settings in the app
    """
    # Default theme if not set
    if 'theme' not in st.session_state:
        st.session_state.theme = 'professional'

def inject_theme_css():
    """
    Inject the current theme's CSS into the app
    """
    theme_name = st.session_state.get('theme', 'professional')
    css = load_theme_css(theme_name)
    st.markdown(css, unsafe_allow_html=True)