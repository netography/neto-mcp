# Neto MCP Server

A local MCP server for [Netography Fusion](https://netography.com/), supporting `stdio`, `streamable-http`, and `sse` interfaces.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [VS Code Integration](#vs-code-integration)
- [Copilot Chat Example Queries](#copilot-chat-example-queries)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- [uv](https://github.com/astral-sh/uv?tab=readme-ov-file#installation) (Python package/dependency manager)
- Python 3.8+
- Access to Netography Fusion and a valid `NETOSECRET` API key

## Installation

1. **Install `uv`**  
   Follow the [official instructions](https://github.com/astral-sh/uv?tab=readme-ov-file#installation) for your OS.

2. **Clone the repository**

   ```bash
   git clone https://github.com/your-org/neto-mcp-server.git
   cd neto-mcp-server
   ```

3. **Install dependencies**

   ```bash
   uv sync
   ```

4. **Install the MCP server tool**

   ```bash
   uv tool install .
   ```

---

## Configuration

### Setting the `NETOSECRET` Environment Variable

The MCP server requires a Netography API secret. You can set this in your shell or directly in your VS Code settings.

**Option 1: Shell**

For zsh:

```bash
echo 'export NETOSECRET="REPLACEME"' >> ~/.zshrc
source ~/.zshrc
```

For bash:

```bash
echo 'export NETOSECRET="your-netography-secret"' >> ~/.bash_profile
source ~/.bash_profile
```

**Option 2: VS Code `settings.json`**
Add the following to your VS Code `settings.json`:

```json
"mcp": {
  "servers": {
    "netography": {
      "command": "uvx",
      "args": [
        "neto-mcp-server"
      ],
      "env": {
        "NETOSECRET": "your-netography-secret"
      }
    }
  }
}
```

## Running the Server

**From the command line:**

```bash
uvx neto-mcp-server
```

**From VS Code:**

1. Open the Command Palette (`Cmd+Shift+P`), search for "MCP: List Servers", and select the `netography` server and then select "Start Server".
2. Confirm the server status is "running" in the MCP output panel.

## Usage with VS Code and Copilot Chat

### Configuring Copilot Chat to Use the MCP Tool

Click 'Add Context...' in Copilot Chat, select 'Tools', and choose the `netography` server. This will enable the MCP tool for your chat session.

- **Find top IPs:**

  ```
  Use Netography MCP to find the top 10 IPs for flow in the past 1 hour.
  ```

- **Count traffic sources:**

  ```
  Use Netography MCP to count the number of configured traffic sources.
  ```

- **List all traffic sources:**

  ```
  Use Netography MCP to list all configured traffic sources.
  ```

- **Show flows for a specific IP:**

  ```
  Use Netography MCP to show all flows for IP 192.0.2.1 in the last 24 hours.
  ```

- **Get traffic by protocol:**

  ```
  Use Netography MCP to summarize traffic by protocol for the past 7 days.
  ```

---

## Troubleshooting

- **Server not starting?**  
  Ensure `NETOSECRET` is set and dependencies are installed.
- **No response in Copilot Chat?**  
  Confirm the MCP server is running and selected as a tool in Copilot Chat.
