# 🎯 Brand Intelligence Pipeline - Streamlit Interface

## Overview
AI-powered brand sentiment and archetype analyzer that processes RSS feeds through an n8n automation workflow using OpenAI GPT-4o-mini.

**Student:** MyclineShareena John Peter Kennedy  
**Course:** INFO7375 - Branding & AI  
**Institution:** Northeastern University  
**Assignment:** Assignment 5 - Wrap Your Tool & Know Your Market

## 🚀 Quick Start

**Try it now - No installation required!**

1. **Visit:** https://brand-intelligence-pipeline.streamlit.app
2. **Select RSS feeds** from sidebar (Azure, OpenAI, Google AI, etc.)
3. **Set article count** (5-50 per feed)
4. **Click "Analyze Brand"**
5. **Wait 1-3 minutes** for AI analysis
6. **Explore results:** Sentiment metrics, archetypes, strategic insights

**First-time users:** The app may take 30-60 seconds to wake up from Render free tier sleep.

## Features
- ✅ **Multi-Feed Analysis:** Process 5 RSS feeds simultaneously (Azure, OpenAI, Google AI, Google Developers, Microsoft Dev)
- ✅ **Dynamic Article Control:** Slider to customize articles per feed (5-50)
- ✅ **Sentiment Detection:** Positive, neutral, negative classification with confidence scores
- ✅ **Brand Archetype Mapping:** 12 Jungian archetypes (Hero, Sage, Explorer, etc.)
- ✅ **Strategic Insights:** AI-generated market trends and positioning recommendations
- ✅ **Rich Visualizations:** Metric cards, archetype distribution, sentiment breakdown, detailed tables
- ✅ **Madison Framework UI:** Clean, professional dashboard design
- ✅ **n8n Integration:** Webhook-based workflow orchestration
- ✅ **Cost Efficient:** ~$0.08 per 100 articles analyzed

## Live Demo
**Streamlit App:** https://brand-intelligence-pipeline.streamlit.app/  
**n8n Workflow:** [https://brand-intelligence-n8n.onrender.com](https://brand-intelligence-n8n.onrender.com/workflow/BmxsjuLzbQO8O1wo)  
**Status:** ✅ Deployed to production (Render + Streamlit Cloud)

## Tech Stack
- **Frontend:** Streamlit (Python web framework)
- **Backend Workflow:** n8n (deployed on Render.com)
- **Integration:** Webhook API (POST requests)
- **AI Model:** OpenAI GPT-4o-mini
- **Data Processing:** pandas, requests
- **Deployment:** 
  - Streamlit Community Cloud (frontend)
  - Render.com Free Tier (n8n backend)

## Architecture

### How It Works
```
Streamlit UI → n8n Webhook → RSS Feed Readers → OpenAI Analysis → Streamlit Display
```

1. **User Selection:** Choose RSS feeds and article count via Streamlit interface
2. **Webhook Call:** Streamlit sends POST request to n8n with `{feeds: [...], max_articles: 10}`
3. **n8n Processing:** n8n workflow fetches RSS articles, limits count, and calls OpenAI API
4. **AI Analysis:** GPT-4o-mini analyzes each article for sentiment, archetype, and insights
5. **Response:** n8n aggregates results and returns `[{data: [...]}]` to Streamlit
6. **Visualization:** Streamlit displays metrics, charts, and detailed tables

## Local Development (Optional)

### Prerequisites
- **Python 3.9+** for Streamlit
- **n8n self-hosted** (localhost:5678) OR **Render deployment** (recommended)
- **OpenAI API key** configured in n8n workflow

### Local Testing with Render n8n (Recommended)

1. **Clone repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/brand-intelligence-pipeline.git
   cd brand-intelligence-pipeline
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Streamlit app**
   ```bash
   streamlit run app.py
   ```
   App uses production Render webhook automatically

4. **Test the app:**
   - Open http://localhost:8501
   - Select RSS feeds from sidebar
   - Set article count (5-50)
   - Click "Analyze Brand"
   - Wait 1-3 minutes for results

### Local Testing with Local n8n (Advanced)

If you want to run n8n locally instead of using Render:

1. **Change webhook URL in app.py** (line 149):
   ```python
   # Comment out production URL
   # n8n_webhook_url = "https://brand-intelligence-n8n.onrender.com/webhook/brand-intelligence"
   
   # Use local URL
   n8n_webhook_url = "http://localhost:5678/webhook-test/brand-intelligence"
   ```

2. **Start n8n locally:**
   ```bash
   npx n8n   # or: n8n start
   ```

3. **Import workflow:**
   - Open n8n at http://localhost:5678
   - Import workflow JSON from Assignment_4_Final or Assignment_5_Final folder
   - Add OpenAI API credentials in n8n
   - Activate the workflow

4. **Activate webhook:**
   - In n8n, click the Webhook node
   - Click "Listen for test event" to activate
   - Test URL: `http://localhost:5678/webhook-test/brand-intelligence`

5. **Run Streamlit:**
   ```bash
   streamlit run app.py
   ```

## Cloud Deployment (Complete Setup)

### ✅ Current Deployment Status
This project is **fully deployed to production**:
- **n8n Workflow:** Running on Render.com (free tier)
- **Streamlit App:** Running on Streamlit Cloud
- **Webhook URL:** `https://brand-intelligence-n8n.onrender.com/webhook/brand-intelligence`

### 📚 Deployment Guides

**For detailed step-by-step instructions, see:**
- **[RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md)** - Complete guide for deploying n8n to Render (15-20 minutes)

### Quick Deploy Steps

**1. Deploy n8n to Render (One-time setup):**
   ```
   1. Sign up at https://render.com (free)
   2. New Web Service → Docker Image: n8nio/n8n:latest
   3. Add environment variables (see RENDER_DEPLOYMENT_GUIDE.md)
   4. Deploy and wait for "Live" status (5-10 minutes)
   5. Import workflow JSON and activate
   ```

**2. Deploy Streamlit to Cloud:**
   ```bash
   # Already configured - webhook URL updated to Render
   git push  # Code is already pushed
   
   # Then deploy:
   # 1. Go to https://streamlit.io/cloud
   # 2. Sign in with GitHub
   # 3. Click "New app"
   # 4. Select repository: brand-intelligence-pipeline
   # 5. Main file: app.py
   # 6. Click "Deploy"
   ```

**3. Test End-to-End:**
   - Open: https://brand-intelligence-pipeline.streamlit.app
   - Select RSS feeds
   - Set slider to 5 articles
   - Click "Analyze Brand"
   - Wait 1-3 minutes for results

### Alternative Deployment Options

<details>
<summary><b>Option 2: Local n8n + ngrok Tunnel</b> (For testing only)</summary>

If you want to test without deploying n8n to cloud:

1. **Install ngrok:** https://ngrok.com/download
2. **Run ngrok:**
   ```bash
   ngrok http 5678
   ```
3. **Update app.py** with ngrok URL:
   ```python
   n8n_webhook_url = "https://abc123.ngrok.io/webhook-test/brand-intelligence"
   ```
4. **Deploy to Streamlit Cloud**

⚠️ **Note:** ngrok URL changes on restart - not suitable for production

</details>

<details>
<summary><b>Option 3: Railway Deployment</b> (Alternative to Render)</summary>

If Render doesn't work:

1. **Go to:** https://railway.app
2. **Sign up** with GitHub ($5 free credit)
3. **New Project** → **Deploy from Docker Hub**
4. **Image:** `n8nio/n8n:latest`
5. **Variables:** Same as Render (see RENDER_DEPLOYMENT_GUIDE.md)
6. **Domain:** Railway provides `https://your-service.up.railway.app`

Railway doesn't spin down like Render but uses paid credits.

</details>

## Usage Guide

### For End Users:
1. **Open the app** at https://brand-intelligence-pipeline.streamlit.app (or localhost:8501)
2. **Select RSS feeds** from sidebar (default: all 5 tech/AI feeds selected)
   - Azure Microsoft Blog
   - OpenAI Blog
   - Google AI Blog
   - Google Developers Blog
   - Microsoft Dev Blogs
3. **Set article count** using slider (5-50 articles per feed)
4. **Click "Analyze Brand"** button
5. **Wait 1-3 minutes** for n8n workflow to process (progress bar shown)
6. **View results:**
   - 📊 Metric cards: Total articles, sentiment distribution, confidence
   - 📈 Charts: Archetype distribution, sentiment breakdown
   - 📑 Detailed table: Title, source, sentiment, archetype, insights
   - 🔍 Deep dive: Expandable sections with full AI reasoning

### Data Flow:
```
Streamlit → POST {feeds: [...], max_articles: 10} → n8n Webhook
          ↓ 
n8n: RSS Feed Readers → Limit Nodes → OpenAI Analysis Loop → Aggregate
          ↓
Streamlit ← [{data: [...]}] Response ← n8n Respond to Webhook
```

### RSS Feeds Included:
- **Azure Blog:** Microsoft cloud and AI updates
- **OpenAI Blog:** GPT, DALL-E, and research announcements  
- **Google AI Blog:** Google's AI research and product launches
- **Google Developers:** Developer tools and platform updates
- **Microsoft DevBlogs:** Cross-platform developer content

## Workflow Design (n8n)

### Nodes & Logic:
1. **Webhook Node:** Receives POST with `{feeds: [], max_articles: int}`
2. **Get Max Articles:** Code node extracts `max_articles` from payload
3. **RSS Feed Readers (5 parallel):** Fetch articles from each feed URL
4. **Limit Nodes (5 parallel):** Keep only first N articles: `={{ $('Get Max Articles').item.json.max_articles }}`
5. **Set Nodes (5 parallel):** Structure data for OpenAI (title, content, link)
6. **Merge Node:** Combine all feed results into single array
7. **Wait Node:** Prevent OpenAI rate limits (1 second delay)
8. **Loop Node:** Iterate through articles one by one
9. **OpenAI Node:** Analyze each article with GPT-4o-mini (sentiment, archetype, insights)
10. **Aggregate Node:** Collect all AI-analyzed results
11. **Respond to Webhook:** Return `[{data: [...]}]` back to Streamlit

### n8n Workflow File:
- `Johnpeterkennedy_Myclineshareena_A5_Workflow_Webhook.json`
- Import via n8n UI → Settings → Import from File

## AI Prompt Design (OpenAI Node in n8n)

The GPT-4o-mini prompt is engineered for multi-dimensional brand analysis:

### Prompt Structure:
```
Analyze this article for brand intelligence:

Title: {{ $json.title }}
Content: {{ $json.content_snippet }}
Source: {{ $json.source }}

Provide JSON response with:
1. Sentiment: {classification: "positive/neutral/negative", confidence: 0-100, reasoning: "..."}
2. Brand Archetype: {primary: "Hero/Sage/Explorer/etc.", reasoning: "..."}
3. Insights: [{category: "market_trend/positioning/opportunity", insight: "...", recommendation: "..."}]
```

### Analysis Dimensions:
- **Sentiment Analysis:** Emotional tone classification (positive/neutral/negative) with 0-100% confidence
- **Brand Archetype:** Maps to 12 Jungian archetypes (Hero, Sage, Explorer, Innocent, Creator, Ruler, Caregiver, Magician, Lover, Jester, Everyman, Rebel)
- **Strategic Insights:** Market trends, competitive positioning, brand opportunities
- **Actionable Recommendations:** Specific strategy advice based on analysis

### Response Format (JSON):
```json
{
  "sentiment": {
    "classification": "positive",
    "confidence": 85,
    "reasoning": "Article highlights innovation and customer success"
  },
  "archetype": {
    "primary": "Hero",
    "reasoning": "Emphasizes overcoming challenges and achieving goals"
  },
  "insights": [
    {
      "category": "market_trend",
      "insight": "Growing demand for AI-powered solutions",
      "recommendation": "Position as innovation leader in AI space"
    }
  ]
}
```

## Cost Analysis
- **GPT-4o-mini pricing:** $0.000150/1K input tokens, $0.000600/1K output tokens
- **Average article:** ~500 tokens input, ~100 tokens output
- **Cost per article:** ~$0.0008
- **100 articles:** ~$0.08
- **500 articles:** ~$0.40

## Assignment 5 Context

This Streamlit interface wraps the **Assignment 4 Brand Intelligence Pipeline** (n8n workflow) into a shareable web application for:
- ✅ **Public Access:** Stakeholders can analyze feeds without n8n knowledge
- ✅ **User Control:** Dynamic article count via slider (cost optimization)
- ✅ **Visual Dashboard:** Madison framework with charts, metrics, and insights
- ✅ **User Testing:** 3 participants tested interface (see Assignment 5 submission doc)
- ✅ **Competitive Analysis:** Compared to Brand24, Crayon, Feedly AI (see submission)
- ✅ **Trademark Research:** "Brand Intelligence" trademark search completed (see submission)

## File Structure
```
brand-intelligence-pipeline/
├── app.py                                    # Streamlit frontend (429 lines)
├── requirements.txt                          # Python dependencies
├── README.md                                 # This comprehensive guide
├── RENDER_DEPLOYMENT_GUIDE.md                # Step-by-step Render deployment
├── .streamlit/                               # Streamlit configuration
└── helper file/
    └── get_max_articles_code.js              # Debug code for n8n node
```

**n8n Workflow File:** Located in parent directory `Assignment_4_Final/` or `Assignment_5_Final/`
- Filename: `Johnpeterkennedy_Myclineshareena_A4_Workflow.json` or similar
- Import this into Render n8n instance

## Troubleshooting

### "Request timed out"
- **Cause:** n8n workflow taking longer than 15 minutes (900s timeout) OR Render cold start
- **Solution:** 
  - Reduce article count slider to 5-10 per feed
  - Wait 60 seconds and retry (Render may be waking up from sleep)
- **Note:** OpenAI API can be slow during peak hours

### "Service Unavailable" or 503 Error (Render)
- **Cause:** Render n8n spinning up from cold start (15min+ inactivity)
- **Solution:** 
  - Wait 30-60 seconds and try again
  - Use UptimeRobot to keep n8n alive (see RENDER_DEPLOYMENT_GUIDE.md)
  - First request after idle takes longer

### "n8n webhook returned error: 404"
- **Cause:** n8n workflow not activated or webhook URL incorrect
- **Solution:** 
  1. Open https://brand-intelligence-n8n.onrender.com
  2. Login and verify workflow is ACTIVE (toggle switch green)
  3. Check webhook node shows correct path: `/webhook/brand-intelligence`
  4. Verify app.py uses production URL (not test URL)

### "Unauthorized" or 401 Error (Render)
- **Cause:** Basic auth blocking webhook requests
- **Solution:** 
  - In Render dashboard → Environment → Set `N8N_BASIC_AUTH_ACTIVE=false`
  - OR access n8n UI at the URL and login to verify credentials

### "Error calling n8n webhook: Connection refused"
- **Cause:** 
  - (Render) Service is down or failed deployment
  - (Local) n8n is not running
- **Solution:** 
  - (Render) Check Render dashboard - service should show "Live" status
  - (Render) Check Render logs for errors
  - (Local) Start n8n with `n8n start` or `npx n8n`

### Slider set to 5 but getting 10 articles (n8n issue)
- **Cause:** Limit nodes not reading max_articles from webhook payload
- **Solution:**
  1. Login to Render n8n: https://brand-intelligence-n8n.onrender.com
  2. Open workflow → Click each "Limit" node
  3. Verify Max Items: `={{ $('Get Max Articles').item.json.max_articles }}`
  4. If hardcoded to `10`, change to expression above
  5. Save workflow and test again

### Limit nodes not working in n8n
- **Cause:** Max Items field has hardcoded `10` instead of expression
- **Solution:** Edit each Limit node:
  - Max Items: `={{ $('Get Max Articles').item.json.max_articles }}`
  - Save and re-activate workflow

### Slow performance (Render free tier)
- **Expected:** Free tier has limited CPU/memory
- **Solutions:**
  - Reduce article count to 5-10 per feed
  - Select fewer RSS feeds (2-3 instead of 5)
  - Upgrade to Render paid tier ($7/month for better performance)

### Workflow runs but returns empty results
- **Cause:** OpenAI credentials missing or invalid
- **Solution:**
  1. Login to Render n8n
  2. Go to Credentials menu
  3. Verify OpenAI API key is saved
  4. Test OpenAI node manually in workflow
  5. Check Render logs for API errors

## Technical Specifications
- **Python Version:** 3.9+
- **Streamlit Version:** 1.31.0+
- **n8n Version:** Deployed on Render (v2.6.3+)
- **OpenAI Model:** GPT-4o-mini
- **Webhook Timeout:** 900 seconds (15 minutes)
- **Default Article Count:** 10 per feed
- **Max Article Count:** 50 per feed
- **Average Processing Time:** 1-3 minutes for 50 articles
- **Average Cost:** $0.0008 per article (~$0.08 per 100 articles)
- **Deployment:** 
  - Frontend: Streamlit Cloud (free tier)
  - Backend: Render.com (free tier)
  - Total Cost: $0/month

## Production Deployment Status

### ✅ Live URLs
- **Streamlit App:** https://brand-intelligence-pipeline.streamlit.app
- **n8n Workflow:** [https://brand-intelligence-n8n.onrender.com](https://brand-intelligence-n8n.onrender.com/workflow/BmxsjuLzbQO8O1wo)
- **Webhook Endpoint:** https://brand-intelligence-n8n.onrender.com/webhook/brand-intelligence

### 🚀 Deployment Details
- **Deployed:** February 14, 2026
- **Status:** Production Ready
- **Uptime:** Render free tier (spins down after 15min inactivity)
- **Cold Start:** ~30-60 seconds on first request
- **Keep-Alive:** Optional via UptimeRobot (see RENDER_DEPLOYMENT_GUIDE.md)

### 📊 Performance Metrics
- **Concurrent Users:** Unlimited (Streamlit Cloud)
- **Analysis Speed:** 1-3 minutes for 50 articles (5 feeds × 10 articles)
- **Rate Limits:** Depends on OpenAI API tier
- **Storage:** None (stateless analysis)


**Quick Links:**
- 🌐 [Live App](https://brand-intelligence-pipeline.streamlit.app)
- 🔧 [n8n Workflow]([https://brand-intelligence-n8n.onrender.com](https://brand-intelligence-n8n.onrender.com/workflow/BmxsjuLzbQO8O1wo))
---

*Built with ❤️ for INFO7375 - Branding & AI at Northeastern University*


