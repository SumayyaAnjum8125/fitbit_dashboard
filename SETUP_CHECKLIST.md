# ✅ Fitbit Dashboard Setup Checklist

Use this checklist to ensure everything is set up correctly before running your app!

---

## 📁 File Structure Check

Make sure your project folder looks like this:

```
fitbit_dashboard/
├── ✅ app.py
├── ✅ setup_db.py
├── ✅ requirements.txt
├── ✅ README.md
├── ✅ DEPLOYMENT.md
├── ✅ SETUP_CHECKLIST.md
├── ✅ data/
│   ├── dailySteps_merged.csv
│   ├── hourlySteps_merged.csv
│   └── heartrate_seconds_merged.csv
└── ✅ fitbit.db (created after running setup_db.py)
```

---

## 🔧 Installation Checklist

### Before You Start
- [ ] Python 3.8+ installed on your computer
  ```bash
  python --version
  ```
  
- [ ] pip (Python package manager) available
  ```bash
  pip --version
  ```

### Installation Steps
- [ ] Navigate to your project folder
  ```bash
  cd fitbit_dashboard
  ```

- [ ] Create virtual environment (optional but recommended)
  ```bash
  python -m venv venv
  # Windows:
  venv\Scripts\activate
  # Mac/Linux:
  source venv/bin/activate
  ```

- [ ] Install required packages
  ```bash
  pip install -r requirements.txt
  ```
  
  **Expected output:**
  ```
  Successfully installed streamlit-1.31.1 pandas-2.1.3
  ```

---

## 📊 Data Preparation Checklist

### CSV Files
- [ ] `dailySteps_merged.csv` is in the `data/` folder
- [ ] `hourlySteps_merged.csv` is in the `data/` folder
- [ ] `heartrate_seconds_merged.csv` is in the `data/` folder

### Check CSV Format (Optional)
Open each CSV file and verify:
- [ ] First row contains column headers
- [ ] Data looks reasonable (dates, step counts, etc.)
- [ ] No obvious corrupted entries

---

## 🗄️ Database Setup Checklist

- [ ] Run the setup script:
  ```bash
  python setup_db.py
  ```

- [ ] Check for success messages:
  - [ ] ✅ "Loaded 'daily_steps' successfully"
  - [ ] ✅ "Loaded 'hourly_steps' successfully"
  - [ ] ✅ "Loaded 'heart_rate' successfully"
  - [ ] ✅ "Database setup complete!"

- [ ] Verify `fitbit.db` file was created
  - [ ] File exists in your project folder
  - [ ] File size > 0 KB (not empty)

- [ ] (Optional) Verify database contents:
  ```bash
  sqlite3 fitbit.db "SELECT COUNT(*) FROM daily_steps;"
  ```
  Should return a number > 0

---

## 🚀 Launch Checklist

### Before Running the App
- [ ] All installation steps complete
- [ ] Database setup successful
- [ ] All CSV files in `data/` folder
- [ ] `fitbit.db` file exists

### Launch the App
- [ ] Run Streamlit:
  ```bash
  streamlit run app.py
  ```

- [ ] Check console output:
  - [ ] "You can now view your Streamlit app in your browser"
  - [ ] URL appears (usually `http://localhost:8501`)

### Test the App
- [ ] Browser opens automatically
- [ ] Dashboard loads without errors
- [ ] Can see "Overview Metrics" view
- [ ] Can select different navigation options
- [ ] Can interact with sliders and filters

---

## 🐛 Troubleshooting Checklist

### App Won't Start
- [ ] Check Python version: `python --version`
- [ ] Reinstall packages: `pip install -r requirements.txt --upgrade`
- [ ] Check if port 8501 is available

### No Data Showing
- [ ] Run `python setup_db.py` again
- [ ] Check CSV files are in `data/` folder
- [ ] Verify CSV file names match exactly:
  - `dailySteps_merged.csv`
  - `hourlySteps_merged.csv`
  - `heartrate_seconds_merged.csv`

### "ModuleNotFoundError"
- [ ] Ensure virtual environment is activated
- [ ] Run: `pip install -r requirements.txt`

### Database Errors
- [ ] Delete `fitbit.db` if corrupted
- [ ] Run `python setup_db.py` to rebuild

---

## 📋 Feature Testing Checklist

Test each dashboard section:

### Overview Metrics
- [ ] Shows "Total Tracked Users" metric
- [ ] Shows "Highest Daily Avg" metric
- [ ] Shows "Overall Avg Daily Steps" metric
- [ ] User table displays correctly

### Step Goal Performance
- [ ] Slider allows setting step goals (1000-20000)
- [ ] Metrics update when slider changes
- [ ] Can filter by "Goal Met" / "Goal Missed"
- [ ] Shows achievement percentage

### Heart Rate Analytics
- [ ] Can select different user IDs
- [ ] Shows min/avg/max heart rate stats
- [ ] Line chart displays heart rate over time
- [ ] Heart rate zones bar chart shows

### Hourly Step Trends
- [ ] Bar chart shows activity by hour
- [ ] Hours are in chronological order

### Custom SQL Runner
- [ ] Can type SQL queries
- [ ] Execute button works
- [ ] Results display in table format

---

## 🌐 Pre-Deployment Checklist (GitHub)

- [ ] GitHub account created
- [ ] Project folder initialized with git: `git init`
- [ ] All files added to git: `git add .`
- [ ] Initial commit made: `git commit -m "Initial commit"`
- [ ] Remote repository created on GitHub
- [ ] Files pushed to GitHub: `git push origin main`
- [ ] Repository is set to **Public**

---

## 🚀 Deployment Checklist (Streamlit Cloud)

- [ ] Streamlit Community Cloud account created
- [ ] GitHub connection authorized
- [ ] Deployed at share.streamlit.io
- [ ] Selected correct repository
- [ ] Set main file path to `app.py`
- [ ] App is building/deployed (green status)
- [ ] Can access public URL
- [ ] All features work on deployed version

---

## ✨ Completion!

If all checkboxes are complete, congratulations! Your Fitbit Dashboard is ready to use! 🎉

**What's next?**
- [ ] Share your app URL with friends
- [ ] Try adding new SQL queries to the Custom SQL Runner
- [ ] Experiment with the interactive features
- [ ] Consider adding more features (date filters, export, etc.)

---

**Need help?** Check README.md for common issues and solutions!
