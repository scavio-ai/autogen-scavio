"""Scavio Reddit tools for AutoGen.

All twelve endpoints cost 1 credit per call. The list keys differ per endpoint
and are worth knowing before chaining: search returns data.results, the
subreddit, user and popular feeds return data.posts, and /reddit/post returns a
flat post object with no comments at all. Comments live on their own endpoints.

Sort values are UPPERCASE and passed through verbatim. Comment and user feeds
take HOT, NEW, TOP, BEST or CONTROVERSIAL; the subreddit feed is the only one
that also accepts RISING.
"""

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


def create_reddit_search_suggestions_tool(max_results: int = 10) -> FunctionTool:
    """Create a Reddit search suggestions tool with the given configuration."""

    async def scavio_reddit_search_suggestions(query: str) -> str:
        """Fetch Reddit autocomplete suggestions for a search query.

        Args:
            query: The partial query to autocomplete, 1 to 500 characters.

        Returns:
            JSON string with data.suggestions, a list of strings, plus
            total_count.
        """
        client = get_async_client()

        raw = await client.reddit.search_suggestions(query=query)

        truncate_list(raw, ["data", "suggestions"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_search_suggestions,
        description=(
            "Fetch Reddit autocomplete suggestions for a search query "
            "(1 credit). Returns plain strings under data.suggestions."
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


def create_reddit_post_comments_tool(max_results: int = 10) -> FunctionTool:
    """Create a Reddit post comments tool with the given configuration."""

    async def scavio_reddit_post_comments(
        post_id: str,
        sort: str | None = None,
        cursor: str | None = None,
    ) -> str:
        """Fetch the top-level comments on a Reddit post.

        The post endpoint carries no comments, so this is the only way to read
        a thread.

        Args:
            post_id: Post fullname such as "t3_1v6ngaf", a bare post id, or a
                post URL. All three are normalized server-side.
            sort: Comment sort order, one of "HOT", "NEW", "TOP", "BEST",
                "CONTROVERSIAL". Uppercase; defaults to "TOP".
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with comments under data.comments (comment_id, text,
            author, score, created_at, depth, reply_cursor), plus next_cursor
            and has_more. Feed a comment's reply_cursor to the comment replies
            tool to expand that subtree.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "post_id": post_id,
            "sort": sort,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.reddit.post_comments(**params)

        truncate_list(raw, ["data", "comments"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_post_comments,
        description=(
            "Fetch the top-level comments on a Reddit post (1 credit). The "
            "post tool returns no comments, so use this for threads."
        ),
    )


def create_reddit_comment_replies_tool(max_results: int = 10) -> FunctionTool:
    """Create a Reddit comment replies tool with the given configuration."""

    async def scavio_reddit_comment_replies(
        post_id: str,
        cursor: str,
        sort: str | None = None,
    ) -> str:
        """Fetch the replies to a specific Reddit comment.

        Args:
            post_id: Post fullname such as "t3_1v6ngaf", or a bare post id.
            cursor: The reply_cursor of a comment from the post comments tool.
                Required: this endpoint cannot be called from a post id alone.
            sort: Comment sort order, one of "HOT", "NEW", "TOP", "BEST",
                "CONTROVERSIAL". Uppercase; defaults to "TOP".

        Returns:
            JSON string with replies under data.replies, same shape as a
            comment, plus next_cursor and has_more.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "post_id": post_id,
            "cursor": cursor,
            "sort": sort,
        }.items() if v is not None}

        raw = await client.reddit.comment_replies(**params)

        truncate_list(raw, ["data", "replies"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_comment_replies,
        description=(
            "Fetch the replies to a Reddit comment (1 credit). Needs the "
            "reply_cursor of a comment from the post comments tool."
        ),
    )


def create_reddit_subreddit_tool() -> FunctionTool:
    """Create a subreddit metadata tool."""

    async def scavio_reddit_subreddit(subreddit: str) -> str:
        """Fetch a subreddit's profile.

        Args:
            subreddit: Subreddit name without the r/ prefix, e.g. "AskReddit".

        Returns:
            JSON string with the subreddit as a flat object under data: name,
            prefixed_name, title, description, public_description,
            subscribers, active_count, type, is_nsfw, icon, banner,
            primary_color, created_at and url. No posts here, use the
            subreddit posts tool for the feed.
        """
        client = get_async_client()

        raw = await client.reddit.subreddit(subreddit=subreddit)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_subreddit,
        description=(
            "Fetch a subreddit's profile and subscriber counts (1 credit). "
            "Pass the bare name, without r/."
        ),
    )


def create_reddit_subreddit_posts_tool(max_results: int = 5) -> FunctionTool:
    """Create a subreddit feed tool with the given configuration."""

    async def scavio_reddit_subreddit_posts(
        subreddit: str,
        sort: str | None = None,
        cursor: str | None = None,
    ) -> str:
        """Fetch a subreddit's post feed.

        Args:
            subreddit: Subreddit name without the r/ prefix.
            sort: Feed sort order, one of "BEST", "HOT", "NEW", "TOP",
                "CONTROVERSIAL", "RISING". Uppercase; defaults to "HOT". This
                is the only Reddit feed that accepts "RISING".
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with posts under data.posts (post_id, title, author,
            author_icon, subreddit, created_at, score, num_comments,
            share_count, url), plus next_cursor and has_more. This feed shape
            carries no text, thumbnail or is_nsfw.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "subreddit": subreddit,
            "sort": sort,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.reddit.subreddit_posts(**params)

        truncate_list(raw, ["data", "posts"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_subreddit_posts,
        description=(
            "Fetch a subreddit's post feed (1 credit). Posts are under "
            "data.posts; sort also accepts RISING here."
        ),
    )


def create_reddit_user_tool() -> FunctionTool:
    """Create a redditor profile tool."""

    async def scavio_reddit_user(username: str) -> str:
        """Fetch a redditor's profile.

        Args:
            username: Reddit username without the u/ prefix, e.g. "spez".

        Returns:
            JSON string with the profile as a flat object under data: name,
            is_employee, is_verified, account_type, is_accepting_pms, is_nsfw,
            avatar, karma, post_karma, comment_karma, description and
            created_at.
        """
        client = get_async_client()

        raw = await client.reddit.user(username=username)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_user,
        description=(
            "Fetch a redditor's profile and karma breakdown (1 credit). Pass "
            "the bare handle, without u/."
        ),
    )


def create_reddit_user_posts_tool(max_results: int = 5) -> FunctionTool:
    """Create a redditor submissions tool with the given configuration."""

    async def scavio_reddit_user_posts(
        username: str,
        sort: str | None = None,
        cursor: str | None = None,
    ) -> str:
        """Fetch the posts a redditor has submitted.

        Args:
            username: Reddit username without the u/ prefix.
            sort: Sort order, one of "HOT", "NEW", "TOP", "BEST",
                "CONTROVERSIAL". Uppercase; defaults to "NEW". No "RISING" on
                user feeds.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with posts under data.posts (post_id, title,
            subreddit, author, score, num_comments, url, created_at, is_nsfw,
            thumbnail), plus next_cursor and has_more.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "username": username,
            "sort": sort,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.reddit.user_posts(**params)

        truncate_list(raw, ["data", "posts"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_user_posts,
        description=(
            "Fetch the posts a redditor has submitted (1 credit). Posts are "
            "under data.posts."
        ),
    )


def create_reddit_user_comments_tool(max_results: int = 10) -> FunctionTool:
    """Create a redditor comments tool with the given configuration."""

    async def scavio_reddit_user_comments(
        username: str,
        sort: str | None = None,
        cursor: str | None = None,
    ) -> str:
        """Fetch the comments a redditor has written.

        Args:
            username: Reddit username without the u/ prefix.
            sort: Sort order, one of "HOT", "NEW", "TOP", "BEST",
                "CONTROVERSIAL". Uppercase; defaults to "NEW".
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with comments under data.comments (comment_id, text,
            author, post with id and title, score, created_at), plus
            next_cursor and has_more. This comment shape nests the post it
            belongs to and carries no depth or reply_cursor.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "username": username,
            "sort": sort,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.reddit.user_comments(**params)

        truncate_list(raw, ["data", "comments"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_user_comments,
        description=(
            "Fetch the comments a redditor has written (1 credit). Each one "
            "names the post it belongs to."
        ),
    )


def create_reddit_popular_tool(max_results: int = 5) -> FunctionTool:
    """Create a Reddit popular feed tool with the given configuration."""

    async def scavio_reddit_popular(cursor: str | None = None) -> str:
        """Fetch the site-wide popular feed, r/popular.

        Args:
            cursor: Pagination cursor from a previous response. The only
                parameter this endpoint takes.

        Returns:
            JSON string with posts under data.posts (post_id, title,
            subreddit, author, score, num_comments, url, created_at, is_nsfw,
            thumbnail), plus next_cursor and has_more.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {"cursor": cursor}.items() if v is not None}

        raw = await client.reddit.popular(**params)

        truncate_list(raw, ["data", "posts"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_popular,
        description=(
            "Fetch the site-wide Reddit popular feed (1 credit). Posts are "
            "under data.posts; cursor is the only parameter."
        ),
    )


def create_reddit_trending_tool(max_results: int = 10) -> FunctionTool:
    """Create a Reddit trending searches tool with the given configuration."""

    async def scavio_reddit_trending() -> str:
        """Fetch the search queries trending on Reddit right now.

        Returns:
            JSON string with data.trending, each entry carrying query and
            raw_query, plus total_count. This endpoint takes no parameters and
            has no cursor.
        """
        client = get_async_client()

        raw = await client.reddit.trending()

        truncate_list(raw, ["data", "trending"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_reddit_trending,
        description=(
            "List the search queries trending on Reddit right now "
            "(1 credit). Takes no parameters."
        ),
    )
