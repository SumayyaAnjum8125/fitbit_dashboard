# 🏃 Fitbit Health & Fitness Analytics Dashboard

A beginner-friendly Streamlit application that analyzes Fitbit activity data using SQLite and SQL queries. This project demonstrates data loading, database management, and interactive web app development.

---

## 📋 Project Structure

```
fitbit_dashboard/
├── app.py                      # Main Streamlit application
├── setup_db.py                 # Database initialization script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── fitbit.db                   # SQLite database (auto-generated)
└── data/                       # Folder for CSV files
    ├── dailySteps_merged.csv
    ├── hourlySteps_merged.csv
    └── heartrate_seconds_merged.csv
```

---

## 🚀 Quick Start Guide

### Step 1: Set Up Your Environment

1. **Create a project folder** on your computer:
   ```bash
   mkdir fitbit_dashboard
   cd fitbit_dashboard
   ```

2. **Create a `data/` subfolder** and add your Fitbit CSV files:
   ```bash
   mkdir data
   # Place your CSV files in this data/ folder
   ```

3. **Install Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Initialize the Database

Run the setup script to load your CSV data into SQLite:

```bash
python setup_db.py
```

**Expected Output:**
```
✅ Loaded 'daily_steps' successfully into database.
✅ Loaded 'hourly_steps' successfully into database.
✅ Loaded 'heart_rate' successfully into database.
✅ Database setup complete! Your fitbit.db file is ready.
```

💡 **What's happening?** This creates a `fitbit.db` file that contains your data organized into 3 tables.

### Step 3: Launch the Streamlit App

```bash
streamlit run app.py
```

Your dashboard will open automatically in your browser at `http://localhost:8501`

---

## 📊 Dashboard Features

### 1. **Overview Metrics**
   - Total tracked users
   - Highest average daily steps
   - Overall average daily steps
   - User performance table

### 2. **Step Goal Performance Filter**
   - 🎯 Interactive slider to set custom daily step goals (1,000 - 20,000 steps)
   - Goal achievement rate percentage
   - Filter results by "Goal Met" or "Goal Missed"
   - Track performance trends

### 3. **Heart Rate Analytics**
   - Min, average, and max heart rate statistics
   - Heart rate visualization over time
   - Heart rate zones breakdown:
     - 🟢 Resting: <60 BPM
     - 🟡 Normal: 60-100 BPM
     - 🔴 Elevated: >100 BPM

### 4. **Hourly Step Trends**
   - Peak activity hours across all users
   - Average steps by hour of day
   - Identify when users are most active

### 5. **Custom SQL Runner**
   - Run your own SQL queries directly
   - Explore the database freely
   - Test SQL commands before using them

---

## 🗄️ Database Schema

Your SQLite database contains 3 main tables:

### `daily_steps` Table
| Column | Type | Description |
|--------|------|-------------|
| Id | INTEGER | User ID |
| ActivityDay | TEXT | Date of activity |
| StepTotal | INTEGER | Total steps for the day |

### `hourly_steps` Table
| Column | Type | Description |
|--------|------|-------------|
| Id | INTEGER | User ID |
| ActivityHour | TEXT | Hour timestamp |
| StepTotal | INTEGER | Steps during that hour |

### `heart_rate` Table
| Column | Type | Description |
|--------|------|-------------|
| Id | INTEGER | User ID |
| Time | TEXT | Timestamp |
| Value | INTEGER | Heart rate in BPM |

---

## 📝 Example SQL Queries

### Find total steps per user:
```sql
SELECT Id, SUM(StepTotal) AS Total_Steps
FROM daily_steps
GROUP BY Id
ORDER BY Total_Steps DESC;
```

### Days exceeding 10,000 steps:
```sql
SELECT ActivityDay, StepTotal
FROM daily_steps
WHERE StepTotal >= 10000
ORDER BY StepTotal DESC;
```

### Peak activity hours:
```sql
SELECT ActivityHour, AVG(StepTotal) AS Avg_Steps
FROM hourly_steps
GROUP BY ActivityHour
ORDER BY Avg_Steps DESC;
```

### Average heart rate per user:
```sql
SELECT Id, ROUND(AVG(Value), 1) AS Avg_Heart_Rate
FROM heart_rate
GROUP BY Id;
```

---

## 🔧 Troubleshooting

### ❌ "No such table" error
**Solution:** Make sure you've run `python setup_db.py` first to create the database.

### ❌ "File not found" warning
**Solution:** Check that your CSV files are in the `data/` folder with the correct names:
- `dailySteps_merged.csv`
- `hourlySteps_merged.csv`
- `heartrate_seconds_merged.csv`

### ❌ Port already in use (error on `streamlit run`)
**Solution:** Run on a different port:
```bash
streamlit run app.py --server.port 8502
```

### ❌ ModuleNotFoundError
**Solution:** Reinstall packages:
```bash
pip install --upgrade -r requirements.txt
```

---

## 🌐 Deploy to Streamlit Community Cloud (Free)

### Option 1: Quick Deploy
1. Push this project to GitHub as a public repository
2. Go to [Streamlit Community Cloud](https://share.streamlit.io)
3. Click "New app" → Select your GitHub repo → Deploy
4. Make sure `fitbit.db` is uploaded to your repository

### Option 2: Manual Deployment Steps
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions

---

## 💡 Learning Tips for Beginners

1. **Start small:** Modify one SQL query at a time
2. **Use Custom SQL Runner:** Test new queries here before adding them to the main app
3. **Explore data:** Use `SELECT * FROM table_name LIMIT 10;` to see table structure
4. **Ask questions:** Every SQL operation is explained in the code comments

---

## 📚 Next Steps to Enhance Your Dashboard

- **Add Date Filters:** Filter data by date range
- **Calculate Calories:** Add calorie burn estimates
- **Weekly Summaries:** Group metrics by week
- **Export Data:** Add CSV export functionality
- **Alerts:** Notify when heart rate exceeds thresholds

---

## 📞 Getting Help

- **Streamlit Docs:** https://docs.streamlit.io
- **SQLite Tutorial:** https://www.w3schools.com/sql/
- **Pandas Reference:** https://pandas.pydata.org/docs/

---

## 📄 License

This project is open source and available for personal and educational use.

**Happy analyzing! 🎉**
