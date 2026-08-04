"""Tests for Scavio Google tools."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

from autogen_scavio.tools.google import (
    create_google_ai_mode_tool,
    create_google_flights_tool,
    create_google_hotels_detail_tool,
    create_google_hotels_tool,
    create_google_maps_place_tool,
    create_google_maps_reviews_tool,
    create_google_maps_search_tool,
    create_google_news_tool,
    create_google_shopping_product_tool,
    create_google_shopping_stores_tool,
    create_google_shopping_tool,
    create_google_trending_tool,
    create_google_trends_tool,
    create_web_search_tool,
)
from tests.conftest import (
    mock_google_ai_mode_response,
    mock_google_flights_response,
    mock_google_hotels_detail_response,
    mock_google_hotels_response,
    mock_google_maps_place_response,
    mock_google_maps_reviews_response,
    mock_google_maps_search_response,
    mock_google_news_response,
    mock_google_shopping_product_response,
    mock_google_shopping_response,
    mock_google_shopping_stores_response,
    mock_google_trending_response,
    mock_google_trends_response,
    mock_search_response,
)


class TestWebSearchTool:
    """Tests for create_web_search_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_web_search_tool()
        assert tool.name == "scavio_web_search"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_results(self, _mock_client):
        """Test that results are truncated to max_results."""
        mock_client = MagicMock()
        mock_client.google.search = AsyncMock(return_value=mock_search_response(10))

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_web_search_tool(max_results=3)
            result = await tool.run_json({"query": "test"}, None)
            parsed = json.loads(result)
            assert len(parsed["organic_results"]) == 3
            assert parsed["organic_results"][0]["link"].startswith("https://")
            assert "snippet" in parsed["organic_results"][0]

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_strips_disabled_sections(self, _mock_client):
        """Test that disabled sections are removed from response."""
        mock_client = MagicMock()
        mock_client.google.search = AsyncMock(return_value=mock_search_response())

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_web_search_tool(
                include_knowledge_graph=False,
                include_questions=False,
            )
            result = await tool.run_json({"query": "test"}, None)
            parsed = json.loads(result)
            assert "knowledge_graph" not in parsed
            # v2 names the block related_questions, not questions.
            assert "related_questions" not in parsed

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_keeps_ai_overview_by_default(self, _mock_client):
        """The AI Overview ships by default and is not resolved twice."""
        mock_client = MagicMock()
        mock_client.google.search = AsyncMock(return_value=mock_search_response())

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_web_search_tool()
            result = await tool.run_json({"query": "test"}, None)
            parsed = json.loads(result)
            assert "ai_overview" in parsed
            assert "resolve_ai_overview" not in (
                mock_client.google.search.call_args.kwargs
            )

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_opting_out_of_ai_overview_skips_the_extra_call(self, _mock_client):
        """Dropping the block also tells the API not to resolve it."""
        mock_client = MagicMock()
        mock_client.google.search = AsyncMock(return_value=mock_search_response())

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_web_search_tool(include_ai_overview=False)
            result = await tool.run_json({"query": "test"}, None)
            parsed = json.loads(result)
            assert "ai_overview" not in parsed
            call_kwargs = mock_client.google.search.call_args.kwargs
            assert call_kwargs["resolve_ai_overview"] is False

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_related_searches_are_optional(self, _mock_client):
        """include_related gates the v2 related_searches block."""
        mock_client = MagicMock()
        # A fresh dict per call: the tool pops sections in place.
        mock_client.google.search = AsyncMock(
            side_effect=lambda **_: mock_search_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            result = await create_web_search_tool().run_json({"query": "t"}, None)
            assert "related_searches" not in json.loads(result)

            result = await create_web_search_tool(include_related=True).run_json(
                {"query": "t"}, None
            )
            assert "related_searches" in json.loads(result)

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_passes_params_to_sdk(self, _mock_client):
        """v2 params are taken natively and forwarded unchanged."""
        mock_client = MagicMock()
        mock_client.google.search = AsyncMock(return_value=mock_search_response())

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_web_search_tool()
            await tool.run_json(
                {
                    "query": "test",
                    "gl": "us",
                    "hl": "en",
                    "start": 20,
                    "google_domain": "google.co.uk",
                    "device": "mobile",
                    "time_period": "last_week",
                },
                None,
            )
            mock_client.google.search.assert_called_once()
            call_kwargs = mock_client.google.search.call_args.kwargs
            assert call_kwargs["query"] == "test"
            assert call_kwargs["gl"] == "us"
            assert call_kwargs["hl"] == "en"
            assert call_kwargs["google_domain"] == "google.co.uk"
            assert call_kwargs["device"] == "mobile"
            assert call_kwargs["time_period"] == "last_week"
            # start is a zero-based offset passed through verbatim, never
            # derived from a page number.
            assert call_kwargs["start"] == 20

    def test_start_is_not_a_page_number(self):
        """The retired v1 params must not exist on the tool at all."""
        import inspect

        from autogen_scavio.tools import google

        sig = inspect.signature(
            google.create_web_search_tool.__wrapped__
            if hasattr(google.create_web_search_tool, "__wrapped__")
            else google.create_web_search_tool
        )
        assert "page" not in sig.parameters

        tool = create_web_search_tool()
        names = set(tool.schema["parameters"]["properties"])
        assert "start" in names
        assert "gl" in names
        assert "hl" in names
        # v1 is retired: no page / country_code / language / search_type /
        # light_request anywhere on the tool surface.
        assert names.isdisjoint(
            {"page", "country_code", "language", "search_type", "light_request"}
        )

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_omits_unset_params(self, _mock_client):
        """Unset optional params are not sent as nulls."""
        mock_client = MagicMock()
        mock_client.google.search = AsyncMock(return_value=mock_search_response())

        with patch("autogen_scavio._client._async_client", mock_client):
            await create_web_search_tool().run_json({"query": "test"}, None)
            call_kwargs = mock_client.google.search.call_args.kwargs
            assert call_kwargs == {"query": "test"}


class TestGoogleVerticals:
    """One call test per v2 vertical: right SDK method, right params, cap."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_ai_mode(self, _mock_client):
        mock_client = MagicMock()
        mock_client.google.ai_mode = AsyncMock(
            return_value=mock_google_ai_mode_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_google_ai_mode_tool(max_results=3)
            assert tool.name == "scavio_google_ai_mode"
            parsed = json.loads(
                await tool.run_json({"query": "what is rag", "gl": "us"}, None)
            )
            assert len(parsed["references"]) == 3
            assert parsed["text_blocks"]
            assert mock_client.google.ai_mode.call_args.kwargs["gl"] == "us"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_maps_search(self, _mock_client):
        mock_client = MagicMock()
        mock_client.google.maps_search = AsyncMock(
            return_value=mock_google_maps_search_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_google_maps_search_tool(max_results=4)
            assert tool.name == "scavio_google_maps_search"
            parsed = json.loads(
                await tool.run_json(
                    {"query": "coffee", "ll": "@40.7128,-74.0060,13z", "start": 20},
                    None,
                )
            )
            assert len(parsed["local_results"]) == 4
            kwargs = mock_client.google.maps_search.call_args.kwargs
            assert kwargs["ll"] == "@40.7128,-74.0060,13z"
            assert kwargs["start"] == 20

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_maps_place(self, _mock_client):
        mock_client = MagicMock()
        mock_client.google.maps_place = AsyncMock(
            return_value=mock_google_maps_place_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_google_maps_place_tool()
            assert tool.name == "scavio_google_maps_place"
            parsed = json.loads(await tool.run_json({"place_id": "ChIJ_1"}, None))
            assert parsed["place_results"]["place_id"] == "ChIJ_1"
            # data_cid was not given, so it is not forwarded as a null.
            assert mock_client.google.maps_place.call_args.kwargs == {
                "place_id": "ChIJ_1"
            }

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_maps_reviews(self, _mock_client):
        mock_client = MagicMock()
        mock_client.google.maps_reviews = AsyncMock(
            return_value=mock_google_maps_reviews_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_google_maps_reviews_tool(max_results=2)
            assert tool.name == "scavio_google_maps_reviews"
            parsed = json.loads(
                await tool.run_json(
                    {"data_id": "0x89c2:0x1", "sort_by": "newest"}, None
                )
            )
            assert len(parsed["reviews"]) == 2
            assert mock_client.google.maps_reviews.call_args.kwargs["sort_by"] == (
                "newest"
            )

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_shopping(self, _mock_client):
        mock_client = MagicMock()
        mock_client.google.shopping = AsyncMock(
            return_value=mock_google_shopping_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_google_shopping_tool(max_results=3)
            assert tool.name == "scavio_google_shopping"
            parsed = json.loads(
                await tool.run_json({"query": "airpods", "sort_by": 1}, None)
            )
            assert len(parsed["shopping_results"]) == 3
            # sort_by is numeric on search, unlike the product endpoint.
            assert mock_client.google.shopping.call_args.kwargs["sort_by"] == 1

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_shopping_product(self, _mock_client):
        mock_client = MagicMock()
        mock_client.google.shopping_product = AsyncMock(
            return_value=mock_google_shopping_product_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_google_shopping_product_tool()
            assert tool.name == "scavio_google_shopping_product"
            parsed = json.loads(
                await tool.run_json(
                    {
                        "catalog_id": "cat_1",
                        "query": "airpods",
                        "sort_by": "total_price",
                    },
                    None,
                )
            )
            assert parsed["product_results"]["title"] == "Product 1"
            # sort_by is a string enum here, unlike shopping search.
            assert mock_client.google.shopping_product.call_args.kwargs["sort_by"] == (
                "total_price"
            )

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_shopping_stores(self, _mock_client):
        mock_client = MagicMock()
        mock_client.google.shopping_stores = AsyncMock(
            return_value=mock_google_shopping_stores_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_google_shopping_stores_tool(max_results=3)
            assert tool.name == "scavio_google_shopping_stores"
            parsed = json.loads(
                await tool.run_json(
                    {"catalog_id": "cat_1", "next_page_token": "tok"}, None
                )
            )
            assert len(parsed["product_results"]["stores"]) == 3

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_flights(self, _mock_client):
        mock_client = MagicMock()
        mock_client.google.flights = AsyncMock(
            return_value=mock_google_flights_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_google_flights_tool(max_results=2)
            assert tool.name == "scavio_google_flights"
            parsed = json.loads(
                await tool.run_json(
                    {
                        "departure_id": "JFK",
                        "arrival_id": "LAX",
                        "outbound_date": "2026-09-01",
                        "type": 2,
                    },
                    None,
                )
            )
            assert len(parsed["best_flights"]) == 2
            assert len(parsed["other_flights"]) == 2
            assert mock_client.google.flights.call_args.kwargs["type"] == 2

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_hotels(self, _mock_client):
        mock_client = MagicMock()
        mock_client.google.hotels = AsyncMock(
            return_value=mock_google_hotels_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_google_hotels_tool(max_results=2)
            assert tool.name == "scavio_google_hotels"
            parsed = json.loads(
                await tool.run_json(
                    {
                        "query": "Paris hotels",
                        "check_in_date": "2026-09-01",
                        "check_out_date": "2026-09-04",
                    },
                    None,
                )
            )
            assert len(parsed["properties"]) == 2
            assert parsed["properties"][0]["detail_token"] == "tok_1"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_hotels_detail(self, _mock_client):
        mock_client = MagicMock()
        mock_client.google.hotels_detail = AsyncMock(
            return_value=mock_google_hotels_detail_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_google_hotels_detail_tool()
            assert tool.name == "scavio_google_hotels_detail"
            parsed = json.loads(
                await tool.run_json(
                    {
                        "detail_token": "tok_1",
                        "check_in_date": "2026-09-01",
                        "check_out_date": "2026-09-04",
                    },
                    None,
                )
            )
            assert parsed["property"]["booking_sources"]

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_news(self, _mock_client):
        mock_client = MagicMock()
        mock_client.google.news = AsyncMock(return_value=mock_google_news_response(10))

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_google_news_tool(max_results=3)
            assert tool.name == "scavio_google_news"
            parsed = json.loads(await tool.run_json({"query": "ai", "so": 1}, None))
            assert len(parsed["news_results"]) == 3
            # Only the driver that was set is sent; the rest stay absent.
            assert mock_client.google.news.call_args.kwargs == {"query": "ai", "so": 1}

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_trends(self, _mock_client):
        mock_client = MagicMock()
        mock_client.google.trends = AsyncMock(
            return_value=mock_google_trends_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_google_trends_tool()
            assert tool.name == "scavio_google_trends"
            parsed = json.loads(
                await tool.run_json({"query": "rag", "geo": "US", "cat": "71"}, None)
            )
            assert parsed["interest_over_time"]["timeline_data"]
            kwargs = mock_client.google.trends.call_args.kwargs
            # geo, uppercase, not gl; cat is a string here.
            assert kwargs["geo"] == "US"
            assert kwargs["cat"] == "71"
            assert "gl" not in kwargs

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_trending(self, _mock_client):
        mock_client = MagicMock()
        mock_client.google.trending = AsyncMock(
            return_value=mock_google_trending_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_google_trending_tool(max_results=5)
            assert tool.name == "scavio_google_trending"
            parsed = json.loads(
                await tool.run_json({"geo": "US", "cat": 0, "sort": "recency"}, None)
            )
            assert len(parsed["trends"]) == 5
            kwargs = mock_client.google.trending.call_args.kwargs
            # cat is a number here, and the field is sort, not sort_by.
            assert kwargs["cat"] == 0
            assert kwargs["sort"] == "recency"
