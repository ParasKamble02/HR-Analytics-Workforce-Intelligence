import streamlit as st

def render_html(html: str):
    cleaned = "\n".join(
        line.strip() for line in html.splitlines() if line.strip()
    )
    st.html(cleaned)