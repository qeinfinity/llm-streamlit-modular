import asyncio
import streamlit as st
from .components import render_sidebar, render_chat_interface, render_model_info
from .config import initialize_session_state

async def main():
    """Main application entry point"""
    # Initialize session state
    initialize_session_state()
    
    # Create columns for chat and agent selection
    chat_col, agent_col = st.columns([4, 1])
    
    with agent_col:
        # Render agent selection and get selected model
        selected_model = render_sidebar()
        # Display model info
        render_model_info(selected_model)
    
    with chat_col:
        # Render main chat interface
        await render_chat_interface()

if __name__ == "__main__":
    asyncio.run(main())
