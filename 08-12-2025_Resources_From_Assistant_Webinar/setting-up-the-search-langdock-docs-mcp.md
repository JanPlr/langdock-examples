# Setting Up the Langdock Docs MCP Integration

This guide walks you through connecting the Langdock Documentation search tool to your workspace using the Model Context Protocol (MCP). Once set up, you can search Langdock's official documentation directly from Chat or Assistants.

---

## What You'll Get

After completing this setup, you'll have access to the **Searchdocs** action which allows you to:
- Search across the Langdock knowledge base
- Find relevant documentation, code examples, and API references
- Get answers grounded in official Langdock documentation

---

## Step 1: Navigate to Integrations

1. Go to **Integrations** in your Langdock workspace
2. Click **New Integration**
3. Select **MCP** as the integration type

---

## Step 2: Name Your Integration

| Field | Value |
|-------|-------|
| **Name** | `LangdockDocsMCPSearch` |
| **Description** | Search across Langdock's official documentation to find answers, code examples, and guides |

Click **Next** to proceed to the configuration page.

---

## Step 3: Configure the MCP Client

### Server Configuration

| Setting | Value |
|---------|-------|
| **Server URL** | `https://docs.langdock.com/mcp` |

After entering the URL, Langdock will automatically detect:
- **Transport mechanism:** Streamable HTTP
- **Protocol version:** 2025-06-18

### Authentication Method

Select **None** from the dropdown.

The Langdock Docs MCP server is publicly accessible and doesn't require authentication.

### Custom Headers

No custom headers are needed. Skip this section.

---

## Step 4: Test Connection and Enable Tools

1. Click the **Test connection** button
2. Wait for the connection to be verified
3. You'll see **Searchdocs** appear in the available tools list

### Enable the Searchdocs Action

1. Check the box next to **Searchdocs**
   - Description: "Search across the Docs knowledge base to find relevant information, code examples, API references, and guides"
2. Click **Save** to complete the setup

---

## Step 5: Using the Searchdocs Action

You can use this action in two ways:

### Option A: In Chat (Actions in Chat)

Use the **@mention** feature to search docs directly from any chat:

1. Type `@LangdockDocsMCPSearch` in your chat message
2. Ask your question about Langdock
3. The AI will automatically use the Searchdocs action to find relevant documentation

**Example:**
```
@LangdockDocsMCPSearch How do I create a new assistant with the API?
```

### Option B: In Assistants

Add the action to any assistant:

1. Open or create an assistant
2. Go to the **Actions** section
3. Find **LangdockDocsMCPSearch** in the integration list
4. Enable the **Searchdocs** action
5. Save the assistant

The assistant will now automatically search the documentation when users ask questions about Langdock.

---

## Configuration Summary

| Setting | Value |
|---------|-------|
| **Integration Name** | LangdockDocsMCPSearch |
| **Type** | MCP |
| **Server URL** | `https://docs.langdock.com/mcp` |
| **Transport** | Streamable HTTP |
| **Protocol Version** | 2025-06-18 |
| **Authentication** | None |
| **Custom Headers** | None |
| **Available Actions** | Searchdocs |

---

## Troubleshooting

### Connection test fails

- Verify the URL is exactly `https://docs.langdock.com/mcp`
- Check your internet connection
- Try refreshing the page and testing again

### Searchdocs action not appearing

- Click **Test connection** again
- Make sure authentication is set to **None**
- Check that no custom headers are accidentally configured

### Action not working in chat

- Verify the integration was saved successfully
- Make sure you're using the exact integration name with `@` (e.g., `@LangdockDocsMCPSearch`)
- Check that your workspace has the "Actions in Chat" feature enabled

---

## Related Resources

- [MCP Documentation](https://docs.langdock.com/resources/integrations/mcp) - Full MCP integration guide
- [Using Integrations](https://docs.langdock.com/resources/integrations/using-integrations) - How to use actions in assistants
- [Model Context Protocol](https://modelcontextprotocol.io/introduction) - Learn more about MCP

