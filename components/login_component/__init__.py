import os
import streamlit.components.v1 as components

# Declare the component by pointing to the directory containing index.html
_component_func = components.declare_component(
    "login_component",
    path=os.path.dirname(os.path.abspath(__file__))
)

def render_login_component(key=None):
    """
    Renders the flip-card login frontend.
    Returns: 'success' when the user clicks 'Log In' or 'Register', else None.
    """
    return _component_func(key=key, default=None)
