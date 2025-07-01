# Neto MCP Server

A local MCP server for [Netography Fusion](https://netography.com/), supporting `stdio`, `streamable-http`, and `sse` interfaces.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Claude Desktop Integration](#claude-desktop-integration)
- [VS Code Integration](#vs-code-integration)
- [Example Queries](#example-queries)
- [Running the Server Manually](#running-the-server-manually)
- [Specifying Transport](#specifying-transport)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- [uv](https://github.com/astral-sh/uv?tab=readme-ov-file#installation) - a Python package/dependency manager. Follow the [official instructions](https://github.com/astral-sh/uv?tab=readme-ov-file#installation) for your OS.
- Python 3.8+
- Access to Netography Fusion and a valid `NETOSECRET` API key

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-org/neto-mcp-server.git
   cd neto-mcp-server
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

## Configuration

### Setting the `NETOSECRET` Environment Variable

The MCP server requires a Netography API secret. You can set this in your shell or directly in your Claude Desktop or VS Code settings.

**Shell Configuration (for manual server runs):**

For zsh:

```bash
echo 'export NETOSECRET="your-netography-secret"' >> ~/.zshrc
source ~/.zshrc
```

For bash:

```bash
echo 'export NETOSECRET="your-netography-secret"' >> ~/.bash_profile
source ~/.bash_profile
```

## Claude Desktop Integration

### Setup

1. **Locate the configuration file:**
  Go to Settings > Developer and click the Edit Config button.  This will open the configuration file.  Alternatively, you can find the file at the following locations based on your OS:

   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. **Edit the configuration file** with the following structure:

   ```json
   {
     "mcpServers": {
       "netography": {
         "command": "/full/path/to/uv",
         "args": [
           "run",
           "--directory",
           "/full/path/to/your/neto-mcp-server",
           "neto-mcp-server"
         ],
         "env": {
           "NETOSECRET": "your-netography-secret"
         }
       }
     }
   }
   ```

3. **Important configuration notes:**
   - **Use full paths:** You must provide the complete absolute path to both the `uv` executable and your `neto-mcp-server` directory
   - **Find your uv path:** Run `which uv` in your terminal to get the full path
   - **Replace placeholders:**
     - Replace `/full/path/to/uv` with the output from `which uv`
     - Replace `/full/path/to/your/neto-mcp-server` with the absolute path to your cloned repository
     - Replace `your-netography-secret` with your actual Netography API secret

4. **Restart Claude Desktop** after saving the configuration file for the changes to take effect.

### Usage

Once configured, Claude Desktop will automatically load and manage the MCP server - no manual starting required. Simply mention Netography queries in your conversations and Claude will use the MCP tools to fetch data from your Fusion instance.  Clicking the search and tools icon (next to the +) in the chat box will allow you to select the `netography` server as a tool and select particular API endpoints to enable/disable

**Note for Claude Desktop Free users:** Free tier users may encounter context length limitations when using multiple MCP tools. If you experience issues, consider disabling some API endpoints/tools in your MCP server configuration to reduce context size.

## VS Code Integration

### Setup

Add the following to your VS Code `settings.json`, replacing the `NETO_MCP_SERVER_REPO_DIR` with the path to the git repo mcp-server directory and `your-netography-secret` with your actual secret:

```json
"mcp": {
  "servers": {
    "netography": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "NETO_MCP_SERVER_REPO_DIR",
        "neto-mcp-server"
      ],
      "env": {
        "NETOSECRET": "your-netography-secret"
      }
    }
  }
}
```

### Usage

1. Open the Command Palette (`Cmd+Shift+P`), search for "MCP: List Servers", and select the `netography` server and then select "Start Server".
2. Confirm the server status is "running" in the MCP output panel.
3. In Copilot Chat, type `@netography` as part of your chat to include usage of the MCP tool.  Alternatively, click 'Add Context...', select 'Tools', and choose the `netography` server.

## Example Queries

- **Find top IPs:**
  Find the top 10 IPs by flow volume in the past hour from Netography data.

- **Count traffic sources:**
  How many traffic sources are configured in Netography

- **List all traffic sources:**
  List all configured traffic sources in Netography

- **Show flows for a specific IP:**
  Show all network flows for IP 192.0.2.1 in the last 24 hours in Netography

- **Get traffic by protocol:**
  Summarize network traffic by protocol for the past 7 days in Netography

## Running the Server Manually

If you prefer to run the MCP server manually instead of through VS Code or Claude Desktop, you can do so using the command line.

**From the command line:**

```bash
uv run --directory NETO_MCP_SERVER_REPO_DIR neto-mcp-server
```

## Specifying Transport

When starting the MCP server, you can specify the transport method to use with the `--transport` (or `-t`) flag. The available options are:

- `stdio`: Standard input/output (default)
- `streamable-http`: Streamable HTTP
- `sse`: Server-sent events

For example, to start the server with streamable HTTP transport:

```bash
uv run --directory NETO_MCP_SERVER_REPO_DIR neto-mcp-server --transport streamable-http
```

## Troubleshooting/FAQ
- **Server not starting?**
  Ensure `NETOSECRET` is set and dependencies are installed with `uv sync`.

- **No response in Copilot Chat?**
  Confirm the MCP server is running and selected as a tool in Copilot Chat.

- **No response from the LLM after running an MCP Tool?**
  The context window is likely full. Try disabling unneeded tools or increasing the context window size.

- **Copilot Chat is always calling the wrong API endpoint and never answering my questions?**
  MCP support in Copilot is very much in early and active development.  We have seen it work perfectly on one Copilot instance and fail entirely on another.  We have had more reliable results using Claude Desktop over Copilot Chat to interact with MCP servers (Anthropic created MCP so they are definitely a bit ahead in support right now).  You may want to try using VS Code Insider and the pre-release Copilot Chat extensions to get the latest features and fixes.

- **Claude Desktop not recognizing the server?**
  Verify that you're using full absolute paths in your `claude_desktop_config.json` and that the file is in the correct location for your operating system.

- **Permission errors?**
  Ensure that the `uv` executable and your project directory have the proper read/execute permissions.

- **I don't see any resources available from the MCP server, only tools?**
  The Model Context Protocol is rapidly evolving, and as such many LLM MCP clients do not yet support `resources`, using `tools` instead. Currently, these are functionally equivalent, but we anticipate that `resources` will be more widely supported in the future. At that time, we will transition to using `resources` more broadly for `GET` endpoints.