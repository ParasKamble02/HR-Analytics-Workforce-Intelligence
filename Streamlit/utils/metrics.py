import pandas as pd

STALLED_YEARS = 5   
MIN_GROUP = 10      

def _num(data, col):
    if col not in data.columns:
        return None
    return pd.to_numeric(data[col], errors="coerce")

def _mean(data, col):
    s = _num(data, col)
    if s is None or s.dropna().empty:
        return None
    return float(s.mean())

def hr_metrics(data):
    keys = [
        "avg_tenure", "avg_income", "avg_satisfaction", "avg_since_promo",
        "overtime_pct", "stalled_pct", "stalled_attrition_rate",
        "income_left", "income_stayed", "income_gap_pct", "income_tenure_corr",
    ]
    m = {k: None for k in keys}

    if data.empty:
        return m

    m["avg_tenure"] = _mean(data, "YearsAtCompany")
    m["avg_income"] = _mean(data, "MonthlyIncome")
    m["avg_satisfaction"] = _mean(data, "JobSatisfaction")
    m["avg_since_promo"] = _mean(data, "YearsSinceLastPromotion")

    if "OverTime" in data.columns:
        m["overtime_pct"] = float(data["OverTime"].eq("Yes").mean() * 100)

    #Promotion indicators
    promo = _num(data, "YearsSinceLastPromotion")
    if promo is not None:
        stalled = promo >= STALLED_YEARS
        m["stalled_pct"] = float(stalled.mean() * 100)
        if "Attrition" in data.columns and stalled.sum() >= MIN_GROUP:
            m["stalled_attrition_rate"] = float(
                data.loc[stalled, "Attrition"].eq("Yes").mean() * 100
            )

    #Income of leavers vs retained employees
    income = _num(data, "MonthlyIncome")
    if income is not None and "Attrition" in data.columns:
        left = income[data["Attrition"].eq("Yes")].dropna()
        stayed = income[data["Attrition"].eq("No")].dropna()
        if len(left) >= MIN_GROUP and len(stayed) >= MIN_GROUP:
            m["income_left"] = float(left.mean())
            m["income_stayed"] = float(stayed.mean())
            m["income_gap_pct"] = float(
                (left.mean() - stayed.mean()) / stayed.mean() * 100
            )

    #Income vs tenure correlation
    tenure = _num(data, "YearsAtCompany")
    if income is not None and tenure is not None and len(data) >= MIN_GROUP:
        r = income.corr(tenure)
        if pd.notna(r):
            m["income_tenure_corr"] = float(r)
    return m

def fmt(value, template, na="N/A"):
    """fmt(12.34, "{:.1f} yrs") -> '12.3 yrs'. Returns 'N/A' when value is None."""
    return na if value is None else template.format(value)