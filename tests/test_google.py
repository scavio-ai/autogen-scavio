"""Tests for Scavio Google Search tool."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

from autogen_scavio.tools.google import create_web_search_tool
from tests.conftest import mock_search_response


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
            assert len(parsed["results"]) == 3

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
            assert "questions" not in parsed

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_passes_params_to_sdk(self, _mock_client):
        """Test that search params are forwarded to the SDK."""
        mock_client = MagicMock()
        mock_client.google.search = AsyncMock(return_value=mock_search_response())

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_web_search_tool()
            await tool.run_json(
                {
                    "query": "test",
                    "search_type": "news",
                    "country_code": "us",
                },
                None,
            )
            mock_client.google.search.assert_called_once()
            call_kwargs = mock_client.google.search.call_args.kwargs
            assert call_kwargs["query"] == "test"
            assert call_kwargs["search_type"] == "news"
            assert call_kwargs["country_code"] == "us"
