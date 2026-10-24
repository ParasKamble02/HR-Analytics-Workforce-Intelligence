import streamlit as st

def kpi_card(title, value, subtitle=""):
    html = (
        '<div class="kpi-card">'
        f'<div class="kpi-title">{title}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-subtitle">{subtitle}</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def insight_card(title, value, text):
    html = (
        '<div class="insight-card">'
        f'<div class="insight-title">{title}</div>'
        f'<div class="insight-value">{value}</div>'
        f'<div class="insight-text">{text}</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

