import streamlit as st
import pandas as pd

from components.cards import kpi_card


def show_employees(df, filtered_df):
    # TITLE
    st.title("Employee Directory")
    st.markdown("Explore and analyze individual employee records")
    data = filtered_df.copy()
    if data.empty:
        st.warning("No employees match the selected filters.")
        return

    #SEARCH + QUICK FILTERS
    st.markdown(
        '<div class="section-title section-title-tight">Search & Filters</div>',
        unsafe_allow_html=True
    )

    search = st.text_input(
        "Search employees",
        placeholder="Search by employee ID, job role, department..."
    )

    if search:
        search = search.lower()
        mask = pd.Series(False, index=data.index)

        for column in data.columns:
            if (
                data[column].dtype == "object"
                or str(data[column].dtype).startswith("string")
            ):
                mask |= (
                    data[column]
                    .astype(str)
                    .str.lower()
                    .str.contains(search, na=False, regex=False)
                )

        data = data[mask]

    c1, c2, c3 = st.columns(3)

    with c1:
        if "Attrition" in data.columns:
            attrition_filter = st.selectbox("Attrition", ["All", "Yes", "No"])
            if attrition_filter != "All":
                data = data[data["Attrition"] == attrition_filter]

    with c2:
        if "Department" in data.columns:
            dept_options = ["All"] + sorted(
                data["Department"].dropna().unique().tolist()
            )
            dept_filter = st.selectbox("Department", dept_options)
            if dept_filter != "All":
                data = data[data["Department"] == dept_filter]

    with c3:
        if "JobRole" in data.columns:
            role_options = ["All"] + sorted(
                data["JobRole"].dropna().unique().tolist()
            )
            role_filter = st.selectbox("Job Role", role_options)
            if role_filter != "All":
                data = data[data["JobRole"] == role_filter]

    #SUMMARY KPIs
    st.markdown(
        '<div class="section-title">Selection Summary</div>',
        unsafe_allow_html=True
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi_card("Displayed Employees", f"{len(data):,}", "Matching your filters")

    with k2:
        if "MonthlyIncome" in data.columns and len(data) > 0:
            kpi_card(
                "Average Income",
                f"${data['MonthlyIncome'].mean():,.0f}",
                "Monthly income"
            )
        else:
            kpi_card("Average Income", "N/A", "Monthly income")

    with k3:
        if "YearsAtCompany" in data.columns and len(data) > 0:
            kpi_card(
                "Avg. Years at Company",
                f"{data['YearsAtCompany'].mean():.1f}",
                "Average tenure"
            )
        else:
            kpi_card("Avg. Years at Company", "N/A", "Average tenure")

    with k4:
        if "Attrition" in data.columns and len(data) > 0:
            rate = data["Attrition"].eq("Yes").mean() * 100
            kpi_card("Attrition Rate", f"{rate:.2f}%", "In this selection")
        else:
            kpi_card("Attrition Rate", "N/A", "In this selection")


    #RECORDS TABLE
    if data.empty:
        st.markdown(
            '<div class="section-title">Employee Records (0)</div>',
            unsafe_allow_html=True
        )
        st.info("No records match your search and filters.")
        return

    preferred = [
        "EmployeeNumber", "Age", "Gender", "Department", "JobRole",
        "MonthlyIncome", "JobSatisfaction", "YearsAtCompany",
        "OverTime", "Attrition"
    ]

    available = [col for col in preferred if col in data.columns]
    remaining = [col for col in data.columns if col not in available]
    export_df = data[available + remaining]

    head_col, btn_col = st.columns([3, 1], vertical_alignment="center")

    with head_col:
        st.markdown(
            f'<div class="section-title">Employee Records ({len(export_df):,})</div>',
            unsafe_allow_html=True
        )

    with btn_col:
        st.download_button(
            label=f"Download {len(export_df):,} records (CSV)",
            data=export_df.to_csv(index=False).encode("utf-8"),
            file_name="employee_records.csv",
            mime="text/csv",
            key="export_employees_csv",
            width="stretch",
        )

    st.dataframe(
        export_df,
        width="stretch",
        height=520,
        hide_index=True
    )
