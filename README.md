# 🎯 Prismly

> AI-powered competitive intelligence tool that analyzes RSS feeds to extract sentiment, brand archetypes, and strategic insights in minutes.

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?logo=streamlit)](https://prismly.streamlit.app)
[![n8n Workflow](https://img.shields.io/badge/n8n-Workflow-blue)](https://brand-intelligence-n8n.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**🔗 Live Demo:** [https://prismly.streamlit.app](https://prismly.streamlit.app)

---

## 🚀 Quick Start

### Try the Live App (No Setup Required)

1. Visit **[https://prismly.streamlit.app](https://prismly.streamlit.app)**
2. Enter your OpenAI API key in the sidebar
3. Select RSS feeds (preset or custom)
4. Set article count (5-50 per feed)
5. Click **"Analyze Brand"** and wait 1-3 minutes
6. Explore sentiment metrics, archetypes, and insights

> **Note:** First request may take 30-60s (Render free tier cold start)

---

## ✨ Features

- **🔍 Multi-Source Analysis:** Analyze any RSS feeds (preset tech blogs or custom URLs)
- **🎭 Brand Archetype Detection:** Maps content to 12 Jungian archetypes (Hero, Sage, Creator, etc.)
- **💭 Sentiment Analysis:** Positive/neutral/negative classification with confidence scores
- **💡 Strategic Insights:** AI-generated market trends and recommendations
- **🔑 BYOK (Bring Your Own Key):** Use your own OpenAI API key for security and cost control
- **⚡ Fast Processing:** Results in 1-3 minutes (~$0.08 per 100 articles)

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Python)
- **Backend:** n8n automation workflow (Render.com)
- **AI Model:** OpenAI GPT-4o-mini
- **Deployment:** Streamlit Cloud + Render (free tier)

**Architecture:** `Streamlit UI → n8n Webhook → RSS Reader → OpenAI Analysis → Results`

---

## 📦 Local Setup

### Prerequisites
- Python 3.9+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/prismly.git
cd prismly

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app connects to the production n8n workflow automatically.

---

## 🌐 Deployment

### Current Deployment

- **Streamlit App:** [https://prismly.streamlit.app](https://prismly.streamlit.app)
- **n8n Workflow:** [https://brand-intelligence-n8n.onrender.com](https://brand-intelligence-n8n.onrender.com)
- **Status:** ✅ Production Ready

### Deploy Your Own

<details>
<summary><b>Deploy to Streamlit Cloud</b></summary>

1. Fork this repository
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Sign in with GitHub
4. Click "New app" → Select your forked repo
5. Main file: `app.py`
6. Click "Deploy"

</details>

<details>
<summary><b>Deploy n8n to Render</b></summary>

1. Sign up at [render.com](https://render.com)
2. New Web Service → Docker Image: `n8nio/n8n:latest`
3. Add environment variables (see [RENDER_DEPLOYMENT_GUIDE.md](helper%20file/RENDER_DEPLOYMENT_GUIDE.md))
4. Deploy and import workflow JSON
5. Update `app.py` with your webhook URL

</details>

---

## 📁 Project Structure

```
prismly/
├── app.py                          # Streamlit frontend
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .streamlit/
│   └── config.toml                 # Streamlit theme config
└── helper file/
    ├── Johnpeterkennedy_Myclineshareena_A6_Workflow_Dynamic.json  # n8n workflow
    ├── DYNAMIC_FEED_GUIDE.md       # User guide for dynamic feeds
    └── RENDER_DEPLOYMENT_GUIDE.md  # Deployment instructions
```

---

## 💰 Cost Analysis

- **OpenAI GPT-4o-mini:** $0.000150/1K input + $0.000600/1K output tokens
- **Cost per article:** ~$0.0008
- **100 articles:** ~$0.08
- **Hosting:** $0/month (Streamlit Cloud + Render free tier)

---

## 🔒 Security

Both `app.py` and the n8n workflow JSON are **safe to publish publicly**:
- ✅ No hardcoded API keys
- ✅ No passwords or secrets
- ✅ Users provide their own OpenAI API key
- ✅ Dynamic authentication only

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs via Issues
- Submit Pull Requests
- Suggest new features
- Improve documentation

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🎓 About

Built for **INFO7375 - Branding & AI** at Northeastern University  
**Author:** MyclineShareena John Peter Kennedy

---

## 📚 Documentation

- [Dynamic Feed Configuration Guide](helper%20file/DYNAMIC_FEED_GUIDE.md)
- [Render Deployment Guide](helper%20file/RENDER_DEPLOYMENT_GUIDE.md)

---

**Quick Links:**
- 🌐 [Live App](https://prismly.streamlit.app)
- 🔧 [n8n Workflow](https://brand-intelligence-n8n.onrender.com)
- 📖 [OpenAI API Keys](https://platform.openai.com/api-keys)

---

*Built with ❤️ using Streamlit, n8n, and OpenAI*


