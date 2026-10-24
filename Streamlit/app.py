
import streamlit as st
import pandas as pd
from pathlib import Path

from components.styles import load_styles
from components.sidebar import show_sidebar

from pages.dashboard import show_dashboard
from pages.workforce import show_workforce
from pages.attrition import show_attrition
from pages.employees import show_employees
from pages.insights import show_insights


#Page Config
st.set_page_config(
    page_title="HR Intelligence",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
load_styles()

# Load Data
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"

csv_files = list(DATA_DIR.glob("*.csv"))

if not csv_files:
    st.error(
        "No CSV dataset found inside the data folder."
    )
    st.stop()

df = pd.read_csv(csv_files[0])


#Data cleaning
df.columns = df.columns.str.strip()

for col in df.select_dtypes(
    include="object"
).columns:
    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
    )

if "Attrition" in df.columns:
    df["Attrition"] = (
        df["Attrition"]
        .astype(str)
        .str.strip()
        .str.title()
    )

if "Department" in df.columns:
    df["Department"] = (
        df["Department"]
        .astype(str)
        .str.strip()
    )

if "JobRole" in df.columns:
    df["JobRole"] = (
        df["JobRole"]
        .astype(str)
        .str.strip()
    )


#Sidebar
page, filtered_df = show_sidebar(df)

# Page Routing
if page == "Dashboard":
    show_dashboard(
        df,
        filtered_df
    )

elif page == "Workforce":
    show_workforce(
        df,
        filtered_df
    )

elif page == "Attrition":
    show_attrition(
        df,
        filtered_df
    )

elif page == "Employees":
    show_employees(
        df,
        filtered_df
    )

elif page == "Insights":
    show_insights(
        df,
        filtered_df
    )


#Footer
st.markdown(
    """
    <div style="
        text-align:center;
        color:#555d6e;
        font-size:0.72rem;
        margin-top:50px;
        padding-top:20px;
        border-top:1px solid #20242e;
    ">
        HR Analytics & Workforce Intelligence
    </div>
    """,
    unsafe_allow_html=True
)

