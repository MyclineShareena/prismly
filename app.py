import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import time
from collections import Counter

# Page config
st.set_page_config(
    page_title="Brand Intelligence Pipeline",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Madison Style
st.markdown("""
<style>
    .success-banner {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 20px;
    }
    .metric-box {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #333;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .insight-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .positive-badge {
        background: #28a745;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
    }
    .neutral-badge {
        background: #ffc107;
        color: #333;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
    }
    .negative-badge {
        background: #dc3545;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
    }
    .footer {
        margin-top: 3rem;
        padding-top: 1rem;
        text-align: center;
        color: #999;
        font-size: 0.85rem;
        border-top: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Define RSS Feed Options (domain-based names)
RSS_FEED_OPTIONS = {
    "Azure Microsoft Blog": "https://azure.microsoft.com/en-us/blog/feed/",
    "OpenAI Blog": "https://openai.com/blog/rss.xml",
    "Google AI Blog": "http://googleaiblog.blogspot.com/atom.xml",
    "Google Developers Blog": "https://developers.googleblog.com/feeds/posts/default",
    "Microsoft Dev Blogs": "https://devblogs.microsoft.com/feed/"
}

# Sidebar - Search Settings
with st.sidebar:
    st.markdown("### ⚙️ Search Settings")
    
    max_articles = st.slider(
        "Posts to Fetch",
        min_value=5,
        max_value=50,
        value=10,
        help="Number of articles to analyze per feed"
    )
    
    st.markdown("---")
    
    selected_feeds = st.multiselect(
        "📡 RSS Feed URLs:",
        options=list(RSS_FEED_OPTIONS.keys()),
        default=list(RSS_FEED_OPTIONS.keys()),
        help="Select RSS feeds to analyze"
    )
    
    st.markdown("---")
    
    st.markdown("### 🎯 About This Tool")
    st.write("""
    **Brand Intelligence Pipeline** uses AI to analyze competitor blog posts and extract:
    - 💭 Sentiment Analysis
    - 🎭 Brand Archetypes
    - 💡 Strategic Insights
    - ✅ Recommendations
    """)
    
    st.markdown("### 🛠️ Tech Stack")
    st.write("• **Frontend:** Streamlit")
    st.write("• **Workflow:** n8n")
    st.write("• **AI Model:** OpenAI GPT-4o-mini")
    st.write("• **Integration:** Webhook API")
    
    st.markdown("### 👤 Created By")
    st.write("**MyclineShareena**")
    st.write("Northeastern University")
    st.write("INFO 7375 - Branding & AI")
    st.write("[GitHub](https://github.com/MyclineShareena)")
    
    st.markdown("---")
    st.caption("Brand Intelligence Framework v1.2")

# n8n Webhook URL - Production (Render Cloud)
n8n_webhook_url = "https://brand-intelligence-n8n.onrender.com/webhook-test/brand-intelligence"

# Main Dashboard Header
st.title("🎯 Brand Intelligence Dashboard")
st.markdown("---")

# Analyze button
analyze_button = st.button("🔍 Analyze Brand", type="primary", use_container_width=True)

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
            timeout=900  # 15 minute timeout for n8n to process
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
        # Get URLs from selected feeds
        feed_urls = [RSS_FEED_OPTIONS[feed_name] for feed_name in selected_feeds]
        
        if not feed_urls:
            st.error("⚠️ Please select at least one RSS feed!")
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
                
                # Parse results from n8n - handle [{data: [...]}] structure
                all_results = []
                
                if isinstance(result_data, list) and len(result_data) > 0:
                    if isinstance(result_data[0], dict) and 'data' in result_data[0]:
                        # n8n webhook response format: [{data: [...]}]
                        all_results = result_data[0]['data']
                    else:
                        all_results = result_data
                elif isinstance(result_data, dict) and 'data' in result_data:
                    all_results = result_data['data']
                
                if not all_results:
                    st.warning("⚠️ No results returned from n8n. Check your workflow output.")
                else:
                    time.sleep(1)
                    status_text.empty()
                    progress_bar.empty()
                    
                    # SUCCESS MESSAGE - Madison Style
                    st.markdown(
                        f'<div class="success-banner">✨ Madison analyzed {len(all_results)} articles successfully!</div>',
                        unsafe_allow_html=True
                    )
                    
                    # Parse and flatten data
                    parsed_data = []
                    for article in all_results:
                        ai_analysis = article.get('ai_analysis', {})
                        sentiment_obj = ai_analysis.get('sentiment', {})
                        archetype_obj = ai_analysis.get('archetype', {})
                        insights = ai_analysis.get('insights', [])
                        
                        parsed_data.append({
                            'title': article.get('title', 'N/A'),
                            'link': article.get('link', ''),
                            'source': article.get('source', 'N/A'),
                            'published_at': article.get('published_at', ''),
                            'summary': article.get('summary', '')[:200] + '...',
                            'sentiment': sentiment_obj.get('classification', 'neutral'),
                            'confidence': sentiment_obj.get('confidence', 0),
                            'sentiment_reasoning': sentiment_obj.get('reasoning', ''),
                            'archetype': archetype_obj.get('primary', 'Unknown'),
                            'archetype_reasoning': archetype_obj.get('reasoning', ''),
                            'insight_category': insights[0].get('category', 'N/A') if insights else 'N/A',
                            'insight': insights[0].get('insight', 'N/A') if insights else 'N/A',
                            'recommendation': insights[0].get('recommendation', 'N/A') if insights else 'N/A'
                        })
                    
                    # Calculate metrics
                    sentiments = Counter([d['sentiment'] for d in parsed_data])
                    archetypes = Counter([d['archetype'] for d in parsed_data])
                    avg_confidence = sum([d['confidence'] for d in parsed_data]) / len(parsed_data)
                    
                    # KEY METRICS - Madison Style
                    st.markdown("### 📊 Key Metrics")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown("""
                        <div class="metric-box">
                            <div class="metric-label">Total Articles</div>
                            <div class="metric-value">{}</div>
                        </div>
                        """.format(len(parsed_data)), unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div class="metric-box" style="border-left: 4px solid #28a745;">
                            <div class="metric-label">Positive Sentiment</div>
                            <div class="metric-value">{}</div>
                        </div>
                        """.format(sentiments.get('positive', 0)), unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown("""
                        <div class="metric-box" style="border-left: 4px solid #ffc107;">
                            <div class="metric-label">Neutral Sentiment</div>
                            <div class="metric-value">{}</div>
                        </div>
                        """.format(sentiments.get('neutral', 0)), unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown("""
                        <div class="metric-box" style="border-left: 4px solid #dc3545;">
                            <div class="metric-label">Avg Confidence</div>
                            <div class="metric-value">{:.0f}%</div>
                        </div>
                        """.format(avg_confidence * 100), unsafe_allow_html=True)
                    
                    # VISUALIZATIONS
                    st.markdown("---")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 🎭 Brand Archetype Distribution")
                        archetype_df = pd.DataFrame(
                            list(archetypes.items()),
                            columns=['Archetype', 'Count']
                        ).sort_values('Count', ascending=False)
                        st.bar_chart(archetype_df.set_index('Archetype'))
                    
                    with col2:
                        st.markdown("### 💭 Sentiment Breakdown")
                        sentiment_df = pd.DataFrame(
                            list(sentiments.items()),
                            columns=['Sentiment', 'Count']
                        )
                        st.bar_chart(sentiment_df.set_index('Sentiment'))
                    
                    # INSIGHTS OVERVIEW TABLE
                    st.markdown("---")
                    st.markdown("### 📝 Article Insights Overview")
                    
                    df = pd.DataFrame(parsed_data)
                    display_df = pd.DataFrame({
                        'Title': df['title'].apply(lambda x: x[:60] + '...' if len(x) > 60 else x),
                        'Source': df['source'].str.replace('_', ' ').str.title(),
                        'Sentiment': df['sentiment'].str.capitalize(),
                        'Confidence': df['confidence'].apply(lambda x: f"{x:.0%}"),
                        'Archetype': df['archetype'],
                        'Insight': df['insight'].apply(lambda x: x[:80] + '...' if len(x) > 80 else x),
                    })
                    
                    st.dataframe(
                        display_df,
                        column_config={
                            "Title": st.column_config.TextColumn("Article Title", width="large"),
                            "Source": st.column_config.TextColumn("Source", width="small"),
                            "Sentiment": st.column_config.TextColumn("Sentiment", width="small"),
                            "Confidence": st.column_config.TextColumn("Confidence", width="small"),
                            "Archetype": st.column_config.TextColumn("Archetype", width="small"),
                            "Insight": st.column_config.TextColumn("Key Insight", width="large"),
                        },
                        hide_index=True,
                        use_container_width=True,
                        height=400
                    )
                    
                    # DEEP DIVE SECTION
                    st.markdown("---")
                    st.markdown("### 🔍 Deep Dive Analysis")
                    
                    for idx, item in enumerate(parsed_data[:10]):
                        with st.expander(f"📄 {item['title'][:100]}..."):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.markdown(f"**🔗 Source:** {item['source'].replace('_', ' ').title()}")
                                st.markdown(f"**📅 Published:** {item['published_at'][:10] if item['published_at'] else 'N/A'}")
                                st.markdown(f"**🔗 [Read Full Article]({item['link']})**")
                                
                                st.markdown("**📝 Summary:**")
                                st.info(item['summary'])
                            
                            with col2:
                                sentiment_badge_class = f"{item['sentiment']}-badge"
                                st.markdown(f"**💭 Sentiment**")
                                st.markdown(f'<span class="{sentiment_badge_class}">{item["sentiment"].upper()}</span>', unsafe_allow_html=True)
                                st.progress(item['confidence'])
                                st.caption(f"Confidence: {item['confidence']:.0%}")
                                
                                st.markdown("**🎭 Archetype**")
                                st.markdown(f"**{item['archetype']}**")
                            
                            st.markdown("---")
                            
                            st.markdown("**🧠 Sentiment Reasoning:**")
                            st.write(item['sentiment_reasoning'])
                            
                            st.markdown("**🎯 Archetype Reasoning:**")
                            st.write(item['archetype_reasoning'])
                            
                            st.markdown("**💡 Strategic Insight:**")
                            st.markdown(f'<div class="insight-card"><strong>{item["insight_category"].replace("_", " ").title()}:</strong> {item["insight"]}</div>', unsafe_allow_html=True)
                            
                            st.markdown("**✅ Recommendation:**")
                            st.success(item['recommendation'])
                    
                    # DOWNLOAD OPTIONS
                    st.markdown("---")
                    st.markdown("### 💾 Export Data")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        json_data = json.dumps(all_results, indent=2)
                        st.download_button(
                            label="📥 Download Full JSON Dataset",
                            data=json_data,
                            file_name=f"brand_intelligence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                    
                    with col2:
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
    <p><strong>Brand Intelligence Pipeline</strong> - AI-Powered Competitive Analysis</p>
    <p>Built with Streamlit + n8n + OpenAI GPT-4o-mini | Assignment 5 - INFO7375 Branding & AI</p>
    <p>Shareena Mycline | Northeastern University | Spring 2026</p>
</div>
""", unsafe_allow_html=True)
