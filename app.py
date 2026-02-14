import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="Brand Intelligence Pipeline",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .positive { 
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%); 
    }
    .neutral { 
        background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%); 
    }
    .negative { 
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); 
    }
    .footer {
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #eee;
        text-align: center;
        color: #999;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - About & Settings
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=Brand+Intelligence", use_column_width=True)
    
    st.markdown("### 🎯 About This Tool")
    st.write("""
    **Brand Intelligence Pipeline** analyzes articles from RSS feeds to extract:
    - Sentiment (Positive/Neutral/Negative)
    - Brand Archetypes (Hero, Sage, etc.)
    - Strategic Insights & Recommendations
    """)
    
    st.markdown("### 🛠️ Tech Stack")
    st.write("• **Framework:** Streamlit")
    st.write("• **AI Model:** OpenAI GPT-4o-mini")
    st.write("• **Data Source:** RSS Feeds")
    st.write("• **Cost:** ~$0.08 per 100 articles")
    
    st.markdown("### 👤 Created By")
    st.write("**MyclineShareena John Peter Kennedy**")
    st.write("Northeastern University")
    st.write("INFO7375 - Branding & AI")
    st.write("[GitHub](https://github.com/MyclineShareena) | [LinkedIn](https://www.linkedin.com/in/mycline-shareena-j-9b8128168/)")
    
    st.markdown("---")
    st.caption("© 2026 Brand Intelligence Pipeline")

# Main content
st.markdown('<div class="main-header">🎯 Brand Intelligence Pipeline</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-powered brand analysis from RSS feeds using GPT-4o-mini</div>', unsafe_allow_html=True)

# Instructions
with st.expander("📖 How to Use This Tool", expanded=False):
    st.markdown("""
    1. **Enter your n8n webhook URL** in the sidebar (optional - uses default if blank)
    2. **Add RSS feed URLs** - one per line (default feeds are pre-loaded)
    3. **Set the number of articles** to analyze (1-50 recommended)
    4. **Click "Analyze Feeds"** and wait for results
    5. **View insights** - sentiment breakdown, archetypes, and recommendations
    6. **Download** the full dataset as JSON
    
    **Example RSS Feeds:**
    - Azure Blog: https://azure.microsoft.com/en-us/blog/feed/
    - OpenAI Blog: https://openai.com/blog/rss.xml
    - Google AI Blog: http://googleaiblog.blogspot.com/atom.xml
    """)

# n8n Webhook URL - HARDCODED
n8n_webhook_url = "http://localhost:5678/webhook-test/brand-intelligence"

with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔗 n8n Configuration")
    st.success(f"✅ Connected to n8n workflow")
    st.caption(f"Webhook: {n8n_webhook_url}")

# Input Section
st.markdown("### 📥 Input Configuration")

col1, col2 = st.columns([3, 1])

with col1:
    rss_feeds = st.text_area(
        "RSS Feed URLs (one per line):",
        value="""https://azure.microsoft.com/en-us/blog/feed/
https://openai.com/blog/rss.xml
http://googleaiblog.blogspot.com/atom.xml
https://developers.googleblog.com/feeds/posts/default
https://devblogs.microsoft.com/feed/""",
        height=150,
        help="Enter RSS feed URLs, one per line. Default feeds are from major tech companies."
    )

with col2:
    max_articles = st.number_input(
        "Max articles per feed:",
        min_value=1,
        max_value=50,
        value=10,
        help="Limit articles per feed to control processing time and cost"
    )

# Analyze button
analyze_button = st.button("🚀 Analyze Feeds", type="primary", use_container_width=True)

# Function to call n8n webhook
def call_n8n_webhook(webhook_url, feed_urls, max_articles_per_feed):
    """Call n8n webhook with RSS feed URLs"""
    try:
        payload = {
            "feeds": feed_urls,
            "max_articles": max_articles_per_feed
        }
        
        response = requests.post(
            webhook_url,
            json=payload,
            timeout=300  # 5 minute timeout for n8n to process
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"n8n webhook returned error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. n8n workflow may be taking too long. Try reducing the number of articles.")
        return None
    except Exception as e:
        st.error(f"Error calling n8n webhook: {str(e)}")
        return None

# Process feeds
if analyze_button:
    if not n8n_webhook_url:
        st.error("⚠️ Please enter your n8n webhook URL in the sidebar!")
    else:
        feed_urls = [url.strip() for url in rss_feeds.split("\n") if url.strip()]
        
        if not feed_urls:
            st.error("⚠️ Please enter at least one RSS feed URL!")
        else:
            st.markdown("---")
            st.markdown("### 🔄 Processing Feeds via n8n...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text(f"📡 Sending {len(feed_urls)} feeds to n8n workflow...")
            progress_bar.progress(0.3)
            
            # Call n8n webhook
            result_data = call_n8n_webhook(n8n_webhook_url, feed_urls, max_articles)
            
            if result_data:
                progress_bar.progress(1.0)
                status_text.text("✅ Analysis complete!")
                
                # Parse results from n8n
                # Assuming n8n returns array of analyzed articles
                all_results = result_data if isinstance(result_data, list) else result_data.get('results', [])
                
                if not all_results:
                    st.warning("⚠️ No results returned from n8n. Check your workflow output.")
                else:
                    time.sleep(1)
                    status_text.empty()
                    progress_bar.empty()
                    
                    # Display Results
                    st.markdown("---")
                    st.markdown("### 📊 Analysis Results")
                    
                    # Calculate metrics
                    sentiments = {'positive': 0, 'neutral': 0, 'negative': 0}
                    archetypes = {}
                    
                    for result in all_results:
                        sent = result.get('sentiment', 'neutral').lower()
                        if sent in sentiments:
                            sentiments[sent] += 1
                        
                        arch = result.get('archetype', 'Unknown')
                        archetypes[arch] = archetypes.get(arch, 0) + 1
                    
                    # Sentiment metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("📰 Total Articles", len(all_results))
                    
                    with col2:
                        st.metric("😊 Positive", sentiments['positive'])
                    
                    with col3:
                        st.metric("😐 Neutral", sentiments['neutral'])
                    
                    with col4:
                        st.metric("😟 Negative", sentiments['negative'])
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Archetype breakdown
                    st.markdown("#### 🎭 Brand Archetype Distribution")
                    archetype_df = pd.DataFrame(list(archetypes.items()), columns=['Archetype', 'Count'])
                    archetype_df = archetype_df.sort_values('Count', ascending=False)
                    st.bar_chart(archetype_df.set_index('Archetype'))
                
                # Article table
                st.markdown("#### 📄 Detailed Article Analysis")
                
                df = pd.DataFrame(all_results)
                df['Sentiment'] = df['sentiment'].apply(lambda x: x.upper())
                df['Confidence'] = df['confidence'].apply(lambda x: f"{x:.2f}")
                
                display_df = df[['title', 'Sentiment', 'Confidence', 'archetype', 'insight']].head(20)
                st.dataframe(
                    display_df,
                    column_config={
                        "title": "Article Title",
                        "Sentiment": st.column_config.TextColumn("Sentiment", width="small"),
                        "Confidence": st.column_config.TextColumn("Confidence", width="small"),
                        "archetype": "Archetype",
                        "insight": "Key Insight"
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Download options
                st.markdown("---")
                st.markdown("### 💾 Download Results")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # JSON download
                    json_data = json.dumps(all_results, indent=2)
                    st.download_button(
                        label="📥 Download JSON Dataset",
                        data=json_data,
                        file_name=f"brand_intelligence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col2:
                    # CSV download
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV Report",
                        data=csv_data,
                        file_name=f"brand_intelligence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            else:
                st.warning("⚠️ No articles were successfully analyzed.")

# Footer
st.markdown("""
<div class="footer">
    <p>Built with Streamlit + OpenAI GPT-4o-mini | Assignment 5 - INFO7375 Branding & AI</p>
    <p>MyclineShareena John Peter Kennedy | Northeastern University | Spring 2026</p>
</div>
""", unsafe_allow_html=True)
