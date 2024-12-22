import streamlit as st
from typing import Optional
from src.ui.config import ModelConfig, AVAILABLE_MODELS, create_agent
from src.utils.config import get_api_key

def render_sidebar() -> Optional[ModelConfig]:
    """Render sidebar with model selection"""
    # Get available models with valid API keys
    available_models = [
        model for model in AVAILABLE_MODELS 
        if get_api_key(model.api_key_name)
    ]
    
    if not available_models:
        st.error("No API keys found. Please add API keys to your .env file.")
        return None
    
    # Agent selection
    st.subheader("Select Agent")
    model_names = [model.name for model in available_models]
    selected_name = st.selectbox("Choose an agent", model_names)
    
    selected_model = next(model for model in available_models if model.name == selected_name)
    
    if st.button("Initialize Agent"):
        with st.spinner("Initializing agent..."):
            try:
                create_agent(selected_model)
                st.success(f"Successfully initialized {selected_model.provider} agent")
                return selected_model
            except Exception as e:
                st.error(f"Error initializing model: {str(e)}")
                return None
    
    return selected_model

async def render_chat_interface():
    """Render the main chat interface"""
    st.title("🤖 Multi-Agent Thinking Chat")
    
    # Chat history display
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            if msg.get("thinking") and st.session_state.selected_model.supports_thinking:
                with st.expander("Thinking Process"):
                    st.write(msg["thinking"])
            st.write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Enter your message"):
        # Add user message to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Get response from current agent
        with st.chat_message("assistant"):
            thinking_placeholder = st.empty()
            response_placeholder = st.empty()
            
            agent = st.session_state.current_agent
            if agent:
                message_placeholder = st.empty()
                thinking = ""
                response = ""
                
                import asyncio
                
                try:
                    async def process_stream():
                        nonlocal thinking, response
                        async for chunk in agent.stream_chat(prompt):
                            thinking = chunk["thinking"]
                            response = chunk["response"]
                            
                            if thinking and st.session_state.selected_model.supports_thinking:
                                with thinking_placeholder:
                                    with st.expander("Thinking Process"):
                                        st.write(thinking)
                            
                            if response:
                                response_placeholder.write(response)
                    
                    # Run the async stream processing
                    await process_stream()
                    
                    # Add assistant message to chat history
                    history_entry = {
                        "role": "assistant",
                        "content": response
                    }
                    if st.session_state.selected_model.supports_thinking:
                        history_entry["thinking"] = thinking
                    st.session_state.chat_history.append(history_entry)
                    
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
            else:
                st.warning("Please initialize an agent first")

def render_model_info(model: Optional[ModelConfig]):
    """Render information about the currently selected model"""
    if model:
        st.write(f"**Provider:** {model.provider}")
        st.write(f"**Description:** {model.description}")
