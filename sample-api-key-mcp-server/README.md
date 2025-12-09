# MCP Test Server with API Key Authentication

This is a simple MCP (Model Context Protocol) server designed to test Langdock's MCP integration with **API Key authentication** using the **"Authorization: Token"** header format.

## Purpose

This server was created to reproduce and debug issues with:
- Shared MCP connections in Langdock
- API Key authentication (Authorization: Token)
- Action confirmation flows

## Quick Start

### 1. Install Dependencies

```bash
cd mcp-server
pip install -r requirements.txt
```

### 2. Run the Server Locally

```bash
# Default API key: test-api-key-12345
python server.py
```

Or with a custom API key:

```bash
MCP_API_KEY="your-secret-key" python server.py
```

The server runs on `http://localhost:8000` by default.

### 3. Expose to Internet (for Langdock Testing)

Since Langdock needs to reach your MCP server, you need to expose it to the internet. Use ngrok:

```bash
# Install ngrok: https://ngrok.com/download
ngrok http 8000
```

This gives you a public URL like `https://abc123.ngrok.io` that you can use in Langdock.

## Langdock Configuration

### Step 1: Create MCP Integration

1. Go to **Settings → Integrations** in Langdock
2. Click **"Create Integration"** or **"Add MCP Server"**
3. Enter your server URL: `https://your-ngrok-url.ngrok.io/mcp`

### Step 2: Authentication Method

Select these settings (matching the customer's setup):
- **Authentication Method**: `API Key`
- **API Key Header Type**: `Authorization: Token`
- **API Key**: `test-api-key-12345` (or your custom key)

### Step 3: Test the Connection

The server provides these tools:
- `get_current_time` - Returns current date/time
- `echo_message` - Echoes back a message
- `calculate` - Basic arithmetic (add, subtract, multiply, divide)
- `slow_operation` - Waits for specified seconds (for timeout testing)

## Available Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/mcp` | POST | Yes | Main MCP protocol endpoint |
| `/health` | GET | No | Health check |
| `/info` | GET | Yes | Server info |

## Testing with cURL

### Test Health Check (no auth)
```bash
curl http://localhost:8000/health
```

### Test MCP Initialize (with auth)
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Token test-api-key-12345" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
```

### List Available Tools
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Token test-api-key-12345" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

### Call a Tool (echo_message)
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Token test-api-key-12345" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"echo_message","arguments":{"message":"Hello from MCP!"}}}'
```

### Call a Tool (calculate)
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Token test-api-key-12345" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"calculate","arguments":{"operation":"multiply","a":6,"b":7}}}'
```

## Reproducing the Bug

Based on the customer ticket (Merck - Ticket #13578):

**Bug Description:** 
When using MCP with a shared connection, the action confirmation dialog appears but doesn't wait for user response - it fails immediately.

**Steps to Reproduce:**

1. Set up this MCP server and connect it to Langdock
2. Create a connection and **share it with other users** (as admin)
3. Create an assistant that uses this MCP integration
4. **Disable confirmation** in the assistant's action settings
5. Have a user (who has the shared connection) try to use the assistant
6. Observe: The confirmation prompt appears but fails without waiting

**Key Variables:**
- Authentication: API Key with "Authorization: Token" header
- Connection type: Shared (not personal)
- Confirmation setting: Disabled

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_API_KEY` | `test-api-key-12345` | The API key clients must provide |
| `PORT` | `8000` | Port the server runs on |

## Logs

The server logs all incoming requests and authentication attempts, which is useful for debugging:

```
INFO:     API key verified successfully
INFO:     Received MCP request: {...}
INFO:     Processing method: tools/call
INFO:     Executing tool: echo_message with arguments: {"message": "test"}
```

