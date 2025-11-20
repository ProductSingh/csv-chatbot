# GitHub Setup Instructions

## 📤 Push to GitHub

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the **"+"** icon → **"New repository"**
3. Fill in:
   - **Repository name**: `csv-chatbot` (or your preferred name)
   - **Description**: "CSV Data Analysis Chatbot with Google ADK"
   - **Visibility**: Public or Private (your choice)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

### Step 2: Connect Local Repository to GitHub

Run these commands in your project directory:

```bash
cd "/Users/mani/Downloads/Uptio Project"

# Add remote (replace YOUR_USERNAME and YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 3: Verify

1. Go to your GitHub repository page
2. You should see all your files
3. Verify `.env` is NOT in the repository (it's in .gitignore)

---

## 🔐 Important: Protect Your API Key

**Before pushing**, ensure:
- ✅ `backend/.env` is in `.gitignore` (it is)
- ✅ `.env.example` is committed (shows format without actual key)
- ✅ No API keys in any committed files

**If you accidentally committed an API key**:
1. Remove it from the file
2. Add it to `.gitignore`
3. Use `git rm --cached backend/.env` to remove from git
4. Commit the change
5. **Rotate your API key** (get a new one from Google)

---

## 📝 Commit Best Practices

### Good Commit Messages

```bash
git commit -m "Add group_by_and_aggregate tool for monthly analysis"
git commit -m "Fix session handling for new queries"
git commit -m "Improve agent instructions for better tool selection"
```

### Before Each Commit

1. Test your changes locally
2. Check for console errors
3. Verify functionality works
4. Don't commit `.env` files
5. Don't commit `node_modules` or `venv`

---

## 🔄 Updating Repository

After making changes:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

---

## 👥 Collaboration

If others will work on this:

1. They should clone: `git clone YOUR_REPO_URL`
2. Follow setup instructions in README.md
3. Create their own `.env` file with their API key
4. Never commit `.env` files

---

## 📋 Repository Checklist

Before pushing, ensure:
- ✅ All code is working
- ✅ `.env` is in `.gitignore`
- ✅ `node_modules/` is in `.gitignore`
- ✅ `venv/` is in `.gitignore`
- ✅ Documentation is up to date
- ✅ README.md is clear
- ✅ No sensitive data in code

---

**Your repository is ready to push!**

