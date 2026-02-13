# Deploy to Streamlit Community Cloud

## Overview
Your code is **already on GitHub** at:
https://github.com/Halm3ga/indian-stock-trading-assistant

Now you need to deploy it through Streamlit's web interface.

---

## Step-by-Step Deployment

### Step 1: Go to Streamlit Community Cloud

Open your browser and visit:
**https://share.streamlit.io/**

### Step 2: Sign In with GitHub

1. Click **"Sign in"** or **"Get started"**
2. Choose **"Continue with GitHub"**
3. Authorize Streamlit to access your GitHub repositories

### Step 3: Create New App

1. Click **"New app"** or **"Deploy an app"**
2. You'll see a form with three fields:

   **Repository:**
   ```
   Halm3ga/indian-stock-trading-assistant
   ```

   **Branch:**
   ```
   main
   ```

   **Main file path:**
   ```
   app.py
   ```

3. (Optional) Set a custom URL or leave default
4. Click **"Deploy!"**

### Step 4: Wait for Deployment

- Streamlit will install dependencies from `requirements.txt`
- This takes 2-5 minutes on first deployment
- You'll see logs showing the installation progress

### Step 5: Your App is Live! 🎉

Once deployed, you'll get a URL like:
```
https://your-app-name.streamlit.app
```

You can share this URL with anyone!

---

## Important Notes

### ⚠️ First Run Will Take Time
- The app downloads 10 years of stock data
- Cache will persist between runs
- Subsequent loads will be faster

### 🔄 Auto-Updates
- Any changes you push to GitHub (`git push`)
- Will automatically redeploy your app
- Changes appear within 1-2 minutes

### 📊 Free Tier Limits
- **1 app** for free accounts
- **1 GB RAM** limit
- Apps sleep after inactivity (wake on visit)
- Upgrade for more apps and resources

---

## Updating Your Deployed App

After making code changes locally:

```powershell
# Make your changes to the code
# Then commit and push

git add .
git commit -m "Update trading strategies"
git push
```

The app will automatically redeploy on Streamlit Cloud!

---

## Troubleshooting

### "Module not found" error
- Check that all packages are in `requirements.txt`
- Streamlit Cloud uses a fresh environment

### App runs slow or times out
- Initial data download takes time
- Consider reducing the default period from 10y to 5y
- Or use cached data after first run

### Memory errors
- Try reducing the number of indicators calculated
- Limit historical data period
- Free tier has 1GB RAM limit

### Authentication issues with GitHub
- Make sure repository is public OR
- Grant Streamlit access to private repositories in GitHub settings

---

## Alternative: Local Deployment Only

If you prefer to keep the app local and not deploy to the cloud:

1. Just run locally: `streamlit run app.py`
2. Access at: `http://localhost:8501`
3. The error you saw was because you tried to use a cloud deployment feature locally

---

## Next Steps

1. ✅ Go to https://share.streamlit.io/
2. ✅ Sign in with GitHub
3. ✅ Deploy your app
4. ✅ Share your app URL!

**Your repository is ready - just deploy it through the website!** 🚀
