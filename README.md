[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/steimerbyte)

> ⭐ If you find this useful, consider [supporting me on Ko-fi](https://ko-fi.com/steimerbyte)!

<img src="https://raw.githubusercontent.com/steimbyte/bsearch-cli/master/assets/profile.jpg" alt="steimerbyte" style="border-radius: 8px; margin: 16px 0;"/>




# Perplexity MCP Server

This is a Model Context Protocol (MCP) server that integrates with the Perplexity AI API to provide web search capabilities.

## Prerequisites

- Python 3.10+
- A Perplexity API Key

## Installation

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set the `PERPLEXITY_API_KEY` environment variable.

```bash
export PERPLEXITY_API_KEY="your-api-key"
```

## Usage

Run the server using Python:

```bash
python server.py
```

This server communicates via Stdio, so it is designed to be run by an MCP client (like Claude Desktop or VSCode Extension).

### VSCode Configuration

Add the following to your VSCode MCP settings (usually in `settings.json` under `mcp.servers` or via the MCP extension config):

```json
{
  "perplexity": {
    "command": "python",
    "args": ["/path/to/perplexity-mcp-server/server.py"],
    "env": {
      "PERPLEXITY_API_KEY": "your-api-key"
    }
  }
}
```
