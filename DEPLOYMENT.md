# Deployment Guide

## Option 1: Deploy to Render (Recommended - Free)

1. **Push to GitHub**
   - Create a new GitHub repo
   - Push your project code
   - Make sure `.env` is in `.gitignore` (it is)

2. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

3. **Connect Your Repo**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Set deployment settings:
     - **Name**: instagram-caption-generator
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`

4. **Add Environment Variables**
   - In Render dashboard, go to Environment
   - Add: `GEMINI_API_KEY` = your API key
   - Add: `FLASK_ENV` = production

5. **Deploy**
   - Click "Deploy"
   - Your app will be live at: `https://instagram-caption-generator.onrender.com`

---

## Option 2: Deploy to Railway (Very Easy)

1. **Push to GitHub** (same as above)

2. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

3. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

4. **Add Environment Variables**
   - In Railway, go to Variables
   - Add `GEMINI_API_KEY` and your key
   - Add `FLASK_ENV=production`

5. **Deploy**
   - Railway auto-deploys
   - Your app gets a public URL instantly

---

## Option 3: Local Ngrok (Quick Testing)

For quick public access without full deployment:

```bash
pip install ngrok
ngrok http 5000
```

This gives you a temporary public URL like `https://xxxx.ngrok.io`

---

## Option 4: Heroku (Paid)

1. Create Heroku account at https://heroku.com
2. Install Heroku CLI
3. Run:
   ```bash
   heroku create your-app-name
   heroku config:set GEMINI_API_KEY=your_key_here
   git push heroku main
   ```

---

## Important Security Notes

✅ **DO NOT commit `.env` file to GitHub**
✅ Store API keys in platform's environment variables
✅ Use `FLASK_ENV=production` in production
✅ Keep debug mode OFF in production

---

## After Deployment

1. Test the live app thoroughly
2. Share the public URL with users
3. Monitor error logs in the platform dashboard
4. Keep your Gemini API key safe and rotate periodically
