import streamlit as st
from utils.helpers import render_html


def show_sidebar(df):

    with st.sidebar:

        #Brand
        render_html("""
        <div class="sidebar-brand">
            <div class="brand-icon">👥</div>
            <div class="brand-content">
                <div class="brand-title">HR Intelligence</div>
                <div class="brand-subtitle">WORKFORCE ANALYTICS</div>
            </div>
        </div>
        """)

        #Navigation
        render_html('<div class="sidebar-section-label">NAVIGATION</div>')

        page = st.radio(
            "Navigation",
            ["Dashboard", "Workforce", "Attrition", "Employees", "Insights"],
            index=0,
            label_visibility="collapsed"
        )

        #Divider
        render_html('<div class="sidebar-divider"></div>')

        #Filters
        render_html('<div class="sidebar-section-label">FILTERS</div>')

        if "Department" in df.columns:
            departments = sorted(df["Department"].dropna().unique().tolist())
            selected_departments = st.multiselect(
                "Select Department",
                options=departments,
                default=departments
            )
        else:
            selected_departments = []

        #Footer
        render_html("""
        <div class="sidebar-footer">
            <div class="footer-status"></div>
            <div>
                <div class="footer-title">HR Analytics & Workforce Intelligence</div>
                <div class="footer-text">Workforce decision support</div>
            </div>
        </div>
        """)

    #Filter Data
    if "Department" in df.columns and selected_departments:
        filtered_df = df[df["Department"].isin(selected_departments)].copy()
    elif "Department" in df.columns:
        filtered_df = df.iloc[0:0].copy()
    else:
        filtered_df = df.copy()
    return page, filtered_df