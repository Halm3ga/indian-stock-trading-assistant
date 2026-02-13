# Git & GitHub Setup Guide

## Current Status
✅ Git installed on your system  
⚠️ PowerShell needs restart to recognize Git

---

## Step 1: Restart PowerShell

**Close and reopen PowerShell** (or your terminal), then verify Git is working:

```powershell
git --version
```

You should see something like: `git version 2.xx.x`

---

## Step 2: Configure Git (First Time Setup)

Set your name and email (this will appear in your commits):

```powershell
cd c:\Users\Me\Desktop\Files\Python\Trading
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

💡 **Tip**: Use the same email as your GitHub account!

---

## Step 3: Initialize Local Repository

```powershell
# Make sure you're in the project directory
cd c:\Users\Me\Desktop\Files\Python\Trading

# Initialize Git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Indian Stock Trading Assistant with backtesting and Streamlit dashboard"

# Check status
git status
```

---

## Step 4: Create GitHub Repository

1. Go to: **https://github.com/new**
2. Fill in:
   - **Repository name**: `indian-stock-trading-assistant`
   - **Description**: `Python trading analysis tool for NSE/BSE with backtesting and Streamlit dashboard`
   - **Visibility**: Public or Private (your choice)
   - ⚠️ **DO NOT** check "Initialize with README" (we already have one)
3. Click **"Create repository"**

---

## Step 5: Connect Local Repository to GitHub

After creating the GitHub repo, you'll see instructions. Use these commands:

### Option A: HTTPS (Easier, may ask for password)
```powershell
git remote add origin https://github.com/YOUR_USERNAME/indian-stock-trading-assistant.git
git branch -M main
git push -u origin main
```

### Option B: SSH (More secure, no passwords)
```powershell
git remote add origin git@github.com:YOUR_USERNAME/indian-stock-trading-assistant.git
git branch -M main
git push -u origin main
```

💡 **For SSH**: You'll need to set up SSH keys first (let me know if you need help with this)

---

## Step 6: Verify on GitHub

Visit your repository URL:
```
https://github.com/YOUR_USERNAME/indian-stock-trading-assistant
```

You should see all your files! 🎉

---

## Future Updates

After making changes to your code:

```powershell
# Stage changes
git add .

# Commit with a message
git commit -m "Description of changes"

# Push to GitHub
git push
```

---

## What's Already Set Up

✅ `.gitignore` file created (excludes cache, data files, etc.)  
✅ `README.md` with project description  
✅ All Python source files ready to commit  

---

## Troubleshooting

### "git: command not found" or "not recognized"
- **Solution**: Restart PowerShell/Terminal
- If still not working, check Git was installed to PATH during installation

### "Permission denied (publickey)" when pushing
- **Solution**: Use HTTPS instead of SSH, or set up SSH keys

### "failed to push some refs"
- **Solution**: Run `git pull origin main` first, then `git push`

### Need to change remote URL?
```powershell
# View current remote
git remote -v

# Change to HTTPS
git remote set-url origin https://github.com/USERNAME/REPO.git

# Change to SSH
git remote set-url origin git@github.com:USERNAME/REPO.git
```

---

## Authentication Methods

### HTTPS (Recommended for beginners)
- GitHub will ask for username and password
- **Important**: Use a **Personal Access Token** instead of password
  - Create token at: https://github.com/settings/tokens
  - Scopes needed: `repo` (full control of private repositories)

### SSH (Advanced, more convenient)
- No password prompts after setup
- Need to generate SSH key and add to GitHub
- Let me know if you want help setting this up!

---

## Next Steps

1. ✅ Restart PowerShell
2. ✅ Run `git --version` to verify
3. ✅ Follow Step 2-6 above
4. 🎉 Your code will be on GitHub!

**Once Git is recognized in your terminal, let me know and I can run these commands for you!**
