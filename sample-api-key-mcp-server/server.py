"""
MCP Server with API Key Authentication (Authorization: Token)

This server is designed to test Langdock's MCP integration with shared connections.
It uses the "Authorization: Token" header format for authentication.

Run with: uvicorn server:app --host 0.0.0.0 --port 8000
"""

import os
import json
import logging
from typing import Any
from datetime import datetime

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The API key that clients must provide
# In production, use environment variables or a secrets manager
API_KEY = os.environ.get("MCP_API_KEY", "test-api-key-12345")

app = FastAPI(
    title="MCP Test Server",
    description="A simple MCP server for testing API Key authentication with shared connections",
    version="1.0.0"
)


# Authentication dependency
async def verify_api_key(request: Request):
    """
    Verifies the API key from the Authorization header.
    Expects format: "Authorization: Token <api-key>"
    """
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        logger.warning("Missing Authorization header")
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    # Parse "Token <key>" format
    parts = auth_header.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "token":
        logger.warning(f"Invalid Authorization format: {auth_header[:20]}...")
        raise HTTPException(
            status_code=401, 
            detail="Invalid Authorization format. Expected: Token <api-key>"
        )
    
    provided_key = parts[1]
    
    if provided_key != API_KEY:
        logger.warning("Invalid API key provided")
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    logger.info("API key verified successfully")
    return provided_key


# MCP Protocol Models
class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: int | str | None = None
    method: str
    params: dict | None = None


class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: int | str | None = None
    result: Any = None
    error: dict | None = None


# Tool definitions for the MCP server
TOOLS = [
    {
        "name": "get_current_time",
        "description": "Returns the current date and time",
        "inputSchema": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "Optional timezone (e.g., 'UTC', 'Europe/Berlin')"
                }
            },
            "required": []
        }
    },
    {
        "name": "echo_message",
        "description": "Echoes back the provided message. Useful for testing.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to echo back"
                }
            },
            "required": ["message"]
        }
    },
    {
        "name": "calculate",
        "description": "Performs basic arithmetic calculations",
        "inputSchema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The arithmetic operation to perform"
                },
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["operation", "a", "b"]
        }
    },
    {
        "name": "slow_operation",
        "description": "A deliberately slow operation for testing timeouts and loading states",
        "inputSchema": {
            "type": "object",
            "properties": {
                "delay_seconds": {
                    "type": "integer",
                    "description": "How many seconds to wait before responding (1-30)",
                    "minimum": 1,
                    "maximum": 30
                }
            },
            "required": ["delay_seconds"]
        }
    }
]


# Tool implementations
def execute_tool(tool_name: str, arguments: dict) -> dict:
    """Execute a tool and return the result."""
    
    if tool_name == "get_current_time":
        timezone = arguments.get("timezone", "UTC")
        current_time = datetime.now().isoformat()
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Current time ({timezone}): {current_time}"
                }
            ]
        }
    
    elif tool_name == "echo_message":
        message = arguments.get("message", "")
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Echo: {message}"
                }
            ]
        }
    
    elif tool_name == "calculate":
        operation = arguments.get("operation")
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return {
                    "content": [{"type": "text", "text": "Error: Division by zero"}],
                    "isError": True
                }
            result = a / b
        else:
            return {
                "content": [{"type": "text", "text": f"Unknown operation: {operation}"}],
                "isError": True
            }
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Result: {a} {operation} {b} = {result}"
                }
            ]
        }
    
    elif tool_name == "slow_operation":
        import time
        delay = min(max(arguments.get("delay_seconds", 5), 1), 30)
        time.sleep(delay)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Operation completed after {delay} seconds"
                }
            ]
        }
    
    else:
        return {
            "content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}],
            "isError": True
        }


# MCP Protocol handlers
def handle_initialize(params: dict) -> dict:
    """Handle the initialize request from MCP client."""
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {}
        },
        "serverInfo": {
            "name": "mcp-test-server",
            "version": "1.0.0"
        }
    }


def handle_tools_list(params: dict) -> dict:
    """Return the list of available tools."""
    return {"tools": TOOLS}


def handle_tools_call(params: dict) -> dict:
    """Execute a tool call."""
    tool_name = params.get("name")
    arguments = params.get("arguments", {})
    
    logger.info(f"Executing tool: {tool_name} with arguments: {arguments}")
    
    result = execute_tool(tool_name, arguments)
    return result


# Main MCP endpoint
@app.post("/mcp")
async def mcp_endpoint(request: Request, api_key: str = Depends(verify_api_key)):
    """
    Main MCP endpoint that handles JSON-RPC requests.
    Requires Authorization: Token <api-key> header.
    """
    try:
        body = await request.json()
        logger.info(f"Received MCP request: {json.dumps(body, indent=2)}")
    except Exception as e:
        logger.error(f"Failed to parse request body: {e}")
        return JSONResponse(
            status_code=400,
            content={
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"}
            }
        )
    
    # Handle batch requests
    if isinstance(body, list):
        responses = []
        for req in body:
            response = process_mcp_request(req)
            if response:
                responses.append(response)
        return JSONResponse(content=responses)
    
    # Handle single request
    response = process_mcp_request(body)
    if response:
        return JSONResponse(content=response)
    
    # For notifications (no id), return empty response
    return JSONResponse(content={})


def process_mcp_request(request_data: dict) -> dict | None:
    """Process a single MCP request and return the response."""
    method = request_data.get("method", "")
    params = request_data.get("params", {})
    request_id = request_data.get("id")
    
    logger.info(f"Processing method: {method}")
    
    try:
        if method == "initialize":
            result = handle_initialize(params)
        elif method == "notifications/initialized":
            # This is a notification, no response needed
            return None
        elif method == "tools/list":
            result = handle_tools_list(params)
        elif method == "tools/call":
            result = handle_tools_call(params)
        else:
            logger.warning(f"Unknown method: {method}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint (no auth required)."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# Info endpoint for debugging
@app.get("/info")
async def server_info(api_key: str = Depends(verify_api_key)):
    """Returns server info (requires auth)."""
    return {
        "server": "mcp-test-server",
        "version": "1.0.0",
        "tools": [t["name"] for t in TOOLS],
        "auth_type": "Token",
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting MCP server on port {port}")
    logger.info(f"API Key: {API_KEY}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)

