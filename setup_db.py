import sqlite3
import pandas as pd

# Connect to (or create) the SQLite database
conn = sqlite3.connect("fitbit.db")

# Load CSV files into SQLite tables
datasets = {
    "daily_steps": "data/dailySteps_merged.csv",
    "hourly_steps": "data/hourlySteps_merged.csv",
    "heart_rate": "data/heartrate_seconds_merged.csv",
}

for table_name, csv_path in datasets.items():
    try:
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"✅ Loaded '{table_name}' successfully into database.")
    except FileNotFoundError:
        print(f"⚠️  Warning: {csv_path} not found. Skipping...")
    except Exception as e:
        print(f"❌ Error loading {csv_path}: {e}")

conn.close()
print("\n✅ Database setup complete! Your fitbit.db file is ready.")
