import streamlit as st
import pandas as pd
import plotly.express as px

from components.cards import kpi_card
from components.charts import style_chart, BLUE, INDIGO

PALETTE = [BLUE, INDIGO, "#8B5CF6", "#06B6D4", "#22C55E", "#F59E0B"]

from components.hr_charts import render_headcount_breakdown, income_tenure_chart
from utils.metrics import hr_metrics, fmt

def corr_label(r):
    """Turn a correlation number into plain words."""
    if r is None:
        return "N/A", "Not enough data"
    
    a = abs(r)
    if a < 0.1:
        strength = "None"
    elif a < 0.3:
        strength = "Weak"
    elif a < 0.6:
        strength = "Moderate"
    else:
        strength = "Strong"

    if strength == "None":
        return strength, f"No clear link ({r:+.2f})"
    direction = "Higher pay with tenure" if r > 0 else "Lower pay with tenure"
    return f"{strength} {'+' if r > 0 else '-'}", f"{direction} ({r:+.2f})"


def show_workforce(df, filtered_df):
    #TITLE
    st.title("Workforce Overview")
    st.markdown("Workforce composition, demographics and organizational structure")
    st.markdown("")
    data = filtered_df.copy()
    if data.empty:
        st.warning("No employees match the selected filters.")
        return

    #KPIs
    total = len(data)
    avg_age = data["Age"].mean() if "Age" in data.columns else 0
    avg_income = data["MonthlyIncome"].mean() if "MonthlyIncome" in data.columns else 0
    departments = data["Department"].nunique() if "Department" in data.columns else 0

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card("Total Employees", f"{total:,}", "Employees in selection")
    with c2:
        kpi_card("Average Age", f"{avg_age:.1f}", "Average employee age")
    with c3:
        kpi_card("Avg. Monthly Income", f"${avg_income:,.0f}", "Per employee")
    with c4:
        kpi_card("Departments", f"{departments}", "In current selection")

    #STRUCTURE
    st.markdown(
        '<div class="section-title">Organizational Structure</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        render_headcount_breakdown(data, height=400)

    with col2:
        st.markdown("### Workforce by Job Role")
        if "JobRole" in data.columns:
            role = data["JobRole"].value_counts().reset_index()
            role.columns = ["Job Role", "Employees"]
            role = role.sort_values("Employees", ascending=True)
            fig = px.bar(
                role,
                x="Employees",
                y="Job Role",
                orientation="h",
                text="Employees",
                color_discrete_sequence=[INDIGO]
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(
                xaxis_title="Employees",
                yaxis_title="",
                xaxis_range=[0, role["Employees"].max() * 1.2]
            )
            fig = style_chart(fig, 400)
            st.plotly_chart(fig, width="stretch")

    #DEMOGRAPHICS
    st.markdown(
        '<div class="section-title">Demographics</div>',
        unsafe_allow_html=True
    )

    if "Age" in data.columns:
        st.markdown("### Age Distribution")
        fig = px.histogram(
            data,
            x="Age",
            nbins=20,
            color_discrete_sequence=[BLUE]
        )
        fig.update_traces(marker_line_color="#11141d", marker_line_width=1)
        fig.update_layout(
            xaxis_title="Age",
            yaxis_title="Employees",
            bargap=0.05
        )
        fig = style_chart(fig, 380)
        st.plotly_chart(fig, width="stretch")

    col1, col2 = st.columns([1, 1.4])

    with col1:
        if "Gender" in data.columns:
            st.markdown("### Gender Composition")
            gender = data["Gender"].value_counts().reset_index()
            gender.columns = ["Gender", "Employees"]
            fig = px.pie(
                gender,
                names="Gender",
                values="Employees",
                hole=0.68,
                color_discrete_sequence=PALETTE
            )
            fig.update_traces(textinfo="percent", textfont_size=14)
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            fig = style_chart(fig, 380)
            st.plotly_chart(fig, width="stretch")

    with col2:
        if "EducationField" in data.columns:
            st.markdown("### Education Field")
            education = data["EducationField"].value_counts().reset_index()
            education.columns = ["Education Field", "Employees"]
            fig = px.bar(
                education,
                x="Education Field",
                y="Employees",
                text="Employees",
                color_discrete_sequence=[BLUE]
            )
            fig.update_traces(textposition="outside", cliponaxis=False)
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Employees",
                yaxis_range=[0, education["Employees"].max() * 1.2]
            )
            fig = style_chart(fig, 380)
            st.plotly_chart(fig, width="stretch")
    
    #COMPENSATION & TENURE
    st.markdown(
        '<div class="section-title">Compensation & Tenure</div>',
        unsafe_allow_html=True
    )

    m = hr_metrics(data)

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        kpi_card("Avg. Income (Retained)", fmt(m["income_stayed"], "${:,.0f}"), "Monthly income")
    with q2:
        kpi_card("Avg. Income (Left)", fmt(m["income_left"], "${:,.0f}"), "Monthly income")
    with q3:
        kpi_card("Leavers' Pay Gap", fmt(m["income_gap_pct"], "{:+.1f}%"), "Left vs. retained average")
    # with q4:
    #     kpi_card("Income-Tenure Link", fmt(m["income_tenure_corr"], "r = {:+.2f}"), "Correlation, -1 to +1")
    with q4:
        corr_value, corr_note = corr_label(m["income_tenure_corr"]) 
        kpi_card("Pay vs Tenure", corr_value, corr_note)

    st.markdown("### Income vs Tenure")

    fig = income_tenure_chart(data, 440)
    if fig is not None:
        st.plotly_chart(fig, width="stretch")
        st.caption("Each dot is one employee. Orange dots are employees who left.")
    else:
        st.info("Income or tenure data is not available.")