"""
Module for handling data related to Foreign Domestic Helpers in Hong Kong.

This module provides functions to fetch and process statistics on Foreign Domestic Helpers
from the Immigration Department of Hong Kong.
"""

from typing import Dict, List, Annotated, Optional, Union
from pydantic import Field
from hkopenai_common.csv_utils import fetch_csv_from_url


def register(mcp):
    """Registers the foreign domestic helpers tool with the FastMCP server."""

    @mcp.tool(
        description="Statistics on Foreign Domestic Helpers in Hong Kong. Data source: Immigration Department"
    )
    def get_foreign_domestic_helpers_statistics(
        year: Annotated[
            Optional[int], Field(description="Filter by specific year")
        ] = None,
    ) -> Dict[str, Union[Dict[str, str], List[Dict[str, str]], str]]:
        """Get statistics on Foreign Domestic Helpers in Hong Kong.
        Data source: Immigration Department"""
        return _get_foreign_domestic_helpers_statistics(year)


def _get_foreign_domestic_helpers_statistics(
    year: Annotated[Optional[int], Field(description="Filter by specific year")] = None,
) -> Dict[str, Union[Dict[str, str], List[Dict[str, str]], str]]:
    """Get statistics on Foreign Domestic Helpers in Hong Kong.
    Data source: Immigration Department"""
    url = (
        "https://www.immd.gov.hk/opendata/eng/law-and-security/visas/statistics_FDH.csv"
    )
    data = fetch_csv_from_url(url)

    if "error" in data:
        return data

    if year:
        year_str = str(year)
        result = next(
            (item for item in data if item["As at end of Year"] == year_str), None
        )
        return {"data": result} if result else {"error": f"No data for year {year}"}

    return {"data": data}
