from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Security Incident & Compliance Dashboard", layout="wide")
st.title("Security Incident & Compliance Tracking Dashboard")
st.caption("Centralized view of security incidents, vulnerabilities, remediation progress and compliance status.")

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

data_path = Path("data/security_tracking_sample.csv")
uploaded = st.sidebar.file_uploader("Upload incident / vulnerability CSV", type=["csv"])
try:
    df = pd.read_csv(uploaded) if uploaded else load_data(data_path)
except Exception as exc:
    st.error(f"Unable to load data: {exc}")
    st.stop()

required = ["Ticket ID", "Type", "Severity", "Status", "Owner", "Reported Date", "Due Date", "Compliance Control"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error("Missing required columns: " + ", ".join(missing))
    st.stop()

df["Reported Date"] = pd.to_datetime(df["Reported Date"], errors="coerce")
df["Due Date"] = pd.to_datetime(df["Due Date"], errors="coerce")
today = pd.Timestamp.today().normalize()
df["Overdue"] = (~df["Status"].str.lower().isin(["closed", "resolved"])) & df["Due Date"].lt(today)
df["Risk Score"] = df["Severity"].str.lower().map({"critical": 10, "high": 8, "medium": 5, "low": 2}).fillna(0)
df["Risk Band"] = df["Risk Score"].map(lambda x: "Critical" if x == 10 else "High" if x >= 8 else "Medium" if x >= 5 else "Low")

st.sidebar.header("Filters")
types = st.sidebar.multiselect("Record type", sorted(df["Type"].dropna().unique()), default=sorted(df["Type"].dropna().unique()))
severities = st.sidebar.multiselect("Severity", sorted(df["Severity"].dropna().unique()), default=sorted(df["Severity"].dropna().unique()))
statuses = st.sidebar.multiselect("Status", sorted(df["Status"].dropna().unique()), default=sorted(df["Status"].dropna().unique()))
view = df[df["Type"].isin(types) & df["Severity"].isin(severities) & df["Status"].isin(statuses)].copy()

total = len(view)
open_count = (~view["Status"].str.lower().isin(["closed", "resolved"])).sum()
overdue = view["Overdue"].sum()
critical_high = view["Severity"].str.lower().isin(["critical","high"]).sum()
closed = view["Status"].str.lower().isin(["closed","resolved"]).sum()
compliance = round(100 * closed / total, 1) if total else 0

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Total records", total)
c2.metric("Open records", int(open_count))
c3.metric("Critical / High", int(critical_high))
c4.metric("Overdue", int(overdue))
c5.metric("Closed / Resolved", f"{compliance}%")

left,right = st.columns(2)
with left:
    st.subheader("Incidents & vulnerabilities by severity")
    sev = view.groupby(["Severity","Type"]).size().reset_index(name="Count")
    if not sev.empty:
        st.plotly_chart(px.bar(sev,x="Severity",y="Count",color="Type",barmode="group"),use_container_width=True)
with right:
    st.subheader("Remediation status")
    stat = view.groupby("Status").size().reset_index(name="Count")
    if not stat.empty:
        st.plotly_chart(px.pie(stat,names="Status",values="Count",hole=.45),use_container_width=True)

st.subheader("Compliance control tracking")
control = view.groupby(["Compliance Control","Status"]).size().reset_index(name="Records")
if not control.empty:
    st.dataframe(control, use_container_width=True, hide_index=True)

st.subheader("Incident and vulnerability register")
show_cols = required + ["Risk Band","Overdue"]
st.dataframe(view[show_cols].sort_values(["Risk Score","Due Date"],ascending=[False,True]), use_container_width=True, hide_index=True)

st.download_button("Download filtered risk report (CSV)", view.to_csv(index=False).encode("utf-8"), "security_risk_report.csv", "text/csv")
st.info("Demo dashboard: sample records are synthetic. Replace them with an authorized export from your ticketing or vulnerability-management system. Risk bands are illustrative prioritization labels, not a formal compliance assessment.")
