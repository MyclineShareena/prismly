# n8n Webhook Setup Guide

## Overview
This guide shows how to modify your Assignment 4 n8n workflow to work with the Streamlit interface via webhook.

## Step 1: Modify n8n Workflow

### 1. Open your existing workflow
- Go to your n8n instance
- Open "Assignment 4 - Brand Intelligence Pipeline" workflow

### 2. Replace Manual Trigger with Webhook

**Delete:** Manual Trigger node

**Add:** Webhook node with these settings:
- **HTTP Method:** POST
- **Path:** `brand-intelligence`
- **Authentication:** None (or Header Auth for security)
- **Response Mode:** `Last Node`
- **Response Data:** `allEntries` 

### 3. Update RSS Feed Node

Your Streamlit app sends this JSON:
```json
{
  "feeds": [
    "https://azure.microsoft.com/en-us/blog/feed/",
    "https://openai.com/blog/rss.xml"
  ],
  "max_articles": 10
}
```

**Modify your RSS Feed Reader node(s):**
- Use `{{ $json.feeds }}` to loop through feed URLs
- Use `{{ $json.max_articles }}` to limit articles

**Option A: Loop over feeds**
1. Add "Split In Batches" node after Webhook
   - Batch Size: 1
   - Input: `{{ $json.feeds }}`
   
2. In RSS Feed Reader:
   - URL: `{{ $input.item }}`
   - Max Items: `{{ $node["Webhook"].json.max_articles }}`

**Option B: Multiple RSS nodes (simpler)**
1. Keep 5 separate RSS Feed Reader nodes
2. Each reads from Streamlit's feed array:
   - Feed 1: `{{ $json.feeds[0] }}`
   - Feed 2: `{{ $json.feeds[1] }}`
   - Feed 3: `{{ $json.feeds[2] }}`
   - Feed 4: `{{ $json.feeds[3] }}`
   - Feed 5: `{{ $json.feeds[4] }}`

### 4. Update Output Format

Your OpenAI node should already return JSON like:
```json
{
  "title": "Article Title",
  "link": "https://...",
  "source": "feed URL",
  "sentiment": "positive",
  "confidence": 0.95,
  "archetype": "Hero",
  "insight": "Key insight here",
  "recommendation": "Action item here"
}
```

**Ensure final output node:**
- Merges all analyzed articles into single array
- Uses "Merge" node or "Aggregate" node
- Output format: Array of article objects

### 5. Deploy Workflow

1. Click "Save" in n8n
2. **Activate the workflow** (toggle switch in top-right)
3. Copy your webhook URL:
   ```
   https://your-n8n-instance.com/webhook/brand-intelligence
   ```
   OR if n8n Cloud:
   ```
   https://your-workspace.app.n8n.cloud/webhook/brand-intelligence
   ```

---

## Step 2: Get Webhook URL

After saving, n8n shows your webhook URL. It looks like:
- **Self-hosted:** `https://your-domain.com/webhook/brand-intelligence`
- **n8n Cloud:** `https://your-name.app.n8n.cloud/webhook/brand-intelligence`

**Copy this URL** - you'll need it for Streamlit!

---

## Step 3: Test Webhook

Test with curl or Postman:

```bash
curl -X POST https://your-n8n-instance.com/webhook/brand-intelligence \
  -H "Content-Type: application/json" \
  -d '{
    "feeds": ["https://azure.microsoft.com/en-us/blog/feed/"],
    "max_articles": 2
  }'
```

Expected response: Array of analyzed articles

---

## Step 4: Add to Streamlit

1. **Deploy version:** Add webhook URL to Streamlit Cloud Secrets:
   ```toml
   N8N_WEBHOOK_URL = "https://your-n8n-instance.com/webhook/brand-intelligence"
   ```

2. **Local testing:** Enter webhook URL in sidebar when running app

---

## Step 5: Update Streamlit Secrets

In Streamlit Cloud dashboard → Your app → Settings → Secrets:

```toml
N8N_WEBHOOK_URL = "https://your-n8n-instance.com/webhook/brand-intelligence"
OPENAI_API_KEY = "sk-your-key-here"
```

(OpenAI key still needed for n8n workflow to use)

---

## Workflow Diagram

```
User enters feeds in Streamlit
    ↓
Streamlit sends POST to n8n webhook
    ↓
n8n Webhook receives feed URLs
    ↓
n8n parses RSS feeds
    ↓
n8n analyzes each article with OpenAI
    ↓
n8n returns JSON array of results
    ↓
Streamlit displays results
```

---

## Troubleshooting

### Webhook not responding
- Check workflow is **activated** (toggle in n8n)
- Verify webhook path matches
- Check n8n logs for errors

### Timeout errors
- Reduce max_articles in Streamlit
- Increase timeout in Streamlit code (currently 300 seconds)
- Check n8n execution time in workflow history

### Missing results
- Verify n8n output node returns array
- Check JSON structure matches expected format
- Test webhook directly with curl

---

## Benefits of n8n Webhook Approach

✅ **Reuses existing workflow** - No code duplication  
✅ **Centralized logic** - Update once in n8n, affects all interfaces  
✅ **Better scaling** - n8n handles heavy RSS/OpenAI work  
✅ **Easier debugging** - See execution logs in n8n  
✅ **API key security** - API key stays in n8n, not exposed to users  

---

## Optional: Add Security

Add Header Auth to webhook:

1. In n8n Webhook node:
   - Authentication: Header Auth
   - Name: `X-API-Key`
   - Value: `your-secret-key-123`

2. In Streamlit `call_n8n_webhook()`:
   ```python
   headers = {"X-API-Key": "your-secret-key-123"}
   response = requests.post(webhook_url, json=payload, headers=headers)
   ```

---

**Once setup is complete, your Streamlit app will leverage your proven n8n workflow!**
