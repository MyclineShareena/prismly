# 🚀 n8n Render Cloud Deployment Guide

## Overview
Deploy your n8n workflow to Render's free tier for public webhook access from Streamlit Cloud.

**Time Required:** 15-20 minutes  
**Cost:** FREE (Render free tier)  
**Result:** Public n8n webhook URL for Streamlit integration

---

## Prerequisites
- ✅ GitHub account
- ✅ Render account (sign up at https://render.com)
- ✅ n8n workflow JSON file (`Johnpeterkennedy_Myclineshareena_A5_Workflow_Webhook.json`)
- ✅ OpenAI API key

---

## Step 1: Create Render Account

1. **Go to** https://render.com
2. **Click "Get Started"** (top right)
3. **Sign up with GitHub** (recommended) or email
4. **Verify email** if using email signup
5. **Complete profile** (name, purpose: "Student Project")

---

## Step 2: Deploy n8n to Render

### Option A: Deploy from n8n's Docker Image (Easiest)

1. **In Render Dashboard:**
   - Click "New +" → "Web Service"

2. **Choose "Deploy an existing image from a registry"**
   - Click "Next"

3. **Configure Service:**
   - **Image URL:** `n8nio/n8n:latest`
   - **Name:** `brand-intelligence-n8n` (or your choice)
   - **Region:** Choose closest to you (e.g., Oregon, Frankfurt)
   - **Instance Type:** **Free** (select from dropdown)

4. **Environment Variables:**
   Click "Add Environment Variable" for each:
   
   ```
   N8N_BASIC_AUTH_ACTIVE=true
   N8N_BASIC_AUTH_USER=admin
   N8N_BASIC_AUTH_PASSWORD=YourStrongPassword123!
   N8N_HOST=0.0.0.0
   N8N_PORT=5678
   N8N_PROTOCOL=https
   WEBHOOK_URL=https://brand-intelligence-n8n.onrender.com/
   EXECUTIONS_MODE=regular
   ```
   
   **⚠️ IMPORTANT:** Replace `YourStrongPassword123!` with your own secure password

5. **Advanced Settings:**
   - **Port:** `5678`
   - **Health Check Path:** `/healthz`
   - **Auto-Deploy:** Yes (recommended)

6. **Click "Create Web Service"**
   - Wait 5-10 minutes for deployment
   - Status will show "Live" when ready

---

## Step 3: Access Your n8n Instance

1. **Get your URL:**
   - Render will assign: `https://brand-intelligence-n8n.onrender.com`
   - Or your custom name: `https://YOUR-SERVICE-NAME.onrender.com`

2. **Open in browser:**
   - Navigate to your n8n URL
   - You'll see n8n login screen

3. **Login:**
   - **Username:** `admin`
   - **Password:** (the one you set in environment variables)

4. **Initial Setup:**
   - Set owner email/password if prompted
   - Skip "Connect to cloud" (use self-hosted)

---

## Step 4: Import Your Workflow

1. **In n8n UI:**
   - Click **Settings** (bottom left gear icon)
   - Click **Import from File**
   - Or use keyboard: `Ctrl + O` (Windows) or `Cmd + O` (Mac)

2. **Upload workflow:**
   - Select `Johnpeterkennedy_Myclineshareena_A5_Workflow_Webhook.json`
   - Click "Import"

3. **Verify workflow loaded:**
   - You should see all nodes: Webhook, Get Max Articles, RSS Feeds, Limit nodes, etc.
   - Check that connections are intact

---

## Step 5: Configure OpenAI Credentials

1. **Click "Credentials" menu** (left sidebar)

2. **Add new credential:**
   - Click "Add Credential"
   - Search for "OpenAI"
   - Click "OpenAI API"

3. **Enter API Key:**
   - **API Key:** `sk-your-openai-api-key-here`
   - **Name:** `OpenAI GPT-4o-mini`
   - Click "Save"

4. **Update OpenAI node:**
   - Go back to your workflow
   - Click the "OpenAI" node (in the loop)
   - In the right panel, select your OpenAI credential
   - Click "Save"

---

## Step 6: Activate Workflow & Get Webhook URL

1. **Activate the workflow:**
   - Toggle the switch at top right from "Inactive" to "Active"
   - It should turn green/blue

2. **Get Production Webhook URL:**
   - Click the **Webhook** node
   - In right panel, you'll see:
     - **Test URL:** `https://brand-intelligence-n8n.onrender.com/webhook-test/brand-intelligence`
     - **Production URL:** `https://brand-intelligence-n8n.onrender.com/webhook/brand-intelligence`

3. **Copy the Production URL:**
   ```
   https://brand-intelligence-n8n.onrender.com/webhook/brand-intelligence
   ```
   ⚠️ Use **Production URL** (not Test URL) for Streamlit Cloud

---

## Step 7: Update Streamlit App

1. **Open `app.py`** in your local editor

2. **Find line 149** (webhook URL):
   ```python
   n8n_webhook_url = "http://localhost:5678/webhook-test/brand-intelligence"
   ```

3. **Replace with your Render URL:**
   ```python
   n8n_webhook_url = "https://brand-intelligence-n8n.onrender.com/webhook/brand-intelligence"
   ```
   ⚠️ Make sure to use **`/webhook/`** (production) not `/webhook-test/`

4. **Save the file**

---

## Step 8: Test the Integration Locally

Before deploying to Streamlit Cloud, test locally:

1. **Make sure n8n workflow is ACTIVE** on Render

2. **Run Streamlit locally:**
   ```bash
   cd brand-intelligence-pipeline
   streamlit run app.py
   ```

3. **In Streamlit:**
   - Select RSS feeds
   - Set slider to 5
   - Click "Analyze Brand"

4. **Wait for results:**
   - Should take 1-3 minutes
   - Check Render logs if errors occur (Dashboard → Service → Logs tab)

5. **Verify results show correct count:**
   - If slider=5, should get ~25 articles total (5 per feed)
   - Check metric cards and table

---

## Step 9: Deploy Streamlit to Cloud

Now that n8n is on Render and working, deploy Streamlit:

1. **Push to GitHub:**
   ```bash
   cd brand-intelligence-pipeline
   git add .
   git commit -m "Update webhook URL to Render production"
   git push
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Repository: `brand-intelligence-pipeline`
   - Branch: `main`
   - Main file: `app.py`
   - Click "Deploy"

3. **Get Streamlit URL:**
   - Your app: `https://brand-intelligence-pipeline.streamlit.app`
   - Or: `https://YOUR-USERNAME-brand-intelligence-pipeline.streamlit.app`

4. **Test end-to-end:**
   - Open Streamlit Cloud URL
   - Select feeds
   - Click "Analyze Brand"
   - Verify results

---

## Important Notes

### ⚠️ Render Free Tier Limitations
- **Spins down after 15 minutes of inactivity**
- **First request after spin-down takes 30-60 seconds to wake up**
- **750 hours/month free** (plenty for assignment)
- **No custom domain** on free tier

### 🔧 Handling Cold Starts
When n8n spins down, the first Streamlit request will timeout. Solutions:

**Option 1: Increase Streamlit timeout**
```python
# In app.py, line ~168
response = requests.post(
    webhook_url,
    json=payload,
    timeout=120  # Increase from 900 to 120 for cold start
)
```

**Option 2: Add retry logic with spinner**
```python
def call_n8n_webhook(webhook_url, feed_urls, max_articles_per_feed):
    """Call n8n webhook with automatic retry for cold starts"""
    max_retries = 2
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                st.info("🔄 Waking up n8n service... (Render cold start)")
            
            response = requests.post(
                webhook_url,
                json={"feeds": feed_urls, "max_articles": max_articles_per_feed},
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()
        
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                st.warning(f"⏱️ Timeout on attempt {attempt + 1}. Retrying...")
                time.sleep(5)
                continue
            else:
                st.error("Request timed out after retries. Try again.")
                return None
    
    return None
```

**Option 3: Keep-alive ping (prevent spin-down)**
Use UptimeRobot (free) to ping your n8n URL every 5 minutes:
- Go to https://uptimerobot.com
- Add monitor: `https://brand-intelligence-n8n.onrender.com/healthz`
- Interval: 5 minutes
- Prevents spin-down during assignment demo

### 🔐 Security Best Practices
1. **Use strong password** for N8N_BASIC_AUTH_PASSWORD
2. **Don't commit API keys** to GitHub
3. **Use Streamlit Secrets** for sensitive data (optional):
   ```toml
   # In Streamlit Cloud → App Settings → Secrets
   N8N_WEBHOOK_URL = "https://brand-intelligence-n8n.onrender.com/webhook/brand-intelligence"
   ```
   ```python
   # In app.py
   import os
   n8n_webhook_url = st.secrets.get("N8N_WEBHOOK_URL", "http://localhost:5678/webhook-test/brand-intelligence")
   ```

### 📊 Monitoring
- **Render Dashboard:** View logs, metrics, deployments
- **n8n Executions:** Check workflow runs (Executions tab in n8n)
- **Streamlit Logs:** View app logs in Streamlit Cloud dashboard

---

## Troubleshooting

### "Service Unavailable" or 503 Error
- **Cause:** n8n spinning up from cold start
- **Solution:** Wait 30-60 seconds and try again, or implement retry logic

### "Unauthorized" or 401 Error
- **Cause:** Basic auth blocking webhook
- **Solution:** In Render environment variables, set:
  ```
  N8N_BASIC_AUTH_ACTIVE=false
  ```
  Or configure webhook authentication separately

### Workflow not executing
- **Check:** n8n workflow is ACTIVE (toggle switch green)
- **Check:** Render service is "Live" (not "Failed")
- **Check:** Render logs for errors (Dashboard → Logs)
- **Check:** OpenAI credentials are saved in n8n

### "max_articles not found" error
- **Check:** "Get Max Articles" code node is correct
- **Check:** Webhook is receiving POST data (check n8n Executions)
- **Re-import:** If nodes broken, re-import workflow JSON

### Slow performance
- **Expected:** Free tier has limited resources
- **Reduce:** Article count to 5-10 per feed
- **Optimize:** Remove Wait node to speed up (may hit OpenAI rate limits)

---

## Alternative: Railway Deployment

If Render doesn't work, try Railway:

1. **Go to** https://railway.app
2. **Sign up** with GitHub
3. **New Project** → **Deploy from Docker Hub**
4. **Image:** `n8nio/n8n:latest`
5. **Variables:** Same as Render (see Step 2)
6. **Domain:** Railway provides `https://your-service.up.railway.app`

Railway gives $5 credit (enough for ~1 month) and doesn't spin down.

---

## Summary Checklist

- [ ] Render account created
- [ ] n8n deployed to Render (free tier)
- [ ] Environment variables configured (basic auth, webhook URL)
- [ ] n8n accessible at `https://brand-intelligence-n8n.onrender.com`
- [ ] Workflow imported successfully
- [ ] OpenAI credentials added to n8n
- [ ] Workflow activated (toggle green)
- [ ] Production webhook URL copied
- [ ] `app.py` updated with Render webhook URL
- [ ] Tested locally (Streamlit → Render n8n)
- [ ] Pushed to GitHub
- [ ] Deployed to Streamlit Cloud
- [ ] Tested end-to-end (Streamlit Cloud → Render n8n)
- [ ] (Optional) UptimeRobot keep-alive configured

---

**Deployment Status:** 🟢 Ready for Assignment 5 Submission

**Streamlit URL:** `https://brand-intelligence-pipeline.streamlit.app`  
**n8n URL:** `https://brand-intelligence-n8n.onrender.com`  
**Webhook URL:** `https://brand-intelligence-n8n.onrender.com/webhook/brand-intelligence`

---

**Last Updated:** February 14, 2026  
**Estimated Setup Time:** 15-20 minutes  
**Cost:** FREE (Render free tier)
