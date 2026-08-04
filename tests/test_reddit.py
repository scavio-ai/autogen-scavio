"""Tests for Scavio Reddit tools."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

from autogen_scavio.tools.reddit import create_reddit_post_tool, create_reddit_search_tool
from tests.conftest import mock_reddit_post_response, mock_reddit_search_response


class TestRedditSearchTool:
    """Tests for create_reddit_search_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_reddit_search_tool()
        assert tool.name == "scavio_reddit_search"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_results(self, _mock_client):
        """Test that data.results is truncated to max_results."""
        mock_client = MagicMock()
        mock_client.reddit.search = AsyncMock(
            return_value=mock_reddit_search_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_search_tool(max_results=3)
            result = await tool.run_json({"query": "python"}, None)
            parsed = json.loads(result)
            assert len(parsed["data"]["results"]) == 3

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_sends_cursor_and_no_phantom_filters(self, _mock_client):
        """Test that only query and cursor reach the SDK."""
        mock_client = MagicMock()
        mock_client.reddit.search = AsyncMock(
            return_value=mock_reddit_search_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_search_tool()
            await tool.run_json({"query": "python", "cursor": "abc"}, None)
            call_kwargs = mock_client.reddit.search.call_args.kwargs
            assert call_kwargs == {"query": "python", "cursor": "abc"}

    def test_has_no_type_or_sort_params(self):
        """The endpoint strips type/sort, so the tool must not offer them."""
        schema = create_reddit_search_tool().schema["parameters"]["properties"]
        assert set(schema) == {"query", "cursor"}


class TestRedditPostTool:
    """Tests for create_reddit_post_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_reddit_post_tool()
        assert tool.name == "scavio_reddit_post"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_flat_post_data(self, _mock_client):
        """Test that the flat post object is returned under data."""
        mock_client = MagicMock()
        mock_client.reddit.post = AsyncMock(
            return_value=mock_reddit_post_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_post_tool()
            result = await tool.run_json(
                {"url": "https://reddit.com/r/test/comments/abc/test"},
                None,
            )
            parsed = json.loads(result)
            assert parsed["data"]["post_id"] == "t3_post_1"
            assert "post" not in parsed["data"]
            assert "comments" not in parsed["data"]
