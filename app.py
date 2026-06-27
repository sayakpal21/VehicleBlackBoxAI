import streamlit as st
import pandas as pd
import plotly.express as px
from agents import *

st.set_page_config(
    page_title="Vehicle Black Box AI",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Vehicle Black Box AI")
st.caption("An Agentic AI Framework for Autonomous Vehicle Failure Investigation")

st.sidebar.title("Upload Vehicle Logs")

can_file = st.sidebar.file_uploader(
    "CAN Log",
    type="csv"
)

dtc_file = st.sidebar.file_uploader(
    "DTC Log",
    type="csv"
)

event_file = st.sidebar.file_uploader(
    "Event Log",
    type="csv"
)

if can_file and dtc_file and event_file:

    can_df = pd.read_csv(can_file)
    dtc_df = pd.read_csv(dtc_file)
    event_df = pd.read_csv(event_file)

    st.success("Vehicle logs uploaded successfully.")

    tabs = st.tabs([
        "📊 Dashboard",
        "🕒 Timeline Agent",
        "📈 Signal Agent",
        "🛠 Diagnostics Agent",
        "🧠 Root Cause Agent",
        "📄 AI Report"
    ])

    ##################################################

    with tabs[0]:

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("CAN Frames",len(can_df))
        c2.metric("DTCs",len(dtc_df))
        c3.metric("Events",len(event_df))
        c4.metric("Vehicle Health","82%")

        fig = px.line(
            can_df,
            x="timestamp",
            y="motor_current",
            title="Motor Current"
        )

        st.plotly_chart(fig,use_container_width=True)

    ##################################################

    with tabs[1]:

        st.subheader("Timeline Agent")

        timeline = timeline_agent(
            can_df,
            dtc_df,
            event_df
        )

        st.dataframe(timeline)

    ##################################################

    with tabs[2]:

        st.subheader("Signal Intelligence Agent")

        anomalies = signal_agent(can_df)

        st.write(anomalies)

        fig = px.line(
            can_df,
            x="timestamp",
            y=[
                "steering_torque",
                "motor_current"
            ]
        )

        st.plotly_chart(fig,use_container_width=True)

    ##################################################

    with tabs[3]:

        st.subheader("Diagnostics Agent")

        diagnosis = diagnostics_agent(
            dtc_df
        )

        st.json(diagnosis)

    ##################################################

    with tabs[4]:

        st.subheader("Root Cause Agent")

        result = rootcause_agent(
            can_df,
            dtc_df,
            event_df
        )

        st.success(result["Root Cause"])

        st.metric(
            "Confidence",
            result["Confidence"]
        )

        st.write(result["Evidence"])

    ##################################################

    with tabs[5]:

        st.subheader("AI Investigation Report")

        report = report_agent(
            can_df,
            dtc_df,
            event_df
        )

        st.markdown(report)

else:

    st.info("Upload all three log files to begin investigation.")