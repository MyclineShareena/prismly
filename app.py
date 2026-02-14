import streamlit as st
import feedparser
import openai
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
    1. **Enter your OpenAI API key** in the sidebar (required for analysis)
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

# API Key input (in sidebar)
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔑 OpenAI API Key")
    api_key = st.text_input(
        "Enter your API key:",
        type="password",
        placeholder="sk-...",
        help="Get your API key from https://platform.openai.com/api-keys"
    )

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

# Analysis function
def analyze_article(title, content, link, api_key):
    """Analyze a single article using GPT-4o-mini"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        prompt = f"""Analyze this article for brand intelligence:

Title: {title}
Content: {content[:1000]}

Provide analysis in JSON format:
{{
    "sentiment": "positive" or "neutral" or "negative",
    "confidence": 0.0-1.0,
    "archetype": "Hero" or "Sage" or "Innocent" or "Explorer" or "Rebel",
    "key_insight": "One strategic insight about market trend or brand positioning",
    "recommendation": "One actionable brand strategy recommendation"
}}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )
        
        result = response.choices[0].message.content.strip()
        
        # Parse JSON (handle markdown code blocks)
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        
        analysis = json.loads(result.strip())
        
        return {
            "title": title,
            "link": link,
            "sentiment": analysis.get("sentiment", "unknown"),
            "confidence": analysis.get("confidence", 0),
            "archetype": analysis.get("archetype", "Unknown"),
            "insight": analysis.get("key_insight", ""),
            "recommendation": analysis.get("recommendation", "")
        }
    
    except Exception as e:
        st.error(f"Error analyzing article: {str(e)}")
        return {
            "title": title,
            "link": link,
            "sentiment": "error",
            "confidence": 0,
            "archetype": "Unknown",
            "insight": f"Analysis failed: {str(e)}",
            "recommendation": "N/A"
        }

# Process feeds
if analyze_button:
    if not api_key:
        st.error("⚠️ Please enter your OpenAI API key in the sidebar!")
    else:
        feed_urls = [url.strip() for url in rss_feeds.split("\n") if url.strip()]
        
        if not feed_urls:
            st.error("⚠️ Please enter at least one RSS feed URL!")
        else:
            st.markdown("---")
            st.markdown("### 🔄 Processing Feeds...")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            all_results = []
            total_feeds = len(feed_urls)
            
            for idx, feed_url in enumerate(feed_urls):
                status_text.text(f"Fetching feed {idx+1}/{total_feeds}: {feed_url}")
                
                try:
                    # Parse RSS feed
                    feed = feedparser.parse(feed_url)
                    articles = feed.entries[:max_articles]
                    
                    st.info(f"📰 Found {len(articles)} articles from {feed_url}")
                    
                    # Analyze each article
                    for art_idx, article in enumerate(articles):
                        status_text.text(f"Analyzing article {art_idx+1}/{len(articles)} from feed {idx+1}/{total_feeds}")
                        
                        title = article.get('title', 'No title')
                        link = article.get('link', '')
                        content = article.get('summary', article.get('description', ''))
                        
                        result = analyze_article(title, content, link, api_key)
                        result['source'] = feed_url
                        all_results.append(result)
                        
                        # Update progress
                        progress = (idx * max_articles + art_idx + 1) / (total_feeds * max_articles)
                        progress_bar.progress(min(progress, 1.0))
                        
                        # Rate limiting
                        time.sleep(0.5)
                
                except Exception as e:
                    st.warning(f"⚠️ Failed to process feed {feed_url}: {str(e)}")
            
            progress_bar.progress(1.0)
            status_text.text("✅ Analysis complete!")
            
            # Display results
            if all_results:
                st.markdown("---")
                st.markdown("### 📊 Analysis Results")
                
                # Summary metrics
                total = len(all_results)
                positive = sum(1 for r in all_results if r['sentiment'] == 'positive')
                neutral = sum(1 for r in all_results if r['sentiment'] == 'neutral')
                negative = sum(1 for r in all_results if r['sentiment'] == 'negative')
                
                # Archetype counts
                archetypes = {}
                for r in all_results:
                    arch = r['archetype']
                    archetypes[arch] = archetypes.get(arch, 0) + 1
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h1>{total}</h1>
                        <p>Total Articles</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card positive">
                        <h1>{positive}</h1>
                        <p>Positive</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card neutral">
                        <h1>{neutral}</h1>
                        <p>Neutral</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="metric-card negative">
                        <h1>{negative}</h1>
                        <p>Negative</p>
                    </div>
                    """, unsafe_allow_html=True)
                
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
