"""Scavio Kuaishou (China) tools for AutoGen.

14 endpoints. PRICED PER ENDPOINT, never per platform: profile 10 credits, video 2,
videos_batch 40, the four search endpoints 10 each, everything else 1. A single
platform-wide figure would be wrong by up to 40x, so each tool states its own price.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_kuaishou_profile_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) profile tool."""

    async def scavio_kuaishou_profile(
        user_id: Annotated[
            str,
            "Kuaishou user id (non-empty); get one from user_resolve or search_users.",
        ],
    ) -> str:
        """Profile details for a Kuaishou user. Costs 10 credits - the dearest
        single-object call.

        Args:
            user_id: Kuaishou user id (non-empty); get one from user_resolve or
                search_users.

        Returns:
            JSON string with profile details for a Kuaishou user.
        """
        client = get_async_client()

        params: dict = {
            "user_id": user_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.profile(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_profile,
        description=(
            "Profile details for a Kuaishou user. Costs 10 credits, the dearest "
            "single-object call on the platform."
        ),
    )


def create_kuaishou_user_posts_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) user posts tool."""

    async def scavio_kuaishou_user_posts(
        user_id: Annotated[
            str,
            "Kuaishou user id (non-empty); get one from user_resolve or search_users.",
        ],
        cursor: Annotated[
            str | None,
            "Opaque next_cursor from a prior response; omit for the first page.",
        ] = None,
    ) -> str:
        """A user's top posts, cursor-paginated.

        Pagination: cursor -> next_cursor.

        Args:
            user_id: Kuaishou user id (non-empty); get one from user_resolve or
                search_users.
            cursor: Opaque next_cursor from a prior response; omit for the first page.

        Returns:
            JSON string with a user's top posts, cursor-paginated.
        """
        client = get_async_client()

        params: dict = {
            "user_id": user_id,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.user_posts(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_user_posts,
        description=(
            "A Kuaishou user's top posts, cursor-paginated via next_cursor. Costs 1 "
            "credit. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    )


def create_kuaishou_user_live_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) user live tool."""

    async def scavio_kuaishou_user_live(
        user_id: Annotated[
            str,
            "Kuaishou user id (non-empty); get one from user_resolve or search_users.",
        ],
    ) -> str:
        """A user's current live-stream status.

        Args:
            user_id: Kuaishou user id (non-empty); get one from user_resolve or
                search_users.

        Returns:
            JSON string with a user's current live-stream status.
        """
        client = get_async_client()

        params: dict = {
            "user_id": user_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.user_live(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_user_live,
        description=(
            "A Kuaishou user's current live-stream status. Not paginated. Costs 1 "
            "credit. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    )


def create_kuaishou_user_resolve_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) user resolve tool."""

    async def scavio_kuaishou_user_resolve(
        share_link: Annotated[
            str,
            "A kuaishou.com or v.kuaishou.com URL; kwai.com links are rejected.",
        ],
    ) -> str:
        """Turns a Kuaishou share link into a user id.

        Args:
            share_link: A kuaishou.com or v.kuaishou.com URL; kwai.com links are
                rejected.

        Returns:
            JSON string with turns a Kuaishou share link into a user id.
        """
        client = get_async_client()

        params: dict = {
            "share_link": share_link,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.user_resolve(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_user_resolve,
        description=(
            "Turns a Kuaishou share link into a user id. Only kuaishou.com and "
            "v.kuaishou.com links are accepted; Kwai international (kwai.com) is not "
            "served upstream. Costs 1 credit. Kuaishou is priced PER ENDPOINT (1, 2, "
            "10 or 40), never per platform."
        ),
    )


def create_kuaishou_video_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) video tool."""

    async def scavio_kuaishou_video(
        photo_id: Annotated[str | None, "Kuaishou photo (video) id, non-empty."] = None,
        url: Annotated[
            str | None,
            "Full kuaishou.com video URL, as an alternative to photo_id.",
        ] = None,
    ) -> str:
        """A single Kuaishou video by photo id or URL.

        Parameter rule: photo_id or url is required.

        Args:
            photo_id: Kuaishou photo (video) id, non-empty.
            url: Full kuaishou.com video URL, as an alternative to photo_id.

        Returns:
            JSON string with a single video by photo id or URL.
        """
        client = get_async_client()

        params: dict = {
            "photo_id": photo_id,
            "url": url,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.video(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_video,
        description=(
            "A single Kuaishou video by photo id or URL. Provide photo_id or url. "
            "Costs 2 credits."
        ),
    )


def create_kuaishou_video_comments_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) video comments tool."""

    async def scavio_kuaishou_video_comments(
        photo_id: Annotated[str, "Kuaishou photo (video) id, non-empty."],
        cursor: Annotated[
            str | None,
            "Opaque next_cursor from a prior response; omit for the first page.",
        ] = None,
    ) -> str:
        """Comments on a video, cursor-paginated.

        Pagination: cursor -> next_cursor.

        Args:
            photo_id: Kuaishou photo (video) id, non-empty.
            cursor: Opaque next_cursor from a prior response; omit for the first page.

        Returns:
            JSON string with comments on a video, cursor-paginated.
        """
        client = get_async_client()

        params: dict = {
            "photo_id": photo_id,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.video_comments(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_video_comments,
        description=(
            "Comments on a Kuaishou video, cursor-paginated via next_cursor. Costs 1 "
            "credit. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    )


def create_kuaishou_comment_replies_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) comment replies tool."""

    async def scavio_kuaishou_comment_replies(
        photo_id: Annotated[str, "Kuaishou photo (video) id, non-empty."],
        root_comment_id: Annotated[
            str,
            "Id of the top-level comment whose replies you want, from video_comments.",
        ],
        cursor: Annotated[
            str | None,
            "Opaque next_cursor from a prior response; omit for the first page.",
        ] = None,
        count: Annotated[
            int | None,
            "Replies per page, 1-50. Omit to use the upstream default.",
        ] = None,
    ) -> str:
        """Replies under a root comment on a Kuaishou video.

        Pagination: cursor -> next_cursor; `count` sizes the page.

        Args:
            photo_id: Kuaishou photo (video) id, non-empty.
            root_comment_id: Id of the top-level comment whose replies you want, from
                video_comments.
            cursor: Opaque next_cursor from a prior response; omit for the first page.
            count: Replies per page, 1-50. Omit to use the upstream default.

        Returns:
            JSON string with replies under a root comment.
        """
        client = get_async_client()

        params: dict = {
            "photo_id": photo_id,
            "root_comment_id": root_comment_id,
            "cursor": cursor,
            "count": count,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.comment_replies(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_comment_replies,
        description=(
            "Replies under a root comment on a Kuaishou video, cursor-paginated via "
            "next_cursor; count sizes the page (1-50). Costs 1 credit. Kuaishou is "
            "priced PER ENDPOINT (1, 2, 10 or 40), never per platform."
        ),
    )


def create_kuaishou_videos_batch_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) videos batch tool."""

    async def scavio_kuaishou_videos_batch(
        photo_ids: Annotated[
            list[str],
            "Kuaishou photo (video) ids, 1-20 per call; more than 20 is rejected.",
        ],
    ) -> str:
        """Several Kuaishou videos in one call, max 20 photo ids. Costs 40 credits.

        Args:
            photo_ids: Kuaishou photo (video) ids, 1-20 per call; more than 20 is
                rejected.

        Returns:
            JSON string with several videos in one call.
        """
        client = get_async_client()

        params: dict = {
            "photo_ids": photo_ids,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.videos_batch(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_videos_batch,
        description=(
            "Several Kuaishou videos in one call, hard-capped at 20 photo ids. Costs "
            "40 credits, the dearest call on the platform."
        ),
    )


def create_kuaishou_search_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) search tool."""

    async def scavio_kuaishou_search(
        keyword: Annotated[str, "Search keyword, 1-200 characters."],
        cursor: Annotated[
            str | None,
            "Opaque next_cursor from a prior response; omit for the first page.",
        ] = None,
    ) -> str:
        """Mixed-result search across Kuaishou. Costs 10 credits.

        Pagination: cursor -> next_cursor.

        Args:
            keyword: Search keyword, 1-200 characters.
            cursor: Opaque next_cursor from a prior response; omit for the first page.

        Returns:
            JSON string with mixed-result search across Kuaishou.
        """
        client = get_async_client()

        params: dict = {
            "keyword": keyword,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_search,
        description=(
            "Mixed-result search across Kuaishou, cursor-paginated via next_cursor. "
            "Costs 10 credits per page."
        ),
    )


def create_kuaishou_search_videos_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) search videos tool."""

    async def scavio_kuaishou_search_videos(
        keyword: Annotated[str, "Search keyword, 1-200 characters."],
        cursor: Annotated[
            str | None,
            "Opaque next_cursor from a prior response; omit for the first page.",
        ] = None,
    ) -> str:
        """Kuaishou video search results. Costs 10 credits.

        Pagination: cursor -> next_cursor.

        Args:
            keyword: Search keyword, 1-200 characters.
            cursor: Opaque next_cursor from a prior response; omit for the first page.

        Returns:
            JSON string with video search results.
        """
        client = get_async_client()

        params: dict = {
            "keyword": keyword,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.search_videos(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_search_videos,
        description=(
            "Kuaishou video search results, cursor-paginated via next_cursor. Costs "
            "10 credits per page."
        ),
    )


def create_kuaishou_search_users_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) search users tool."""

    async def scavio_kuaishou_search_users(
        keyword: Annotated[str, "Search keyword, 1-200 characters."],
        cursor: Annotated[
            str | None,
            "Opaque next_cursor from a prior response; omit for the first page.",
        ] = None,
    ) -> str:
        """Kuaishou user search results. Costs 10 credits.

        Pagination: cursor -> next_cursor.

        Args:
            keyword: Search keyword, 1-200 characters.
            cursor: Opaque next_cursor from a prior response; omit for the first page.

        Returns:
            JSON string with user search results.
        """
        client = get_async_client()

        params: dict = {
            "keyword": keyword,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.search_users(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_search_users,
        description=(
            "Kuaishou user search results, cursor-paginated via next_cursor. Costs 10 "
            "credits per page."
        ),
    )


def create_kuaishou_search_live_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) search live tool."""

    async def scavio_kuaishou_search_live(
        keyword: Annotated[str, "Search keyword, 1-200 characters."],
        cursor: Annotated[
            str | None,
            "Opaque next_cursor from a prior response; omit for the first page.",
        ] = None,
    ) -> str:
        """Kuaishou live-stream search results. Costs 10 credits.

        Pagination: cursor -> next_cursor.

        Args:
            keyword: Search keyword, 1-200 characters.
            cursor: Opaque next_cursor from a prior response; omit for the first page.

        Returns:
            JSON string with live-stream search results.
        """
        client = get_async_client()

        params: dict = {
            "keyword": keyword,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.search_live(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_search_live,
        description=(
            "Kuaishou live-stream search results, cursor-paginated via next_cursor. "
            "Costs 10 credits per page."
        ),
    )


def create_kuaishou_tag_feed_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) tag feed tool."""

    async def scavio_kuaishou_tag_feed(
        tag: Annotated[str, "Hashtag text without the leading '#', 1-200 characters."],
        cursor: Annotated[
            str | None,
            "Opaque next_cursor from a prior response; omit for the first page.",
        ] = None,
    ) -> str:
        """Posts under a Kuaishou hashtag, cursor-paginated.

        Pagination: cursor -> next_cursor.

        Args:
            tag: Hashtag text without the leading '#', 1-200 characters.
            cursor: Opaque next_cursor from a prior response; omit for the first page.

        Returns:
            JSON string with posts under a hashtag, cursor-paginated.
        """
        client = get_async_client()

        params: dict = {
            "tag": tag,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.tag_feed(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_tag_feed,
        description=(
            "Posts under a Kuaishou hashtag, cursor-paginated via next_cursor. Costs "
            "1 credit. Kuaishou is priced PER ENDPOINT (1, 2, 10 or 40), never per "
            "platform."
        ),
    )


def create_kuaishou_trending_tool() -> FunctionTool:
    """Create a Scavio Kuaishou (China) trending tool."""

    async def scavio_kuaishou_trending(
        board: Annotated[
            Literal["hot", "live", "shopping", "brand", "music"] | None,
            "Leaderboard to return; defaults to 'hot' when omitted.",
        ] = None,
    ) -> str:
        """Kuaishou hot / live / shopping / brand / music leaderboards.

        Args:
            board: Leaderboard to return; defaults to 'hot' when omitted.

        Returns:
            JSON string with hot / live / shopping / brand / music leaderboards.
        """
        client = get_async_client()

        params: dict = {
            "board": board,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kuaishou.trending(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kuaishou_trending,
        description=(
            "Kuaishou hot / live / shopping / brand / music leaderboards. One board "
            "per call, not paginated. Costs 1 credit. Kuaishou is priced PER ENDPOINT "
            "(1, 2, 10 or 40), never per platform."
        ),
    )
