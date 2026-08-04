"""Scavio Reddit tools for AutoGen."""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list


def create_reddit_search_tool(max_results: int = 5) -> FunctionTool:
    """Create a Reddit search tool with the given configuration."""

    async def scavio_reddit_search(
        query: str,
        cursor: str | None = None,
    ) -> str:
        """Search Reddit posts by keyword.

        Returns post titles, URLs, subreddits, authors, and scores.

        The endpoint takes only a query and a cursor. There is no type or sort
        filter, so narrow the result set through the query itself.

        Args:
            query: Reddit search query.
            cursor: Pagination cursor (next_cursor from a previous response).

        Returns:
            JSON string with matching Reddit posts under data.results, plus
            next_cursor and has_more for pagination.
        """
        client = get_async_client()

        params: dict = {"query": query}
        if cursor is not None:
            params["cursor"] = cursor

        raw = await client.reddit.search(**params)

        truncate_list(raw, ["data", "results"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_search,
        description=(
            "Search Reddit posts using the Scavio API (1 credit). Query and "
            "cursor only, no type or sort filter."
        ),
    )


def create_reddit_post_tool() -> FunctionTool:
    """Create a Reddit post detail tool."""

    async def scavio_reddit_post(url: str) -> str:
        """Fetch a single Reddit post by URL.

        Args:
            url: Full URL of the Reddit post.

        Returns:
            JSON string with the post as a flat object under data (post_id,
            title, text, url, subreddit, author, score, upvote_ratio,
            num_comments, created_at, is_nsfw, is_video, thumbnail, media).
            Comments are not included.
        """
        client = get_async_client()

        raw = await client.reddit.post(url=url)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_post,
        description=(
            "Fetch a single Reddit post by URL (1 credit). Returns post "
            "metadata only, without comments."
        ),
    )
