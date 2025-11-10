# 🚀 DEPLOYMENT GUIDE - Stock Analysis Tool

Deploy your Stock Analysis Tool to the cloud and access it from anywhere!

---

## 🎯 Option 1: Streamlit Cloud (RECOMMENDED - 100% FREE)

**Best for:** Quick deployment, completely free, easiest setup

### Prerequisites
- GitHub account (free)
- This project

### Step-by-Step Guide

#### 1. Create GitHub Repository

```bash
cd ~/Downloads/stock_analysis_project

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Stock Analysis Tool"

# Create repo on GitHub and push
# Go to github.com and create a new repository named "stock-analysis-tool"
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/stock-analysis-tool.git
git branch -M main
git push -u origin main
```

#### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub account
4. Select your repository: `stock-analysis-tool`
5. Set main file path: `dashboard.py`
6. Click "Deploy"!

**That's it!** Your app will be live at:
`https://YOUR_USERNAME-stock-analysis-tool.streamlit.app`

### Streamlit Cloud Features
✅ **Free forever**
✅ **Automatic updates** when you push to GitHub
✅ **Free SSL/HTTPS**
✅ **Custom domain** support
✅ **500 MB storage**
✅ **1 GB RAM**

---

## 🎯 Option 2: Heroku (FREE TIER)

**Best for:** More control, custom domains, databases

### Prerequisites
- Heroku account (free)
- Heroku CLI installed
- Git

### Step-by-Step Guide

#### 1. Install Heroku CLI

**Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Windows:**
Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. Login to Heroku

```bash
heroku login
```

#### 3. Create Heroku App

```bash
cd ~/Downloads/stock_analysis_project

# Create app
heroku create your-stock-analyzer

# Or let Heroku generate a name
heroku create
```

#### 4. Deploy

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial deployment"

# Deploy to Heroku
git push heroku main

# Open your app
heroku open
```

Your app will be live at:
`https://your-stock-analyzer.herokuapp.com`

### Heroku Configuration

**Set environment variables (if needed):**
```bash
heroku config:set ENABLE_CACHE=true
```

**View logs:**
```bash
heroku logs --tail
```

**Scale up (if needed):**
```bash
heroku ps:scale web=1
```

---

## 🎯 Option 3: Railway (MODERN & SIMPLE)

**Best for:** Modern deployment, generous free tier

### Step-by-Step Guide

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `stock-analysis-tool` repository
6. Railway auto-detects and deploys!

**Free Tier:**
- $5 credit/month
- Automatic deployments
- Custom domains

---

## 🎯 Option 4: Render (FREE TIER)

**Best for:** Simple deployment, good free tier

### Step-by-Step Guide

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name:** stock-analysis-tool
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0`
6. Click "Create Web Service"

**Free Tier:**
- 750 hours/month free
- Auto-deploy from GitHub
- Free SSL

---

## 🔒 Security & Best Practices

### 1. Environment Variables

For sensitive data, use environment variables instead of hardcoding:

**Create `.streamlit/secrets.toml` (local only, not committed):**
```toml
# API Keys (if you add them later)
ALPHA_VANTAGE_API_KEY = "your-key-here"
ANTHROPIC_API_KEY = "your-key-here"
```

**Access in code:**
```python
import streamlit as st
api_key = st.secrets.get("ALPHA_VANTAGE_API_KEY", None)
```

**For Streamlit Cloud:**
- Go to App Settings → Secrets
- Paste your secrets.toml content

**For Heroku:**
```bash
heroku config:set ALPHA_VANTAGE_API_KEY=your-key-here
```

### 2. Database Persistence

**Important:** The SQLite database will be recreated on each deployment.

**Solutions:**
1. **Use cloud storage** (AWS S3, Google Cloud Storage)
2. **Use PostgreSQL** (Heroku provides free Postgres)
3. **Rebuild data on startup** (current default behavior)

### 3. Custom Domain

**Streamlit Cloud:**
- Go to App Settings → General → Custom domain
- Add your domain (e.g., `stocks.yourdomain.com`)
- Update DNS CNAME record

**Heroku:**
```bash
heroku domains:add stocks.yourdomain.com
```

---

## 📊 Monitoring & Maintenance

### Check App Health

**Streamlit Cloud:**
- Dashboard at share.streamlit.io shows app status
- View logs in real-time

**Heroku:**
```bash
heroku logs --tail
heroku ps
```

### Update Your App

1. Make changes locally
2. Test locally: `./run.sh`
3. Commit and push:
   ```bash
   git add .
   git commit -m "Update description"
   git push origin main  # Auto-deploys on Streamlit Cloud
   git push heroku main  # For Heroku
   ```

### Performance Tips

1. **Cache data:** App already uses `@st.cache_resource`
2. **Limit watchlist:** Keep it to 10-15 stocks for faster loading
3. **Update frequency:** Set reasonable intervals in config.py
4. **Optimize queries:** Database is already indexed

---

## 🌍 Accessing From Anywhere

Once deployed, access your app from:
- 📱 **Mobile phones**
- 💻 **Laptops**
- 🖥️ **Work computers**
- 🌐 **Any country** (no VPN needed)

Just bookmark your deployment URL!

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plans Start At |
|----------|-----------|---------------------|
| **Streamlit Cloud** | ✅ Unlimited (1 app) | Free forever |
| **Heroku** | ✅ 550-1000 hrs/mo | $7/month |
| **Railway** | ✅ $5 credit/mo | $5/month |
| **Render** | ✅ 750 hrs/month | $7/month |

**Recommendation:** Start with **Streamlit Cloud** (free forever)

---

## 🆘 Troubleshooting

### App Crashes on Startup

**Check logs:**
- Streamlit Cloud: View in dashboard
- Heroku: `heroku logs --tail`

**Common fixes:**
1. Ensure all dependencies in requirements.txt
2. Check Python version compatibility
3. Verify file paths are relative, not absolute

### Data Not Persisting

- SQLite databases are ephemeral on cloud platforms
- Solution: App rebuilds data on first load (automatic)
- For production: Consider PostgreSQL

### Slow Performance

- Reduce watchlist size
- Increase cache timeout
- Consider upgrading to paid tier for more resources

### Port Already in Use

Make sure your config uses `$PORT` environment variable (already configured)

---

## 🎉 Next Steps

After deployment:

1. ✅ **Share your URL** with friends/family
2. ✅ **Bookmark on mobile** for quick access
3. ✅ **Set up custom domain** (optional)
4. ✅ **Monitor usage** and performance
5. ✅ **Keep updating** with new features

---

## 📞 Support

**Deployment Issues:**
- Streamlit: [discuss.streamlit.io](https://discuss.streamlit.io)
- Heroku: [help.heroku.com](https://help.heroku.com)
- Railway: [docs.railway.app](https://docs.railway.app)

**App Issues:**
- Check your terminal/logs
- Review error messages
- Test locally first

---

## ✅ Quick Start Checklist

For fastest deployment (Streamlit Cloud):

- [ ] Create GitHub account
- [ ] Push code to GitHub repository
- [ ] Go to share.streamlit.io
- [ ] Connect GitHub and deploy
- [ ] **Done!** Share your URL

**Estimated time:** 10-15 minutes

---

**Happy deploying! 🚀**

Your Stock Analysis Tool will be accessible from anywhere in the world!
