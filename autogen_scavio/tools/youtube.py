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
            "search": query,
            "upload_date": upload_date,
            "type": video_type,
            "duration": duration,
            "sort_by": sort_by,
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


def create_youtube_metadata_tool() -> FunctionTool:
    """Create a YouTube metadata tool."""

    async def scavio_youtube_metadata(video_id: str) -> str:
        """Fetch full metadata for a YouTube video by video ID.

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
        description="Fetch full metadata for a YouTube video by video ID.",
    )
