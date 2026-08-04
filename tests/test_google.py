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
        """Test that search params are forwarded to the SDK."""
        mock_client = MagicMock()
        mock_client.google.search = AsyncMock(return_value=mock_search_response())

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_web_search_tool()
            await tool.run_json(
                {
                    "query": "test",
                    "country_code": "us",
                    "language": "en",
                    "page": 3,
                },
                None,
            )
            mock_client.google.search.assert_called_once()
            call_kwargs = mock_client.google.search.call_args.kwargs
            assert call_kwargs["query"] == "test"
            # v1 params are mapped to their v2 equivalents.
            assert call_kwargs["gl"] == "us"
            assert call_kwargs["hl"] == "en"
            assert call_kwargs["start"] == 20
            # Dead v1 params must not be forwarded.
            assert "search_type" not in call_kwargs
            assert "light_request" not in call_kwargs
            assert "country_code" not in call_kwargs
            assert "language" not in call_kwargs
            assert "page" not in call_kwargs
