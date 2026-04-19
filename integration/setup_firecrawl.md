# Firecrawl Web Agent Integration

**GitHub:** https://github.com/firecrawl/web-agent  
**Docs:** https://docs.firecrawl.dev

## What is Firecrawl?

Open-source web data agent optimized for structured web research. Powers autonomous research loops with:
- Web search and scraping
- Browser automation (Interact tool)
- Plan-act-observe loops
- Subagent spawning for parallel tasks

## Installation

### Option 1: npm package (full agent)
```bash
npm i -g firecrawl-cli
firecrawl create agent -t next  # Full Next.js app
firecrawl create agent -t library  # Library only
```

### Option 2: REST API (Python-friendly)
```bash
# Get API key from https://firecrawl.dev
export FIRECRAWL_API_KEY=your_key_here
```

## Usage

### Python Client (REST API)
```python
from integration.firecrawl_integration import FirecrawlClient, research_topic

# Direct API access
client = FirecrawlClient()
result = client.search("PHGDH cancer metabolism 2024", limit=5)
result = client.scrape("https://pubmed.ncbi.nlm.nih.gov/...")

# High-level research function
result = research_topic("PHGDH inhibitors cancer clinical trials")
```

### Full Agent (npm)
```python
from integration.firecrawl_integration import FirecrawlAgent

agent = FirecrawlAgent()
output = agent.run("Research PHGDH inhibitors in cancer treatment")
```

## ARP Integration Points

| Capability | ARP Use Case |
|-----------|-------------|
| Web Search | Latest papers, competition, clinical trials |
| Web Scraping | Extract data from pharma sites,PubMed, FDA |
| Browser Automation | Login-required sources, dynamic content |
| Autonomous Agent | End-to-end research tasks |

## Example: Research PHGDH Clinical Trials

```python
from integration.firecrawl_integration import research_topic

# Comprehensive research
result = research_topic(
    "PHGDH inhibitor clinical trial 2024 cancer",
    max_sources=10
)

print(result["summary"])
for source in result["content"]:
    print(f"  - {source['url']}")
```

## Environment Variables

- `FIRECRAWL_API_KEY` - API key from firecrawl.dev

## See Also

- [Firecrawl App](https://firecrawl.dev/app/agent) - Web-based agent UI
- [Firecrawl SDK](https://www.npmjs.com/package/@mendable/firecrawl-js) - npm package
- [Deep Agents](https://docs.langchain.com/oss/javascript/deepagents/overview) - The agent harness