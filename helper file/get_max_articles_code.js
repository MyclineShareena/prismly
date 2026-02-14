// Enhanced "Get Max Articles" code for n8n Code node
// This checks multiple possible webhook payload locations

const input = $input.item.json;

// Log the full structure to see what we're actually receiving
console.log('=== WEBHOOK PAYLOAD DEBUG ===');
console.log('Full input:', JSON.stringify($input.item, null, 2));

let maxArticles = 10; // default fallback
let source = 'default';

// Try different possible locations where the data might be
if (input.max_articles !== undefined && input.max_articles !== null) {
  // Direct access: {max_articles: 5, feeds: [...]}
  maxArticles = Number(input.max_articles);
  source = 'direct (input.max_articles)';
} 
else if (input.body && input.body.max_articles !== undefined) {
  // Wrapped in body: {body: {max_articles: 5, feeds: [...]}}
  maxArticles = Number(input.body.max_articles);
  source = 'wrapped in body (input.body.max_articles)';
}
else if (input.bodyJson && input.bodyJson.max_articles !== undefined) {
  // Wrapped in bodyJson
  maxArticles = Number(input.bodyJson.max_articles);
  source = 'wrapped in bodyJson';
}
else if (input.query && input.query.max_articles !== undefined) {
  // From query parameters
  maxArticles = Number(input.query.max_articles);
  source = 'query parameters';
}
else if (typeof input === 'string') {
  // Sometimes webhook body comes as string that needs parsing
  try {
    const parsed = JSON.parse(input);
    if (parsed.max_articles !== undefined) {
      maxArticles = Number(parsed.max_articles);
      source = 'parsed from string';
    }
  } catch (e) {
    console.log('Failed to parse input as JSON');
  }
}

console.log('Extracted max_articles:', maxArticles, 'from source:', source);
console.log('=========================');

return [{
  json: {
    max_articles: maxArticles,
    source: source,
    debug_received: input
  }
}];
