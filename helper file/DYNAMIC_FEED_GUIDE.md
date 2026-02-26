# Dynamic Feed Configuration Guide

## What Changed?

Your Prismly pipeline is now **fully dynamic** — you can:
- ✅ Select preset feeds OR enter custom RSS feed URLs
- ✅ **Bring your own OpenAI API key** (no shared credentials!)
- ✅ No code changes needed for any configuration

---

## 🎯 Streamlit App Updates

### New Features:

1. **🔑 Dynamic API Key Input:**
   - Each user enters their own OpenAI API key
   - Secure password input field (masked)
   - No shared API keys = better security & cost control
   - Link to get API key: https://platform.openai.com/api-keys

2. **Feed Selection Modes:**
   - **Preset Feeds:** Choose from 5 curated AI/tech blog feeds
   - **Custom Feeds:** Enter any RSS feed URLs you want to analyze

3. **Custom Feed Input:**
   - Multi-line text area for entering RSS URLs
   - Automatic URL validation (must start with http:// or https://)
   - Real-time feedback on number of feeds loaded

### How to Use:

#### Step 1: Enter Your OpenAI API Key
1. Get your API key from: https://platform.openai.com/api-keys
2. Enter it in the "OpenAI API Key" field (sidebar)
3. Key is sent securely with each request (never stored)

#### Step 2a: Use Preset Feeds
1. Select "Preset Feeds" radio button
2. Choose feeds from the multiselect dropdown
3. Click "Analyze Brand"

#### Step 2b: Use Custom Feeds
1. Select "Custom Feeds" radio button
2. Enter RSS URLs in the text area (one per line)
3. Example:
   ```
   https://techcrunch.com/feed/
   https://www.theverge.com/rss/index.xml
   https://blog.google/feed/
   ```
4. Click "Analyze Brand"

---

## 🔧 n8n Workflow Updates

### New Dynamic Workflow Architecture:

**Old Workflow (Hardcoded):**
```
Webhook → 5 separate RSS nodes (always all 5) → AI with stored credential
```

**New Workflow (Dynamic):**
```
Webhook → Extract (feeds + API key) → Loop through feeds → Dynamic RSS → AI with user's key
```

### Key Changes:

1. **Extract Feeds & Settings Node:**
   - Reads `feeds` array from webhook payload
   - Reads `max_articles` setting
   - **Reads `openai_api_key` from user input**
   - Creates one item per feed URL with API key

2. **Single Dynamic RSS Feed Read Node:**
   - URL is set dynamically: `={{ $json.feed_url }}`
   - Processes only the feeds sent from Streamlit

3. **Dynamic OpenAI Authentication:**
   - No stored credentials in n8n
   - Authorization header: `Bearer {{ API_KEY }}`
   - Each request uses the user's provided key

4. **Automatic Source Naming:**
   - Detects feed source from URL
   - Falls back to domain name for custom feeds

---

## 📦 Installation Steps

### Step 1: Update Streamlit App

The `app.py` file has already been updated with dynamic feed support and API key input.

**Test it locally:**
```powershell
cd "C:\Users\Shari\...\brand-intelligence-pipeline"
streamlit run app.py
```

### Step 2: Import New n8n Workflow

1. **Open n8n** (https://brand-intelligence-n8n.onrender.com)

2. **Import the new workflow:**
   - Click "+" → "Import from File"
   - Select: `helper file/Johnpeterkennedy_Myclineshareena_A6_Workflow_Dynamic.json`

3. **NO Credentials Setup Needed! 🎉**
   - The new workflow does NOT require stored OpenAI credentials
   - Users provide their own API key through the Streamlit app
   - API key is passed dynamically with each request

4. **Activate the Workflow:**
   - Click "Active" toggle (top right)
   - Confirm webhook URL matches your app: `/webhook/brand-intelligence`

5. **Test the Workflow:**
   - Use Streamlit app or test with curl:
   ```bash
   curl -X POST https://brand-intelligence-n8n.onrender.com/webhook/brand-intelligence \
   -H "Content-Type: application/json" \
   -d '{
     "feeds": ["https://openai.com/blog/rss.xml"],
     "max_articles": 5,
     "openai_api_key": "sk-your-test-key"
   }'
   ```

---

## 🔐 Security Benefits

### Why Dynamic API Keys Are Better:

1. **No Shared Credentials:**
   - Each user uses their own OpenAI account
   - No risk of exceeding shared quota
   - Individual cost control

2. **Better Security:**
   - API key never stored in n8n or Streamlit
   - Transmitted securely in HTTPS requests only
   - No credential management needed

3. **Fair Usage:**
   - Users pay for their own API calls
   - No surprise bills on your account
   - Transparent cost allocation

4. **Easier Deployment:**
   - No need to configure n8n credentials
   - No secret management in Render
   - Users bring their own keys

---

## 🧪 Testing Guide

### Test 1: Preset Feeds
1. Open Streamlit app
2. Select "Preset Feeds"
3. Choose 2-3 feeds from dropdown
4. Set max articles to 5
5. Click "Analyze Brand"
6. **Expected:** Only selected feeds should be analyzed

### Test 2: Custom Feeds
1. Select "Custom Feeds"
2. Enter these URLs:
   ```
   https://blog.google/technology/ai/rss/
   https://openai.com/blog/rss.xml
   ```
3. Set max articles to 5
4. Click "Analyze Brand"
5. **Expected:** Only these 2 custom feeds analyzed

### Test 3: Mixed Content
1. Try different RSS feeds (tech blogs, news sites, etc.)
2. Verify AI analysis works for various content types

---

## 🔍 Troubleshooting

### Issue: "Please enter your OpenAI API key"
**Solution:**
1. Get API key from https://platform.openai.com/api-keys
2. Copy the key starting with "sk-..."
3. Paste into the "OpenAI API Key" field in Streamlit sidebar
4. Make sure you have credits in your OpenAI account

### Issue: "Invalid API key" or "401 Unauthorized"
**Solution:**
- Verify your API key is correct (starts with sk-)
- Check your OpenAI account has available credits
- Make sure the key hasn't been revoked
- Try generating a new API key

### Issue: "No valid URLs found"
**Solution:** Make sure URLs:
- Start with `http://` or `https://`
- Are on separate lines
- Are valid RSS feed URLs

### Issue: "No results returned from n8n"
**Solutions:**
1. Check n8n workflow is Active
2. Check n8n execution logs for errors
3. Verify API key was sent correctly
4. Test one feed at a time to isolate issues

### Issue: Some feeds fail
**Solution:** 
- RSS Feed Read node has `onError: continueRegularOutput`
- Failed feeds are skipped automatically
- Check n8n logs to see which feeds failed and why

### Issue: Different sentiment/archetypes now
**Solution:**
- This is expected! The new prompt is more dynamic
- AI now analyzes actual content instead of using hardcoded examples
- Results should vary based on article content

### Issue: High OpenAI costs
**Solution:**
- Reduce "Posts to Fetch" slider (fewer articles = lower cost)
- Select fewer RSS feeds
- Use GPT-3.5-turbo instead of GPT-4 (modify model in n8n if needed)
- Monitor usage at https://platform.openai.com/usage

---

## 🎓 Benefits of Dynamic Architecture

### 1. **Flexibility**
- Analyze ANY RSS feed without code changes
- Test competitor blogs, industry news, etc.
- Each user brings their own API key

### 2. **Scalability**
- Add/remove feeds on the fly
- No workflow redeployment needed
- Support unlimited users

### 3. **Cost Efficiency**
- Only process selected feeds (save API costs)
- Only fetch articles you actually need
- Users pay for their own OpenAI usage

### 4. **Better Analysis**
- Improved AI prompt gives varied, accurate results
- Source detection works for custom feeds
- Real-time analysis with user's own quota

### 5. **Security & Privacy**
- No shared API credentials
- API keys never stored
- Each user controls their own usage

---

## 📊 Comparison: Old vs New

| Feature | Old (Hardcoded) | New (Dynamic) |
|---------|----------------|---------------|
| **Feed Selection** | Hardcoded 5 feeds | Any RSS feeds |
| **Custom Feeds** | Requires code change | Text input, no code |
| **n8n Workflow** | 5 separate RSS nodes | 1 dynamic RSS node |
| **Feed Processing** | Always all 5 | Only selected |
| **OpenAI API Key** | Stored in n8n | User-provided (BYOK) |
| **Cost Management** | Shared account | Per-user billing |
| **Security** | Shared credential risk | No stored credentials |
| **Source Detection** | Manual mapping | Automatic |
| **AI Prompt** | Hardcoded examples | Dynamic analysis |
| **Scalability** | Limited to 5 | Unlimited |
| **User Quota** | Shared quota issues | Individual quotas |

---

## 🚀 Next Steps

1. ✅ Test with preset feeds
2. ✅ Test with custom feeds
3. ✅ Verify AI analysis quality
4. ✅ Deploy to production (git push)
5. ✅ Update README with new features

---

## 💡 Example Custom Feed Lists

### Tech News:
```
https://techcrunch.com/feed/
https://www.theverge.com/rss/index.xml
https://arstechnica.com/feed/
```

### AI/ML Research:
```
https://openai.com/blog/rss.xml
https://blog.google/technology/ai/rss/
https://www.deepmind.com/blog/rss.xml
```

### Developer Blogs:
```
https://github.blog/feed/
https://stackoverflow.blog/feed/
https://devblogs.microsoft.com/feed/
```

---

**Questions?** Check n8n execution logs or Streamlit error messages for detailed debugging info.
