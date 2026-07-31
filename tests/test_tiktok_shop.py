"""Tests for Scavio TikTok Shop tools.

The mock bodies in tests/conftest.py are the normalized shapes the backend
emits, produced by running the backend normalizers over the recorded fixtures,
so a tool reading the wrong key fails here rather than at runtime.
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from autogen_scavio.tools.tiktok_shop import (
    create_tiktok_shop_categories_tool,
    create_tiktok_shop_category_products_tool,
    create_tiktok_shop_product_reviews_tool,
    create_tiktok_shop_product_tool,
    create_tiktok_shop_resolve_tool,
    create_tiktok_shop_search_suggestions_tool,
    create_tiktok_shop_search_tool,
    create_tiktok_shop_shop_products_tool,
)
from tests.conftest import (
    MockNotFoundError,
    mock_tiktok_shop_categories_response,
    mock_tiktok_shop_category_products_response,
    mock_tiktok_shop_product_response,
    mock_tiktok_shop_resolve_response,
    mock_tiktok_shop_reviews_response,
    mock_tiktok_shop_search_response,
    mock_tiktok_shop_shop_products_response,
    mock_tiktok_shop_suggestions_response,
)


class TestTikTokShopSearchTool:
    """Tests for create_tiktok_shop_search_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool with the expected name."""
        tool = create_tiktok_shop_search_tool()
        assert tool.name == "scavio_tiktok_shop_search"

    def test_description_states_coverage_limit(self):
        """Search must never advertise a reliable detail pipeline."""
        tool = create_tiktok_shop_search_tool()
        assert "44%" in tool.description
        assert "exact prices" in tool.description

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_products_with_exact_prices(self):
        """Test that search returns product cards carrying real prices."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.search = AsyncMock(
            return_value=mock_tiktok_shop_search_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_search_tool()
            result = await tool.run_json({"search": "phone case"}, None)
            parsed = json.loads(result)
            assert parsed["data"]["products"][0]["price"]["current"] == 4.88
            assert parsed["data"]["has_more"] is True
            assert parsed["data"]["degraded"] is False

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_products(self):
        """Test that products are truncated to max_results."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.search = AsyncMock(
            return_value=mock_tiktok_shop_search_response(30)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_search_tool(max_results=3)
            result = await tool.run_json({"search": "phone case"}, None)
            assert len(json.loads(result)["data"]["products"]) == 3

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_wire_param_is_search(self):
        """The wire field is 'search', not 'query'."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.search = AsyncMock(
            return_value=mock_tiktok_shop_search_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_search_tool()
            await tool.run_json({"search": "phone case", "cursor": "eyJ"}, None)
            mock_client.tiktok_shop.search.assert_awaited_once_with(
                search="phone case", cursor="eyJ"
            )


class TestTikTokShopSearchSuggestionsTool:
    """Tests for create_tiktok_shop_search_suggestions_tool."""

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_plain_strings(self):
        """Test that suggestions come back as a flat list of strings."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.search_suggestions = AsyncMock(
            return_value=mock_tiktok_shop_suggestions_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_search_suggestions_tool()
            result = await tool.run_json({"search": "wireless", "region": "GB"}, None)
            parsed = json.loads(result)
            assert parsed["data"]["suggestions"][0] == "wireless charger"
            mock_client.tiktok_shop.search_suggestions.assert_awaited_once_with(
                search="wireless", region="GB"
            )


class TestTikTokShopProductTool:
    """Tests for create_tiktok_shop_product_tool."""

    def test_description_carries_both_honesty_notes(self):
        """Both the price gap and the 44% coverage must be stated."""
        tool = create_tiktok_shop_product_tool()
        assert "does NOT return a price" in tool.description
        assert "44%" in tool.description

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_detail_without_price(self):
        """Upstream masks the digits, so detail never carries a price."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.product = AsyncMock(
            return_value=mock_tiktok_shop_product_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_product_tool()
            result = await tool.run_json(
                {"product_id": "1732293553906094315"}, None
            )
            parsed = json.loads(result)
            assert parsed["data"]["price"]["current"] is None
            assert parsed["data"]["price"]["original"] is None
            assert parsed["data"]["shop"]["followers_count"] == 588860
            assert parsed["data"]["variants"][0]["in_stock"] is True

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_404_is_a_normal_not_found(self):
        """A 404 is a normal answer here, not a raised error."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.product = AsyncMock(
            side_effect=MockNotFoundError("Product not found in this region.")
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_product_tool()
            result = await tool.run_json(
                {"product_id": "1732293553906094315"}, None
            )
            parsed = json.loads(result)
            assert parsed["not_found"] is True
            assert parsed["data"] is None
            assert "44%" in parsed["guidance"]

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_other_errors_still_raise(self):
        """A non-404 failure is a real failure and must not be swallowed."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.product = AsyncMock(side_effect=RuntimeError("boom"))

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_product_tool()
            with pytest.raises(RuntimeError):
                await tool.run_json({"product_id": "1732293553906094315"}, None)


class TestTikTokShopProductReviewsTool:
    """Tests for create_tiktok_shop_product_reviews_tool."""

    def test_description_warns_about_total_reviews(self):
        """total_reviews drifts and must not drive page math."""
        tool = create_tiktok_shop_product_reviews_tool()
        assert "drifts" in tool.description

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_and_truncates_reviews(self):
        """Test that reviews are returned and truncated to max_results."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.product_reviews = AsyncMock(
            return_value=mock_tiktok_shop_reviews_response(20)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_product_reviews_tool(max_results=5)
            result = await tool.run_json(
                {"product_id": "1732293553906094315"}, None
            )
            parsed = json.loads(result)
            assert len(parsed["data"]["reviews"]) == 5
            assert parsed["data"]["reviews"][0]["reviewer_name"] == "C**"
            assert parsed["data"]["rating"]["distribution"]["1"] == 431

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_all_filters_forwarded(self):
        """Test that every review filter reaches the client unchanged."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.product_reviews = AsyncMock(
            return_value=mock_tiktok_shop_reviews_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_product_reviews_tool()
            await tool.run_json(
                {
                    "product_id": "1732293553906094315",
                    "page": 2,
                    "page_size": 100,
                    "sort": "recent",
                    "rating": 5,
                    "has_media": True,
                    "verified_only": False,
                    "region": "US",
                },
                None,
            )
            mock_client.tiktok_shop.product_reviews.assert_awaited_once_with(
                product_id="1732293553906094315",
                page=2,
                page_size=100,
                sort="recent",
                rating=5,
                has_media=True,
                verified_only=False,
                region="US",
            )


class TestTikTokShopCategoriesTool:
    """Tests for create_tiktok_shop_categories_tool."""

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_tree_with_no_arguments(self):
        """Test that the two-level category tree comes back intact."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.categories = AsyncMock(
            return_value=mock_tiktok_shop_categories_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_categories_tool()
            result = await tool.run_json({}, None)
            parsed = json.loads(result)
            assert parsed["data"]["total_categories"] == 240
            top = parsed["data"]["categories"][0]
            assert top["parent_id"] is None
            assert top["children"][0]["parent_id"] == "601450"
            mock_client.tiktok_shop.categories.assert_awaited_once_with()


class TestTikTokShopCategoryProductsTool:
    """Tests for create_tiktok_shop_category_products_tool."""

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_listing(self):
        """Test that a category listing returns cards with exact prices."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.category_products = AsyncMock(
            return_value=mock_tiktok_shop_category_products_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_category_products_tool(max_results=4)
            result = await tool.run_json(
                {"category_id": "601450", "region": "GB"}, None
            )
            parsed = json.loads(result)
            assert parsed["data"]["category_id"] == "601450"
            assert len(parsed["data"]["products"]) == 4
            mock_client.tiktok_shop.category_products.assert_awaited_once_with(
                category_id="601450", region="GB"
            )

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_unknown_category_is_not_found(self):
        """An unknown category id is a not-found result, not a raise."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.category_products = AsyncMock(
            side_effect=MockNotFoundError("No products found for this category id.")
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_category_products_tool()
            result = await tool.run_json({"category_id": "999999"}, None)
            assert json.loads(result)["not_found"] is True


class TestTikTokShopShopProductsTool:
    """Tests for create_tiktok_shop_shop_products_tool."""

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_catalog(self):
        """Test that a shop catalog returns the brief shop block and cards."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.shop_products = AsyncMock(
            return_value=mock_tiktok_shop_shop_products_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_shop_products_tool(max_results=2)
            result = await tool.run_json(
                {"shop_id": "7495514739648989419"}, None
            )
            parsed = json.loads(result)
            assert parsed["data"]["shop"]["shop_name"] == "medicube US Store"
            assert "followers_count" not in parsed["data"]["shop"]
            assert len(parsed["data"]["products"]) == 2

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_unknown_shop_is_not_found(self):
        """An unknown shop id is a not-found result, not a raise."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.shop_products = AsyncMock(
            side_effect=MockNotFoundError("Shop not found or has no products.")
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_shop_products_tool()
            result = await tool.run_json({"shop_id": "123456"}, None)
            assert json.loads(result)["not_found"] is True


class TestTikTokShopResolveTool:
    """Tests for create_tiktok_shop_resolve_tool."""

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_resolves_share_link(self):
        """Test that a share link resolves to an id and a canonical URL."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.resolve = AsyncMock(
            return_value=mock_tiktok_shop_resolve_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_resolve_tool()
            result = await tool.run_json(
                {"url": "https://vt.tiktok.com/ZT2AHoGsE/"}, None
            )
            parsed = json.loads(result)
            assert parsed["data"]["type"] == "product"
            assert parsed["data"]["product_id"] == "8651224669119091502"
            assert parsed["data"]["url"].startswith("https://shop.tiktok.com/")
            assert parsed["data"]["resolved_by"] == "share_link"

    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_dead_link_is_not_found(self):
        """A dead share link is a not-found result, not a raise."""
        mock_client = MagicMock()
        mock_client.tiktok_shop.resolve = AsyncMock(
            side_effect=MockNotFoundError("Could not resolve this link.")
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_shop_resolve_tool()
            result = await tool.run_json(
                {"url": "https://vt.tiktok.com/DEAD/"}, None
            )
            assert json.loads(result)["not_found"] is True


class TestTikTokShopProvider:
    """The provider map must expose all eight tools."""

    def test_provider_returns_eight_tools(self):
        """Test that create_scavio_tools('tiktok_shop') builds every tool."""
        from autogen_scavio import create_scavio_tools

        tools = create_scavio_tools(
            api_key="sk_live_test", providers=["tiktok_shop"]
        )
        assert [t.name for t in tools] == [
            "scavio_tiktok_shop_search",
            "scavio_tiktok_shop_search_suggestions",
            "scavio_tiktok_shop_product",
            "scavio_tiktok_shop_product_reviews",
            "scavio_tiktok_shop_categories",
            "scavio_tiktok_shop_category_products",
            "scavio_tiktok_shop_shop_products",
            "scavio_tiktok_shop_resolve",
        ]

    def test_factories_exported(self):
        """Test that every factory is in the package __all__."""
        import autogen_scavio

        for name in (
            "create_tiktok_shop_search_tool",
            "create_tiktok_shop_search_suggestions_tool",
            "create_tiktok_shop_product_tool",
            "create_tiktok_shop_product_reviews_tool",
            "create_tiktok_shop_categories_tool",
            "create_tiktok_shop_category_products_tool",
            "create_tiktok_shop_shop_products_tool",
            "create_tiktok_shop_resolve_tool",
        ):
            assert name in autogen_scavio.__all__
            assert hasattr(autogen_scavio, name)
