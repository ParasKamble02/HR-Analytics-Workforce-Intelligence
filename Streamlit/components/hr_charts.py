import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.charts import style_chart, department_attrition_chart, BLUE, INDIGO

AMBER = "#F59E0B"

TENURE_BINS = [-1, 2, 5, 10, 100]
TENURE_LABELS = ["0-2 yrs", "3-5 yrs", "6-10 yrs", "11+ yrs"]

PROMO_BINS = [-1, 1, 4, 7, 100]
PROMO_LABELS = ["0-1 yrs", "2-4 yrs", "5-7 yrs", "8+ yrs"]

AGE_BINS = [0, 29, 39, 49, 100]
AGE_LABELS = ["Under 30", "30-39", "40-49", "50+"]


# Rate charts
def _rate_figure(x_labels, rates, lefts, totals, height, x_title=""):
    fig = go.Figure(go.Bar(
        x=x_labels,
        y=rates,
        text=[f"{r:.1f}%" for r in rates],
        textposition="outside",
        cliponaxis=False,
        marker_color=INDIGO,
        customdata=list(zip(lefts, totals)),
        hovertemplate=(
            "%{x}<br>Attrition rate: %{y:.1f}%"
            "<br>%{customdata[0]} of %{customdata[1]} employees left"
            "<extra></extra>"
        ),
    ))
    top = max(max(rates), 5)
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title="Attrition Rate (%)",
        yaxis_range=[0, top * 1.3],
    )
    return style_chart(fig, height)


def rate_band_chart(data, column, bins, labels, height=400, x_title=""):
    """Attrition rate per band of a numeric column (tenure, age, years since promotion)."""
    if column not in data.columns or "Attrition" not in data.columns or data.empty:
        return None
    band = pd.cut(pd.to_numeric(data[column], errors="coerce"), bins=bins, labels=labels)
    t = (
        pd.DataFrame({"Band": band, "Left": data["Attrition"].eq("Yes")})
        .groupby("Band", observed=False)["Left"]
        .agg(total="size", left="sum")
        .reset_index()
    )
    t["rate"] = (t["left"] / t["total"].where(t["total"] > 0) * 100).fillna(0)

    x_labels = [f"{b}<br>n={n}" for b, n in zip(t["Band"].astype(str), t["total"])]

    return _rate_figure(
        x_labels, t["rate"].tolist(), t["left"].tolist(), t["total"].tolist(),
        height, x_title
    )


def department_rate_chart(data, height=400):
    if "Department" not in data.columns or "Attrition" not in data.columns or data.empty:
        return None
    t = (
        pd.DataFrame({"Department": data["Department"], "Left": data["Attrition"].eq("Yes")})
        .groupby("Department")["Left"]
        .agg(total="size", left="sum")
        .reset_index()
    )
    t["rate"] = t["left"] / t["total"] * 100
    return _rate_figure(
        t["Department"].tolist(), t["rate"].tolist(),
        t["left"].tolist(), t["total"].tolist(), height
    )


# Headcount charts
def _count_figure(x_labels, counts, height, color=BLUE, x_title=""):
    fig = go.Figure(go.Bar(
        x=x_labels,
        y=counts,
        text=counts,
        textposition="outside",
        cliponaxis=False,
        marker_color=color,
    ))
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title="Employees",
        yaxis_range=[0, max(max(counts), 1) * 1.2],
    )
    return style_chart(fig, height)

def headcount_band_chart(data, column, bins, labels, height=400, x_title=""):
    if column not in data.columns or data.empty:
        return None

    band = pd.cut(pd.to_numeric(data[column], errors="coerce"), bins=bins, labels=labels)
    counts = band.value_counts(sort=False).reindex(labels, fill_value=0)

    return _count_figure(list(counts.index.astype(str)), counts.tolist(), height, x_title=x_title)


def department_headcount_chart(data, height=400):
    if "Department" not in data.columns or data.empty:
        return None

    counts = data["Department"].value_counts()
    return _count_figure(counts.index.tolist(), counts.tolist(), height)


#single department charts
def _single_department(data):
    return None


def render_attrition_breakdown(data, mode="counts", fallback="tenure", height=430):
    # Several departments -> attrition by department. One department -> attrition by tenure (or age) band instead.
    if data.empty or "Attrition" not in data.columns:
        st.markdown("### Attrition Breakdown")
        st.info("Not enough data for this chart.")
        return

    single = _single_department(data)

    if single is None:
        st.markdown("### Attrition by Department")
        fig = (
            department_attrition_chart(data)
            if mode == "counts"
            else department_rate_chart(data, height)
        )
    else:
        if fallback == "age":
            st.markdown("### Attrition by Age Band")
            fig = rate_band_chart(data, "Age", AGE_BINS, AGE_LABELS, height)
            what = "age band"
        else:
            st.markdown("### Attrition by Tenure Band")
            fig = rate_band_chart(data, "YearsAtCompany", TENURE_BINS, TENURE_LABELS, height)
            what = "tenure band"
        st.caption(f"Only {single} is selected, so this is broken down by {what} instead of by department.")

    if fig is None:
        st.info("Not enough data for this chart.")
        return

    st.plotly_chart(fig, width="stretch")


def render_headcount_breakdown(data, height=400):
    # Several departments -> headcount by department. One -> headcount by tenure band.
    if data.empty:
        return

    single = _single_department(data)

    if single is None:
        st.markdown("### Workforce by Department")
        fig = department_headcount_chart(data, height)
    else:
        st.markdown("### Workforce by Tenure")
        fig = headcount_band_chart(data, "YearsAtCompany", TENURE_BINS, TENURE_LABELS, height)
        st.caption(f"Only {single} is selected, so this is broken down by tenure instead of by department.")

    if fig is None:
        st.info("Not enough data for this chart.")
        return

    st.plotly_chart(fig, width="stretch")


# INCOME VS TENURE
def income_tenure_chart(data, height=440):
    if not {"MonthlyIncome", "YearsAtCompany"}.issubset(data.columns) or data.empty:
        return None

    plot = data.copy()

    if "Attrition" in plot.columns:
        plot["Status"] = plot["Attrition"].map({"No": "Retained", "Yes": "Left"}).fillna("Unknown")
    else:
        plot["Status"] = "Employees"

    fig = px.scatter(
        plot,
        x="YearsAtCompany",
        y="MonthlyIncome",
        color="Status",
        color_discrete_map={
            "Retained": BLUE,
            "Left": AMBER,
            "Employees": BLUE,
            "Unknown": "#8f98aa",
        },
        category_orders={"Status": ["Retained", "Left"]},
        hover_data=[c for c in ["JobRole", "Department"] if c in plot.columns],
        opacity=0.6,
        labels={
            "YearsAtCompany": "Years at Company",
            "MonthlyIncome": "Monthly Income ($)",
        },
    )
    fig.update_traces(marker=dict(size=7))
    fig.update_layout(legend_title_text="")

    return style_chart(fig, height)