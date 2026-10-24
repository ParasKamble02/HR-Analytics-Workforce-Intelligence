def calculate_kpis(df):
    total_employees = len(df)

    if "Attrition" in df.columns:
        attrition_count = df["Attrition"].eq("Yes").sum()
    else:
        attrition_count = 0

    if total_employees > 0:
        attrition_rate = (
            attrition_count / total_employees
        ) * 100
    else:
        attrition_rate = 0

    if "Age" in df.columns:
        avg_age = df["Age"].mean()
    else:
        avg_age = 0

    return {
        "total_employees": total_employees,
        "attrition_count": attrition_count,
        "attrition_rate": attrition_rate,
        "avg_age": avg_age
    }