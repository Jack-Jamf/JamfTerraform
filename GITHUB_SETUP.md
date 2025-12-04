# GitHub Setup Guide

## ✅ Git Initialized

Your project is now ready for GitHub! Here's what to do next:

## 📝 Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `JamfTerraform` (or your preferred name)
3. Description: "AI-powered Terraform HCL generator for Jamf Pro"
4. **Make it Private** (recommended - contains API integration)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click "Create repository"

## 🔗 Step 2: Connect Local to GitHub

GitHub will show you commands. Use these:

```bash
cd /Users/Shared/Tools/JamfTerraform

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/JamfTerraform.git

# Or if using SSH:
git remote add origin git@github.com:YOUR_USERNAME/JamfTerraform.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🔒 Step 3: Verify Security

Make sure these are **NOT** in your repo:

```bash
# Check what's being tracked
git ls-files | grep -E "(\.env$|venv|node_modules)"

# Should return nothing!
```

If you see `.env` or sensitive files, they're in `.gitignore` and won't be pushed.

## 📋 Step 4: Add Repository Secrets (for CI/CD later)

In GitHub repository settings:

1. Go to Settings → Secrets and variables → Actions
2. Add these secrets:
   - `GEMINI_API_KEY` - Your Gemini API key
   - `JAMF_TOKEN` - Your Jamf API token (for testing)

## 🚀 Step 5: Optional - Add GitHub Actions

Create `.github/workflows/test.yml` for automated testing:

```yaml
name: Test

on: [push, pull_request]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - run: |
          cd backend
          pip install -r requirements.txt
          # Add tests here

  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "18"
      - run: |
          cd frontend
          npm install
          npm run build
```

## 📊 Current Status

✅ Git initialized
✅ Initial commit created (78 files)
✅ .gitignore configured
✅ Sensitive files excluded
⏳ Waiting for GitHub remote

## 🎯 Quick Commands

```bash
# Check status
git status

# See what's committed
git log --oneline

# See what's ignored
git status --ignored

# Add more changes
git add .
git commit -m "Your message"
git push
```

## 🔐 Security Checklist

- [x] `.env` in `.gitignore`
- [x] `venv/` in `.gitignore`
- [x] `node_modules/` in `.gitignore`
- [x] API keys not committed
- [x] `.env.example` included (safe template)

## 📝 Recommended Repository Settings

**After pushing to GitHub**:

1. **Branch Protection** (Settings → Branches):

   - Require pull request reviews
   - Require status checks to pass

2. **Collaborators** (Settings → Collaborators):

   - Add team members

3. **Topics** (About section):
   - `terraform`
   - `jamf-pro`
   - `ai`
   - `fastapi`
   - `react`
   - `tauri`

## 🎉 You're Ready!

Once you push to GitHub, you can:

- Share with team members
- Set up CI/CD
- Deploy to Railway/Render
- Track issues and features
- Collaborate with pull requests

---

**Next**: Create the GitHub repo and run the commands from Step 2!
