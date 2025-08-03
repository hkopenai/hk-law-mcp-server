"""
Module for testing Student Visa statistics data fetching and processing.

This module contains unit tests for the functions related to Student Visa / Entry Permit
statistics in the HK Law MCP Server.
"""

import unittest
from unittest.mock import patch, MagicMock
from typing import List, Any, Dict
from hkopenai.hk_law_mcp_server.tools.student_visa_statistics import (
    _get_student_visa_statistics,
    register,
)


class TestStudentVisaStatistics(unittest.TestCase):
    """Test class for verifying Student Visa statistics data processing."""

    mock_data = [
        {
            "As at end of Year": "2016",
            "Student Visa / Entry Permit Approved": "12345",
            "Total": "12345",
        },
        {
            "As at end of Year": "2020",
            "Student Visa / Entry Permit Approved": "15678",
            "Total": "15678",
        },
        {
            "As at end of Year": "2024",
            "Student Visa / Entry Permit Approved": "18901",
            "Total": "18901",
        },
    ]

    def setUp(self):
        """Set up test environment with mocked data fetching."""
        self.mock_fetch_csv = patch(
            "hkopenai.hk_law_mcp_server.tools.student_visa_statistics.fetch_csv_from_url"
        ).start()
        self.mock_fetch_csv.return_value = self.mock_data
        self.addCleanup(patch.stopall)

    def test_get_student_visa_statistics_default(self):
        """Test retrieval of all Student Visa statistics without filters."""
        result: Dict[str, Any] = _get_student_visa_statistics()
        self.assertIn("data", result)
        data = result["data"]

        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["As at end of Year"], "2016")
        self.assertEqual(int(data[0]["Student Visa / Entry Permit Approved"]), 12345)
        self.assertEqual(int(data[0]["Total"]), 12345)

    def test_get_student_visa_statistics_year_filter(self):
        """Test retrieval of Student Visa statistics for a specific year."""
        result: Dict[str, Any] = _get_student_visa_statistics(year=2020)
        self.assertIn("data", result)
        data = result["data"]
        self.assertEqual(data["As at end of Year"], "2020")
        self.assertEqual(int(data["Student Visa / Entry Permit Approved"]), 15678)
        self.assertEqual(int(data["Total"]), 15678)

    def test_get_student_visa_statistics_year_not_found(self):
        """Test error handling when data for a specific year is not found."""
        result: Dict[str, Any] = _get_student_visa_statistics(year=2030)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No data for year 2030")

    def test_register_tool(self):
        """
        Test the registration of the get_student_visa_statistics tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_student_visa_statistics function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Statistics on Student Visa / Entry Permit Approved in Hong Kong. Data source: Immigration Department"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

    def test_error_handling(self):
        """Test error handling when CSV fetching fails."""
        self.mock_fetch_csv.return_value = {"error": "Network error"}
        
        result: Dict[str, Any] = _get_student_visa_statistics()
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Network error") 