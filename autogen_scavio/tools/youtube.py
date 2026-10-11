"""Scavio YouTube tools for AutoGen."""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list


def create_youtube_search_tool(
    max_results: int = 5,
    fourk: bool | None = None,
    hdr: bool | None = None,
    three_sixty: bool | None = None,
    threed: bool | None = None,
    vr180: bool | None = None,
) -> FunctionTool:
    """Create a YouTube search tool with the given configuration."""

    async def scavio_youtube_search(
        query: str,
        upload_date: str | None = None,
        video_type: str | None = None,
        duration: str | None = None,
        sort_by: str | None = None,
        features: list[str] | None = None,
        cursor: str | None = None,
        hd: bool | None = None,
        subtitles: bool | None = None,
        creative_commons: bool | None = None,
        live: bool | None = None,
    ) -> str:
        """Search YouTube videos using the Scavio API.

        Args:
            query: The search query string.
            upload_date: Filter by upload date, one of "last_hour", "today",
                "this_week", "this_month", "this_year".
            video_type: Filter by video type, one of "video", "channel",
                "playlist", "movie".
            duration: Filter by duration, one of "short", "medium", "long".
            sort_by: Sort order for results, one of "relevance", "date",
                "view_count", "rating".
            features: Feature filters (e.g. "hd", "4k", "subtitles", "creative_commons",
                "live", "360", "3d", "hdr", "vr180").
            cursor: Pagination cursor from a previous response.
            hd: Filter for HD videos only.
            subtitles: Filter for videos with subtitles.
            creative_commons: Filter for Creative Commons licensed videos.
            live: Filter for live videos.

        Returns:
            JSON string with YouTube search results including video titles,
            channels, view counts, durations, and video IDs.
        """
        client = get_async_client()

        params = {
            "query": query,
            "upload_date": upload_date,
            "type": video_type,
            "duration": duration,
            "sort_by": sort_by,
            "features": features,
            "cursor": cursor,
            "hd": hd,
            "subtitles": subtitles,
            "creative_commons": creative_commons,
            "live": live,
            "4k": fourk,
            "hdr": hdr,
            "360": three_sixty,
            "3d": threed,
            "vr180": vr180,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.youtube.search(**params)

        truncate_list(raw, ["data", "results"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_search,
        description=(
            "Search YouTube videos (2 credits). Returns video titles, "
            "channels, view counts, durations, and video IDs."
        ),
    )


def create_youtube_video_tool() -> FunctionTool:
    """Create a YouTube video details tool."""

    async def scavio_youtube_video(video_id: str) -> str:
        """Fetch full details for a YouTube video by video ID.

        Args:
            video_id: The YouTube video ID (or a full watch URL) to retrieve.

        Returns:
            JSON string with full video details including title, description,
            channel info, statistics, captions, and chapters.
        """
        client = get_async_client()

        raw = await client.youtube.video(video_id=video_id)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_video,
        description="Fetch full details for a YouTube video by video ID (1 credit).",
    )


def create_youtube_metadata_tool() -> FunctionTool:
    """Create a YouTube metadata tool (deprecated alias of the video tool)."""

    async def scavio_youtube_metadata(video_id: str) -> str:
        """Fetch full metadata for a YouTube video by video ID.

        Deprecated: use the video tool instead.

        Args:
            video_id: The YouTube video ID to retrieve metadata for.

        Returns:
            JSON string with full video metadata including title, description,
            channel info, statistics, and other details.
        """
        client = get_async_client()

        raw = await client.youtube.metadata(video_id=video_id)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_metadata,
        description="Fetch full metadata for a YouTube video by video ID (deprecated: use the video tool).",
    )


def create_youtube_comments_tool(max_results: int = 10) -> FunctionTool:
    """Create a YouTube comments tool with the given configuration."""

    async def scavio_youtube_comments(
        video_id: str,
        cursor: str | None = None,
    ) -> str:
        """Fetch comments on a YouTube video.

        Args:
            video_id: The YouTube video ID.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with video comments including text, like counts,
            reply counts, and author info.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "video_id": video_id,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.youtube.comments(**params)

        truncate_list(raw, ["data", "comments"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_comments,
        description="Fetch comments on a YouTube video (1 credit).",
    )


def create_youtube_transcript_tool() -> FunctionTool:
    """Create a YouTube transcript tool."""

    async def scavio_youtube_transcript(
        video_id: str,
        language: str | None = None,
        format: str | None = None,
    ) -> str:
        """Fetch the transcript for a YouTube video.

        Args:
            video_id: The YouTube video ID.
            language: Transcript language code (default "en").
            format: Output format, "text" for plain text or "srt" for timed subtitles.

        Returns:
            JSON string with the transcript content.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "video_id": video_id,
            "language": language,
            "format": format,
        }.items() if v is not None}

        raw = await client.youtube.transcript(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_transcript,
        description="Fetch the transcript for a YouTube video (5 credits).",
    )


def create_youtube_channel_tool() -> FunctionTool:
    """Create a YouTube channel info tool."""

    async def scavio_youtube_channel(channel_id: str) -> str:
        """Fetch information about a YouTube channel.

        Args:
            channel_id: The YouTube channel ID (or an @handle or channel URL).

        Returns:
            JSON string with channel details including title, description,
            subscriber count, video count, view count, and links.
        """
        client = get_async_client()

        raw = await client.youtube.channel(channel_id=channel_id)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_channel,
        description="Fetch information about a YouTube channel (1 credit).",
    )


def create_youtube_channel_videos_tool(max_results: int = 5) -> FunctionTool:
    """Create a YouTube channel videos tool with the given configuration."""

    async def scavio_youtube_channel_videos(
        channel_id: str,
        cursor: str | None = None,
    ) -> str:
        """Fetch the videos posted by a YouTube channel.

        Args:
            channel_id: The YouTube channel ID.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with the channel's videos including titles, view counts,
            durations, and published times.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "channel_id": channel_id,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.youtube.channel_videos(**params)

        truncate_list(raw, ["data", "results"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_channel_videos,
        description="Fetch the videos posted by a YouTube channel (1 credit).",
    )


def create_youtube_streams_tool() -> FunctionTool:
    """Create a YouTube streams tool."""

    async def scavio_youtube_streams(video_id: str) -> str:
        """Fetch playable and downloadable stream URLs for a YouTube video.

        Args:
            video_id: The YouTube video ID.

        Returns:
            JSON string with available stream formats including direct URLs,
            qualities, and codecs.
        """
        client = get_async_client()

        raw = await client.youtube.streams(video_id=video_id)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_streams,
        description=(
            "Fetch playable and downloadable stream URLs for a YouTube video "
            "(3 credits)."
        ),
    )


def create_youtube_shorts_tool(max_results: int = 5) -> FunctionTool:
    """Create a YouTube Shorts search tool with the given configuration."""

    async def scavio_youtube_shorts(
        query: str,
        sort_by: str | None = None,
        cursor: str | None = None,
    ) -> str:
        """Search YouTube Shorts.

        Args:
            query: The search query string.
            sort_by: Sort order for results, one of "relevance", "date",
                "view_count", "rating".
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with matching Shorts under data.results, plus
            next_cursor and has_more. There are no type, duration,
            upload_date or features filters on this endpoint.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "query": query,
            "sort_by": sort_by,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.youtube.shorts(**params)

        truncate_list(raw, ["data", "results"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_shorts,
        description=(
            "Search YouTube Shorts (2 credits). Returns short-form videos "
            "under data.results."
        ),
    )


def create_youtube_suggestions_tool(max_results: int = 10) -> FunctionTool:
    """Create a YouTube search suggestions tool with the given configuration."""

    async def scavio_youtube_suggestions(
        query: str,
        language: str | None = None,
        region: str | None = None,
    ) -> str:
        """Fetch YouTube autocomplete suggestions for a query.

        Args:
            query: The partial query to autocomplete.
            language: Language code, e.g. "en".
            region: Region code, e.g. "US".

        Returns:
            JSON string with data.suggestions, a list of strings, plus
            total_count.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "query": query,
            "language": language,
            "region": region,
        }.items() if v is not None}

        raw = await client.youtube.suggestions(**params)

        truncate_list(raw, ["data", "suggestions"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_suggestions,
        description=(
            "Fetch YouTube autocomplete suggestions for a query (1 credit)."
        ),
    )


def create_youtube_comment_replies_tool(max_results: int = 10) -> FunctionTool:
    """Create a YouTube comment replies tool with the given configuration."""

    async def scavio_youtube_comment_replies(
        video_id: str,
        reply_cursor: str,
        cursor: str | None = None,
    ) -> str:
        """Fetch replies to a specific comment on a YouTube video.

        Args:
            video_id: The YouTube video ID.
            reply_cursor: The reply_cursor of a comment from the comments
                tool. Required: this endpoint cannot be called from a video
                ID alone.
            cursor: Pagination cursor for page 2 onwards. Wins over
                reply_cursor when both are set.

        Returns:
            JSON string with data.replies, plus next_cursor and has_more.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "video_id": video_id,
            "reply_cursor": reply_cursor,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.youtube.comment_replies(**params)

        truncate_list(raw, ["data", "replies"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_comment_replies,
        description=(
            "Fetch replies to a YouTube comment (1 credit). Needs the "
            "reply_cursor of a comment from the comments tool."
        ),
    )


def create_youtube_related_tool(max_results: int = 5) -> FunctionTool:
    """Create a YouTube related videos tool with the given configuration."""

    async def scavio_youtube_related(
        video_id: str,
        cursor: str | None = None,
    ) -> str:
        """Fetch videos related to a YouTube video.

        Args:
            video_id: The YouTube video ID.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with related videos under data.results, plus
            total_count. This endpoint accepts a cursor but returns no
            next_cursor or has_more.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "video_id": video_id,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.youtube.related(**params)

        truncate_list(raw, ["data", "results"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_related,
        description="Fetch videos related to a YouTube video (1 credit).",
    )


def create_youtube_channel_search_tool(max_results: int = 5) -> FunctionTool:
    """Create a YouTube channel search tool with the given configuration."""

    async def scavio_youtube_channel_search(
        query: str,
        cursor: str | None = None,
    ) -> str:
        """Search YouTube for channels.

        Args:
            query: The channel search query.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with matching channels under data.results with
            channel_id, name, handle, subscriber_count and verified, plus
            next_cursor, has_more and total_count.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "query": query,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.youtube.channel_search(**params)

        truncate_list(raw, ["data", "results"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_channel_search,
        description=(
            "Search YouTube for channels (1 credit). Returns channel ids, "
            "handles and subscriber counts."
        ),
    )


def create_youtube_channel_shorts_tool(max_results: int = 5) -> FunctionTool:
    """Create a YouTube channel shorts tool with the given configuration."""

    async def scavio_youtube_channel_shorts(
        channel_id: str,
        cursor: str | None = None,
    ) -> str:
        """Fetch the Shorts posted by a YouTube channel.

        Args:
            channel_id: The YouTube channel ID, @handle, or channel URL.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with the channel's Shorts under data.results
            (video_id, title, url, thumbnail), plus next_cursor, has_more and
            total_count. View counts are deliberately omitted: upstream
            reports promo text there for Shorts.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "channel_id": channel_id,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.youtube.channel_shorts(**params)

        truncate_list(raw, ["data", "results"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_channel_shorts,
        description="Fetch the Shorts posted by a YouTube channel (1 credit).",
    )


def create_youtube_channel_community_tool(max_results: int = 5) -> FunctionTool:
    """Create a YouTube channel community tool with the given configuration."""

    async def scavio_youtube_channel_community(
        channel_id: str,
        cursor: str | None = None,
    ) -> str:
        """Fetch a YouTube channel's community posts.

        Args:
            channel_id: The YouTube channel ID, @handle, or channel URL.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with community posts under data.posts (text,
            vote_count, comment_count, images), plus next_cursor and has_more.
            This is the only YouTube endpoint whose list key is posts.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "channel_id": channel_id,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.youtube.channel_community(**params)

        truncate_list(raw, ["data", "posts"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_channel_community,
        description=(
            "Fetch a YouTube channel's community posts (1 credit). The list "
            "key is data.posts, not data.results."
        ),
    )


def create_youtube_channel_resolve_tool() -> FunctionTool:
    """Create a YouTube channel resolve tool."""

    async def scavio_youtube_channel_resolve(channel: str) -> str:
        """Resolve a YouTube @handle or channel URL to a channel ID.

        Args:
            channel: A channel @handle, bare name, or channel URL, e.g.
                "@MrBeast". The field is channel, not channel_id.

        Returns:
            JSON string with data.channel_id and data.channel_url.
        """
        client = get_async_client()

        raw = await client.youtube.channel_resolve(channel=channel)

        return format_response(raw)

    return FunctionTool(
        scavio_youtube_channel_resolve,
        description=(
            "Resolve a YouTube @handle or channel URL to a channel ID "
            "(1 credit)."
        ),
    )
