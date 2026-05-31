"""Tests for Scavio Walmart tools."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

from autogen_scavio.tools.walmart import create_walmart_product_tool, create_walmart_search_tool
from tests.conftest import mock_walmart_product_response, mock_walmart_search_response


class TestWalmartSearchTool:
    """Tests for create_walmart_search_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_walmart_search_tool()
        assert tool.name == "scavio_walmart_search"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_products(self, _mock_client):
        """Test that products are truncated to max_results."""
        mock_client = MagicMock()
        mock_client.walmart.search = AsyncMock(
            return_value=mock_walmart_search_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_walmart_search_tool(max_results=3)
            result = await tool.run_json({"query": "air fryer"}, None)
            parsed = json.loads(result)
            assert len(parsed["data"]["products"]) == 3


class TestWalmartProductTool:
    """Tests for create_walmart_product_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_walmart_product_tool()
        assert tool.name == "scavio_walmart_product"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_product_data(self, _mock_client):
        """Test that product data is returned."""
        mock_client = MagicMock()
        mock_client.walmart.product = AsyncMock(
            return_value=mock_walmart_product_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_walmart_product_tool()
            result = await tool.run_json({"product_id": "WM1"}, None)
            parsed = json.loads(result)
            assert parsed["data"]["product_id"] == "WM1"
