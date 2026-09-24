# 🚀 Deployment Guide: Streamlit Community Cloud

Deploy your Fitbit Dashboard online for free in minutes!

---

## Prerequisites

- GitHub account (free at [github.com](https://github.com))
- Streamlit Community Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- Your project files ready

---

## Step 1: Create a GitHub Repository

### Option A: Using GitHub Web Interface (Easiest)

1. **Go to [GitHub](https://github.com)** and log in
2. **Click the `+` icon** in the top-right corner → "New repository"
3. **Fill in the details:**
   - Repository name: `fitbit-dashboard`
   - Description: "Fitbit Activity Analytics Dashboard with Streamlit & SQL"
   - Set to **Public** (required for Streamlit Cloud)
   - ✅ Check "Add a README file"
4. **Click "Create repository"**

### Option B: Using Git Command Line

```bash
# Initialize git in your project folder
git init

# Configure git
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add files
git add .

# Commit
git commit -m "Initial commit: Fitbit Dashboard"

# Add remote and push
git remote add origin https://github.com/your-username/fitbit-dashboard.git
git branch -M main
git push -u origin main
```

---

## Step 2: Upload Your Project Files to GitHub

### Via Web Interface:
1. **Go to your repository page** on GitHub
2. **Click "Add file" → "Upload files"**
3. **Drag and drop or select these files:**
   - ✅ `app.py`
   - ✅ `setup_db.py`
   - ✅ `requirements.txt`
   - ✅ `README.md`
   - ✅ `fitbit.db` (your SQLite database with data)

4. **Add a commit message:** "Add Streamlit dashboard files"
5. **Click "Commit changes"**

### Via Command Line:
```bash
# From your project folder
git add .
git commit -m "Add Streamlit dashboard files"
git push origin main
```

---

## Step 3: Deploy on Streamlit Community Cloud

1. **Go to [Streamlit Community Cloud](https://share.streamlit.io)**
2. **Click "Sign in with GitHub"** (or create account)
3. **Authorize Streamlit** to access your GitHub repositories
4. **Click "New app"** button
5. **Fill in the deployment form:**
   - **Repository:** `your-username/fitbit-dashboard`
   - **Branch:** `main` (or `master`)
   - **Main file path:** `app.py`
6. **Click "Deploy!"**

---

## Step 4: Wait for Deployment

Streamlit will:
1. ✅ Clone your GitHub repository
2. ✅ Install packages from `requirements.txt`
3. ✅ Run your `app.py`
4. ✅ Create a public URL

**Status indicators:**
- 🔵 Blue: Building
- 🟢 Green: Running (Success!)
- 🔴 Red: Error

---

## Step 5: Share Your App!

Once deployed (green status), you'll get a public URL like:
```
https://fitbit-dashboard.streamlit.app
```

**Share it with friends and colleagues!**

---

## 🔄 Updating Your App

After deployment, any changes you push to GitHub automatically redeploy:

```bash
# Make changes to your files
nano app.py  # Edit as needed

# Push to GitHub
git add .
git commit -m "Update dashboard features"
git push origin main
```

Streamlit will automatically rebuild your app! ✨

---

## ⚠️ Common Deployment Issues

### Issue 1: "Module not found" Error
**Solution:** Ensure all packages are in `requirements.txt`
```bash
pip freeze > requirements.txt
```

### Issue 2: "No such table" Error
**Solution:** Upload `fitbit.db` to your GitHub repository
```bash
git add fitbit.db
git commit -m "Add database"
git push origin main
```

### Issue 3: CSV Files Not Found
**Solution:** Either:
- Upload the `data/` folder with CSV files to GitHub, OR
- Include a note in the app to run `setup_db.py` locally first

### Issue 4: App takes too long to load
**Solution:** Optimize your queries or add caching:
```python
@st.cache_data
def run_query(query):
    conn = sqlite3.connect("fitbit.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
```

---

## 📊 Access Your Deployed App

1. **View your app** at the Streamlit Cloud URL
2. **Share the link** with anyone (no login required!)
3. **Monitor usage** in your Streamlit Cloud dashboard
4. **Check logs** if there are errors

---

## 🔒 Important Notes

### Private Data
- Your app is **public by default**
- Don't commit sensitive data to GitHub
- If you have private data, use Streamlit Secrets instead:

```python
# Add to secrets in Streamlit Cloud dashboard
import streamlit as st
password = st.secrets["app_password"]
```

### Database Updates
- If you update your CSV files, re-run `setup_db.py` locally
- Commit the updated `fitbit.db` to GitHub
- Push to GitHub → Streamlit automatically redeploys

---

## 💡 Pro Tips

✅ **Add app description:** Click "Settings" → Add a description for your app  
✅ **Custom domain:** Upgrade to Streamlit Team for custom domains  
✅ **Email notifications:** Get alerts if your app crashes  
✅ **Monitor resources:** Check RAM/CPU usage in Cloud dashboard  

---

## 🎉 Success!

Your Fitbit Dashboard is now live and shareable! 

**Next steps:**
- Share the link on social media
- Add more features to your dashboard
- Experiment with new visualizations
- Learn more about Streamlit at [docs.streamlit.io](https://docs.streamlit.io)

---

**Happy deploying!** 🚀
