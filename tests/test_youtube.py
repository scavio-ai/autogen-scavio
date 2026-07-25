"""Tests for Scavio YouTube tools."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

from autogen_scavio.tools.youtube import (
    create_youtube_channel_tool,
    create_youtube_channel_videos_tool,
    create_youtube_comments_tool,
    create_youtube_metadata_tool,
    create_youtube_search_tool,
    create_youtube_streams_tool,
    create_youtube_transcript_tool,
    create_youtube_video_tool,
)
from tests.conftest import (
    mock_youtube_channel_response,
    mock_youtube_channel_videos_response,
    mock_youtube_comments_response,
    mock_youtube_metadata_response,
    mock_youtube_search_response,
    mock_youtube_streams_response,
    mock_youtube_transcript_response,
    mock_youtube_video_response,
)


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

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_passes_features_and_cursor(self, _mock_client):
        """Test that features and cursor are forwarded to the SDK."""
        mock_client = MagicMock()
        mock_client.youtube.search = AsyncMock(
            return_value=mock_youtube_search_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_youtube_search_tool()
            await tool.run_json(
                {"query": "test", "features": ["hd", "4k"], "cursor": "abc"}, None
            )
            call_kwargs = mock_client.youtube.search.call_args.kwargs
            assert call_kwargs["features"] == ["hd", "4k"]
            assert call_kwargs["cursor"] == "abc"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_passes_legacy_booleans(self, _mock_client):
        """Test that legacy boolean init args map to their wire flags."""
        mock_client = MagicMock()
        mock_client.youtube.search = AsyncMock(
            return_value=mock_youtube_search_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_youtube_search_tool(fourk=True, hdr=True, vr180=True)
            await tool.run_json({"query": "test"}, None)
            call_kwargs = mock_client.youtube.search.call_args.kwargs
            assert call_kwargs["4k"] is True
            assert call_kwargs["hdr"] is True
            assert call_kwargs["vr180"] is True


class TestYouTubeVideoTool:
    """Tests for create_youtube_video_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_youtube_video_tool()
        assert tool.name == "scavio_youtube_video"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_video(self, _mock_client):
        """Test that video details are returned."""
        mock_client = MagicMock()
        mock_client.youtube.video = AsyncMock(
            return_value=mock_youtube_video_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_youtube_video_tool()
            result = await tool.run_json({"video_id": "vid_1"}, None)
            parsed = json.loads(result)
            assert parsed["data"]["video_id"] == "vid_1"
            assert mock_client.youtube.video.call_args.kwargs["video_id"] == "vid_1"


class TestYouTubeCommentsTool:
    """Tests for create_youtube_comments_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_youtube_comments_tool()
        assert tool.name == "scavio_youtube_comments"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_comments(self, _mock_client):
        """Test that comments are truncated to max_results."""
        mock_client = MagicMock()
        mock_client.youtube.comments = AsyncMock(
            return_value=mock_youtube_comments_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_youtube_comments_tool(max_results=4)
            result = await tool.run_json(
                {"video_id": "vid_1", "cursor": "abc"}, None
            )
            parsed = json.loads(result)
            assert len(parsed["data"]["comments"]) == 4
            assert mock_client.youtube.comments.call_args.kwargs["cursor"] == "abc"


class TestYouTubeTranscriptTool:
    """Tests for create_youtube_transcript_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_youtube_transcript_tool()
        assert tool.name == "scavio_youtube_transcript"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_transcript(self, _mock_client):
        """Test that transcript content is returned."""
        mock_client = MagicMock()
        mock_client.youtube.transcript = AsyncMock(
            return_value=mock_youtube_transcript_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_youtube_transcript_tool()
            result = await tool.run_json(
                {"video_id": "vid_1", "format": "srt"}, None
            )
            parsed = json.loads(result)
            assert parsed["data"]["content"] == "This is a transcript."
            assert mock_client.youtube.transcript.call_args.kwargs["format"] == "srt"


class TestYouTubeChannelTool:
    """Tests for create_youtube_channel_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_youtube_channel_tool()
        assert tool.name == "scavio_youtube_channel"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_channel(self, _mock_client):
        """Test that channel info is returned."""
        mock_client = MagicMock()
        mock_client.youtube.channel = AsyncMock(
            return_value=mock_youtube_channel_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_youtube_channel_tool()
            result = await tool.run_json({"channel_id": "chan_1"}, None)
            parsed = json.loads(result)
            assert parsed["data"]["channel_id"] == "chan_1"


class TestYouTubeChannelVideosTool:
    """Tests for create_youtube_channel_videos_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_youtube_channel_videos_tool()
        assert tool.name == "scavio_youtube_channel_videos"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_videos(self, _mock_client):
        """Test that channel videos are truncated to max_results."""
        mock_client = MagicMock()
        mock_client.youtube.channel_videos = AsyncMock(
            return_value=mock_youtube_channel_videos_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_youtube_channel_videos_tool(max_results=3)
            result = await tool.run_json({"channel_id": "chan_1"}, None)
            parsed = json.loads(result)
            assert len(parsed["data"]["results"]) == 3


class TestYouTubeStreamsTool:
    """Tests for create_youtube_streams_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_youtube_streams_tool()
        assert tool.name == "scavio_youtube_streams"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_streams(self, _mock_client):
        """Test that stream formats are returned."""
        mock_client = MagicMock()
        mock_client.youtube.streams = AsyncMock(
            return_value=mock_youtube_streams_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_youtube_streams_tool()
            result = await tool.run_json({"video_id": "vid_1"}, None)
            parsed = json.loads(result)
            assert parsed["data"]["formats"][0]["itag"] == 18


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
