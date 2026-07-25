import pandas as pd
import plotly.express as px
import streamlit as st
from main import analyze_threat_with_real_ai, detect_brute_force, load_logs

# 1. הגדרת תצורת העמוד
st.set_page_config(
    page_title="CyberThreat-AI Sentinel", page_icon="🛡️", layout="wide"
)

# 2. כותרת ראשית
st.title("🛡️ CyberThreat-AI Sentinel")
st.markdown("### Real-time Log Analysis & AI Threat Investigation Dashboard")
st.divider()

# 3. תפריט צד (Sidebar) – העלאת קבצים
st.sidebar.header("⚙️ Configuration")
log_file = st.sidebar.file_uploader("Upload Log File (CSV)", type=["csv"])

# טעינת נתונים בטוחה
if log_file is not None:
    try:
        # Streamlit מעביר אובייקט זיכרון, pd.read_csv יודע לקרוא אותו ישירות!
        df = pd.read_csv(log_file)
        st.sidebar.success("✅ File uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error reading CSV file: {e}")
        df = load_logs("network_logs.csv")
else:
    df = load_logs("network_logs.csv")

# 4. שורת מטריקות עליונה
col1, col2, col3 = st.columns(3)

total_logs = len(df)
brute_force_df = detect_brute_force(df)
total_threats = len(brute_force_df)
total_bytes = df["bytes_transferred"].sum()

col1.metric("Total Logs Processed", total_logs)
col2.metric("Detected Threats", total_threats, delta_color="inverse")
col3.metric("Total Data Volume (Bytes)", f"{total_bytes:,}")

st.divider()

# 5. ויזואליזציות וגרפים (Plotly)
st.subheader("📊 Network Activity & Traffic Analysis")

fig = px.bar(
    df,
    x="timestamp",
    y="bytes_transferred",
    color="action",
    title="Data Transfer Volume by Timestamp and Action",
    labels={
        "bytes_transferred": "Bytes Transferred",
        "timestamp": "Timestamp",
    },
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# 6. תחקיר AI
st.subheader("🤖 AI SOC Analyst Reports")

if not brute_force_df.empty:
    st.warning(
        f"⚠️ Found {len(brute_force_df)} Suspicious Activity Pattern(s)!"
    )

    # כפתור להרצת ניתוח ה-AI
    if st.button("🚀 Run AI Analysis on Threats"):
        with st.spinner("Communicating with AI Agent via Groq API..."):
            for index, row in brute_force_df.iterrows():
                analysis = analyze_threat_with_real_ai(row, "Brute Force")

                if analysis:
                    severity = analysis.get("severity", "UNKNOWN")
                    ip = row["source_ip"]

                    with st.expander(
                        f"🚨 Threat Alert: Source IP {ip} (Severity: {severity})",
                        expanded=True,
                    ):
                        st.json(analysis)
else:
    st.success("✅ No threats detected in current logs.")