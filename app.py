import sqlite3
import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')
 
# ========================================================
# PAGE CONFIGURATION
# ========================================================
st.set_page_config(
    page_title="🔥 Advanced Fitbit Analytics Pro", 
    page_icon="🔥", 
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# Hide streamlit style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
 
st.title("🔥 Advanced Fitbit Analytics Pro - AI Powered Fitness Intelligence")
st.markdown("""
    **Enterprise-Grade Fitness Analytics Dashboard**
    
    Powered by AI, machine learning, and advanced statistical analysis. 
    Get intelligent insights, personalized recommendations, and predictive analytics for your fitness journey.
""")
 
# ========================================================
# DATABASE & CACHING
# ========================================================
@st.cache_data(ttl=300)
def run_query(query):
    """Execute SQL query with caching"""
    try:
        conn = sqlite3.connect("fitbit.db")
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return None
 
# ========================================================
# ADVANCED ANALYTICS FUNCTIONS
# ========================================================
 
def classify_fitness_level(avg_steps):
    """Classify fitness level with detailed description"""
    classifications = {
        'Sedentary': (0, 5000, "🔴", "Below WHO recommendations. High health risk."),
        'Low Active': (5000, 7500, "🟠", "Some activity but needs improvement."),
        'Somewhat Active': (7500, 10000, "🟡", "Approaching recommended level."),
        'Active': (10000, 12500, "🟢", "Meeting WHO daily activity recommendations."),
        'Very Active': (12500, float('inf'), "🟢", "Excellent fitness level!"),
    }
    
    for level, (min_val, max_val, emoji, desc) in classifications.items():
        if min_val <= avg_steps < max_val:
            return level, emoji, desc
    
    return 'Sedentary', '🔴', 'Below recommendations'
 
 
def calculate_advanced_metrics(df_daily):
    """Calculate comprehensive fitness metrics"""
    if df_daily is None or df_daily.empty:
        return {}
    
    data = df_daily['StepTotal'].values
    
    return {
        'total_steps': int(data.sum()),
        'avg_daily': float(data.mean()),
        'median': float(np.median(data)),
        'std_dev': float(data.std()),
        'min': int(data.min()),
        'max': int(data.max()),
        'q1': float(np.percentile(data, 25)),
        'q3': float(np.percentile(data, 75)),
        'iqr': float(np.percentile(data, 75) - np.percentile(data, 25)),
        'skewness': float(stats.skew(data)),
        'kurtosis': float(stats.kurtosis(data)),
        'cv': float((data.std() / data.mean() * 100)) if data.mean() != 0 else 0,  # Coefficient of variation
        'days_tracked': len(df_daily),
    }
 
 
def calculate_goal_achievement(df_daily, goal=10000):
    """Calculate goal achievement metrics"""
    if df_daily is None or df_daily.empty:
        return {}
    
    goal_met = len(df_daily[df_daily['StepTotal'] >= goal])
    total_days = len(df_daily)
    
    return {
        'days_met': goal_met,
        'total_days': total_days,
        'percentage': (goal_met / total_days * 100) if total_days > 0 else 0,
        'deficit': max(0, goal - df_daily['StepTotal'].mean()),
    }
 
 
def calculate_streaks(df_daily, goal=10000):
    """Calculate current and best streaks"""
    if df_daily is None or df_daily.empty:
        return {'current': 0, 'best': 0}
    
    df_sorted = df_daily.sort_values('ActivityDay')
    streaks = []
    current_streak = 0
    
    for steps in df_sorted['StepTotal']:
        if steps >= goal:
            current_streak += 1
        else:
            if current_streak > 0:
                streaks.append(current_streak)
            current_streak = 0
    
    if current_streak > 0:
        streaks.append(current_streak)
    
    return {
        'current': current_streak,
        'best': max(streaks) if streaks else 0,
        'average': np.mean(streaks) if streaks else 0,
    }
 
 
def predict_trend(df_daily, days_ahead=30):
    """Predict future activity trend using linear regression"""
    if df_daily is None or len(df_daily) < 7:
        return None
    
    df_copy = df_daily.copy()
    df_copy['ActivityDay'] = pd.to_datetime(df_copy['ActivityDay'])
    df_copy = df_copy.sort_values('ActivityDay')
    
    x = np.arange(len(df_copy))
    y = df_copy['StepTotal'].values
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    future_days = np.arange(len(df_copy), len(df_copy) + days_ahead)
    predictions = slope * future_days + intercept
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_value ** 2,
        'predictions': predictions,
        'trend': 'Improving 📈' if slope > 0 else 'Declining 📉' if slope < 0 else 'Stable 📊',
    }
 
 
def get_insights(metrics, goal_metrics, streaks):
    """Generate AI-powered insights based on data"""
    insights = []
    
    # Insight 1: Consistency
    if metrics.get('cv', 0) < 20:
        insights.append(("✅ High Consistency", f"Your activity varies only {metrics.get('cv', 0):.1f}%. Very consistent!"))
    elif metrics.get('cv', 0) > 50:
        insights.append(("⚠️ High Variability", f"Your activity varies {metrics.get('cv', 0):.1f}%. Consider scheduling regular walks."))
    
    # Insight 2: Goal Performance
    if goal_metrics.get('percentage', 0) >= 80:
        insights.append(("🎯 Goal Champion", f"You're achieving your goal {goal_metrics.get('percentage', 0):.1f}% of days!"))
    elif goal_metrics.get('percentage', 0) < 20:
        insights.append(("📈 Growth Opportunity", f"Only {goal_metrics.get('percentage', 0):.1f}% goal achievement. Add 2-3 short walks daily."))
    
    # Insight 3: Streak
    if streaks.get('current', 0) > 7:
        insights.append(("🔥 Hot Streak!", f"You're on a {streaks.get('current', 0)}-day streak! Don't break it!"))
    
    # Insight 4: Distribution
    if metrics.get('skewness', 0) > 1:
        insights.append(("📊 Right Skewed", "You have some exceptional high-activity days. Try to replicate those!"))
    elif metrics.get('skewness', 0) < -1:
        insights.append(("📊 Left Skewed", "You have many high-activity days. Keep maintaining this!"))
    
    return insights
 
 
def get_personalized_plan(metrics, goal=10000):
    """Generate personalized weekly activity plan"""
    avg = metrics.get('avg_daily', 0)
    
    if avg < 5000:
        return {
            'level': 'Beginner',
            'weekly_total': 35000,
            'plan': {
                'Monday': '🚶 20-min walk (2,500 steps)',
                'Tuesday': '🚶 20-min walk (2,500 steps)',
                'Wednesday': '🚶 20-min walk (2,500 steps)',
                'Thursday': 'Rest day (1,000 steps)',
                'Friday': '🚶 20-min walk (2,500 steps)',
                'Saturday': '🚶 30-min walk (3,500 steps)',
                'Sunday': '🚶 30-min walk (3,500 steps)',
            }
        }
    elif avg < 7500:
        return {
            'level': 'Intermediate',
            'weekly_total': 52500,
            'plan': {
                'Monday': '🚶 30-min walk (3,500 steps)',
                'Tuesday': '🏃 15-min jog + walk (5,000 steps)',
                'Wednesday': '🚶 30-min walk (3,500 steps)',
                'Thursday': '🧘 Yoga + light walk (2,500 steps)',
                'Friday': '🚶 30-min walk (3,500 steps)',
                'Saturday': '🎾 Sports/hiking (7,500 steps)',
                'Sunday': '🚶 Casual walk (4,000 steps)',
            }
        }
    else:
        return {
            'level': 'Advanced',
            'weekly_total': 70000,
            'plan': {
                'Monday': '🏃 Running (8,000 steps)',
                'Tuesday': '🚴 Cycling (7,000 steps)',
                'Wednesday': '🏃 Running (8,000 steps)',
                'Thursday': '🧘 Cross-training (5,000 steps)',
                'Friday': '🏃 Running (8,000 steps)',
                'Saturday': '🎾 Intensive sport (12,000 steps)',
                'Sunday': '🚶 Active recovery (7,000 steps)',
            }
        }
 
 
def analyze_day_of_week_patterns(df_daily):
    """Analyze patterns by day of week"""
    if df_daily is None or df_daily.empty:
        return pd.DataFrame()
    
    df_daily['ActivityDay'] = pd.to_datetime(df_daily['ActivityDay'])
    df_daily['DayOfWeek'] = df_daily['ActivityDay'].dt.day_name()
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    analysis = df_daily.groupby('DayOfWeek')['StepTotal'].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).reindex(day_order)
    
    return analysis.reset_index()
 
 
def analyze_time_of_day(df_hourly):
    """Analyze activity patterns by hour"""
    if df_hourly is None or df_hourly.empty:
        return pd.DataFrame()
    
    analysis = df_hourly.groupby('ActivityHour')['StepTotal'].agg([
        'count', 'mean', 'max', 'min'
    ]).reset_index()
    
    return analysis
 
 
def calculate_health_score(metrics, goal_metrics):
    """Calculate overall fitness health score (0-100)"""
    score = 0
    
    # Base score (0-40 points)
    avg_achievement = min(metrics.get('avg_daily', 0) / 10000 * 40, 40)
    score += avg_achievement
    
    # Consistency bonus (0-30 points)
    consistency = max(0, 100 - metrics.get('cv', 0))
    consistency_points = consistency / 100 * 30
    score += consistency_points
    
    # Streak bonus (0-20 points)
    streak_bonus = min((metrics.get('days_tracked', 0) / 365 * 20), 20)
    score += streak_bonus
    
    # Variability penalty (0-10 points)
    if metrics.get('skewness', 0) > 1:
        score += 10  # Good skewness
    
    return min(score, 100)
 
 
def generate_advanced_recommendations(metrics, goal_metrics, streaks, day_analysis):
    """Generate advanced, AI-powered recommendations"""
    recommendations = []
    
    # Recommendation 1: Time-based
    if day_analysis is not None and not day_analysis.empty:
        best_day = day_analysis.loc[day_analysis['mean'].idxmax(), 'DayOfWeek']
        worst_day = day_analysis.loc[day_analysis['mean'].idxmin(), 'DayOfWeek']
        
        rec = f"📅 **Schedule workouts:** Your best day is {best_day} ({day_analysis.loc[day_analysis['DayOfWeek']==best_day, 'mean'].values[0]:.0f} avg). "
        rec += f"Boost {worst_day} activity ({day_analysis.loc[day_analysis['DayOfWeek']==worst_day, 'mean'].values[0]:.0f} avg) with an extra walk."
        recommendations.append(rec)
    
    # Recommendation 2: Goal setting
    if goal_metrics.get('percentage', 0) < 50:
        current_avg = metrics.get('avg_daily', 0)
        target = current_avg * 1.15  # 15% increase
        recommendations.append(f"🎯 **Gradual increase:** Aim for {int(target):,} steps (15% above your current average). Add this gradually over 2-3 weeks.")
    
    # Recommendation 3: Variability management
    if metrics.get('cv', 0) > 40:
        recommendations.append(f"⏰ **Schedule consistency:** Set alarms for morning (7 AM) and evening (5 PM) walks. This reduces variability from {metrics.get('cv', 0):.1f}% to ~20%.")
    
    # Recommendation 4: Intensity
    if metrics.get('avg_daily', 0) >= 10000 and metrics.get('max', 0) > metrics.get('avg_daily', 0) * 1.5:
        recommendations.append(f"💪 **Add variety:** Mix in different activities (cycling, swimming, hiking) to prevent adaptation plateau.")
    
    # Recommendation 5: Recovery
    if metrics.get('std_dev', 0) > metrics.get('avg_daily', 0) * 0.5:
        recommendations.append(f"🧘 **Include rest days:** Plan 1-2 low-intensity days per week to prevent burnout and injury.")
    
    return recommendations
 
 
# ========================================================
# SIDEBAR NAVIGATION
# ========================================================
st.sidebar.header("🎯 Advanced Analytics Pro Menu")
st.sidebar.markdown("---")
 
main_option = st.sidebar.radio(
    "📊 Select Dashboard",
    ["🏠 Executive Dashboard", "📈 Advanced Analytics", "💡 AI Insights", "📊 Detailed Reports"],
    label_visibility="collapsed"
)
 
if main_option == "🏠 Executive Dashboard":
    sub_option = st.sidebar.selectbox(
        "Choose View",
        ["🎯 Overview", "❤️ Health Score", "📱 Quick Stats"]
    )
elif main_option == "📈 Advanced Analytics":
    sub_option = st.sidebar.selectbox(
        "Choose Analysis",
        ["📊 Trend Analysis", "🗓️ Day of Week Patterns", "⏰ Peak Hours", "📈 Predictive Analytics"]
    )
elif main_option == "💡 AI Insights":
    sub_option = st.sidebar.selectbox(
        "Choose Insight",
        ["🧠 AI Recommendations", "🎖️ Achievements", "🎯 Goal Strategy", "💪 Performance Tips"]
    )
else:
    sub_option = st.sidebar.selectbox(
        "Choose Report",
        ["📋 Weekly Report", "📅 Monthly Report", "🔧 SQL Explorer", "📥 Data Export"]
    )
 
st.sidebar.markdown("---")
 
# ========================================================
# USER SELECTION
# ========================================================
users_query = "SELECT DISTINCT Id FROM daily_steps ORDER BY Id;"
users_df = run_query(users_query)
 
if users_df is not None and not users_df.empty:
    users_list = users_df['Id'].tolist()
    selected_user = st.sidebar.selectbox("👤 Select User", users_list)
    
    # Load user data
    user_query = f"SELECT * FROM daily_steps WHERE Id = {selected_user} ORDER BY ActivityDay;"
    df_user = run_query(user_query)
    
    hourly_query = f"SELECT * FROM hourly_steps WHERE Id = {selected_user} ORDER BY ActivityHour;"
    df_hourly = run_query(hourly_query)
    
    if df_user is not None and not df_user.empty:
        # Calculate all metrics
        metrics = calculate_advanced_metrics(df_user)
        goal = st.sidebar.slider("🎯 Daily Goal", 5000, 20000, 10000, 500)
        goal_metrics = calculate_goal_achievement(df_user, goal)
        streaks = calculate_streaks(df_user, goal)
        day_analysis = analyze_day_of_week_patterns(df_user)
        fitness_level, emoji, description = classify_fitness_level(metrics['avg_daily'])
        health_score = calculate_health_score(metrics, goal_metrics)
        
        # ====================================================
        # VIEW 1: EXECUTIVE DASHBOARD - OVERVIEW
        # ====================================================
        if main_option == "🏠 Executive Dashboard" and sub_option == "🎯 Overview":
            st.header("🎯 Your Fitness Overview")
            
            # Top metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📊 Total Steps", f"{metrics['total_steps']:,}")
            col2.metric("📈 Daily Average", f"{metrics['avg_daily']:,.0f}")
            col3.metric("🔥 Best Day", f"{metrics['max']:,}")
            col4.metric("🏆 Fitness Level", f"{emoji} {fitness_level}")
            
            # Progress metrics
            st.markdown("### 🎯 Goal Progress")
            col1, col2, col3 = st.columns(3)
            
            col1.metric("🎯 Daily Goal", f"{goal:,} steps")
            col2.metric("✅ Days Met", f"{goal_metrics['days_met']}/{goal_metrics['total_days']}")
            col3.metric("📊 Achievement", f"{goal_metrics['percentage']:.1f}%")
            
            st.progress(min(goal_metrics['percentage'] / 100, 1.0))
            
            # 30-day trend
            st.markdown("### 📉 Last 30 Days Trend")
            df_recent = df_user.tail(30).copy()
            df_recent['ActivityDay'] = pd.to_datetime(df_recent['ActivityDay'])
            df_recent = df_recent.sort_values('ActivityDay')
            
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(df_recent['ActivityDay'], df_recent['StepTotal'], marker='o', linewidth=2, markersize=4)
            ax.axhline(y=goal, color='r', linestyle='--', label=f'Goal: {goal:,}')
            ax.fill_between(df_recent['ActivityDay'], 0, df_recent['StepTotal'], alpha=0.3)
            ax.set_xlabel('Date')
            ax.set_ylabel('Steps')
            ax.set_title('30-Day Activity Trend')
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
            # Key insights
            st.markdown("### 💡 Key Insights")
            insights = get_insights(metrics, goal_metrics, streaks)
            for title, text in insights:
                if "✅" in title or "🔥" in title:
                    st.success(f"{title}: {text}")
                else:
                    st.warning(f"{title}: {text}")
        
        # ====================================================
        # VIEW 2: EXECUTIVE DASHBOARD - HEALTH SCORE
        # ====================================================
        elif main_option == "🏠 Executive Dashboard" and sub_option == "❤️ Health Score":
            st.header("❤️ Fitness Health Score")
            
            # Display health score
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🎖️ Overall Score", f"{health_score:.1f}/100")
            with col2:
                st.metric("📈 Activity Level", f"{metrics['avg_daily']:.0f} steps/day")
            with col3:
                st.metric("🎯 Consistency", f"{100 - metrics['cv']:.1f}%")
            
            # Score breakdown
            st.markdown("### 📊 Score Breakdown")
            
            breakdown_data = pd.DataFrame({
                'Component': ['Activity Level', 'Consistency', 'Streak Bonus', 'Stability'],
                'Score': [
                    min(metrics['avg_daily'] / 10000 * 40, 40),
                    max(0, 100 - metrics['cv']) / 100 * 30,
                    min((metrics['days_tracked'] / 365 * 20), 20),
                    10 if metrics['skewness'] > 1 else 5
                ]
            })
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.barh(breakdown_data['Component'], breakdown_data['Score'], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
            ax.set_xlabel('Points')
            ax.set_title('Health Score Breakdown')
            ax.set_xlim(0, 40)
            for i, v in enumerate(breakdown_data['Score']):
                ax.text(v + 1, i, f'{v:.1f}', va='center')
            st.pyplot(fig)
            
            # Improvement areas
            st.markdown("### 🚀 Improvement Opportunities")
            if health_score < 50:
                st.warning(f"⚠️ Your score ({health_score:.1f}) is below average. Focus on consistency and increasing daily steps.")
            elif health_score < 75:
                st.info(f"📈 Your score ({health_score:.1f}) is good! Continue building consistency.")
            else:
                st.success(f"🌟 Excellent score ({health_score:.1f})! You're in great shape!")
            
            # Recommendations
            st.markdown("### 💡 How to Improve")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Quick Wins (+5-10 points):**
                - Add 15-min walk after lunch
                - Take stairs instead of elevator
                - Park farther away
                """)
            with col2:
                st.markdown("""
                **Long-term Gains (+15-25 points):**
                - Join a sports club
                - Daily exercise routine
                - Weekend hiking trips
                """)
        
        # ====================================================
        # VIEW 3: QUICK STATS
        # ====================================================
        elif main_option == "🏠 Executive Dashboard" and sub_option == "📱 Quick Stats":
            st.header("📊 Quick Statistics")
            
            # Statistics table
            stats_data = pd.DataFrame({
                'Metric': [
                    'Total Steps',
                    'Average Daily',
                    'Median Daily',
                    'Best Day',
                    'Worst Day',
                    'Standard Deviation',
                    'Coefficient of Variation',
                    'Days Tracked',
                    'Skewness',
                    'Kurtosis'
                ],
                'Value': [
                    f"{metrics['total_steps']:,}",
                    f"{metrics['avg_daily']:,.0f}",
                    f"{metrics['median']:,.0f}",
                    f"{metrics['max']:,}",
                    f"{metrics['min']:,}",
                    f"{metrics['std_dev']:,.0f}",
                    f"{metrics['cv']:.1f}%",
                    f"{metrics['days_tracked']}",
                    f"{metrics['skewness']:.2f}",
                    f"{metrics['kurtosis']:.2f}"
                ]
            })
            
            st.dataframe(stats_data, use_container_width=True)
            
            # Distribution visualization
            st.markdown("### 📊 Activity Distribution")
            
            fig, axes = plt.subplots(1, 2, figsize=(12, 4))
            
            # Histogram
            axes[0].hist(df_user['StepTotal'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
            axes[0].axvline(metrics['avg_daily'], color='red', linestyle='--', linewidth=2, label='Mean')
            axes[0].axvline(metrics['median'], color='green', linestyle='--', linewidth=2, label='Median')
            axes[0].set_xlabel('Steps')
            axes[0].set_ylabel('Frequency')
            axes[0].set_title('Step Distribution')
            axes[0].legend()
            axes[0].grid(True, alpha=0.3)
            
            # Box plot
            axes[1].boxplot(df_user['StepTotal'], vert=True)
            axes[1].set_ylabel('Steps')
            axes[1].set_title('Activity Box Plot')
            axes[1].grid(True, alpha=0.3)
            
            st.pyplot(fig)
        
        # ====================================================
        # VIEW 4: ADVANCED ANALYTICS - TREND ANALYSIS
        # ====================================================
        elif main_option == "📈 Advanced Analytics" and sub_option == "📊 Trend Analysis":
            st.header("📊 Advanced Trend Analysis")
            
            # Trend prediction
            trend_data = predict_trend(df_user)
            
            if trend_data:
                col1, col2, col3 = st.columns(3)
                col1.metric("📈 Trend Direction", trend_data['trend'])
                col2.metric("📊 R² Score", f"{trend_data['r_squared']:.3f}")
                col3.metric("📉 Daily Change", f"{trend_data['slope']:.1f} steps/day")
                
                # Visualization with prediction
                st.markdown("### 📈 Activity Trend + 30-Day Prediction")
                
                df_user_sorted = df_user.sort_values('ActivityDay')
                x_vals = np.arange(len(df_user_sorted))
                
                fig, ax = plt.subplots(figsize=(12, 6))
                
                # Historical data
                ax.plot(x_vals, df_user_sorted['StepTotal'].values, 'o-', label='Actual', alpha=0.6)
                
                # Trend line
                trend_line = trend_data['slope'] * x_vals + trend_data['intercept']
                ax.plot(x_vals, trend_line, 'r--', linewidth=2, label='Trend Line')
                
                # Prediction
                future_x = np.arange(len(df_user_sorted), len(df_user_sorted) + 30)
                ax.plot(future_x, trend_data['predictions'], 'g--', linewidth=2, label='30-Day Prediction')
                
                ax.set_xlabel('Days')
                ax.set_ylabel('Steps')
                ax.set_title('Historical Trend & Future Prediction')
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                
                # Prediction summary
                st.markdown("### 🔮 30-Day Forecast")
                pred_avg = np.mean(trend_data['predictions'])
                current_avg = metrics['avg_daily']
                change = pred_avg - current_avg
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Current Average", f"{current_avg:,.0f} steps")
                col2.metric("Predicted Average", f"{pred_avg:,.0f} steps")
                col3.metric("Expected Change", f"{change:+,.0f} steps")
        
        # ====================================================
        # VIEW 5: DAY OF WEEK PATTERNS
        # ====================================================
        elif main_option == "📈 Advanced Analytics" and sub_option == "🗓️ Day of Week Patterns":
            st.header("🗓️ Day of Week Activity Patterns")
            
            st.markdown("### 📊 Average Steps by Day")
            
            fig, axes = plt.subplots(2, 1, figsize=(12, 8))
            
            # Bar chart
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_analysis_ordered = day_analysis.set_index('DayOfWeek').reindex(day_order).reset_index()
            
            colors = ['#FF6B6B' if x < 10000 else '#4ECDC4' for x in day_analysis_ordered['mean']]
            axes[0].bar(day_analysis_ordered['DayOfWeek'], day_analysis_ordered['mean'], color=colors, edgecolor='black', alpha=0.7)
            axes[0].axhline(y=10000, color='red', linestyle='--', label='10k Goal')
            axes[0].set_ylabel('Average Steps')
            axes[0].set_title('Average Steps by Day of Week')
            axes[0].legend()
            axes[0].grid(True, alpha=0.3, axis='y')
            
            # Variability
            axes[1].bar(day_analysis_ordered['DayOfWeek'], day_analysis_ordered['std'], color='skyblue', edgecolor='black', alpha=0.7)
            axes[1].set_ylabel('Standard Deviation')
            axes[1].set_xlabel('Day of Week')
            axes[1].set_title('Activity Variability by Day')
            axes[1].grid(True, alpha=0.3, axis='y')
            
            st.pyplot(fig)
            
            # Detailed stats table
            st.markdown("### 📈 Detailed Statistics")
            detailed_stats = day_analysis_ordered[[
                'DayOfWeek', 'count', 'mean', 'median', 'std', 'min', 'max'
            ]].rename(columns={
                'DayOfWeek': 'Day',
                'count': 'Count',
                'mean': 'Average',
                'median': 'Median',
                'std': 'Std Dev',
                'min': 'Minimum',
                'max': 'Maximum'
            })
            
            for col in ['Average', 'Median', 'Std Dev', 'Minimum', 'Maximum']:
                detailed_stats[col] = detailed_stats[col].round(0).astype(int)
            
            st.dataframe(detailed_stats, use_container_width=True)
            
            # Insights
            st.markdown("### 💡 Insights")
            best_day = day_analysis_ordered.loc[day_analysis_ordered['mean'].idxmax(), 'DayOfWeek']
            worst_day = day_analysis_ordered.loc[day_analysis_ordered['mean'].idxmin(), 'DayOfWeek']
            best_avg = day_analysis_ordered['mean'].max()
            worst_avg = day_analysis_ordered['mean'].min()
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"🔥 **Best Day:** {best_day} ({best_avg:.0f} steps)")
            with col2:
                st.warning(f"📉 **Lowest Day:** {worst_day} ({worst_avg:.0f} steps)")
        
        # ====================================================
        # VIEW 6: PEAK HOURS
        # ====================================================
        elif main_option == "📈 Advanced Analytics" and sub_option == "⏰ Peak Hours":
            st.header("⏰ Peak Activity Hours Analysis")
            
            if df_hourly is not None and not df_hourly.empty:
                hourly_analysis = analyze_time_of_day(df_hourly)
                
                st.markdown("### 📊 Activity by Hour")
                
                fig, ax = plt.subplots(figsize=(14, 6))
                ax.bar(hourly_analysis['ActivityHour'], hourly_analysis['mean'], color='steelblue', edgecolor='black', alpha=0.7)
                ax.set_xlabel('Hour of Day')
                ax.set_ylabel('Average Steps')
                ax.set_title('Average Steps by Hour')
                ax.grid(True, alpha=0.3, axis='y')
                plt.xticks(rotation=45)
                st.pyplot(fig)
                
                # Top hours
                st.markdown("### 🔥 Peak Activity Hours")
                top_5 = hourly_analysis.nlargest(5, 'mean')
                
                for idx, row in top_5.iterrows():
                    st.success(f"⏰ {row['ActivityHour']}: {row['mean']:.0f} avg steps")
                
                # Hour-by-hour comparison
                st.markdown("### 📈 Detailed Hourly Breakdown")
                hourly_display = hourly_analysis.rename(columns={
                    'ActivityHour': 'Hour',
                    'count': 'Count',
                    'mean': 'Avg Steps',
                    'max': 'Peak',
                    'min': 'Low'
                })
                
                for col in ['Avg Steps', 'Peak', 'Low']:
                    hourly_display[col] = hourly_display[col].round(0).astype(int)
                
                st.dataframe(hourly_display, use_container_width=True)
        
        # ====================================================
        # VIEW 7: PREDICTIVE ANALYTICS
        # ====================================================
        elif main_option == "📈 Advanced Analytics" and sub_option == "📈 Predictive Analytics":
            st.header("🔮 Predictive Analytics & Forecasting")
            
            trend_data = predict_trend(df_user, days_ahead=60)
            
            if trend_data:
                st.markdown("### 📊 90-Day Forecast")
                
                # Extended forecast
                trend_60 = predict_trend(df_user, days_ahead=60)
                
                df_future = pd.DataFrame({
                    'Days Ahead': range(1, 61),
                    'Predicted Steps': trend_60['predictions']
                })
                
                fig, ax = plt.subplots(figsize=(12, 6))
                
                # Current trend
                df_recent = df_user.tail(30).copy()
                df_recent['ActivityDay'] = pd.to_datetime(df_recent['ActivityDay'])
                df_recent = df_recent.sort_values('ActivityDay')
                ax.plot(range(-30, 0), df_recent['StepTotal'].values, 'o-', label='Last 30 Days', linewidth=2)
                
                # Prediction
                ax.plot(range(1, 61), df_future['Predicted Steps'], 'g--', label='60-Day Forecast', linewidth=2)
                ax.axhline(y=goal, color='r', linestyle='--', label=f'Goal ({goal:,})', alpha=0.7)
                
                ax.set_xlabel('Days (0 = Today)')
                ax.set_ylabel('Steps')
                ax.set_title('60-Day Activity Forecast')
                ax.legend()
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                
                # Forecast metrics
                st.markdown("### 📊 Forecast Summary")
                col1, col2, col3, col4 = st.columns(4)
                
                col1.metric("Current Trend", trend_data['trend'])
                col2.metric("Avg (Next 30d)", f"{df_future.head(30)['Predicted Steps'].mean():.0f}")
                col3.metric("Avg (Days 31-60)", f"{df_future.tail(30)['Predicted Steps'].mean():.0f}")
                col4.metric("Trend Strength (R²)", f"{trend_data['r_squared']:.3f}")
                
                # Forecast interpretation
                st.markdown("### 💡 What This Means")
                
                if trend_data['slope'] > 0:
                    st.success(f"""
                    ✅ **You're improving!**
                    - Daily steps increasing by {trend_data['slope']:.1f} steps/day
                    - In 60 days, you could be at ~{(metrics['avg_daily'] + trend_data['slope']*60):,.0f} steps/day
                    - Continue this trend and you'll achieve your goals!
                    """)
                elif trend_data['slope'] < 0:
                    st.warning(f"""
                    ⚠️ **Activity is declining**
                    - Daily steps decreasing by {abs(trend_data['slope']):.1f} steps/day
                    - In 60 days, you could be at ~{max(0, metrics['avg_daily'] + trend_data['slope']*60):,.0f} steps/day
                    - Consider increasing activity to reverse trend
                    """)
                else:
                    st.info("""
                    📊 **Activity is stable**
                    - Your step count is consistent
                    - Maintain this level for health benefits
                    """)
        
        # ====================================================
        # VIEW 8: AI RECOMMENDATIONS
        # ====================================================
        elif main_option == "💡 AI Insights" and sub_option == "🧠 AI Recommendations":
            st.header("🧠 AI-Powered Personalized Recommendations")
            
            recommendations = generate_advanced_recommendations(metrics, goal_metrics, streaks, day_analysis)
            
            st.markdown("### 💡 Your Personalized Plan")
            for i, rec in enumerate(recommendations, 1):
                st.info(f"{i}. {rec}")
            
            # Personalized activity plan
            st.markdown("### 📅 Recommended Weekly Plan")
            plan = get_personalized_plan(metrics, goal)
            
            st.subheader(f"Level: {plan['level']} | Weekly Target: {plan['weekly_total']:,} steps")
            
            plan_df = pd.DataFrame([
                {'Day': day, 'Activity': activity}
                for day, activity in plan['plan'].items()
            ])
            
            st.dataframe(plan_df, use_container_width=True)
            
            # Implementation tips
            st.markdown("### 🚀 How to Implement")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Week 1-2: Establish Routine**
                - Pick specific times for walks
                - Set phone reminders
                - Track first week carefully
                """)
            with col2:
                st.markdown("""
                **Week 3-4: Build Momentum**
                - Gradually increase intensity
                - Add variety (different routes)
                - Invite friends/family
                """)
        
        # ====================================================
        # VIEW 9: ACHIEVEMENTS
        # ====================================================
        elif main_option == "💡 AI Insights" and sub_option == "🎖️ Achievements":
            st.header("🎖️ Achievement Badges & Milestones")
            
            # Define achievements
            achievements = [
                ("🥉 Bronze Milestone", 5000, metrics['max'] >= 5000, "Single day with 5k+ steps"),
                ("🥈 Silver Milestone", 10000, metrics['max'] >= 10000, "Single day with 10k+ steps"),
                ("🥇 Gold Milestone", 15000, metrics['max'] >= 15000, "Single day with 15k+ steps"),
                ("💎 Platinum Milestone", 20000, metrics['max'] >= 20000, "Single day with 20k+ steps"),
                ("⭐ Weekly Warrior", 50000, metrics['total_steps'] >= 50000, "50k steps total"),
                ("🔥 Consistency Champion", 100, metrics['days_tracked'] >= 100, "100+ consecutive days tracked"),
                ("🎯 Goal Master", 10000, metrics['avg_daily'] >= 10000, "Averaging 10k+ steps daily"),
                ("📈 Progress Maker", 30, (metrics['max'] - metrics['min']) > 10000, "Improved performance by 10k+ steps"),
                ("🌟 Super Achiever", 60, metrics['days_tracked'] >= 60, "60+ days of activity"),
                ("💪 Fitness Expert", 12500, metrics['avg_daily'] >= 12500, "Averaging 12.5k+ steps daily"),
            ]
            
            earned = []
            locked = []
            
            for badge, requirement, condition, desc in achievements:
                if condition:
                    earned.append((badge, desc))
                else:
                    locked.append((badge, desc, requirement))
            
            # Display earned
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ✅ Earned Badges")
                if earned:
                    for badge, desc in earned:
                        st.success(f"{badge}\n*{desc}*")
                else:
                    st.info("Keep working to earn badges!")
            
            with col2:
                st.markdown("### 🔓 Locked Badges")
                if locked:
                    for badge, desc, req in locked:
                        st.warning(f"{badge}\n*{desc}*")
            
            # Progress to next badges
            st.markdown("### 🚀 Progress to Next Badges")
            
            if metrics['max'] < 20000:
                target = 20000
                progress = (metrics['max'] / target) * 100
                st.progress(min(progress / 100, 1.0))
                st.write(f"💎 Platinum: {metrics['max']}/{target} steps ({progress:.1f}%)")
            
            if metrics['avg_daily'] < 12500:
                target = 12500
                progress = (metrics['avg_daily'] / target) * 100
                st.progress(min(progress / 100, 1.0))
                st.write(f"💪 Fitness Expert: {metrics['avg_daily']:.0f}/{target} steps ({progress:.1f}%)")
        
        # ====================================================
        # VIEW 10: GOAL STRATEGY
        # ====================================================
        elif main_option == "💡 AI Insights" and sub_option == "🎯 Goal Strategy":
            st.header("🎯 Intelligent Goal Strategy")
            
            st.markdown("### 📊 Current Performance Analysis")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Average", f"{metrics['avg_daily']:.0f} steps")
            col2.metric("Personal Best", f"{metrics['max']:,} steps")
            col3.metric("Realistic Range", f"{metrics['q1']:.0f} - {metrics['q3']:.0f}")
            
            # SMART goal recommendation
            st.markdown("### 🎯 SMART Goal Framework")
            
            conservative_goal = int(metrics['avg_daily'] * 1.10)  # 10% increase
            moderate_goal = int(metrics['avg_daily'] * 1.20)      # 20% increase
            aggressive_goal = int(metrics['avg_daily'] * 1.35)    # 35% increase
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.success(f"""
                **🎯 Conservative**
                Goal: {conservative_goal:,} steps
                
                - 10% above average
                - Very achievable
                - Build momentum
                """)
            
            with col2:
                st.info(f"""
                **📈 Moderate**
                Goal: {moderate_goal:,} steps
                
                - 20% above average
                - Challenging but doable
                - Recommended
                """)
            
            with col3:
                st.warning(f"""
                **💪 Aggressive**
                Goal: {aggressive_goal:,} steps
                
                - 35% above average
                - Very challenging
                - 3-month+ timeline
                """)
            
            # Historical goal achievement
            st.markdown("### 📈 Historical Goal Achievement")
            
            goal_history = []
            for test_goal in [5000, 7500, 10000, 12500, 15000]:
                achievement = calculate_goal_achievement(df_user, test_goal)
                goal_history.append({
                    'Goal': f"{test_goal:,}",
                    'Days Met': achievement['days_met'],
                    'Percentage': f"{achievement['percentage']:.1f}%"
                })
            
            goal_hist_df = pd.DataFrame(goal_history)
            st.dataframe(goal_hist_df, use_container_width=True)
            
            # Visualization
            st.markdown("### 📊 Goal Achievement Visualization")
            
            goals = [5000, 7500, 10000, 12500, 15000, conservative_goal, moderate_goal, aggressive_goal]
            achievements = [calculate_goal_achievement(df_user, g)['percentage'] for g in goals]
            
            fig, ax = plt.subplots(figsize=(12, 5))
            colors = ['#4ECDC4' if g <= moderate_goal else '#FFA07A' for g in goals]
            ax.bar([str(g) for g in goals], achievements, color=colors, edgecolor='black', alpha=0.7)
            ax.axhline(y=80, color='green', linestyle='--', label='80% Achievement Target', alpha=0.7)
            ax.set_ylabel('Achievement %')
            ax.set_title('Goal Achievement Rates')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            st.pyplot(fig)
        
        # ====================================================
        # VIEW 11: PERFORMANCE TIPS
        # ====================================================
        elif main_option == "💡 AI Insights" and sub_option == "💪 Performance Tips":
            st.header("💪 Evidence-Based Performance Tips")
            
            st.markdown("### 🏃 Training Principles")
            
            st.markdown("""
            #### 1. **Progressive Overload**
            Gradually increase your daily steps by 5-10% every 2 weeks.
            - Week 1-2: Current average
            - Week 3-4: +5%
            - Week 5-6: +10%
            
            #### 2. **Consistency Over Intensity**
            Research shows consistency is more important than occasional high-intensity days.
            - 30-min daily walk > 3-hour weekend hike
            - Current consistency score: {:.0f}%
            
            #### 3. **Periodization**
            Structure your week with varying intensity:
            - **Hard Days** (Mon, Wed, Fri): High-intensity activities
            - **Moderate Days** (Tue, Thu): Moderate walks
            - **Easy Days** (Sat, Sun): Leisurely walks
            
            #### 4. **Recovery Days**
            Include 1-2 low-activity days per week to prevent burnout.
            """.format(100 - metrics['cv']))
            
            st.markdown("### 🎯 Quick Wins (Implement Today)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **Morning Routine (+1,500 steps)**
                - Walk while breakfast brews (5 min)
                - Walk to bathroom (round trip)
                - Walk while on phone calls
                """)
            
            with col2:
                st.markdown("""
                **Throughout Day (+2,000 steps)**
                - Walk to co-worker's desk instead of email
                - Lunch walk (15 min)
                - Take stairs instead of elevator
                """)
            
            st.markdown("""
            ### 📊 Advanced Strategies
            
            #### Strategy 1: The "Movement Snacking" Technique
            Instead of one 30-minute walk, do 6x 5-minute walks throughout the day.
            - More feasible with busy schedules
            - Improves metabolism
            - Reduces sedentary time
            
            #### Strategy 2: The "Stacking" Method
            Stack walking with existing activities:
            - Walk while on calls
            - Walk while listening to podcasts
            - Walk while thinking through problems
            
            #### Strategy 3: The "Social Accountability" System
            - Join a walking group
            - Share daily step targets with friends
            - Create friendly competitions
            - Public commitment increases adherence by 65%
            """)
            
            st.markdown("### ⚕️ Health Benefits (Science-Based)")
            
            benefits_data = {
                'Steps/Day': ['<5,000', '5,000-7,500', '7,500-10,000', '10,000-12,500', '12,500+'],
                'Cardiovascular': ['⚠️ High Risk', '⚠️ Moderate Risk', '✅ Lower Risk', '✅ Good', '✅✅ Excellent'],
                'Mental Health': ['⚠️ Low Mood', '📊 Improving', '✅ Better', '✅ Good', '✅✅ Excellent'],
                'Lifespan': ['😟 Shorter', '📊 Longer', '✅ Good', '✅ Better', '✅✅ Best']
            }
            
            benefits_df = pd.DataFrame(benefits_data)
            st.dataframe(benefits_df, use_container_width=True)
        
        # ====================================================
        # VIEW 12: WEEKLY REPORT
        # ====================================================
        elif main_option == "📊 Detailed Reports" and sub_option == "📋 Weekly Report":
            st.header("📋 Weekly Performance Report")
            
            # Get last 7 days
            df_weekly = df_user.tail(7).copy()
            df_weekly['ActivityDay'] = pd.to_datetime(df_weekly['ActivityDay'])
            
            st.markdown("### 📊 Last 7 Days Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Steps", f"{df_weekly['StepTotal'].sum():,}")
            col2.metric("Daily Average", f"{df_weekly['StepTotal'].mean():.0f}")
            col3.metric("Best Day", f"{df_weekly['StepTotal'].max():,}")
            col4.metric("Days Over Goal", len(df_weekly[df_weekly['StepTotal'] >= goal]))
            
            # Daily breakdown
            st.markdown("### 📈 Daily Breakdown")
            
            weekly_display = df_weekly.copy()
            weekly_display['ActivityDay'] = weekly_display['ActivityDay'].dt.strftime('%A, %m/%d')
            weekly_display = weekly_display.rename(columns={'ActivityDay': 'Date', 'StepTotal': 'Steps'})
            weekly_display['Goal Status'] = weekly_display['Steps'].apply(lambda x: '✅ Met' if x >= goal else '❌ Missed')
            
            st.dataframe(weekly_display[['Date', 'Steps', 'Goal Status']], use_container_width=True)
            
            # Weekly visualization
            st.markdown("### 📊 Visual Summary")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            colors = ['#4ECDC4' if x >= goal else '#FF6B6B' for x in df_weekly['StepTotal']]
            ax.bar(df_weekly['ActivityDay'].dt.day_name(), df_weekly['StepTotal'], color=colors, edgecolor='black', alpha=0.7)
            ax.axhline(y=goal, color='green', linestyle='--', label=f'Goal: {goal:,}', linewidth=2)
            ax.set_ylabel('Steps')
            ax.set_title('Weekly Step Count')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        # ====================================================
        # VIEW 13: MONTHLY REPORT
        # ====================================================
        elif main_option == "📊 Detailed Reports" and sub_option == "📅 Monthly Report":
            st.header("📅 Monthly Performance Report")
            
            st.markdown("### 📊 Month Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Steps", f"{metrics['total_steps']:,}")
            col2.metric("Daily Average", f"{metrics['avg_daily']:.0f}")
            col3.metric("Best Day", f"{metrics['max']:,}")
            col4.metric("Days Tracked", metrics['days_tracked'])
            
            st.markdown("### 📈 Weekly Breakdown")
            
            df_user_copy = df_user.copy()
            df_user_copy['ActivityDay'] = pd.to_datetime(df_user_copy['ActivityDay'])
            df_user_copy['Week'] = df_user_copy['ActivityDay'].dt.isocalendar().week
            
            weekly_summary = df_user_copy.groupby('Week').agg({
                'StepTotal': ['sum', 'mean', 'max', 'min', 'count']
            }).round(0).astype(int)
            
            weekly_summary.columns = ['Total', 'Avg Daily', 'Best Day', 'Worst Day', 'Days']
            
            st.dataframe(weekly_summary.reset_index(), use_container_width=True)
            
            st.markdown("### 🎖️ Monthly Milestones")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                days_over_goal = goal_metrics['days_met']
                st.success(f"🎯 **{days_over_goal}** days reached {goal:,} step goal")
            
            with col2:
                best_week = weekly_summary['Total'].max()
                st.info(f"🔥 **Best week:** {best_week:,} steps")
            
            with col3:
                improvement = ((metrics['max'] - metrics['min']) / metrics['min'] * 100) if metrics['min'] > 0 else 0
                st.warning(f"📈 **{improvement:.0f}%** variation (best vs worst)")
        
        # ====================================================
        # VIEW 14: SQL EXPLORER
        # ====================================================
        elif main_option == "📊 Detailed Reports" and sub_option == "🔧 SQL Explorer":
            st.header("🔧 Advanced SQL Explorer")
            
            st.markdown("""
            Write custom SQL queries to explore your data. Available tables:
            - `daily_steps`: Id, ActivityDay, StepTotal
            - `hourly_steps`: Id, ActivityHour, StepTotal
            - `heart_rate`: Id, Time, Value
            """)
            
            # Preset queries
            preset = st.selectbox(
                "📋 Quick Templates:",
                [
                    "Custom Query",
                    "All Users Comparison",
                    "Top 10 Best Days",
                    "Weekly Totals",
                    "Days Under Goal",
                    "Hour Analysis",
                    "Heart Rate Zones",
                    "Consistency Score",
                ]
            )
            
            queries = {
                "Custom Query": "SELECT * FROM daily_steps LIMIT 10;",
                "All Users Comparison": """
                    SELECT Id, COUNT(*) AS Days, SUM(StepTotal) AS Total, 
                    ROUND(AVG(StepTotal), 0) AS Daily_Avg, MAX(StepTotal) AS Best
                    FROM daily_steps GROUP BY Id ORDER BY Daily_Avg DESC;
                """,
                "Top 10 Best Days": """
                    SELECT ActivityDay, StepTotal, Id FROM daily_steps 
                    ORDER BY StepTotal DESC LIMIT 10;
                """,
                "Weekly Totals": """
                    SELECT Id, strftime('%Y-W%W', ActivityDay) AS Week,
                    SUM(StepTotal) AS Total FROM daily_steps 
                    GROUP BY Id, Week ORDER BY Week DESC, Total DESC;
                """,
                "Days Under Goal": """
                    SELECT ActivityDay, StepTotal FROM daily_steps 
                    WHERE StepTotal < 5000 ORDER BY StepTotal;
                """,
                "Hour Analysis": """
                    SELECT ActivityHour, ROUND(AVG(StepTotal), 1) AS Avg_Steps,
                    MAX(StepTotal) AS Peak, COUNT(*) AS Times
                    FROM hourly_steps GROUP BY ActivityHour 
                    ORDER BY Avg_Steps DESC;
                """,
                "Heart Rate Zones": """
                    SELECT 
                    CASE WHEN Value < 60 THEN 'Resting'
                         WHEN Value < 100 THEN 'Normal'
                         WHEN Value < 130 THEN 'Elevated'
                         ELSE 'Max Zone' END AS Zone,
                    COUNT(*) AS Count, ROUND(AVG(Value), 1) AS Avg_BPM
                    FROM heart_rate GROUP BY Zone;
                """,
                "Consistency Score": """
                    SELECT Id, 
                    ROUND(AVG(StepTotal), 0) AS Avg,
                    ROUND(STDEV(StepTotal), 0) AS Std_Dev,
                    ROUND(STDEV(StepTotal) * 100.0 / AVG(StepTotal), 1) AS CV_Percent
                    FROM daily_steps GROUP BY Id ORDER BY CV_Percent;
                """
            }
            
            default_query = queries.get(preset, queries["Custom Query"])
            
            user_query = st.text_area("SQL Query:", default_query, height=150)
            
            if st.button("🚀 Execute"):
                result = run_query(user_query)
                if result is not None:
                    st.success(f"✅ {len(result)} rows returned")
                    st.dataframe(result, use_container_width=True)
                    
                    csv = result.to_csv(index=False)
                    st.download_button("📥 Download CSV", csv, "query_results.csv", "text/csv")
        
        # ====================================================
        # VIEW 15: DATA EXPORT
        # ====================================================
        elif main_option == "📊 Detailed Reports" and sub_option == "📥 Data Export":
            st.header("📥 Export Your Data")
            
            st.markdown("Download your fitness data in various formats for external analysis.")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("📊 Daily Steps")
                daily = run_query("SELECT * FROM daily_steps ORDER BY Id, ActivityDay;")
                if daily is not None:
                    csv = daily.to_csv(index=False)
                    st.download_button("📥 CSV", csv, "daily_steps.csv", "text/csv", key="daily_csv")
            
            with col2:
                st.subheader("⏰ Hourly Steps")
                hourly = run_query("SELECT * FROM hourly_steps ORDER BY Id, ActivityHour;")
                if hourly is not None:
                    csv = hourly.to_csv(index=False)
                    st.download_button("📥 CSV", csv, "hourly_steps.csv", "text/csv", key="hourly_csv")
            
            with col3:
                st.subheader("❤️ Heart Rate")
                hr = run_query("SELECT * FROM heart_rate ORDER BY Id, Time;")
                if hr is not None:
                    csv = hr.to_csv(index=False)
                    st.download_button("📥 CSV", csv, "heart_rate.csv", "text/csv", key="hr_csv")
            
            # Summary report
            st.markdown("### 📋 Generate Comprehensive Report")
            
            if st.button("📊 Create Report"):
                report = f"""
FITBIT DATA COMPREHENSIVE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 
USER ID: {selected_user}
FITNESS LEVEL: {fitness_level}
HEALTH SCORE: {health_score:.1f}/100
 
ACTIVITY SUMMARY:
- Total Steps: {metrics['total_steps']:,}
- Daily Average: {metrics['avg_daily']:.0f}
- Median: {metrics['median']:.0f}
- Best Day: {metrics['max']:,}
- Worst Day: {metrics['min']:,}
- Days Tracked: {metrics['days_tracked']}
 
STATISTICS:
- Standard Deviation: {metrics['std_dev']:.0f}
- Coefficient of Variation: {metrics['cv']:.1f}%
- Skewness: {metrics['skewness']:.2f}
- Kurtosis: {metrics['kurtosis']:.2f}
 
GOAL METRICS ({goal:,} steps/day):
- Days Met: {goal_metrics['days_met']}/{goal_metrics['total_days']}
- Achievement Rate: {goal_metrics['percentage']:.1f}%
 
STREAKS:
- Current Streak: {streaks['current']} days
- Best Streak: {streaks['best']} days
- Average Streak: {streaks['average']:.1f} days
 
TREND:
- Direction: {trend_data['trend'] if trend_data else 'N/A'}
"""
                
                st.text(report)
                st.download_button("📥 Download Report", report, "fitbit_report.txt", "text/plain")
 
st.sidebar.markdown("---")
st.sidebar.markdown("""
🔥 **Advanced Fitbit Analytics Pro v3.0**
 
*Enterprise-grade fitness intelligence powered by AI and machine learning.*
""")
 
