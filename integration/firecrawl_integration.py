"""
ARP v24 - Firecrawl Web Agent Integration

Firecrawl: Open-source web data agent for structured web research.
GitHub: https://github.com/firecrawl/web-agent

Capabilities:
- Web search and scraping
- Browser automation (Interact tool)
- Autonomous research loops (plan-act-observe)
- Structured output

Installation:
    npm i -g firecrawl-cli
    firecrawl create agent -t library

Or use REST API directly (Python-friendly):
    https://docs.firecrawl.dev/api-reference/v2-introduction
"""

import os
import json
import subprocess
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


@dataclass
class FirecrawlResult:
    """Structured result from Firecrawl research."""
    success: bool
    data: Any
    sources: List[str]
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "sources": self.sources,
            "error": self.error,
        }


class FirecrawlClient:
    """
    Firecrawl REST API client for Python environments.
    
    For full agent capabilities, use the npm package:
        npx firecrawl-cli scrape <url>
        firecrawl create agent -t next
    
    This client provides Python-friendly access to Firecrawl's scraping capabilities.
    """
    
    # Firecrawl API base (get key from firecrawl.dev)
    BASE_URL = "https://api.firecrawl.dev/v0"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable required")
        self._client = httpx.Client(timeout=60.0)

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def scrape(self, url: str, parse: bool = True) -> FirecrawlResult:
        """
        Scrape a single URL with Firecrawl's AI-powered parsing.
        
        Args:
            url: URL to scrape
            parse: Use AI to extract structured data
        
        Returns:
            FirecrawlResult with scraped content
        """
        try:
            response = self._client.post(
                f"{self.BASE_URL}/scrape",
                headers=self._headers(),
                json={"url": url, "parse": parse},
            )
            response.raise_for_status()
            data = response.json()
            
            return FirecrawlResult(
                success=True,
                data=data.get("content", data),
                sources=[url],
            )
        except Exception as e:
            return FirecrawlResult(
                success=False,
                data=None,
                sources=[],
                error=str(e),
            )

    def search(self, query: str, limit: int = 10) -> FirecrawlResult:
        """
        Search the web using Firecrawl.
        
        Args:
            query: Search query
            limit: Max results
        
        Returns:
            FirecrawlResult with search results
        """
        try:
            response = self._client.post(
                f"{self.BASE_URL}/search",
                headers=self._headers(),
                json={"query": query, "limit": limit},
            )
            response.raise_for_status()
            data = response.json()
            
            results = data.get("results", [])
            sources = [r.get("url", "") for r in results]
            
            return FirecrawlResult(
                success=True,
                data=results,
                sources=sources,
            )
        except Exception as e:
            return FirecrawlResult(
                success=False,
                data=None,
                sources=[],
                error=str(e),
            )

    def crawl(self, url: str, limit: int = 10) -> FirecrawlResult:
        """
        Crawl a website starting from URL.
        
        Args:
            url: Starting URL
            limit: Max pages to crawl
        
        Returns:
            FirecrawlResult with crawled pages
        """
        try:
            response = self._client.post(
                f"{self.BASE_URL}/crawl",
                headers=self._headers(),
                json={"url": url, "limit": limit},
            )
            response.raise_for_status()
            data = response.json()
            
            return FirecrawlResult(
                success=True,
                data=data,
                sources=[url],
            )
        except Exception as e:
            return FirecrawlResult(
                success=False,
                data=None,
                sources=[],
                error=str(e),
            )


class FirecrawlAgent:
    """
    Full Firecrawl Agent for autonomous research.
    
    Uses npm firecrawl-cli for full agent capabilities:
    - Plan-act-observe loops
    - Browser automation
    - Subagent spawning
    
    Usage:
        agent = FirecrawlAgent()
        result = agent.run("Research PHGDH inhibitors in cancer treatment")
    """
    
    def __init__(self, model: str = "firecrawl"):
        self.model = model

    def run(self, task: str, output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Run Firecrawl agent on a research task.
        
        Requires npm firecrawl-cli installed:
            npm i -g firecrawl-cli
        
        Args:
            task: Research task description
            output_file: Optional file to save results
        
        Returns:
            Agent output dict
        """
        cmd = ["npx", "-y", "firecrawl-cli", "agent", "--task", task]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 min timeout
            )
            
            output = {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "task": task,
            }
            
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(output, f, indent=2)
            
            return output
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Timeout after 5 minutes",
                "task": task,
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "firecrawl-cli not installed. Run: npm i -g firecrawl-cli",
                "task": task,
            }


# Integration seam for ARP research pipeline
def research_topic(topic: str, max_sources: int = 5) -> Dict[str, Any]:
    """
    Use Firecrawl to research a biomedical topic.
    
    This is the main integration point for ARP.
    
    Args:
        topic: Research topic (e.g., "PHGDH inhibitors cancer 2024")
        max_sources: Max web sources to fetch
    
    Returns:
        Structured research results
    """
    if not HAS_HTTPX:
        return {
            "success": False,
            "error": "httpx required for Firecrawl",
            "topic": topic,
        }
    
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "FIRECRAWL_API_KEY not set",
            "topic": topic,
        }
    
    client = FirecrawlClient(api_key)
    
    # Search for relevant sources
    search_result = client.search(topic, limit=max_sources)
    
    if not search_result.success:
        return {
            "success": False,
            "error": search_result.error,
            "topic": topic,
        }
    
    # Scrape top sources
    scraped_content = []
    for url in search_result.sources[:max_sources]:
        scrape_result = client.scrape(url)
        if scrape_result.success:
            scraped_content.append({
                "url": url,
                "content": scrape_result.data,
            })
    
    return {
        "success": True,
        "topic": topic,
        "sources": search_result.sources[:max_sources],
        "content": scraped_content,
        "summary": f"Researched {len(scraped_content)} sources on '{topic}'",
    }


def main():
    """CLI demo of Firecrawl integration."""
    print("=" * 60)
    print("  Firecrawl Web Agent Integration")
    print("=" * 60)
    
    # Check API key
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print("\n⚠️  FIRECRAWL_API_KEY not set")
        print("   Get key at: https://firecrawl.dev")
        print("   Export: export FIRECRAWL_API_KEY=your_key_here")
        return
    
    # Demo search
    client = FirecrawlClient(api_key)
    
    print("\n🔍 Demo: Search 'PHGDH cancer metabolism'")
    result = client.search("PHGDH cancer metabolism 2024", limit=5)
    
    if result.success:
        print(f"\n   Found {len(result.data)} results")
        for i, r in enumerate(result.data[:3]):
            print(f"   {i+1}. {r.get('title', 'N/A')[:60]}")
            print(f"      {r.get('url', 'N/A')[:50]}...")
    else:
        print(f"\n   Error: {result.error}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()