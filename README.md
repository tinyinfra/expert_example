# Expert Example

A simple MCP (Model Context Protocol) server for testing the AI Suite expert registry.

## Tools

This expert provides three simple tools:

- **echo** - Echo back the input message
- **add** - Add two numbers together
- **get_time** - Get the current time

## Installation

This expert is installed automatically via the AI Suite registry.

For manual testing:

```bash
# Install with uv
uv sync

# Run the server
uv run expert-example
```

## Usage

Add the AI Suite registry source, then install and enable this expert from the Settings panel.
