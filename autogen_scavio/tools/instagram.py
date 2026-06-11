"""Scavio Instagram tools for AutoGen."""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list


def create_instagram_profile_tool() -> FunctionTool:
    """Create an Instagram profile lookup tool."""

    async def scavio_instagram_profile(
        username: str | None = None,
        user_id: str | None = None,
    ) -> str:
        """Look up an Instagram user profile by username or user_id.

        Args:
            username: Instagram username to look up.
            user_id: Instagram user_id to look up.

        Returns:
            JSON string with user profile information.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "username": username,
            "user_id": user_id,
        }.items() if v is not None}

        raw = await client.instagram.profile(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_instagram_profile,
        description="Look up an Instagram user profile by username or user_id.",
    )


def create_instagram_user_posts_tool(max_results: int = 5) -> FunctionTool:
    """Create an Instagram user posts tool with the given configuration."""

    async def scavio_instagram_user_posts(
        username: str | None = None,
        user_id: str | None = None,
        count: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """Fetch an Instagram user's posts.

        Args:
            username: Instagram username to look up.
            user_id: Instagram user_id to look up.
            count: Number of results to request.
            cursor: Pagination cursor from previous response.

        Returns:
            JSON string with the user's posts.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "username": username,
            "user_id": user_id,
            "count": count,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.instagram.user_posts(**params)

        truncate_list(raw, ["data", "items"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_instagram_user_posts,
        description="Fetch an Instagram user's posts.",
    )


def create_instagram_user_reels_tool(max_results: int = 5) -> FunctionTool:
    """Create an Instagram user reels tool with the given configuration."""

    async def scavio_instagram_user_reels(
        username: str | None = None,
        user_id: str | None = None,
        count: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """Fetch an Instagram user's reels.

        Args:
            username: Instagram username to look up.
            user_id: Instagram user_id to look up.
            count: Number of results to request.
            cursor: Pagination cursor from previous response.

        Returns:
            JSON string with the user's reels.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "username": username,
            "user_id": user_id,
            "count": count,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.instagram.user_reels(**params)

        truncate_list(raw, ["data", "items"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_instagram_user_reels,
        description="Fetch an Instagram user's reels.",
    )


def create_instagram_user_tagged_tool(max_results: int = 5) -> FunctionTool:
    """Create an Instagram user tagged tool with the given configuration."""

    async def scavio_instagram_user_tagged(
        username: str | None = None,
        user_id: str | None = None,
        count: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """Fetch posts an Instagram user is tagged in.

        Args:
            username: Instagram username to look up.
            user_id: Instagram user_id to look up.
            count: Number of results to request.
            cursor: Pagination cursor from previous response.

        Returns:
            JSON string with posts the user is tagged in.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "username": username,
            "user_id": user_id,
            "count": count,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.instagram.user_tagged(**params)

        truncate_list(raw, ["data", "items"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_instagram_user_tagged,
        description="Fetch posts an Instagram user is tagged in.",
    )


def create_instagram_user_stories_tool() -> FunctionTool:
    """Create an Instagram user stories tool."""

    async def scavio_instagram_user_stories(
        username: str | None = None,
        user_id: str | None = None,
    ) -> str:
        """Fetch an Instagram user's active stories.

        Args:
            username: Instagram username to look up.
            user_id: Instagram user_id to look up.

        Returns:
            JSON string with the user's active stories.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "username": username,
            "user_id": user_id,
        }.items() if v is not None}

        raw = await client.instagram.user_stories(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_instagram_user_stories,
        description="Fetch an Instagram user's active stories.",
    )


def create_instagram_post_tool() -> FunctionTool:
    """Create an Instagram post detail tool."""

    async def scavio_instagram_post(
        url: str | None = None,
        media_id: str | None = None,
        shortcode: str | None = None,
    ) -> str:
        """Fetch details for a single Instagram post by url, media_id, or shortcode.

        Args:
            url: The Instagram post URL.
            media_id: The Instagram media ID.
            shortcode: The Instagram post shortcode.

        Returns:
            JSON string with post details.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "url": url,
            "media_id": media_id,
            "shortcode": shortcode,
        }.items() if v is not None}

        raw = await client.instagram.post(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_instagram_post,
        description="Fetch details for a single Instagram post by url, media_id, or shortcode.",
    )


def create_instagram_post_comments_tool(max_results: int = 10) -> FunctionTool:
    """Create an Instagram post comments tool with the given configuration."""

    async def scavio_instagram_post_comments(
        shortcode: str | None = None,
        url: str | None = None,
        cursor: str | None = None,
        sort_order: str | None = None,
    ) -> str:
        """Fetch comments on an Instagram post.

        Args:
            shortcode: The Instagram post shortcode.
            url: The Instagram post URL.
            cursor: Pagination cursor from previous response.
            sort_order: Comment sort order ("popular" or "newest").

        Returns:
            JSON string with post comments.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "shortcode": shortcode,
            "url": url,
            "cursor": cursor,
            "sort_order": sort_order,
        }.items() if v is not None}

        raw = await client.instagram.post_comments(**params)

        truncate_list(raw, ["data", "comments"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_instagram_post_comments,
        description="Fetch comments on an Instagram post.",
    )


def create_instagram_comment_replies_tool(max_results: int = 10) -> FunctionTool:
    """Create an Instagram comment replies tool with the given configuration."""

    async def scavio_instagram_comment_replies(
        media_id: str,
        comment_id: str,
        cursor: str | None = None,
    ) -> str:
        """Fetch replies to a specific comment on an Instagram post.

        Args:
            media_id: The Instagram media ID.
            comment_id: The comment ID to fetch replies for.
            cursor: Pagination cursor from previous response.

        Returns:
            JSON string with comment replies.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "media_id": media_id,
            "comment_id": comment_id,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.instagram.comment_replies(**params)

        truncate_list(raw, ["data", "comments"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_instagram_comment_replies,
        description="Fetch replies to a specific comment on an Instagram post.",
    )


def create_instagram_search_users_tool(max_results: int = 5) -> FunctionTool:
    """Create an Instagram user search tool with the given configuration."""

    async def scavio_instagram_search_users(
        keyword: str,
        cursor: str | None = None,
    ) -> str:
        """Search Instagram users by keyword.

        Args:
            keyword: Search keyword.
            cursor: Pagination cursor from previous response.

        Returns:
            JSON string with matching Instagram users.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "keyword": keyword,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.instagram.search_users(**params)

        truncate_list(raw, ["data", "users"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_instagram_search_users,
        description="Search Instagram users by keyword.",
    )


def create_instagram_search_hashtags_tool(max_results: int = 5) -> FunctionTool:
    """Create an Instagram hashtag search tool with the given configuration."""

    async def scavio_instagram_search_hashtags(
        keyword: str,
        cursor: str | None = None,
    ) -> str:
        """Search Instagram hashtags by keyword.

        Args:
            keyword: Search keyword.
            cursor: Pagination cursor from previous response.

        Returns:
            JSON string with matching Instagram hashtags.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "keyword": keyword,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.instagram.search_hashtags(**params)

        truncate_list(raw, ["data", "hashtags"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_instagram_search_hashtags,
        description="Search Instagram hashtags by keyword.",
    )


def create_instagram_user_followers_tool(max_results: int = 10) -> FunctionTool:
    """Create an Instagram user followers tool with the given configuration."""

    async def scavio_instagram_user_followers(
        username: str | None = None,
        user_id: str | None = None,
        count: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """Fetch an Instagram user's followers.

        Args:
            username: Instagram username to look up.
            user_id: Instagram user_id to look up.
            count: Number of followers to request.
            cursor: Pagination cursor from previous response.

        Returns:
            JSON string with the user's followers.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "username": username,
            "user_id": user_id,
            "count": count,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.instagram.user_followers(**params)

        truncate_list(raw, ["data", "users"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_instagram_user_followers,
        description="Fetch an Instagram user's followers.",
    )


def create_instagram_user_followings_tool(max_results: int = 10) -> FunctionTool:
    """Create an Instagram user followings tool with the given configuration."""

    async def scavio_instagram_user_followings(
        username: str | None = None,
        user_id: str | None = None,
        count: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """Fetch accounts an Instagram user is following.

        Args:
            username: Instagram username to look up.
            user_id: Instagram user_id to look up.
            count: Number of followings to request.
            cursor: Pagination cursor from previous response.

        Returns:
            JSON string with accounts the user is following.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "username": username,
            "user_id": user_id,
            "count": count,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.instagram.user_followings(**params)

        truncate_list(raw, ["data", "users"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_instagram_user_followings,
        description="Fetch accounts an Instagram user is following.",
    )
