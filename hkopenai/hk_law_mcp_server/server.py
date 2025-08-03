"""
Module for setting up and running the HK OpenAI Law and Security MCP Server.

This module configures the server with tools for law and security data in Hong Kong.
"""

from fastmcp import FastMCP
from .tools import foreign_domestic_helpers, student_visa_statistics


def server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI Law and Security Server")

    foreign_domestic_helpers.register(mcp)
    student_visa_statistics.register(mcp)

    return mcp
