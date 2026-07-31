"""Tests for Scavio Amazon tools."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

from autogen_scavio.tools.amazon import (
    create_amazon_offers_tool,
    create_amazon_product_tool,
    create_amazon_search_tool,
)
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
    async def test_passes_country_and_page(self, _mock_client):
        """country and page reach the SDK; unset params are omitted."""
        mock_client = MagicMock()
        mock_client.amazon.search = AsyncMock(
            return_value=mock_amazon_search_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_amazon_search_tool()
            await tool.run_json({"query": "tea", "country": "gb", "page": 2}, None)
            assert mock_client.amazon.search.call_args.kwargs == {
                "query": "tea",
                "country": "gb",
                "page": 2,
            }

    def test_retired_params_are_not_in_the_schema(self):
        """A tool schema must not advertise a filter the API drops."""
        retired = {
            "sort_by",
            "pages",
            "category_id",
            "merchant_id",
            "language",
            "currency",
            "device",
            "zip_code",
            "autoselect_variant",
            "domain",
        }
        props = set(create_amazon_search_tool().schema["parameters"]["properties"])
        assert not props & retired
        assert props == {"query", "country", "page"}


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


class TestAmazonOffersTool:
    """Tests for create_amazon_offers_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_amazon_offers_tool()
        assert tool.name == "scavio_amazon_offers"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_offers(self, _mock_client):
        """The ASIN and country reach the SDK and offers come back."""
        mock_client = MagicMock()
        mock_client.amazon.offers = AsyncMock(
            return_value={
                "data": {
                    "asin": "B001",
                    "count": 1,
                    "offers": [{"seller_name": "A", "is_buy_box_winner": True}],
                }
            }
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_amazon_offers_tool()
            result = await tool.run_json({"asin": "B001", "country": "gb"}, None)
            parsed = json.loads(result)
            assert parsed["data"]["offers"][0]["is_buy_box_winner"] is True
            assert mock_client.amazon.offers.call_args.kwargs == {
                "asin": "B001",
                "country": "gb",
            }
