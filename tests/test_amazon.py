"""Tests for Scavio Amazon tools."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

from autogen_scavio.tools.amazon import create_amazon_product_tool, create_amazon_search_tool
from tests.conftest import mock_amazon_product_response, mock_amazon_search_response


class TestAmazonSearchTool:
    """Tests for create_amazon_search_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_amazon_search_tool()
        assert tool.name == "scavio_amazon_search"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_products(self, _mock_client):
        """Test that products are truncated to max_results."""
        mock_client = MagicMock()
        mock_client.amazon.search = AsyncMock(
            return_value=mock_amazon_search_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_amazon_search_tool(max_results=3)
            result = await tool.run_json({"query": "headphones"}, None)
            parsed = json.loads(result)
            assert len(parsed["data"]["products"]) == 3

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_passes_domain(self, _mock_client):
        """Test that domain is passed to SDK."""
        mock_client = MagicMock()
        mock_client.amazon.search = AsyncMock(
            return_value=mock_amazon_search_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_amazon_search_tool()
            await tool.run_json({"query": "tea", "domain": "co.uk"}, None)
            call_kwargs = mock_client.amazon.search.call_args.kwargs
            assert call_kwargs["domain"] == "co.uk"


class TestAmazonProductTool:
    """Tests for create_amazon_product_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_amazon_product_tool()
        assert tool.name == "scavio_amazon_product"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_product_data(self, _mock_client):
        """Test that product data is returned."""
        mock_client = MagicMock()
        mock_client.amazon.product = AsyncMock(
            return_value=mock_amazon_product_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_amazon_product_tool()
            result = await tool.run_json({"asin": "B001"}, None)
            parsed = json.loads(result)
            assert parsed["data"]["asin"] == "B001"
