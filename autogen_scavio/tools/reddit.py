"""Scavio Reddit tools for AutoGen."""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list


def create_reddit_search_tool(max_results: int = 5) -> FunctionTool:
    """Create a Reddit search tool with the given configuration."""

    async def scavio_reddit_search(
        query: str,
        type: str | None = None,
        sort: str | None = None,
        cursor: str | None = None,
    ) -> str:
        """Search Reddit posts or comments. Returns post titles, URLs, subreddits, authors, and timestamps.

        Args:
            query: Reddit search query.
            type: Search scope - "posts" or "comments".
            sort: Sort order - "new", "relevance", "hot", "top", "comments".
            cursor: Pagination cursor from previous response.

        Returns:
            JSON string with matching Reddit posts or comments.
        """
        client = get_async_client()

        params: dict = {"query": query}
        if type is not None:
            params["type"] = type
        if sort is not None:
            params["sort"] = sort
        if cursor is not None:
            params["cursor"] = cursor

        raw = await client.reddit.search(**params)

        truncate_list(raw, ["data", "posts"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_search,
        description="Search Reddit posts or comments using the Scavio API.",
    )


def create_reddit_post_tool() -> FunctionTool:
    """Create a Reddit post detail tool."""

    async def scavio_reddit_post(url: str) -> str:
        """Fetch a Reddit post's metadata and comment thread.

        Args:
            url: Full URL of the Reddit post.

        Returns:
            JSON string with the post metadata and comment thread.
        """
        client = get_async_client()

        raw = await client.reddit.post(url=url)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_post,
        description="Fetch a Reddit post's metadata and comment thread by URL.",
    )
