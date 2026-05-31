"""Tests for Scavio TikTok tools."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

from autogen_scavio.tools.tiktok import (
    create_tiktok_comment_replies_tool,
    create_tiktok_hashtag_tool,
    create_tiktok_hashtag_videos_tool,
    create_tiktok_profile_tool,
    create_tiktok_search_users_tool,
    create_tiktok_search_videos_tool,
    create_tiktok_user_followers_tool,
    create_tiktok_user_followings_tool,
    create_tiktok_user_posts_tool,
    create_tiktok_video_comments_tool,
    create_tiktok_video_tool,
)
from tests.conftest import (
    mock_tiktok_comments_response,
    mock_tiktok_followers_response,
    mock_tiktok_hashtag_response,
    mock_tiktok_profile_response,
    mock_tiktok_search_videos_response,
    mock_tiktok_users_response,
    mock_tiktok_video_list_response,
)


class TestTikTokProfileTool:
    """Tests for create_tiktok_profile_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_tiktok_profile_tool()
        assert tool.name == "scavio_tiktok_profile"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_profile(self, _mock_client):
        """Test that profile data is returned."""
        mock_client = MagicMock()
        mock_client.tiktok.profile = AsyncMock(
            return_value=mock_tiktok_profile_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_profile_tool()
            result = await tool.run_json({"username": "testuser"}, None)
            parsed = json.loads(result)
            assert parsed["data"]["user"]["username"] == "testuser"


class TestTikTokUserPostsTool:
    """Tests for create_tiktok_user_posts_tool."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_posts(self, _mock_client):
        """Test that posts are truncated to max_results."""
        mock_client = MagicMock()
        mock_client.tiktok.user_posts = AsyncMock(
            return_value=mock_tiktok_video_list_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_user_posts_tool(max_results=3)
            result = await tool.run_json({"sec_user_id": "MS4wLjAB"}, None)
            parsed = json.loads(result)
            assert len(parsed["data"]["aweme_list"]) == 3


class TestTikTokVideoTool:
    """Tests for create_tiktok_video_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_tiktok_video_tool()
        assert tool.name == "scavio_tiktok_video"


class TestTikTokVideoCommentsTool:
    """Tests for create_tiktok_video_comments_tool."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_comments(self, _mock_client):
        """Test that comments are truncated to max_results."""
        mock_client = MagicMock()
        mock_client.tiktok.video_comments = AsyncMock(
            return_value=mock_tiktok_comments_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_video_comments_tool(max_results=3)
            result = await tool.run_json({"video_id": "vid_1"}, None)
            parsed = json.loads(result)
            assert len(parsed["data"]["comments"]) == 3


class TestTikTokCommentRepliesTool:
    """Tests for create_tiktok_comment_replies_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_tiktok_comment_replies_tool()
        assert tool.name == "scavio_tiktok_comment_replies"


class TestTikTokSearchVideosTool:
    """Tests for create_tiktok_search_videos_tool."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_search_results(self, _mock_client):
        """Test that search results are truncated."""
        mock_client = MagicMock()
        mock_client.tiktok.search_videos = AsyncMock(
            return_value=mock_tiktok_search_videos_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_search_videos_tool(max_results=3)
            result = await tool.run_json({"keyword": "python"}, None)
            parsed = json.loads(result)
            assert len(parsed["data"]["search_item_list"]) == 3


class TestTikTokSearchUsersTool:
    """Tests for create_tiktok_search_users_tool."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_users(self, _mock_client):
        """Test that user list is truncated."""
        mock_client = MagicMock()
        mock_client.tiktok.search_users = AsyncMock(
            return_value=mock_tiktok_users_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_search_users_tool(max_results=3)
            result = await tool.run_json({"keyword": "cooking"}, None)
            parsed = json.loads(result)
            assert len(parsed["data"]["user_list"]) == 3


class TestTikTokHashtagTool:
    """Tests for create_tiktok_hashtag_tool."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_returns_hashtag_info(self, _mock_client):
        """Test that hashtag info is returned."""
        mock_client = MagicMock()
        mock_client.tiktok.hashtag = AsyncMock(
            return_value=mock_tiktok_hashtag_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_hashtag_tool()
            result = await tool.run_json({"hashtag_name": "python"}, None)
            parsed = json.loads(result)
            assert "challengeInfo" in parsed["data"]


class TestTikTokHashtagVideosTool:
    """Tests for create_tiktok_hashtag_videos_tool."""

    def test_creates_function_tool(self):
        """Test that factory returns a FunctionTool."""
        tool = create_tiktok_hashtag_videos_tool()
        assert tool.name == "scavio_tiktok_hashtag_videos"


class TestTikTokUserFollowersTool:
    """Tests for create_tiktok_user_followers_tool."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_followers(self, _mock_client):
        """Test that followers are truncated."""
        mock_client = MagicMock()
        mock_client.tiktok.user_followers = AsyncMock(
            return_value=mock_tiktok_followers_response(10, "followers")
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_user_followers_tool(max_results=3)
            result = await tool.run_json({"sec_user_id": "MS4wLjAB"}, None)
            parsed = json.loads(result)
            assert len(parsed["data"]["followers"]) == 3


class TestTikTokUserFollowingsTool:
    """Tests for create_tiktok_user_followings_tool."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_followings(self, _mock_client):
        """Test that followings are truncated."""
        mock_client = MagicMock()
        mock_client.tiktok.user_followings = AsyncMock(
            return_value=mock_tiktok_followers_response(10, "followings")
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_tiktok_user_followings_tool(max_results=3)
            result = await tool.run_json({"sec_user_id": "MS4wLjAB"}, None)
            parsed = json.loads(result)
            assert len(parsed["data"]["followings"]) == 3
