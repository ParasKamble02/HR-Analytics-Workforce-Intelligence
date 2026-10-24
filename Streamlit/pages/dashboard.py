
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.cards import kpi_card, insight_card
from components.charts import style_chart, BLUE, INDIGO

from components.hr_charts import render_attrition_breakdown
from utils.metrics import hr_metrics, fmt


# Dashboard Page
def show_dashboard(df, filtered_df):
    # Calculations
    total_employees = len(filtered_df)
    if "Attrition" in filtered_df.columns:
        attrition_count = (
            filtered_df["Attrition"]
            .eq("Yes")
            .sum()
        )
    else:
        attrition_count = 0

    if total_employees > 0:
        attrition_rate = (
            attrition_count / total_employees
        ) * 100
    else:
        attrition_rate = 0

    if "Age" in filtered_df.columns:
        avg_age = filtered_df["Age"].mean()
    else:
        avg_age = 0
    
    m = hr_metrics(filtered_df)


    #Title
    st.title("HR Analytics & Workforce Intelligence")
    st.markdown(
        "Employee attrition, workforce composition and organizational insights"
    )
    st.markdown("")

    # KPI ROW
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card(
            "Total Employees",
            f"{total_employees:,}",
            "Employees currently tracked"
        )

    with c2:
        kpi_card(
            "Attrition",
            f"{attrition_count:,}",
            "Employees who left"
        )

    with c3:
        kpi_card(
            "Attrition Rate",
            f"{attrition_rate:.2f}%",
            "Workforce attrition"
        )

    with c4:
        kpi_card(
            "Average Age",
            f"{avg_age:.1f}",
            "Average employee age"
        )

    # Workfoce Analytics
    st.markdown(
        '<div class="section-title">Workforce Analytics</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1.55, 1])

    st.markdown(
        '<div class="section-title">Workforce Health</div>',
        unsafe_allow_html=True
    )

    h1, h2, h3, h4 = st.columns(4)

    with h1:
        kpi_card("Avg. Tenure", fmt(m["avg_tenure"], "{:.1f} yrs"), "Average years at company")
    with h2:
        kpi_card("Avg. Monthly Income", fmt(m["avg_income"], "${:,.0f}"), "Per employee")
    with h3:
        kpi_card("Overtime", fmt(m["overtime_pct"], "{:.1f}%"), "Employees working overtime")
    with h4:
        kpi_card("Job Satisfaction", fmt(m["avg_satisfaction"], "{:.2f} / 4"), "Average rating")

    with col1:
        render_attrition_breakdown(
            filtered_df,
            mode="counts",
            fallback="tenure"
        )


    # ATTRITION SUMMARY
    with col2:
        st.markdown("### Attrition Summary")
        attrition_summary = pd.DataFrame({
            "Status": [
                "No",
                "Yes"
            ],

            "Employees": [
                total_employees - attrition_count,
                attrition_count
            ]

        })

        fig = px.pie(
            attrition_summary,
            names="Status",
            values="Employees",
            hole=0.68,
            color="Status",
            color_discrete_map={
                "No": BLUE,
                "Yes": INDIGO
            }
        )

        fig.update_traces(
            textinfo="percent",
            textfont_size=14
        )

        fig.update_layout(
            showlegend=True,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            )
        )

        fig = style_chart(
            fig,
            430
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Role Level Analysis
    st.markdown(
        '<div class="section-title">Role-Level Analysis</div>',
        unsafe_allow_html=True
    )

    if "JobRole" in filtered_df.columns:
        role_data = pd.crosstab(
            filtered_df["JobRole"],
            filtered_df["Attrition"]
        ).reset_index()

        fig = go.Figure()

        if "No" in role_data.columns:
            fig.add_trace(
                go.Bar(
                    x=role_data["JobRole"],
                    y=role_data["No"],
                    name="Retained",
                    marker_color=BLUE
                )
            )

        if "Yes" in role_data.columns:
            fig.add_trace(
                go.Bar(
                    x=role_data["JobRole"],
                    y=role_data["Yes"],
                    name="Attrition",
                    marker_color=INDIGO
                )
            )

        fig.update_layout(
            barmode="group",
            xaxis_title="Job Role",
            yaxis_title="Employees"
        )

        fig = style_chart(
            fig,
            480
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Key Workforce Insights
    st.markdown(
        '<div class="section-title">Key Workforce Insights</div>',
        unsafe_allow_html=True
    )

    i1, i2, i3 = st.columns(3)


    # INSIGHT 1 — ATTRITION
    with i1:
        insight_card(
            "Attrition Overview",
            f"{attrition_count:,} employees",
            f"{attrition_rate:.2f}% of the selected "
            "workforce has left the organization."
        )

    # INSIGHT 2 — TOP ROLE
    with i2:
        if "JobRole" in filtered_df.columns:
            if len(filtered_df) > 0:
                top_role = (
                    filtered_df["JobRole"]
                    .value_counts()
                    .idxmax()
                )
            else:
                top_role = "N/A"
        else:
            top_role = "N/A"


        insight_card(
            "Workforce Composition",
            top_role,
            "Most represented job role in the "
            "selected workforce."
        )

    # INSIGHT 3 — AVERAGE AGE
    with i3:
        insight_card(
            "Average Workforce Age",
            f"{avg_age:.1f} years",
            "Average age of employees in the "
            "selected departments."
        )