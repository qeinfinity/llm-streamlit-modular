import asyncio
import streamlit as st
from src.ui.app import main

if __name__ == "__main__":
    st.set_page_config(
        page_title="Multi-Agent Thinking Chat",
        page_icon="🤖",
        layout="wide"
    )
    asyncio.run(main())
