import asyncio
import os
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# Initialize server
server = Server("perplexity-server")

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="perplexity_search",
            description="Search the web using Perplexity AI. Use this tool for up-to-date information.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "model": {
                        "type": "string",
                        "description": "Perplexity model to use (default: sonar-pro)",
                        "default": "sonar-pro"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name != "perplexity_search":
        raise ValueError(f"Unknown tool: {name}")

    if not arguments:
        raise ValueError("Missing arguments")

    if not PERPLEXITY_API_KEY:
        return [
            types.TextContent(
                type="text",
                text="Error: PERPLEXITY_API_KEY environment variable is not set."
            )
        ]

    query = arguments.get("query")
    if not query:
        raise ValueError("Missing query argument")
    
    model = arguments.get("model", "sonar-pro")

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(PERPLEXITY_URL, json=payload, headers=headers, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            
            # Extract content from Perplexity response
            # Format: {"choices": [{"message": {"content": "..."}}]}
            content = data["choices"][0]["message"]["content"]
            
            return [
                types.TextContent(
                    type="text",
                    text=content
                )
            ]
        except Exception as e:
            return [
                types.TextContent(
                    type="text",
                    text=f"Error querying Perplexity: {str(e)}"
                )
            ]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())

