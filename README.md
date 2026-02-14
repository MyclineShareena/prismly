# 🎯 Brand Intelligence Pipeline - Streamlit Interface

## Overview
AI-powered brand sentiment and archetype analyzer that processes RSS feeds through an n8n automation workflow using OpenAI GPT-4o-mini.

**Student:** MyclineShareena John Peter Kennedy  
**Course:** INFO7375 - Branding & AI  
**Institution:** Northeastern University  
**Assignment:** Assignment 5 - Wrap Your Tool & Know Your Market

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
**Deployment URL:** https://brand-intelligence-pipeline.streamlit.app/  
**Note:** Cloud deployment requires n8n workflow hosted on a public server (see deployment section below)

## Tech Stack
- **Frontend:** Streamlit (Python web framework)
- **Backend Workflow:** n8n (currently localhost:5678)
- **Integration:** Webhook API (POST requests)
- **AI Model:** OpenAI GPT-4o-mini
- **Data Processing:** pandas, requests
- **Deployment:** Streamlit Community Cloud (frontend only)

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

## Local Installation

### Prerequisites
- **Python 3.9+** for Streamlit
- **n8n self-hosted** (localhost:5678) with workflow imported
- **OpenAI API key** configured in n8n workflow

### Setup Steps

1. **Clone or download this folder**
   ```bash
   cd brand-intelligence-pipeline
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Import n8n workflow**
   - Open n8n at http://localhost:5678
   - Import `Johnpeterkennedy_Myclineshareena_A5_Workflow_Webhook.json`
   - Add OpenAI API credentials in n8n
   - Activate the workflow

4. **Verify webhook URL**
   - In n8n, click the Webhook node
   - **Test URL should be:** `http://localhost:5678/webhook-test/brand-intelligence`
   - Click "Listen for test event" to activate

5. **Run Streamlit app**
   ```bash
   streamlit run app.py
   ```

6. **Analyze feeds!**
   - Select RSS feeds from sidebar
   - Set article count (5-50)
   - Click "Analyze Brand"
   - Wait 1-3 minutes for results

## Streamlit Cloud Deployment

### ⚠️ Important Deployment Consideration
The current app uses **localhost:5678** for the n8n webhook, which won't work when deployed to Streamlit Cloud. You have **two options**:

### Option 1: Deploy n8n to Cloud (Recommended for Production)

**Deploy n8n workflow to a cloud service:**
- **Render:** https://render.com (free tier available)
- **Railway:** https://railway.app (free $5 credit)
- **DigitalOcean:** https://www.digitalocean.com (cheapest $4/month droplet)
- **n8n Cloud:** https://n8n.io/pricing ($20/month, easiest setup)

**Steps:**
1. Deploy n8n to chosen platform
2. Get your public webhook URL (e.g., `https://your-n8n.onrender.com/webhook/brand-intelligence`)
3. Update `app.py` line 149 with the new URL:
   ```python
   n8n_webhook_url = "https://your-n8n.onrender.com/webhook/brand-intelligence"
   ```
4. Push to GitHub and deploy to Streamlit Cloud (see steps below)

### Option 2: Local n8n + Streamlit Cloud (For Assignment Demo)

**Use ngrok to tunnel localhost n8n:**
1. Install ngrok: https://ngrok.com/download
2. Run: `ngrok http 5678`
3. Copy the forwarding URL (e.g., `https://abc123.ngrok.io`)
4. Update `app.py` line 149:
   ```python
   n8n_webhook_url = "https://abc123.ngrok.io/webhook-test/brand-intelligence"
   ```
5. Deploy to Streamlit Cloud
6. **Note:** ngrok URL changes on restart (not permanent solution)

### Deploy Streamlit App to Cloud

**1. Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Brand Intelligence Pipeline"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/brand-intelligence-pipeline.git
   git push -u origin main
   ```

**2. Deploy to Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select repository: `brand-intelligence-pipeline`
   - Main file: `app.py`
   - Click "Deploy"

**3. Get Public URL**
   - Your app will be live at: `https://brand-intelligence-pipeline.streamlit.app`
   - Share this URL in your assignment submission

**4. (Optional) Environment Variables**
   If you want to use environment variables for the webhook URL:
   - In Streamlit Cloud dashboard → App Settings → Secrets
   - Add:
     ```toml
     N8N_WEBHOOK_URL = "https://your-n8n-url.com/webhook/brand-intelligence"
     ```
   - Update `app.py`:
     ```python
     import os
     n8n_webhook_url = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook-test/brand-intelligence")
     ```

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
├── README.md                                 # This deployment guide
└── helper file/ get_max_articles_code.js                  # Debug code for n8n node
```

## Troubleshooting

### "Request timed out"
- **Cause:** n8n workflow taking longer than 15 minutes (900s timeout)
- **Solution:** Reduce article count slider to 5-10 per feed
- **Note:** OpenAI API can be slow during peak hours

### "n8n webhook returned error: 404"
- **Cause:** n8n workflow not activated or webhook URL incorrect
- **Solution:** 
  1. Open n8n workflow
  2. Click Webhook node → "Listen for test event"
  3. Verify test URL is `http://localhost:5678/webhook-test/brand-intelligence`
  4. Try Streamlit again

### "Error calling n8n webhook: Connection refused"
- **Cause:** n8n is not running
- **Solution:** Start n8n with `n8n start` or `npx n8n`

### Slider set to 5 but getting 10 articles
- **Cause:** n8n using cached webhook test event data
- **Solution:**
  1. n8n: Webhook node → "Listen for test event" (clears cache)
  2. Streamlit: Set slider to 5 → "Analyze Brand"
  3. n8n: "Execute workflow" button (full workflow, not individual nodes)
  4. Verify "Get Max Articles" OUTPUT shows `{max_articles: 5}`

### Limit nodes not working in n8n
- **Cause:** Max Items field has hardcoded `10` instead of expression
- **Solution:** Edit each Limit node:
  - Max Items: `={{ $('Get Max Articles').item.json.max_articles }}`
  - Save and re-run workflow

### Cloud deployment: localhost webhook doesn't work
- **Cause:** Streamlit Cloud can't access localhost:5678
- **Solutions:** 
  - **Production:** Deploy n8n to Render/Railway/DigitalOcean, update webhook URL
  - **Quick demo:** Use ngrok tunnel (`ngrok http 5678`)
  - **Alternative:** Refactor to use OpenAI API directly in Streamlit (no n8n)

## Future Enhancements
- [ ] **Cloud n8n Deployment:** Move from localhost to Render/Railway for production
- [ ] **Caching:** Store results in Redis/SQLite for faster repeated analysis
- [ ] **Export Options:** Add JSON/CSV download buttons
- [ ] **Historical Tracking:** Track sentiment trends over time (weekly/monthly)
- [ ] **Competitor Comparison:** Side-by-side brand archetype analysis
- [ ] **Email Reports:** Schedule weekly digest emails
- [ ] **Real-time Updates:** WebSocket connection for live workflow progress
- [ ] **Custom Feeds:** Allow users to add their own RSS feeds
- [ ] **Multi-language:** Support non-English RSS feeds
- [ ] **Advanced Filtering:** Filter by date range, sentiment, archetype

## Technical Specifications
- **Python Version:** 3.9+
- **Streamlit Version:** 1.31.0+
- **n8n Version:** Self-hosted (2.6.3 or higher recommended)
- **OpenAI Model:** GPT-4o-mini
- **Webhook Timeout:** 900 seconds (15 minutes)
- **Default Article Count:** 10 per feed
- **Max Article Count:** 50 per feed
- **Average Processing Time:** 1-3 minutes for 50 articles
- **Average Cost:** $0.0008 per article (~$0.08 per 100 articles)


