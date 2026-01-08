import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Aadhaar Pulse Index | UIDAI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Custom CSS (Clean Government-Grade UI)
# -------------------------------------------------
st.markdown("""
<style>
.metric-card {
    background-color: #f8f9fa;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
}
.metric-title {
    font-size: 14px;
    color: #6c757d;
}
.metric-value {
    font-size: 34px;
    font-weight: 700;
}
.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 35px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Title & Executive Summary
# -------------------------------------------------
st.title("📊 Aadhaar Pulse Index Dashboard")
st.caption(
    "Early-warning analytics system for Aadhaar enrolment & demographic updates"
)

st.info(
    "📌 **Executive Insight**: The Aadhaar Pulse Index converts enrolment momentum, "
    "demographic update behaviour, and volatility into a single early-warning signal. "
    "It enables UIDAI and policymakers to proactively identify operational stress, "
    "awareness gaps, and abnormal trends before citizen service delivery is impacted."
)

st.divider()

# -------------------------------------------------
# Load Data
# -------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("outputs/monthly_combined_features.csv")

df = load_data()

# -------------------------------------------------
# Sidebar – Policy Simulation Controls
# -------------------------------------------------
st.sidebar.header("🏛️ Policy Simulation Controls")

state = st.sidebar.selectbox(
    "Select Geography",
    ["All India"] + sorted(df["state"].unique())
)

# -------------------------------------------------
# Filter Data
# -------------------------------------------------
if state == "All India":
    filtered_df = df.copy()
else:
    filtered_df = df[df["state"] == state]

latest_month = filtered_df["year_month"].max()
latest_df = filtered_df[filtered_df["year_month"] == latest_month]

# -------------------------------------------------
# KPI Calculations
# -------------------------------------------------
national_index = round(filtered_df["aadhaar_pulse_index"].mean(), 2)
anomaly_count = latest_df[latest_df["anomaly_flag"] == -1].shape[0]

if anomaly_count <= 1:
    risk_label = "🟢 STABLE"
    risk_color = "#198754"
    line_color = "green"
elif anomaly_count <= 4:
    risk_label = "🟡 WARNING"
    risk_color = "#ffc107"
    line_color = "orange"
else:
    risk_label = "🔴 CRITICAL"
    risk_color = "#dc3545"
    line_color = "red"

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">National Aadhaar Pulse Index</div>
        <div class="metric-value">{national_index}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">States Flagged (Latest Month)</div>
        <div class="metric-value">{anomaly_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">System Risk Level</div>
        <div class="metric-value" style="color:{risk_color};">
            {risk_label}
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# Trend Analysis
# -------------------------------------------------
st.markdown("<div class='section-title'>📉 Aadhaar Pulse Index Trend</div>", unsafe_allow_html=True)

trend_df = filtered_df.groupby("year_month")["aadhaar_pulse_index"].mean()

fig, ax = plt.subplots(figsize=(12,5))
ax.plot(trend_df.index, trend_df.values, linewidth=3, marker="o", color=line_color)
ax.set_ylabel("Pulse Index")
ax.set_xlabel("Month")

ax.set_title(
    "India – Aadhaar Pulse Index Over Time"
    if state == "All India"
    else f"{state} – Aadhaar Pulse Index Over Time"
)

ax.grid(alpha=0.3)
st.pyplot(fig)

# -------------------------------------------------
# Anomaly Detection
# -------------------------------------------------
st.markdown("<div class='section-title'>⚠️ Anomaly Detection & Early Warnings</div>", unsafe_allow_html=True)

st.info(
    "States are flagged when abnormal divergence is detected between enrolment growth, "
    "demographic updates, and historical volatility patterns."
)

anomalies = filtered_df[filtered_df["anomaly_flag"] == -1]

if anomalies.empty:
    st.success("✅ No abnormal behaviour detected for the selected view.")
else:
    st.warning("⚠️ Potential risk signals detected. Policy attention recommended.")

    st.dataframe(
        anomalies[[
            "state",
            "year_month",
            "aadhaar_pulse_index",
            "update_enrolment_ratio",
            "enrolment_growth_rate",
            "enrolment_volatility"
        ]].sort_values("aadhaar_pulse_index", ascending=False),
        use_container_width=True
    )

# -------------------------------------------------
# Policy Recommendations (WINNING SECTION)
# -------------------------------------------------
st.markdown("<div class='section-title'>🏛️ Policy Recommendations</div>", unsafe_allow_html=True)

if anomaly_count == 0:
    st.write(
        "✅ **No immediate intervention required.** Continue standard monitoring "
        "and routine enrolment awareness programmes."
    )
elif anomaly_count <= 3:
    st.write(
        "⚠️ **Targeted intervention advised.** Conduct district-level audits, "
        "strengthen outreach campaigns, and review update infrastructure capacity."
    )
else:
    st.write(
        "🚨 **Immediate policy action recommended.** Deploy focused enrolment drives, "
        "review system bottlenecks, and initiate rapid diagnostics at affected locations."
    )

# -------------------------------------------------
# Interpretation Guide
# -------------------------------------------------
st.markdown("<div class='section-title'>🧠 How to Interpret This Dashboard</div>", unsafe_allow_html=True)

st.markdown("""
- **Pulse Index** combines enrolment momentum, update behaviour, and volatility.
- **Low index + anomaly flag** → Possible operational or awareness gap.
- **Sudden spikes** → Policy drives, campaigns, or reporting irregularities.
- **Stable trend** → Healthy Aadhaar enrolment ecosystem.
""")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.divider()
st.caption(
    "UIDAI Hackathon 2026 | Built with Python, Pandas, Scikit-learn & Streamlit | "
    "Public aggregated data only.\n\n"
    "*Aadhaar Pulse Index transforms raw operational data into actionable national intelligence.*"
)
