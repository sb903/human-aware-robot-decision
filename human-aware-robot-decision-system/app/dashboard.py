import streamlit as st
import sys, os
import pandas as pd
from datetime import datetime

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from decision_engine.risk_assessment import calculate_risk
from decision_engine.action_selector import select_action

st.set_page_config(
    page_title="Human-Aware Robot Decision System",
    layout="wide"
)

# -------------------------------
# Title
# -------------------------------
st.title("🤖 Human-Aware Robot Decision System")
st.caption("Real-time risk-aware robot decision making around humans")

# -------------------------------
# Sidebar Inputs
# -------------------------------
st.sidebar.header(" Human Situation")

distance = st.sidebar.slider("Distance (meters)", 0.3, 5.0, 1.5, 0.1)
motion = st.sidebar.selectbox("Motion", ["standing", "walking", "running"])
env = st.sidebar.selectbox("Environment", ["room", "corridor", "open_space"])

# -------------------------------
# Decision Logic
# -------------------------------
risk = calculate_risk(distance, motion, env)
action = select_action(risk)

# Risk label
if risk < 0.4:
    risk_label = "LOW"
elif risk < 0.7:
    risk_label = "MEDIUM"
else:
    risk_label = "HIGH"

# -------------------------------
# Layout
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader(" Risk Assessment")

    st.metric("Risk Score", round(risk, 2))
    st.metric("Risk Level", risk_label)

    if risk_label == "LOW":
        st.success("Safe to proceed")
    elif risk_label == "MEDIUM":
        st.warning("Caution advised")
    else:
        st.error("Unsafe — stop robot")

with col2:
    st.subheader("🤖 Robot Decision")

    if action == "PROCEED":
        st.success("✅ PROCEED")
    elif action == "SLOW_DOWN":
        st.warning("⚠️ SLOW DOWN")
    else:
        st.error("🛑 STOP")

# -------------------------------
# Explanation
# -------------------------------
st.subheader(" Explanation")
st.write(f"""
- **Distance:** {distance} m  
- **Motion:** {motion}  
- **Environment:** {env}  
- **Calculated risk:** {round(risk, 2)}  
- **Selected action:** {action}
""")

# -------------------------------
# History (session memory)
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Save this decision"):
    st.session_state.history.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "distance": distance,
        "motion": motion,
        "environment": env,
        "risk": round(risk, 2),
        "action": action
    })

# -------------------------------
# History Table
# -------------------------------
if st.session_state.history:
    st.subheader(" Decision History")
    hist_df = pd.DataFrame(st.session_state.history)
    st.dataframe(hist_df, use_container_width=True)

    # Download button
    csv = hist_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download History as CSV",
        csv,
        "robot_decisions.csv",
        "text/csv"
    )

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Built by you • Human-Aware Robotics Project")
