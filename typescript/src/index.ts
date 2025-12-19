import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "expert-example-ts", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "add",
      description: "Add two numbers together",
      inputSchema: {
        type: "object",
        properties: {
          a: { type: "number", description: "First number" },
          b: { type: "number", description: "Second number" },
        },
        required: ["a", "b"],
      },
    },
    {
      name: "echo",
      description: "Echo back the input message",
      inputSchema: {
        type: "object",
        properties: {
          message: { type: "string", description: "Message to echo" },
        },
        required: ["message"],
      },
    },
    {
      name: "delay",
      description: "Wait for a specified number of seconds",
      inputSchema: {
        type: "object",
        properties: {
          seconds: { type: "number", description: "Seconds to wait" },
        },
        required: ["seconds"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "add": {
      const a = args?.a as number;
      const b = args?.b as number;
      return { content: [{ type: "text", text: String(a + b) }] };
    }
    case "echo": {
      const message = args?.message as string;
      return { content: [{ type: "text", text: message }] };
    }
    case "delay": {
      const seconds = args?.seconds as number;
      await new Promise((r) => setTimeout(r, seconds * 1000));
      return { content: [{ type: "text", text: `Delayed ${seconds} seconds` }] };
    }
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
