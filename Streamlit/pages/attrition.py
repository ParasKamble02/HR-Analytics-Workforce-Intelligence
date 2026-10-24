import streamlit as st
import pandas as pd
import plotly.express as px

from components.cards import kpi_card
from components.charts import style_chart, BLUE, INDIGO

from components.hr_charts import (render_attrition_breakdown, rate_band_chart, TENURE_BINS, TENURE_LABELS, PROMO_BINS, PROMO_LABELS,)
from utils.metrics import hr_metrics, fmt, STALLED_YEARS

ATTRITION_COLORS = {"No": BLUE, "Yes": INDIGO}

def show_attrition(df, filtered_df):
    # Title
    st.title("Attrition Intelligence")
    st.markdown(
        "Analyze employee turnover and identify major attrition patterns"
    )
    st.markdown("")

    data = filtered_df.copy()

    if data.empty:
        st.warning("No employees match the selected filters.")
        return

    # KPIs
    total = len(data)

    if "Attrition" in data.columns:
        attrition_count = data["Attrition"].eq("Yes").sum()
    else:
        attrition_count = 0

    attrition_rate = attrition_count / total * 100 if total > 0 else 0
    retained = total - attrition_count

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card("Total Employees", f"{total:,}", "Employees in selection")
    with c2:
        kpi_card("Employees Left", f"{attrition_count:,}", "Attrition count")
    with c3:
        kpi_card("Attrition Rate", f"{attrition_rate:.2f}%", "Share of workforce")
    with c4:
        kpi_card("Retained", f"{retained:,}", "Employees still active")

    # DEPARTMENT + SUMMARY
    st.markdown(
        '<div class="section-title">Attrition Breakdown</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1.55, 1])

    with col1:
        render_attrition_breakdown(data, mode="rate", fallback="age", height=400)

    with col2:
        st.markdown("### Attrition Summary")
        if "Attrition" in data.columns:
            summary = data["Attrition"].value_counts().reset_index()
            summary.columns = ["Attrition", "Employees"]

            fig = px.pie(
                summary,
                names="Attrition",
                values="Employees",
                hole=0.68,
                color="Attrition",
                color_discrete_map=ATTRITION_COLORS
            )
            fig.update_traces(textinfo="percent", textfont_size=14)
            fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
            fig = style_chart(fig, 400)
            st.plotly_chart(fig, width="stretch")

    #Job Role
    st.markdown(
        '<div class="section-title">Role-Level Analysis</div>',
        unsafe_allow_html=True
    )

    if "JobRole" in data.columns and "Attrition" in data.columns:
        role = pd.crosstab(data["JobRole"], data["Attrition"]).reset_index()

        for col in ["Yes", "No"]:
            if col not in role.columns:
                role[col] = 0

        role["Attrition Rate"] = role["Yes"] / (role["Yes"] + role["No"]) * 100
        role = role.sort_values("Attrition Rate", ascending=True)

        fig = px.bar(
            role,
            x="Attrition Rate",
            y="JobRole",
            orientation="h",
            text=role["Attrition Rate"].round(1).astype(str) + "%",
            color_discrete_sequence=[BLUE]
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(
            xaxis_title="Attrition Rate (%)",
            yaxis_title="",
            xaxis_range=[0, role["Attrition Rate"].max() * 1.2]
        )
        fig = style_chart(fig, 480)
        st.plotly_chart(fig, width="stretch")

    # Overtime + Satisfaction
    st.markdown(
        '<div class="section-title">Attrition Drivers</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if "OverTime" in data.columns and "Attrition" in data.columns:
            st.markdown("### Attrition vs Overtime")

            overtime = pd.crosstab(data["OverTime"], data["Attrition"]).reset_index()
            y_cols = [c for c in ["No", "Yes"] if c in overtime.columns]

            fig = px.bar(
                overtime,
                x="OverTime",
                y=y_cols,
                barmode="group",
                color_discrete_map=ATTRITION_COLORS,
                labels={"value": "Employees", "variable": "Attrition"}
            )
            fig.update_layout(xaxis_title="Overtime", yaxis_title="Employees")
            fig = style_chart(fig, 380)
            st.plotly_chart(fig, width="stretch")

    with col2:
        if "JobSatisfaction" in data.columns and "Attrition" in data.columns:
            st.markdown("### Attrition vs Job Satisfaction")

            satisfaction = pd.crosstab(
                data["JobSatisfaction"], data["Attrition"]
            ).reset_index()
            y_cols = [c for c in ["No", "Yes"] if c in satisfaction.columns]

            fig = px.bar(
                satisfaction,
                x="JobSatisfaction",
                y=y_cols,
                barmode="group",
                color_discrete_map=ATTRITION_COLORS,
                labels={"value": "Employees", "variable": "Attrition"}
            )
            fig.update_layout(
                xaxis_title="Job Satisfaction",
                yaxis_title="Employees",
                xaxis_type="category"
            )
            fig = style_chart(fig, 380)
            st.plotly_chart(fig, width="stretch")
    

    #Tenure & Promotion
    st.markdown(
        '<div class="section-title">Tenure & Promotion</div>',
        unsafe_allow_html=True
    )

    m = hr_metrics(data)

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        kpi_card("Avg. Tenure", fmt(m["avg_tenure"], "{:.1f} yrs"), "Average years at company")
    with p2:
        kpi_card(
            "Since Last Promotion",
            fmt(m["avg_since_promo"], "{:.1f} yrs"),
            "Average years without promotion"
        )
    with p3:
        kpi_card(
            "Promotion Stalled",
            fmt(m["stalled_pct"], "{:.1f}%"),
            f"{STALLED_YEARS}+ years since promotion"
        )
    with p4:
        kpi_card(
            "Attrition if Stalled",
            fmt(m["stalled_attrition_rate"], "{:.1f}%"),
            "Stalled employees who left"
        )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Attrition by Tenure")
        fig = rate_band_chart(data, "YearsAtCompany", TENURE_BINS, TENURE_LABELS, 380)
        if fig is not None:
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Tenure data is not available.")

    with col2:
        st.markdown("### Attrition by Years Since Promotion")
        fig = rate_band_chart(data, "YearsSinceLastPromotion", PROMO_BINS, PROMO_LABELS, 380)
        if fig is not None:
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Promotion data is not available.")