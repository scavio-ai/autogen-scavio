"""Tests for Scavio Reddit tools."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

from autogen_scavio.tools.reddit import (
    create_reddit_comment_replies_tool,
    create_reddit_popular_tool,
    create_reddit_post_comments_tool,
    create_reddit_post_tool,
    create_reddit_search_suggestions_tool,
    create_reddit_search_tool,
    create_reddit_subreddit_posts_tool,
    create_reddit_subreddit_tool,
    create_reddit_trending_tool,
    create_reddit_user_comments_tool,
    create_reddit_user_posts_tool,
    create_reddit_user_tool,
)
from tests.conftest import (
    mock_reddit_comments_response,
    mock_reddit_feed_response,
    mock_reddit_post_response,
    mock_reddit_replies_response,
    mock_reddit_search_response,
    mock_reddit_subreddit_response,
    mock_reddit_suggestions_response,
    mock_reddit_trending_response,
    mock_reddit_user_comments_response,
    mock_reddit_user_response,
)


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


class TestRedditSearchSuggestionsTool:
    """Tests for create_reddit_search_suggestions_tool."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_truncates_suggestions(self, _mock_client):
        mock_client = MagicMock()
        mock_client.reddit.search_suggestions = AsyncMock(
            return_value=mock_reddit_suggestions_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_search_suggestions_tool(max_results=4)
            assert tool.name == "scavio_reddit_search_suggestions"
            parsed = json.loads(await tool.run_json({"query": "python"}, None))
            assert len(parsed["data"]["suggestions"]) == 4
            assert mock_client.reddit.search_suggestions.call_args.kwargs == {
                "query": "python"
            }

    def test_takes_query_only(self):
        schema = create_reddit_search_suggestions_tool().schema["parameters"]
        assert set(schema["properties"]) == {"query"}


class TestRedditCommentTools:
    """Tests for the post-scoped comment tools."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_post_comments(self, _mock_client):
        mock_client = MagicMock()
        mock_client.reddit.post_comments = AsyncMock(
            return_value=mock_reddit_comments_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_post_comments_tool(max_results=3)
            assert tool.name == "scavio_reddit_post_comments"
            parsed = json.loads(
                await tool.run_json({"post_id": "t3_1v6ngaf", "sort": "NEW"}, None)
            )
            assert len(parsed["data"]["comments"]) == 3
            # reply_cursor is what feeds the replies tool.
            assert parsed["data"]["comments"][0]["reply_cursor"] == "reply_1"
            assert mock_client.reddit.post_comments.call_args.kwargs == {
                "post_id": "t3_1v6ngaf",
                "sort": "NEW",
            }

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_comment_replies_reads_replies_key(self, _mock_client):
        mock_client = MagicMock()
        mock_client.reddit.comment_replies = AsyncMock(
            return_value=mock_reddit_replies_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_comment_replies_tool(max_results=2)
            assert tool.name == "scavio_reddit_comment_replies"
            parsed = json.loads(
                await tool.run_json(
                    {"post_id": "t3_1v6ngaf", "cursor": "reply_1"}, None
                )
            )
            assert len(parsed["data"]["replies"]) == 2
            assert "comments" not in parsed["data"]

    def test_comment_replies_requires_cursor(self):
        """The cursor is mandatory here, unlike on the comments endpoint."""
        schema = create_reddit_comment_replies_tool().schema["parameters"]
        assert set(schema["required"]) == {"post_id", "cursor"}


class TestRedditSubredditTools:
    """Tests for the subreddit tools."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_subreddit_is_flat(self, _mock_client):
        mock_client = MagicMock()
        mock_client.reddit.subreddit = AsyncMock(
            return_value=mock_reddit_subreddit_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_subreddit_tool()
            assert tool.name == "scavio_reddit_subreddit"
            parsed = json.loads(await tool.run_json({"subreddit": "AskReddit"}, None))
            assert parsed["data"]["subscribers"] == 45000000
            assert "posts" not in parsed["data"]

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_subreddit_posts_reads_posts_key(self, _mock_client):
        mock_client = MagicMock()
        mock_client.reddit.subreddit_posts = AsyncMock(
            return_value=mock_reddit_feed_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_subreddit_posts_tool(max_results=3)
            assert tool.name == "scavio_reddit_subreddit_posts"
            parsed = json.loads(
                await tool.run_json({"subreddit": "AskReddit", "sort": "RISING"}, None)
            )
            assert len(parsed["data"]["posts"]) == 3
            assert "results" not in parsed["data"]
            # RISING is accepted here and nowhere else.
            assert mock_client.reddit.subreddit_posts.call_args.kwargs == {
                "subreddit": "AskReddit",
                "sort": "RISING",
            }


class TestRedditUserTools:
    """Tests for the redditor tools."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_user_is_flat(self, _mock_client):
        mock_client = MagicMock()
        mock_client.reddit.user = AsyncMock(return_value=mock_reddit_user_response())

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_user_tool()
            assert tool.name == "scavio_reddit_user"
            parsed = json.loads(await tool.run_json({"username": "spez"}, None))
            assert parsed["data"]["comment_karma"] == 700000
            assert mock_client.reddit.user.call_args.kwargs == {"username": "spez"}

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_user_posts(self, _mock_client):
        mock_client = MagicMock()
        mock_client.reddit.user_posts = AsyncMock(
            return_value=mock_reddit_feed_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_user_posts_tool(max_results=2)
            assert tool.name == "scavio_reddit_user_posts"
            parsed = json.loads(await tool.run_json({"username": "spez"}, None))
            assert len(parsed["data"]["posts"]) == 2
            assert mock_client.reddit.user_posts.call_args.kwargs == {
                "username": "spez"
            }

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_user_comments_nest_their_post(self, _mock_client):
        mock_client = MagicMock()
        mock_client.reddit.user_comments = AsyncMock(
            return_value=mock_reddit_user_comments_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_user_comments_tool(max_results=5)
            assert tool.name == "scavio_reddit_user_comments"
            parsed = json.loads(
                await tool.run_json({"username": "spez", "cursor": "abc"}, None)
            )
            assert len(parsed["data"]["comments"]) == 5
            assert parsed["data"]["comments"][0]["post"]["title"] == "Post 1"
            assert mock_client.reddit.user_comments.call_args.kwargs == {
                "username": "spez",
                "cursor": "abc",
            }


class TestRedditFeedTools:
    """Tests for the site-wide feeds."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_popular_takes_cursor_only(self, _mock_client):
        mock_client = MagicMock()
        mock_client.reddit.popular = AsyncMock(
            return_value=mock_reddit_feed_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_popular_tool(max_results=3)
            assert tool.name == "scavio_reddit_popular"
            parsed = json.loads(await tool.run_json({}, None))
            assert len(parsed["data"]["posts"]) == 3
            assert mock_client.reddit.popular.call_args.kwargs == {}
            assert set(tool.schema["parameters"]["properties"]) == {"cursor"}

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_trending_reads_trending_key(self, _mock_client):
        mock_client = MagicMock()
        mock_client.reddit.trending = AsyncMock(
            return_value=mock_reddit_trending_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_reddit_trending_tool(max_results=4)
            assert tool.name == "scavio_reddit_trending"
            parsed = json.loads(await tool.run_json({}, None))
            assert len(parsed["data"]["trending"]) == 4
            # data.trending, not data.trends as on X.
            assert "trends" not in parsed["data"]
            assert mock_client.reddit.trending.call_args.kwargs == {}

    def test_trending_takes_no_parameters(self):
        schema = create_reddit_trending_tool().schema["parameters"]
        assert schema["properties"] == {}
