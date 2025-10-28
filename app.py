# app.py
# 🏥 Hospital Appointment No-Show Analysis Dashboard

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Hospital Appointment Dashboard", layout="wide")

st.title("🏥 Hospital Appointment No-Show Dashboard")
st.markdown("""
Analyze hospital appointment data to identify trends and reduce patient no-shows.
""")

# --- File Upload ---
uploaded_file = st.file_uploader("📂 Upload appointment dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # --- Basic Cleaning ---
    if 'No-show' in df.columns:
        df.rename(columns={'No-show': 'No_show'}, inplace=True)
    df['No_show'] = df['No_show'].apply(lambda x: 1 if x == 'Yes' else 0)

    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
    df['WaitingDays'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days

    df = df[(df['Age'] >= 0) & (df['WaitingDays'] >= 0)]
    
    # --- Summary Metrics ---
    total_appointments = len(df)
    no_show_rate = df['No_show'].mean() * 100
    avg_wait = df['WaitingDays'].mean()

    st.subheader("📊 Summary Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", f"{total_appointments:,}")
    col2.metric("No-Show Rate", f"{no_show_rate:.1f}%")
    col3.metric("Avg. Waiting Days", f"{avg_wait:.1f}")

    st.divider()

    # --- Filters ---
    st.sidebar.header("🔍 Filters")
    gender_filter = st.sidebar.selectbox("Filter by Gender", options=["All"] + list(df["Gender"].unique()))
    if gender_filter != "All":
        df = df[df["Gender"] == gender_filter]

    sms_filter = st.sidebar.radio("Filter by SMS Received", options=["All", "Yes", "No"])
    if sms_filter == "Yes":
        df = df[df["SMS_received"] == 1]
    elif sms_filter == "No":
        df = df[df["SMS_received"] == 0]

    st.sidebar.markdown("---")
    st.sidebar.caption("Filters help you explore different patient segments.")

    # --- Visual Insights ---
    st.subheader("📈 Visual Insights")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        sns.countplot(x='No_show', data=df, ax=ax)
        ax.set_title('Attendance vs No-Show')
        ax.set_xlabel("0 = Show, 1 = No-Show")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        sns.barplot(x='SMS_received', y='No_show', data=df, ax=ax)
        ax.set_title('Effect of SMS Reminders on Attendance')
        ax.set_xlabel('SMS Received (1 = Yes)')
        ax.set_ylabel('No-Show Rate')
        st.pyplot(fig)

    # --- Age & Waiting Days ---
    st.subheader("📉 Age & Waiting Time Insights")

    col3, col4 = st.columns(2)

    with col3:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(data=df, x='Age', hue='No_show', multiple='stack', bins=30, ax=ax)
        ax.set_title('Age Distribution by Attendance')
        st.pyplot(fig)

    with col4:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(x='No_show', y='WaitingDays', data=df, ax=ax)
        ax.set_title('Waiting Days vs Attendance')
        st.pyplot(fig)

    # --- Insights Summary ---
    st.subheader("🧠 Insights Summary")
    st.markdown(f"""
    - **Overall no-show rate:** {no_show_rate:.1f}%  
    - **SMS reminders:** Patients with SMS are far less likely to miss appointments.  
    - **Waiting time:** Patients with longer waiting periods are more likely to skip.  
    - **Age trend:** Youth and elderly show higher absence rates.  
    """)

    st.success("✅ Tip: Use SMS reminders and shorter scheduling windows to reduce no-shows in Kenyan hospitals.")

else:
    st.info("👆 Upload your dataset to begin analysis.")
