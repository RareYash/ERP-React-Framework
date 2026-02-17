

import streamlit as st
import os
import json

def chatbot_component(chat_history, key=None):
    """
    Renders the chatbot custom component.

    Args:
        chat_history: A list of chat messages.
        key: A unique key for the component.

    Returns:
        A dictionary with 'query' key containing the user's query, or None.
    """
    component_path = os.path.join(os.path.dirname(__file__))
    
    with open(os.path.join(component_path, 'index.html'), 'r') as f:
        html = f.read()

    with open(os.path.join(component_path, 'style.css'), 'r') as f:
        css = f.read()

    with open(os.path.join(component_path, 'script.js'), 'r') as f:
        js = f.read()

    # Inject CSS and JS into the HTML
    html = html.replace('<link rel="stylesheet" href="style.css">', f'<style>{css}</style>')
    
    # Inject chat history into the JS
    js_with_history = f"""
        const chatHistory = {json.dumps(chat_history)};
        {js}
    """
    html = html.replace('<script src="script.js"></script>', f'<script>{js_with_history}</script>')

    # Render the component
    st.components.v1.html(html, height=0)
    
    # Check for query parameter in URL
    query_params = st.query_params
    if 'chatbot_query' in query_params:
        query = query_params['chatbot_query']
        # Clear the query parameter
        del st.query_params['chatbot_query']
        return {'query': query}
    
    return None
