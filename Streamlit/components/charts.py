import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

PLOT_BG = "#11141d"
GRID_COLOR = "#292e3a"
TEXT_COLOR = "#c8cdd8"
BLUE = "#3B82F6"
INDIGO = "#6366F1"

def style_chart(fig, height=400):
    fig.update_layout(
        height=height,
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(
            color=TEXT_COLOR,
            family="Inter, Arial"
        ),
        margin=dict(
            l=50,
            r=25,
            t=25,
            b=50
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#b9bfcc")
        ),
        hoverlabel=dict(
            bgcolor="#181c26",
            font_color="#ffffff"
        )
    )

    fig.update_xaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor=GRID_COLOR,
        linecolor=GRID_COLOR
    )

    fig.update_yaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor=GRID_COLOR,
        linecolor=GRID_COLOR
    )
    return fig

def department_attrition_chart(df):
    data = pd.crosstab(
        df["Department"],
        df["Attrition"]
    ).reset_index()

    fig = go.Figure()

    if "No" in data.columns:
        fig.add_trace(
            go.Bar(
                x=data["Department"],
                y=data["No"],
                name="Retained",
                marker_color=BLUE
            )
        )
    if "Yes" in data.columns:
        fig.add_trace(
            go.Bar(
                x=data["Department"],
                y=data["Yes"],
                name="Attrition",
                marker_color=INDIGO
            )
        )
    fig.update_layout(
        barmode="stack",
        xaxis_title="",
        yaxis_title="Employees"
    )
    return style_chart(fig, 430)

def attrition_donut(df):
    attrition_count = df["Attrition"].eq("Yes").sum()
    total = len(df)
    data = {
        "Status": ["No", "Yes"],
        "Employees": [
            total - attrition_count,
            attrition_count
        ]
    }
    fig = px.pie(
        data,
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
    return style_chart(fig, 430)