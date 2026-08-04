"""Tests for Scavio X (formerly Twitter) tools."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

from autogen_scavio.tools.x import (
    create_x_search_tool,
    create_x_trending_tool,
    create_x_tweet_comments_tool,
    create_x_tweet_retweeters_tool,
    create_x_tweet_tool,
    create_x_user_followers_tool,
    create_x_user_followings_tool,
    create_x_user_media_tool,
    create_x_user_replies_tool,
    create_x_user_tool,
    create_x_user_tweets_tool,
)
from tests.conftest import (
    mock_x_followers_response,
    mock_x_followings_response,
    mock_x_retweeters_response,
    mock_x_timeline_response,
    mock_x_trending_response,
    mock_x_tweet_response,
    mock_x_user_response,
)


class TestXSearchTool:
    """Tests for create_x_search_tool."""

    def test_creates_function_tool(self):
        tool = create_x_search_tool()
        assert tool.name == "scavio_x_search"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_uses_search_not_query(self, _mock_client):
        """The wire field is `search`; `query` does not exist on this endpoint."""
        mock_client = MagicMock()
        mock_client.x.search = AsyncMock(return_value=mock_x_timeline_response())

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_x_search_tool()
            await tool.run_json({"search": "scavio", "search_type": "Latest"}, None)
            kwargs = mock_client.x.search.call_args.kwargs
            assert kwargs["search"] == "scavio"
            assert kwargs["search_type"] == "Latest"
            assert "query" not in kwargs

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_timeline(self, _mock_client):
        mock_client = MagicMock()
        mock_client.x.search = AsyncMock(return_value=mock_x_timeline_response(10))

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_x_search_tool(max_results=3)
            parsed = json.loads(await tool.run_json({"search": "scavio"}, None))
            assert len(parsed["data"]["timeline"]) == 3
            assert parsed["data"]["next_cursor"] == "next"


class TestXTweetTools:
    """Tests for the tweet-scoped tools."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_tweet(self, _mock_client):
        mock_client = MagicMock()
        mock_client.x.tweet = AsyncMock(return_value=mock_x_tweet_response())

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_x_tweet_tool()
            assert tool.name == "scavio_x_tweet"
            parsed = json.loads(await tool.run_json({"tweet_id": "1808168"}, None))
            assert parsed["data"]["text"] == "Tweet 1"
            # favorites, not likes.
            assert "favorites" in parsed["data"]

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_tweet_comments(self, _mock_client):
        mock_client = MagicMock()
        mock_client.x.tweet_comments = AsyncMock(
            return_value=mock_x_timeline_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_x_tweet_comments_tool(max_results=4)
            assert tool.name == "scavio_x_tweet_comments"
            parsed = json.loads(
                await tool.run_json({"tweet_id": "1808168", "rank": "latest"}, None)
            )
            # Replies land under timeline, flattened from thread/timeline.
            assert len(parsed["data"]["timeline"]) == 4
            # rank is lowercase, unlike search_type.
            assert mock_client.x.tweet_comments.call_args.kwargs["rank"] == "latest"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_tweet_retweeters(self, _mock_client):
        mock_client = MagicMock()
        mock_client.x.tweet_retweeters = AsyncMock(
            return_value=mock_x_retweeters_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_x_tweet_retweeters_tool(max_results=2)
            assert tool.name == "scavio_x_tweet_retweeters"
            parsed = json.loads(await tool.run_json({"tweet_id": "1808168"}, None))
            # The response key is retweeters, mapped from upstream retweets.
            assert len(parsed["data"]["retweeters"]) == 2


class TestXUserTools:
    """Tests for the user-scoped tools."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_user(self, _mock_client):
        mock_client = MagicMock()
        mock_client.x.user = AsyncMock(return_value=mock_x_user_response())

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_x_user_tool()
            assert tool.name == "scavio_x_user"
            parsed = json.loads(await tool.run_json({"screen_name": "elonmusk"}, None))
            assert parsed["data"]["screen_name"] == "elonmusk"
            assert mock_client.x.user.call_args.kwargs == {"screen_name": "elonmusk"}

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_user_tweets(self, _mock_client):
        mock_client = MagicMock()
        mock_client.x.user_tweets = AsyncMock(return_value=mock_x_timeline_response(10))

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_x_user_tweets_tool(max_results=3)
            assert tool.name == "scavio_x_user_tweets"
            parsed = json.loads(await tool.run_json({"screen_name": "elonmusk"}, None))
            assert len(parsed["data"]["timeline"]) == 3

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_user_replies(self, _mock_client):
        mock_client = MagicMock()
        mock_client.x.user_replies = AsyncMock(
            return_value=mock_x_timeline_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_x_user_replies_tool(max_results=3)
            assert tool.name == "scavio_x_user_replies"
            parsed = json.loads(
                await tool.run_json({"screen_name": "elonmusk", "cursor": "c"}, None)
            )
            assert len(parsed["data"]["timeline"]) == 3
            assert mock_client.x.user_replies.call_args.kwargs["cursor"] == "c"

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_user_media(self, _mock_client):
        mock_client = MagicMock()
        mock_client.x.user_media = AsyncMock(return_value=mock_x_timeline_response(10))

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_x_user_media_tool(max_results=2)
            assert tool.name == "scavio_x_user_media"
            parsed = json.loads(await tool.run_json({"screen_name": "elonmusk"}, None))
            assert len(parsed["data"]["timeline"]) == 2

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_user_followers(self, _mock_client):
        mock_client = MagicMock()
        mock_client.x.user_followers = AsyncMock(
            return_value=mock_x_followers_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_x_user_followers_tool(max_results=4)
            assert tool.name == "scavio_x_user_followers"
            parsed = json.loads(await tool.run_json({"screen_name": "elonmusk"}, None))
            assert len(parsed["data"]["followers"]) == 4
            assert parsed["data"]["followers_count"] == 220000000

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_user_followings_uses_singular_key(self, _mock_client):
        """The array is `following`, not `followings`."""
        mock_client = MagicMock()
        mock_client.x.user_followings = AsyncMock(
            return_value=mock_x_followings_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_x_user_followings_tool(max_results=4)
            assert tool.name == "scavio_x_user_followings"
            parsed = json.loads(await tool.run_json({"screen_name": "elonmusk"}, None))
            assert len(parsed["data"]["following"]) == 4
            assert "followings" not in parsed["data"]


class TestXTrendingTool:
    """Tests for create_x_trending_tool."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_trending(self, _mock_client):
        mock_client = MagicMock()
        mock_client.x.trending = AsyncMock(return_value=mock_x_trending_response(10))

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_x_trending_tool(max_results=5)
            assert tool.name == "scavio_x_trending"
            parsed = json.loads(await tool.run_json({"country": "UnitedStates"}, None))
            assert len(parsed["data"]["trends"]) == 5
            # A country NAME, not an ISO code.
            assert mock_client.x.trending.call_args.kwargs == {
                "country": "UnitedStates"
            }

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_trending_without_country(self, _mock_client):
        mock_client = MagicMock()
        mock_client.x.trending = AsyncMock(return_value=mock_x_trending_response(3))

        with patch("autogen_scavio._client._async_client", mock_client):
            await create_x_trending_tool().run_json({}, None)
            assert mock_client.x.trending.call_args.kwargs == {}
