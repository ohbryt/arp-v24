# BioContext MCP Integration Setup Guide

## Overview

BioContext provides MCP (Model Context Protocol) servers for major biological databases. This integration enhances ARP v24 with direct access to:

- PubChem (compound data)
- ChEMBL (bioactivities)
- UniProt (protein information)
- PubMed (literature)
- AlphaFold (protein structures)
- OpenTargets (drug-target evidence)

## Installation

### Option 1: Direct API Integration (Recommended for now)

```bash
# Install required packages
pip install requests

# The integration uses direct API calls as fallback
# In production, would use actual MCP client
```

### Option 2: Full MCP Server Setup

```bash
# Install uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone BioContext repositories
git clone https://github.com/BioContext/PubChem-MCP.git
git clone https://github.com/BioContext/ChemBL-MCP.git
git clone https://github.com/BioContext/UniProt-MCP.git

# Setup PubChem MCP
cd PubChem-MCP
uv venv
source .venv/bin/activate
pip install -r requirements.txt

# Setup ChEMBL MCP
cd ../ChemBL-MCP
uv venv
source .venv/bin/activate
pip install -r requirements.txt

# Setup UniProt MCP
cd ../UniProt-MCP
uv venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pubchem": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "PYTHONPATH": "/path/to/PubChem-MCP"
      }
    },
    "chembl": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "PYTHONPATH": "/path/to/ChemBL-MCP"
      }
    },
    "uniprot": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "PYTHONPATH": "/path/to/UniProt-MCP"
      }
    }
  }
}
```

## ARP Integration Usage

### 1. Target Validation

```python
from integration.biocontext_mcp import BioContextIntegration

biocontext = BioContextIntegration()

# Validate target using UniProt
target_info = biocontext.validate_target("P00746", "protein")
print(f"Target validation: {target_info}")
```

### 2. Compound Screening

```python
# Screen compounds against target
candidates = ["aspirin", "ibuprofen", "warfarin"]
screening_results = biocontext.screen_compounds("P00746", candidates)
```

### 3. Property Lookup

```python
# Get compound properties
properties = biocontext.get_compound_properties("resveratrol")
```

### 4. Literature Search

```python
# Search PubMed for literature
papers = biocontext.literature_search("sarcopenia treatment", limit=10)
```

## Benefits for ARP

### Enhanced Data Access
- Real-time database queries during pipeline execution
- Structured data formats for easy processing
- No manual API key management needed

### Improved Target Discovery
- UniProt for target validation
- OpenTargets for evidence-based prioritization
- PubMed for literature mining

### Better Compound Screening
- PubChem for compound property lookup
- ChEMBL for bioactivity data
- AlphaFold for structure-based design

## Example ARP Workflow

```python
from integration.biocontext_mcp import BioContextIntegration

# Initialize integration
biocontext = BioContextIntegration()

# 1. Target identification
target_info = biocontext.validate_target("MSTN", "gene")

# 2. Compound screening
candidates = ["embelin", "curcumin", "resveratrol"]
screening = biocontext.screen_compounds("MSTN", candidates)

# 3. Property analysis
properties = {}
for candidate in candidates:
    properties[candidate] = biocontext.get_compound_properties(candidate)

# 4. Literature mining
literature = biocontext.literature_search("MSTN inhibition sarcopenia")

# 5. Generate report
arp_report = {
    'target_validation': target_info,
    'compound_screening': screening,
    'compound_properties': properties,
    'literature': literature
}
```

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Check MCP server is running
   - Verify configuration file syntax
   - Ensure proper permissions

2. **API Rate Limits**
   - Implement caching
   - Use exponential backoff
   - Consider premium API access

3. **Data Format Issues**
   - Validate JSON responses
   - Handle missing fields
   - Implement data transformation

### Performance Tips

- Cache frequently accessed data
- Use async requests for parallel queries
- Implement data validation and sanitization

## Future Enhancements

1. **Full MCP Integration**: Replace API calls with actual MCP client
2. **Additional Servers**: Integrate all BioContext servers
3. **Advanced Features**: Add similarity search, structure-based queries
4. **Caching Layer**: Implement Redis for performance optimization

## References

- BioContext GitHub: https://github.com/BioContext
- MCP Specification: https://modelcontextprotocol.io
- ARP Documentation: /Users/ocm/.openclaw/workspace/arp-v24/README.md
