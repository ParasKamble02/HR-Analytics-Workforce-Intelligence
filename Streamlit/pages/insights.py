import html
import streamlit as st
import pandas as pd

from components.cards import insight_card

# Ignore groups smaller than this, so one-person roles can't show "100% attrition"
MIN_GROUP = 10


# Insight Calculation Based On Filtered Data
def highest_attrition_role(data):
    if "JobRole" not in data.columns or "Attrition" not in data.columns:
        return None

    g = data.groupby("JobRole")["Attrition"].agg(
        total="size",
        left=lambda s: s.eq("Yes").sum()
    )
    g = g[g["total"] >= MIN_GROUP]

    if g.empty:
        return None

    g["rate"] = g["left"] / g["total"] * 100
    top = g.sort_values(["rate", "total"], ascending=False).iloc[0]

    return {
        "role": top.name,
        "rate": float(top["rate"]),
        "left": int(top["left"]),
        "total": int(top["total"]),
    }


def overtime_risk(data):
    if "OverTime" not in data.columns or "Attrition" not in data.columns:
        return None

    ot = data[data["OverTime"] == "Yes"]
    no_ot = data[data["OverTime"] == "No"]

    if len(ot) < MIN_GROUP:
        return None

    return {
        "ot_rate": ot["Attrition"].eq("Yes").mean() * 100,
        "no_ot_rate": (
            no_ot["Attrition"].eq("Yes").mean() * 100
            if len(no_ot) >= MIN_GROUP else None
        ),
    }


def satisfaction_effect(data):
    if "JobSatisfaction" not in data.columns or "Attrition" not in data.columns:
        return None

    sat = pd.to_numeric(data["JobSatisfaction"], errors="coerce")
    low = data.loc[sat <= 2, "Attrition"]   
    high = data.loc[sat >= 3, "Attrition"]  

    if len(low) < MIN_GROUP or len(high) < MIN_GROUP:
        return None

    return {
        "low_rate": low.eq("Yes").mean() * 100,
        "high_rate": high.eq("Yes").mean() * 100,
    }


def top_role_composition(data):
    if "JobRole" not in data.columns:
        return None

    counts = data["JobRole"].value_counts()

    if counts.empty:
        return None

    return {
        "role": counts.index[0],
        "count": int(counts.iloc[0]),
        "share": counts.iloc[0] / len(data) * 100,
    }


#Page
def show_insights(df, filtered_df):
    #TITLE
    st.title("Workforce Insights")
    st.markdown("Data-driven findings to support workforce decisions")
    st.markdown("")
    data = filtered_df.copy()
    if data.empty:
        st.warning("No employees match the selected filters.")
        return

    #BASE METRICS
    total = len(data)
    attrition_count = (
        int(data["Attrition"].eq("Yes").sum())
        if "Attrition" in data.columns else 0
    )
    attrition_rate = attrition_count / total * 100
    avg_age = data["Age"].mean() if "Age" in data.columns else 0

    #DYNAMIC INSIGHTS
    role_risk = highest_attrition_role(data)
    ot = overtime_risk(data)
    sat = satisfaction_effect(data)
    comp = top_role_composition(data)
    top_role_name = comp["role"] if comp else "N/A"

    #EXECUTIVE SUMMARY
    st.markdown(
        '<div class="section-title">Executive Summary</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        insight_card(
            "Attrition Overview",
            f"{attrition_count:,} employees",
            f"{attrition_rate:.2f}% of the selected workforce has left the organization."
        )

    with col2:
        insight_card(
            "Workforce Composition",
            html.escape(str(top_role_name)),
            "Most represented job role in the selected workforce."
        )

    with col3:
        insight_card(
            "Average Workforce Age",
            f"{avg_age:.1f} years",
            "Average age of employees in the selected departments."
        )

    #KEY FINDINGS
    st.markdown(
        '<div class="section-title">Key Findings</div>',
        unsafe_allow_html=True
    )

    findings = []

    #Highest attrition role
    if role_risk:
        if role_risk["rate"] > 0:
            findings.append(
                f"{role_risk['role']} has the highest attrition rate at "
                f"{role_risk['rate']:.1f}% "
                f"({role_risk['left']} of {role_risk['total']} employees)."
            )
        else:
            findings.append(
                "No job role in the current selection has recorded any attrition."
            )
    else:
        findings.append(
            "Not enough data to compare attrition across job roles in this selection."
        )

    #Overtime risk
    if ot:
        text = (
            f"Employees working overtime have an attrition rate of {ot['ot_rate']:.1f}%"
        )
        if ot["no_ot_rate"] is not None:
            text += f", compared with {ot['no_ot_rate']:.1f}% for those who do not."
        else:
            text += "."
        findings.append(text)
    else:
        findings.append(
            "Not enough overtime data to assess overtime risk in this selection."
        )

    #Job satisfaction
    if sat:
        if sat["low_rate"] > sat["high_rate"]:
            findings.append(
                f"Employees with low job satisfaction show higher turnover "
                f"({sat['low_rate']:.1f}% vs {sat['high_rate']:.1f}% for satisfied employees)."
            )
        else:
            findings.append(
                f"Employees with low job satisfaction do not show higher turnover "
                f"in this selection ({sat['low_rate']:.1f}% vs {sat['high_rate']:.1f}%)."
            )
    else:
        findings.append(
            "Not enough job satisfaction data to compare turnover in this selection."
        )

    #Workforce composition
    if comp:
        findings.append(
            f"{comp['role']} is the most represented role, with "
            f"{comp['count']:,} employees ({comp['share']:.0f}% of the selection)."
        )
    else:
        findings.append("Job role data is not available for this selection.")

    for i, finding in enumerate(findings, start=1):
        st.markdown(
            f'<div class="finding-row">'
            f'<div class="finding-num">{i:02d}</div>'
            f'<div class="finding-text">{html.escape(finding)}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    #Recommended Actions By Above Findings
    st.markdown(
        '<div class="section-title">Recommended Actions</div>',
        unsafe_allow_html=True
    )
    recommendations = []

    #Role attrition
    if role_risk and role_risk["rate"] > 0:
        recommendations.append((
            "Target High-Attrition Roles",
            f"Prioritise retention for {role_risk['role']}, where "
            f"{role_risk['rate']:.1f}% of employees have left. Review pay, "
            f"workload and career paths for this role first."
        ))
    else:
        recommendations.append((
            "Monitor Attrition",
            "Track attrition by department and job role to catch early "
            "warning signs before turnover rises."
        ))

    #Overtime
    if ot and ot["no_ot_rate"] is not None and ot["ot_rate"] > ot["no_ot_rate"]:
        recommendations.append((
            "Reduce Overtime Pressure",
            f"Overtime staff leave at {ot['ot_rate']:.1f}% versus "
            f"{ot['no_ot_rate']:.1f}% for others. Rebalance workloads or add "
            f"staffing in overtime-heavy roles."
        ))
    elif ot:
        recommendations.append((
            "Keep Overtime Under Review",
            f"Overtime is not linked to higher attrition here "
            f"({ot['ot_rate']:.1f}% for overtime staff). Keep monitoring "
            f"workload as the team changes."
        ))
    else:
        recommendations.append((
            "Review Workload",
            "Collect overtime data so workload-related attrition risk "
            "can be measured."
        ))

    #Satisfaction
    if sat and sat["low_rate"] > sat["high_rate"]:
        recommendations.append((
            "Improve Job Satisfaction",
            f"Low-satisfaction employees leave at {sat['low_rate']:.1f}% versus "
            f"{sat['high_rate']:.1f}%. Run pulse surveys and act on the "
            f"lowest-scoring teams."
        ))
    elif sat:
        recommendations.append((
            "Look Beyond Satisfaction",
            "Satisfaction scores do not explain turnover in this selection. "
            "Check compensation, tenure and manager relationships next."
        ))
    else:
        recommendations.append((
            "Measure Satisfaction",
            "Gather more job satisfaction responses to understand "
            "what drives retention."
        ))

    #Workforce planning
    if comp:
        recommendations.append((
            "Plan Around Key Roles",
            f"{comp['role']} makes up {comp['share']:.0f}% of this selection "
            f"({comp['count']:,} employees). Align hiring and succession "
            f"planning with this concentration."
        ))
    else:
        recommendations.append((
            "Workforce Planning",
            "Use workforce composition and role-level trends to support "
            "future hiring and resource allocation."
        ))
    
    cards = "".join(
        f'<div class="reco-card">'
        f'<div class="insight-title">{html.escape(title)}</div>'
        f'<div class="insight-text">{html.escape(description)}</div>'
        f'</div>'
        for title, description in recommendations
    )

    st.markdown(f'<div class="reco-grid">{cards}</div>', unsafe_allow_html=True)