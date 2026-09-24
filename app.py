import sqlite3
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Fitbit Health & Activity Dashboard", 
    page_icon="🏃", 
    layout="wide"
)

st.title("🏃 Fitbit Health & Fitness Analytics Dashboard")
st.markdown("Explore step counts, goal performance, and heart rate metrics using SQL-powered insights.")


# Database Helper Function
def run_query(query):
    """Execute SQL query and return results as DataFrame"""
    try:
        conn = sqlite3.connect("fitbit.db")
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return None


# Navigation Sidebar
st.sidebar.header("📊 Navigation")
option = st.sidebar.selectbox(
    "Select Analysis View",
    [
        "Overview Metrics",
        "Step Goal Performance Filter",
        "Heart Rate Analytics",
        "Hourly Step Trends",
        "Custom SQL Runner",
    ],
)

# ====================================================
# View 1: Overview Metrics
# ====================================================
if option == "Overview Metrics":
    st.header("📈 Overall User Summaries")

    query = """
        SELECT 
            Id AS User_ID, 
            SUM(StepTotal) AS Total_Steps, 
            ROUND(AVG(StepTotal), 0) AS Avg_Daily_Steps,
            COUNT(ActivityDay) AS Days_Tracked
        FROM daily_steps
        GROUP BY Id
        ORDER BY Total_Steps DESC;
    """
    df_overview = run_query(query)

    if df_overview is not None:
        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Total Tracked Users", len(df_overview))
        col2.metric(
            "🏆 Highest Daily Avg", 
            f"{int(df_overview['Avg_Daily_Steps'].max()):,} steps"
        )
        col3.metric(
            "📊 Overall Avg Daily Steps",
            f"{int(df_overview['Avg_Daily_Steps'].mean()):,} steps",
        )

        st.subheader("User Step Performance Summary")
        st.dataframe(df_overview, use_container_width=True)

# ====================================================
# View 2: Step Goal Performance Filter
# ====================================================
elif option == "Step Goal Performance Filter":
    st.header("🎯 Interactive Step-Goal Filter")

    # Interactive Goal Slider
    step_goal = st.sidebar.slider(
        "Set Custom Daily Step Goal",
        min_value=1000,
        max_value=20000,
        value=10000,
        step=500,
    )

    query = f"""
        SELECT 
            Id AS User_ID,
            ActivityDay,
            StepTotal,
            CASE WHEN StepTotal >= {step_goal} THEN 'Goal Met' ELSE 'Goal Missed' END AS Goal_Status
        FROM daily_steps
        ORDER BY StepTotal DESC;
    """
    df_goals = run_query(query)

    if df_goals is not None:
        total_days = len(df_goals)
        met_days = len(df_goals[df_goals["Goal_Status"] == "Goal Met"])
        pct_met = round((met_days / total_days) * 100, 1) if total_days > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("🎯 Target Step Goal", f"{step_goal:,} steps")
        col2.metric("✅ Total Days Goal Met", f"{met_days} days")
        col3.metric("📈 Goal Achievement Rate", f"{pct_met}%")

        st.subheader("Goal Performance Breakdown")
        status_filter = st.radio(
            "Filter View By Goal Status:", ["All", "Goal Met", "Goal Missed"]
        )

        if status_filter != "All":
            df_goals = df_goals[df_goals["Goal_Status"] == status_filter]

        st.dataframe(df_goals, use_container_width=True)

# ====================================================
# View 3: Heart Rate Analytics
# ====================================================
elif option == "Heart Rate Analytics":
    st.header("❤️ Heart Rate Analysis")

    try:
        # User Selection
        users = run_query("SELECT DISTINCT Id FROM heart_rate;")
        if users is not None and not users.empty:
            users_list = users["Id"].tolist()
            selected_user = st.selectbox("Select User ID", users_list)

            query = f"""
                SELECT Time, Value AS HeartRate
                FROM heart_rate
                WHERE Id = {selected_user}
                ORDER BY Time;
            """
            df_hr = run_query(query)

            if df_hr is not None and not df_hr.empty:
                col1, col2, col3 = st.columns(3)
                col1.metric("📉 Min Heart Rate", f"{int(df_hr['HeartRate'].min())} BPM")
                col2.metric("📊 Avg Heart Rate", f"{int(df_hr['HeartRate'].mean())} BPM")
                col3.metric("📈 Max Heart Rate", f"{int(df_hr['HeartRate'].max())} BPM")

                st.subheader(f"Heart Rate Over Time for User {selected_user}")
                st.line_chart(df_hr.set_index("Time")["HeartRate"])

                # Intensity Distribution Breakdown
                st.subheader("❤️ Heart Rate Zones Breakdown")
                resting = len(df_hr[df_hr["HeartRate"] < 60])
                moderate = len(
                    df_hr[(df_hr["HeartRate"] >= 60) & (df_hr["HeartRate"] <= 100)]
                )
                active = len(df_hr[df_hr["HeartRate"] > 100])

                zones_df = pd.DataFrame({
                    "Zone": ["Resting (<60 BPM)", "Normal (60-100 BPM)", "Elevated (>100 BPM)"],
                    "Record Count": [resting, moderate, active],
                })
                st.bar_chart(zones_df.set_index("Zone"))
            else:
                st.warning("No heart rate data available for this user.")
        else:
            st.warning("No heart rate data found in database.")

    except Exception as e:
        st.error(
            f"Unable to load heart rate data. Error: {e}\n\n"
            "💡 Tip: Make sure your `heart_rate` table is loaded in fitbit.db"
        )

# ====================================================
# View 4: Hourly Step Trends
# ====================================================
elif option == "Hourly Step Trends":
    st.header("📊 Hourly Activity Trends")

    query = """
        SELECT ActivityHour, ROUND(AVG(StepTotal), 1) AS Avg_Steps
        FROM hourly_steps
        GROUP BY ActivityHour
        ORDER BY ActivityHour;
    """
    df_hourly = run_query(query)

    if df_hourly is not None:
        st.subheader("Average Steps Across All Users by Hour")
        st.bar_chart(df_hourly.set_index("ActivityHour"))

# ====================================================
# View 5: Custom SQL Runner
# ====================================================
elif option == "Custom SQL Runner":
    st.header("🔧 Run Custom SQL Query")
    st.caption("Available tables: `daily_steps`, `hourly_steps`, `heart_rate`")

    default_query = "SELECT * FROM daily_steps LIMIT 10;"
    user_query = st.text_area("Enter your SQL Query:", default_query, height=120)

    if st.button("Execute Query"):
        result = run_query(user_query)
        if result is not None:
            st.success(f"✅ Query returned {len(result)} rows.")
            st.dataframe(result, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("📚 **Built with:** Streamlit + SQLite + Pandas")
