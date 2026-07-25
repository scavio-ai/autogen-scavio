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
        location: bool | None = None,
    ) -> str:
        """Search YouTube videos using the Scavio API.

        Args:
            query: The search query string.
            upload_date: Filter by upload date (e.g. "hour", "today", "week", "month", "year").
            video_type: Filter by video type (e.g. "video", "channel", "playlist", "movie").
            duration: Filter by duration (e.g. "short", "medium", "long").
            sort_by: Sort order for results (e.g. "relevance", "date", "views", "rating").
            features: Feature filters (e.g. "hd", "4k", "subtitles", "creative_commons",
                "live", "360", "3d", "hdr", "vr180").
            cursor: Pagination cursor from a previous response.
            hd: Filter for HD videos only.
            subtitles: Filter for videos with subtitles.
            creative_commons: Filter for Creative Commons licensed videos.
            live: Filter for live videos.
            location: Filter for videos with location data.

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
            "location": location,
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
            "Search YouTube videos. Returns video titles, channels, "
            "view counts, durations, and video IDs."
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
        description="Fetch full details for a YouTube video by video ID.",
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
        description="Fetch comments on a YouTube video.",
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
        description="Fetch the transcript for a YouTube video.",
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
        description="Fetch information about a YouTube channel.",
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
        description="Fetch the videos posted by a YouTube channel.",
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
        description="Fetch playable and downloadable stream URLs for a YouTube video.",
    )
