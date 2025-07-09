# Netography Fusion MCP Server

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
- [Supported Tools](#supported-tools)
- [Troubleshooting/FAQ](#troubleshootingfaq)

## Prerequisites

- [uv](https://github.com/astral-sh/uv?tab=readme-ov-file#installation) - a Python package/dependency manager. Follow the [official instructions](https://github.com/astral-sh/uv?tab=readme-ov-file#installation) for your OS.
- Python 3.11+
- Access to Netography Fusion and a valid `NETOSECRET` API key. For more information on obtaining a `NETOSECRET` key, please refer to the [Netography Fusion documentation](https://docs.netography.com/reference/create-a-netography-api-key).

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/netography/neto-mcp.git
   cd neto-mcp
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

**Note for Claude Desktop Free users:** The context is very limited for the free plan, so you may quickly receive a context limit error when interacting with the Netography MCP server.  Disabling some API endpoints/tools in your MCP server configuration will reduce context size.  The Claude Pro plan does not have this issue and is recommended.

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


## VS Code / Copilot Integration

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
3. In Copilot Chat, click 'Add Context...', select 'Tools', and choose the `netography` server.

## Example Queries

- **Find top IPs:**
  Find the top 10 IPs by flow volume in the past hour from Netography

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

## Supported Tools

All query endpoints in the Netography Fusion API are supported. As MCP clients continue to evolve, we will add resource creation and management endpoints as well. Currently, the following endpoints are available:

| Endpoint                          | Description                                                                                   |
|-----------------------------------|-----------------------------------------------------------------------------------------------|
| `search_context_fields_get`       | Get valid fields that can be used in search API calls for a given data type.                 |
| `search_context_post`             | Retrieve events or records for a specified context over a time range using an NQL query.     |
| `stats_context_fields_get`        | Get valid fields that can be used in statistical API calls for a given context.              |
| `stats_context_aliases_get`       | Get field aliases (shortcuts for multiple fields) for use in search API calls.               |
| `stats_context_metrics_get`       | Get valid metrics that can be used in statistical API calls for a given context.             |
| `stats_context_agg_post`          | Get summarized statistics by aggregating data for a specified context over time.             |
| `intel_lookup_asns_post`          | Look up the organization name for one or more ASNs.                                          |
| `intel_lookup_ips_post`           | Look up intelligence information (Geo, Reputation, RDNS, etc.) for one or more IPs.          |
| `labels_ips_get`                  | Return a list of all IP labels.                                                              |
| `labels_ips_all_context_get`      | Fetch all labels for all IPs within a specific context.                                      |
| `labels_ips_ip_get`               | Fetch all labels for a specific IP address.                                                  |
| `labels_ips_ip_context_get`       | Fetch labels of a specific context for a given IP address.                                   |
| `labels_ports_get`                | Return a list of all port labels.                                                            |
| `labels_ports_protocols_get`      | Return a list of all protocols that have port labels.                                        |
| `labels_ports_all_protocol_get`   | Fetch all port labels for a specific protocol.                                               |
| `labels_ports_port_get`           | Fetch all labels for a specific port across all protocols.                                   |
| `labels_port_protocol_get`        | Fetch the label for a specific port and protocol combination.                                |
| `integrations_aws_role_get`       | Get info for configuring AWS Role-based auth, including Account ID and External ID.          |
| `vpc_get`                         | Return a list of all configured Cloud Sources, with optional filtering.                      |
| `vpc_name_get`                    | Fetch a specific Cloud Source by its name.                                                   |
| `vpc_id_get`                      | Fetch a specific Cloud Source by its numeric ID.                                             |
| `vpc_status_get`                  | Return the status for all configured Cloud Sources.                                          |
| `vpc_status_id_get`               | Fetch the status for a specific Cloud Source by its ID.                                      |
| `vpc_regions_get`                 | Return all available cloud provider regions.                                                 |
| `vpc_regions_flowtype_get`        | Return all available regions for a specific cloud provider (flowtype).                       |
| `integrations_context_get`        | Return a list of all context integrations.                                                   |
| `integrations_context_id_get`     | Fetch a specific context integration by its ID.                                              |
| `integrations_context_id_run_get` | Run a specified context integration and return a list of IP labels to be imported.           |
| `integrations_response_get`       | Return a list of all response integrations.                                                  |
| `integrations_response_id_get`    | Fetch a specific response integration by its ID.                                             |
| `nql_guide`                       | Provides a guide to NQL (Netography Query Language) for creating queries and searches.       |
| `get_detection_model_list`        | Get the list of available detection models.                                                  |
| `get_detection_model_details`     | Get the details of a specific detection model.                                               |

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

- **Why are there two `netography` servers in the MCP server list in VSCode?**
  If you have already configured the `netography` server in Claude Desktop, it will also appear in the MCP server list in VSCode if you have `chat.mcp.discovery.enabled` set to `true`. You can safely ignore the duplicate entry, change the name of the server in your VSCode settings, or disable MCP discovery in VSCode settings by setting `chat.mcp.discovery.enabled` to `false`.
