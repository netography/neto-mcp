# Neto MCP Server

A local MCP server for [Netography Fusion](https://netography.com/) supporting `stdio`, `streamable-http` and `sse`. 

# Installation

If you haven't already, install `uv`. You can find a guide for each OS here: [https://github.com/astral-sh/uv?tab=readme-ov-file#installation](https://github.com/astral-sh/uv?tab=readme-ov-file#installation).

Next, add your `netosecret` to a system environment variable named `NETOSECRET`. You can do this on UNIX systems by adding the following command in ~your `.bashrc`, `.zshrc`, or equivalent shell configuration file:

```bash
export NETOSECRET="your_netography_secret"
```

Then, clone the repository and run the following command:

```bash
uv sync
```
This will install all the dependencies required to run the server as well as the `neto-mcp-server` command.

# Usage - VSCode

To use the MCP server with VSCode, add the following configuration to your `settings.json`:

```json
"chat.mcp.enabled": true,
"mcp": {
    "servers": {
        "netography": {
        "command": "uvx",
        "args": [
            "neto-mcp-server"
        ],
        }
    },
}
```
After adding the configuration click restart and confirm that it is running correctly. 

# Example Usage

To start using the MCP after installing the server, open the VSCode copilot chat and click `Add Context`. Click `Tools` and then select `netography` from the list of available servers.

As a test query, try asking:
`Use Netography MCP to find the top 10 ips for flow in the past 1 hour.`

Congratulations! You have successfully set up the Neto MCP server and can now use it to query Netography Fusion data.