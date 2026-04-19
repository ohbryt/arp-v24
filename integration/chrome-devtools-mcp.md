# Chrome DevTools MCP Integration

**GitHub:** https://github.com/ChromeDevTools/chrome-devtools-mcp

Chrome DevTools MCP lets coding agents control a live Chrome browser for automation, debugging, and performance analysis.

## Installation

```bash
npm install chrome-devtools-mcp
```

## OpenClaw MCP Configuration

Add to your OpenClaw config (`~/.openclaw/openclaw.json`):

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

## Usage in ARP

### 1. Web Scraping for Literature

```javascript
// Example: Scrape PubMed search results
const chrome = await chromeDevtoolsMCP.openBrowser();
await chrome.navigate('https://pubmed.ncbi.nlm.nih.gov/?term=PHGDH+cancer+2024');
const articles = await chrome.getElements('.results-list article');
const data = articles.map(a => ({
  title: a.find('.title').text(),
  pmid: a.find('.pmid').text(),
  date: a.find('.date').text()
}));
await chrome.screenshot('pubmed_search.png');
```

### 2. ClinicalTrials.gov Automation

```javascript
// Search for PHGDH inhibitors in clinical trials
await chrome.navigate('https://clinicaltrials.gov/search?term=PHGDH+inhibitor');
const trials = await chrome.getElements('.results-section .trial-card');
```

### 3. Performance Metrics for Web Apps

```javascript
// Get Core Web Vitals for a biomedical web app
const metrics = await chrome.getPerformanceMetrics({
  url: 'https://pubmed.ncbi.nlm.nih.gov',
  metrics: ['LCP', 'FID', 'CLS', 'INP']
});
```

### 4. Network Request Analysis

```javascript
// Analyze API calls during literature fetch
await chrome.startNetworkRecording();
await chrome.navigate('https://pubmed.ncbi.nlm.nih.gov/api/');
const requests = await chrome.getNetworkRequests({
  pattern: /\/esearch|\/efetch|clinicaltrials\.gov/
});
```

## Tools Available

| Tool | Description |
|------|-------------|
| `screenshot` | Take screenshot of current page |
| `get_elements` | Extract DOM elements by selector |
| `click` | Click element by selector |
| `type` | Type text into input field |
| `navigate` | Navigate to URL |
| `evaluate` | Execute JavaScript in page context |
| `get_console_messages` | Get browser console output |
| `get_network_requests` | Analyze network traffic |
| `get_performance_metrics` | Get Core Web Vitals |
| `record_trace` | Record performance trace |

## Integration with ARP Research Pipeline

### Literature Collection

```javascript
// Collect papers from multiple sources
async function collectLiterature(gene, disease) {
  const sources = [
    `https://pubmed.ncbi.nlm.nih.gov/?term=${gene}+${disease}`,
    `https://clinicaltrials.gov/search?term=${gene}+${disease}`,
    `https://www.cancer.gov/publications/pdq?term=${gene}`
  ];
  
  const results = [];
  for (const url of sources) {
    await chrome.navigate(url);
    await chrome.waitForSelector('.results-list');
    const data = await chrome.evaluate(extractResults);
    results.push(...data);
    await chrome.screenshot(`${gene}_${disease}_${index}.png`);
  }
  return results;
}
```

### Competition Analysis

```javascript
// Monitor competitor websites for new publications
async function monitorCompetitors(competitorUrls) {
  for (const url of competitorUrls) {
    await chrome.navigate(url);
    const newPapers = await chrome.evaluate(checkNewPapers);
    if (newPapers.length > 0) {
      console.log(`New papers from ${url}:`, newPapers);
      await chrome.screenshot(`new_papers_${Date.now()}.png`);
    }
  }
}
```

## Troubleshooting

### Chrome Not Starting

```bash
# Start Chrome with remote debugging
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

### Permission Issues on macOS

```bash
# If you get security warnings, you may need to allow Chrome DevTools
open /Applications/Google\ Chrome.app
```

## See Also

- [Chrome DevTools MCP GitHub](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Puppeteer Documentation](https://puppeteer.github.io/puppeteer/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)