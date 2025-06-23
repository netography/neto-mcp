import json
import logging
import os
import sys
from typing import Any

import httpx
from fastmcp import FastMCP
from fastmcp.server.openapi import (
    HTTPRoute,
    MCPType,
    OpenAPIResource,
    OpenAPIResourceTemplate,
    OpenAPITool,
    RouteMap,
)

from neto.api import NetoAPI

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logging.info("Starting Netography Fusion MCP...")

netosecret = os.getenv("NETOSECRET")

neto_api: NetoAPI = NetoAPI(netosecret)

script_dir = os.path.dirname(os.path.abspath(__file__))

neto_api.authenticate()


def download_if_changed(url: str, local_path: str) -> bool:
    """
    Download the S3 object at `url` only if it’s been modified since
    the last download. Returns True if we fetched a fresh copy.
    """
    etag_store = local_path + ".etag"
    headers = {}

    if os.path.exists(local_path) and os.path.exists(etag_store):
        with open(etag_store, "r") as f:
            etag = f.read().strip()
        headers["If-None-Match"] = etag

    resp = httpx.get(url, headers=headers)
    if resp.status_code == 304:
        logging.info("✔︎ OpenAPI spec hasn’t changed on S3; skipping download.")
        return False
    resp.raise_for_status()

    with open(local_path, "wb") as f:
        f.write(resp.content)
    logging.info(f"⬇️  Downloaded OpenAPI spec to {local_path}")

    new_etag = resp.headers.get("ETag")
    if new_etag:
        with open(etag_store, "w") as f:
            f.write(new_etag)
    return True


api_client = httpx.AsyncClient(
    base_url=neto_api.NETO_BASE_URL,
    headers={"Authorization": f"Bearer {neto_api.token}"},
    timeout=20,  # Adjust timeout as needed
)

download_if_changed(
    url="https://neto-downloads.s3.us-east-1.amazonaws.com/openapi/openapi.json",
    local_path=os.path.join(script_dir, "openapi.json"),
)

with open(os.path.join(script_dir, "openapi.json"), "r") as f:
    openapi_spec = json.load(f)


def customize_components(
    route: HTTPRoute,
    component: OpenAPITool | OpenAPIResource | OpenAPIResourceTemplate,
) -> None:
    if route.path.startswith("/api/v1/search/"):
        component.description = f"{component.description} ALWAYS PASS A SIZE PARAMETER OF 1000 IF NOT OTHERWISE SPECIFIED."
    # Use for debugging purposes
    # if route.path.startswith("/api/v1/stats/"):
    #     print(component.name)
    #     print(component.description)
    #     # print(component.parameters)


mcp = FastMCP.from_openapi(
    name="netography",
    openapi_spec=openapi_spec,
    client=api_client,
    route_maps=[
        RouteMap(
            pattern=r"^/api/v1/labels/",
            mcp_type=MCPType.TOOL,
            methods=["GET", "DELETE", "POST"],
        ),
        RouteMap(
            pattern=r"^/api/v1/labels/[^/]+/bulk$",
            mcp_type=MCPType.TOOL,
            methods=["PUT"],
        ),
        RouteMap(pattern=r"^/api/v1/search/", mcp_type=MCPType.TOOL),
        RouteMap(pattern=r"^/api/v1/intel/", mcp_type=MCPType.TOOL),
        RouteMap(pattern=r"^/api/v1/vpc", mcp_type=MCPType.TOOL, methods=["GET"]),
        RouteMap(
            pattern=r"^/api/v1/integrations/", mcp_type=MCPType.TOOL, methods=["GET"]
        ),
        RouteMap(pattern=r"^/api/v1/stats/", mcp_type=MCPType.TOOL),
        RouteMap(mcp_type=MCPType.EXCLUDE),
    ],
    mcp_component_fn=customize_components,
)


@mcp.tool(
    name="nql_guide",
    description="A guide to NQL (Netography Query Language). This should be used whenever it is neccesary to create a query or search in Netography Fusion. It also provides guidance in the event of a failed query.",
)
async def nql_guide() -> Any:
    """
    A guide to NQL (Netography Query Language).
    This tool provides a comprehensive guide to NQL, including syntax, examples, and best practices
    """
    with open(f"{script_dir}/nql-guide.md", "r") as file:
        content = file.read()
    return {"content": content}


if __name__ == "__main__":
    mcp.run()
