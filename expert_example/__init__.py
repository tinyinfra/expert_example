"""
Expert Example - A simple MCP server for testing AI Suite registry.

Provides basic tools for demonstration and testing.
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Create server instance
server = Server("expert-example")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="echo",
            description="Echo back the input message",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to echo back"
                    }
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="get_time",
            description="Get the current time",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "echo":
        message = arguments.get("message", "")
        return [TextContent(type="text", text=f"Echo: {message}")]

    elif name == "add":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a + b
        return [TextContent(type="text", text=f"{a} + {b} = {result}")]

    elif name == "get_time":
        from datetime import datetime
        now = datetime.now().isoformat()
        return [TextContent(type="text", text=f"Current time: {now}")]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


def main():
    """Run the MCP server."""
    asyncio.run(run_server())


async def run_server():
    """Start the stdio server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    main()
