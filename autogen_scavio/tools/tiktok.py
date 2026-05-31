"""Scavio TikTok tools for AutoGen."""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list


def create_tiktok_profile_tool() -> FunctionTool:
    """Create a TikTok profile lookup tool."""

    async def scavio_tiktok_profile(
        username: str | None = None,
        sec_user_id: str | None = None,
    ) -> str:
        """Look up a TikTok user profile by username or sec_user_id.

        Args:
            username: TikTok username to look up.
            sec_user_id: TikTok sec_user_id to look up.

        Returns:
            JSON string with user profile information.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "username": username,
            "sec_user_id": sec_user_id,
        }.items() if v is not None}

        raw = await client.tiktok.profile(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_profile,
        description="Look up a TikTok user profile by username or sec_user_id.",
    )


def create_tiktok_user_posts_tool(max_results: int = 5) -> FunctionTool:
    """Create a TikTok user posts tool with the given configuration."""

    async def scavio_tiktok_user_posts(
        sec_user_id: str,
        cursor: str | None = None,
        count: int | None = None,
        sort_type: str | None = None,
    ) -> str:
        """Fetch a TikTok user's posted videos.

        Args:
            sec_user_id: The TikTok user's sec_user_id.
            cursor: Pagination cursor from previous response.
            count: Number of results to request.
            sort_type: Sort order for the results.

        Returns:
            JSON string with the user's posted videos.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "sec_user_id": sec_user_id,
            "cursor": cursor,
            "count": count,
            "sort_type": sort_type,
        }.items() if v is not None}

        raw = await client.tiktok.user_posts(**params)

        truncate_list(raw, ["data", "aweme_list"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_user_posts,
        description="Fetch a TikTok user's posted videos.",
    )


def create_tiktok_video_tool() -> FunctionTool:
    """Create a TikTok video detail tool."""

    async def scavio_tiktok_video(video_id: str) -> str:
        """Fetch details for a single TikTok video.

        Args:
            video_id: The TikTok video ID.

        Returns:
            JSON string with video details.
        """
        client = get_async_client()

        raw = await client.tiktok.video(video_id=video_id)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_video,
        description="Fetch details for a single TikTok video.",
    )


def create_tiktok_video_comments_tool(max_results: int = 10) -> FunctionTool:
    """Create a TikTok video comments tool with the given configuration."""

    async def scavio_tiktok_video_comments(
        video_id: str,
        cursor: str | None = None,
        count: int | None = None,
    ) -> str:
        """Fetch comments on a TikTok video.

        Args:
            video_id: The TikTok video ID.
            cursor: Pagination cursor from previous response.
            count: Number of comments to request.

        Returns:
            JSON string with video comments.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "video_id": video_id,
            "cursor": cursor,
            "count": count,
        }.items() if v is not None}

        raw = await client.tiktok.video_comments(**params)

        truncate_list(raw, ["data", "comments"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_video_comments,
        description="Fetch comments on a TikTok video.",
    )


def create_tiktok_comment_replies_tool(max_results: int = 10) -> FunctionTool:
    """Create a TikTok comment replies tool with the given configuration."""

    async def scavio_tiktok_comment_replies(
        video_id: str,
        comment_id: str,
        cursor: str | None = None,
        count: int | None = None,
    ) -> str:
        """Fetch replies to a specific comment on a TikTok video.

        Args:
            video_id: The TikTok video ID.
            comment_id: The comment ID to fetch replies for.
            cursor: Pagination cursor from previous response.
            count: Number of replies to request.

        Returns:
            JSON string with comment replies.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "video_id": video_id,
            "comment_id": comment_id,
            "cursor": cursor,
            "count": count,
        }.items() if v is not None}

        raw = await client.tiktok.comment_replies(**params)

        truncate_list(raw, ["data", "comments"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_comment_replies,
        description="Fetch replies to a specific comment on a TikTok video.",
    )


def create_tiktok_search_videos_tool(max_results: int = 5) -> FunctionTool:
    """Create a TikTok video search tool with the given configuration."""

    async def scavio_tiktok_search_videos(
        keyword: str,
        cursor: str | None = None,
        count: int | None = None,
        sort_type: str | None = None,
        publish_time: str | None = None,
    ) -> str:
        """Search TikTok videos by keyword.

        Args:
            keyword: Search keyword.
            cursor: Pagination cursor from previous response.
            count: Number of results to request.
            sort_type: Sort order for the results.
            publish_time: Filter by publish time.

        Returns:
            JSON string with matching TikTok videos.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "keyword": keyword,
            "cursor": cursor,
            "count": count,
            "sort_type": sort_type,
            "publish_time": publish_time,
        }.items() if v is not None}

        raw = await client.tiktok.search_videos(**params)

        truncate_list(raw, ["data", "search_item_list"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_search_videos,
        description="Search TikTok videos by keyword.",
    )


def create_tiktok_search_users_tool(max_results: int = 5) -> FunctionTool:
    """Create a TikTok user search tool with the given configuration."""

    async def scavio_tiktok_search_users(
        keyword: str,
        cursor: str | None = None,
        count: int | None = None,
    ) -> str:
        """Search TikTok users by keyword.

        Args:
            keyword: Search keyword.
            cursor: Pagination cursor from previous response.
            count: Number of results to request.

        Returns:
            JSON string with matching TikTok users.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "keyword": keyword,
            "cursor": cursor,
            "count": count,
        }.items() if v is not None}

        raw = await client.tiktok.search_users(**params)

        truncate_list(raw, ["data", "user_list"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_search_users,
        description="Search TikTok users by keyword.",
    )


def create_tiktok_hashtag_tool() -> FunctionTool:
    """Create a TikTok hashtag lookup tool."""

    async def scavio_tiktok_hashtag(
        hashtag_name: str | None = None,
        hashtag_id: str | None = None,
    ) -> str:
        """Look up TikTok hashtag information.

        Args:
            hashtag_name: The hashtag name to look up.
            hashtag_id: The hashtag ID to look up.

        Returns:
            JSON string with hashtag information.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "hashtag_name": hashtag_name,
            "hashtag_id": hashtag_id,
        }.items() if v is not None}

        raw = await client.tiktok.hashtag(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_hashtag,
        description="Look up TikTok hashtag information.",
    )


def create_tiktok_hashtag_videos_tool(max_results: int = 5) -> FunctionTool:
    """Create a TikTok hashtag videos tool with the given configuration."""

    async def scavio_tiktok_hashtag_videos(
        hashtag_id: str,
        cursor: str | None = None,
        count: int | None = None,
    ) -> str:
        """Fetch TikTok videos for a specific hashtag.

        Args:
            hashtag_id: The hashtag ID to fetch videos for.
            cursor: Pagination cursor from previous response.
            count: Number of results to request.

        Returns:
            JSON string with videos tagged with the hashtag.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "hashtag_id": hashtag_id,
            "cursor": cursor,
            "count": count,
        }.items() if v is not None}

        raw = await client.tiktok.hashtag_videos(**params)

        truncate_list(raw, ["data", "aweme_list"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_hashtag_videos,
        description="Fetch TikTok videos for a specific hashtag.",
    )


def create_tiktok_user_followers_tool(max_results: int = 10) -> FunctionTool:
    """Create a TikTok user followers tool with the given configuration."""

    async def scavio_tiktok_user_followers(
        sec_user_id: str,
        count: int | None = None,
        page_token: str | None = None,
        min_time: int | None = None,
    ) -> str:
        """Fetch a TikTok user's followers.

        Args:
            sec_user_id: The TikTok user's sec_user_id.
            count: Number of followers to request.
            page_token: Pagination token from previous response.
            min_time: Minimum follow time filter (unix timestamp).

        Returns:
            JSON string with the user's followers.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "sec_user_id": sec_user_id,
            "count": count,
            "page_token": page_token,
            "min_time": min_time,
        }.items() if v is not None}

        raw = await client.tiktok.user_followers(**params)

        truncate_list(raw, ["data", "followers"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_user_followers,
        description="Fetch a TikTok user's followers.",
    )


def create_tiktok_user_followings_tool(max_results: int = 10) -> FunctionTool:
    """Create a TikTok user followings tool with the given configuration."""

    async def scavio_tiktok_user_followings(
        sec_user_id: str,
        count: int | None = None,
        page_token: str | None = None,
        min_time: int | None = None,
    ) -> str:
        """Fetch accounts a TikTok user is following.

        Args:
            sec_user_id: The TikTok user's sec_user_id.
            count: Number of followings to request.
            page_token: Pagination token from previous response.
            min_time: Minimum follow time filter (unix timestamp).

        Returns:
            JSON string with accounts the user is following.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "sec_user_id": sec_user_id,
            "count": count,
            "page_token": page_token,
            "min_time": min_time,
        }.items() if v is not None}

        raw = await client.tiktok.user_followings(**params)

        truncate_list(raw, ["data", "followings"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_user_followings,
        description="Fetch accounts a TikTok user is following.",
    )
