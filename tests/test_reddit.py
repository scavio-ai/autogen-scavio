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
    async def test_truncates_posts(self, _mock_client):
        """Test that posts are truncated to max_results."""
        mock_client = MagicMock()
        mock_client.reddit.search = AsyncMock(
            return_value=mock_reddit_search_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_search_tool(max_results=3)
            result = await tool.run_json({"query": "python"}, None)
            parsed = json.loads(result)
            assert len(parsed["data"]["posts"]) == 3


class TestRedditPostTool:
    """Tests for create_reddit_post_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_reddit_post_tool()
        assert tool.name == "scavio_reddit_post"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_post_data(self, _mock_client):
        """Test that post data is returned."""
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
            assert parsed["data"]["post"]["id"] == "post_1"
