"""Tests for Scavio YouTube tools."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

from autogen_scavio.tools.youtube import create_youtube_metadata_tool, create_youtube_search_tool
from tests.conftest import mock_youtube_metadata_response, mock_youtube_search_response


class TestYouTubeSearchTool:
    """Tests for create_youtube_search_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_youtube_search_tool()
        assert tool.name == "scavio_youtube_search"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_results(self, _mock_client):
        """Test that results are truncated to max_results."""
        mock_client = MagicMock()
        mock_client.youtube.search = AsyncMock(
            return_value=mock_youtube_search_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_youtube_search_tool(max_results=3)
            result = await tool.run_json({"query": "python tutorial"}, None)
            parsed = json.loads(result)
            assert len(parsed["data"]["results"]) == 3

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_uses_query_param(self, _mock_client):
        """Test that query maps to the 'query' SDK param."""
        mock_client = MagicMock()
        mock_client.youtube.search = AsyncMock(
            return_value=mock_youtube_search_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_youtube_search_tool()
            await tool.run_json({"query": "test"}, None)
            call_kwargs = mock_client.youtube.search.call_args.kwargs
            assert call_kwargs["query"] == "test"
            assert "search" not in call_kwargs


class TestYouTubeMetadataTool:
    """Tests for create_youtube_metadata_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_youtube_metadata_tool()
        assert tool.name == "scavio_youtube_metadata"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_metadata(self, _mock_client):
        """Test that metadata is returned."""
        mock_client = MagicMock()
        mock_client.youtube.metadata = AsyncMock(
            return_value=mock_youtube_metadata_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_youtube_metadata_tool()
            result = await tool.run_json({"video_id": "vid_1"}, None)
            parsed = json.loads(result)
            assert parsed["data"]["video_id"] == "vid_1"
