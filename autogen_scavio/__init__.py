"""AutoGen integration for Scavio Search API."""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import configure
from autogen_scavio.tools.amazon import create_amazon_product_tool, create_amazon_search_tool
from autogen_scavio.tools.google import create_web_search_tool
from autogen_scavio.tools.instagram import (
    create_instagram_comment_replies_tool,
    create_instagram_post_comments_tool,
    create_instagram_post_tool,
    create_instagram_profile_tool,
    create_instagram_search_hashtags_tool,
    create_instagram_search_users_tool,
    create_instagram_user_followers_tool,
    create_instagram_user_followings_tool,
    create_instagram_user_posts_tool,
    create_instagram_user_reels_tool,
    create_instagram_user_stories_tool,
    create_instagram_user_tagged_tool,
)
from autogen_scavio.tools.reddit import create_reddit_post_tool, create_reddit_search_tool
from autogen_scavio.tools.tiktok import (
    create_tiktok_comment_replies_tool,
    create_tiktok_hashtag_tool,
    create_tiktok_hashtag_videos_tool,
    create_tiktok_profile_tool,
    create_tiktok_search_users_tool,
    create_tiktok_search_videos_tool,
    create_tiktok_user_followers_tool,
    create_tiktok_user_followings_tool,
    create_tiktok_user_posts_tool,
    create_tiktok_video_comments_tool,
    create_tiktok_video_tool,
)
from autogen_scavio.tools.walmart import create_walmart_product_tool, create_walmart_search_tool
from autogen_scavio.tools.youtube import create_youtube_metadata_tool, create_youtube_search_tool

__version__ = "0.2.2"

_PROVIDER_MAP: dict[str, list] = {
    "google": [create_web_search_tool],
    "amazon": [create_amazon_search_tool, create_amazon_product_tool],
    "youtube": [create_youtube_search_tool, create_youtube_metadata_tool],
    "walmart": [create_walmart_search_tool, create_walmart_product_tool],
    "reddit": [create_reddit_search_tool, create_reddit_post_tool],
    "tiktok": [
        create_tiktok_profile_tool,
        create_tiktok_user_posts_tool,
        create_tiktok_video_tool,
        create_tiktok_video_comments_tool,
        create_tiktok_comment_replies_tool,
        create_tiktok_search_videos_tool,
        create_tiktok_search_users_tool,
        create_tiktok_hashtag_tool,
        create_tiktok_hashtag_videos_tool,
        create_tiktok_user_followers_tool,
        create_tiktok_user_followings_tool,
    ],
    "instagram": [
        create_instagram_profile_tool,
        create_instagram_user_posts_tool,
        create_instagram_user_reels_tool,
        create_instagram_user_tagged_tool,
        create_instagram_user_stories_tool,
        create_instagram_post_tool,
        create_instagram_post_comments_tool,
        create_instagram_comment_replies_tool,
        create_instagram_search_users_tool,
        create_instagram_search_hashtags_tool,
        create_instagram_user_followers_tool,
        create_instagram_user_followings_tool,
    ],
}


def create_scavio_tools(
    api_key: str | None = None,
    max_results: int = 5,
    providers: list[str] | None = None,
) -> list[FunctionTool]:
    """Create Scavio search tools for AutoGen agents.

    Args:
        api_key: Scavio API key. If None, reads from SCAVIO_API_KEY env var.
        max_results: Default maximum results for search tools.
        providers: List of providers to include (e.g. ["google", "amazon"]).
            Defaults to all providers.

    Returns:
        List of FunctionTool instances ready for use with AutoGen agents.
    """
    configure(api_key)

    selected = providers or list(_PROVIDER_MAP.keys())
    tools: list[FunctionTool] = []

    for provider in selected:
        factories = _PROVIDER_MAP.get(provider)
        if not factories:
            raise ValueError(
                f"Unknown provider '{provider}'. "
                f"Available: {', '.join(_PROVIDER_MAP.keys())}"
            )
        for factory in factories:
            import inspect

            sig = inspect.signature(factory)
            kwargs: dict = {}
            if "max_results" in sig.parameters:
                kwargs["max_results"] = max_results
            tools.append(factory(**kwargs))

    return tools


__all__ = [
    "__version__",
    "configure",
    "create_scavio_tools",
    "create_web_search_tool",
    "create_amazon_search_tool",
    "create_amazon_product_tool",
    "create_youtube_search_tool",
    "create_youtube_metadata_tool",
    "create_walmart_search_tool",
    "create_walmart_product_tool",
    "create_reddit_search_tool",
    "create_reddit_post_tool",
    "create_tiktok_profile_tool",
    "create_tiktok_user_posts_tool",
    "create_tiktok_video_tool",
    "create_tiktok_video_comments_tool",
    "create_tiktok_comment_replies_tool",
    "create_tiktok_search_videos_tool",
    "create_tiktok_search_users_tool",
    "create_tiktok_hashtag_tool",
    "create_tiktok_hashtag_videos_tool",
    "create_tiktok_user_followers_tool",
    "create_tiktok_user_followings_tool",
    "create_instagram_profile_tool",
    "create_instagram_user_posts_tool",
    "create_instagram_user_reels_tool",
    "create_instagram_user_tagged_tool",
    "create_instagram_user_stories_tool",
    "create_instagram_post_tool",
    "create_instagram_post_comments_tool",
    "create_instagram_comment_replies_tool",
    "create_instagram_search_users_tool",
    "create_instagram_search_hashtags_tool",
    "create_instagram_user_followers_tool",
    "create_instagram_user_followings_tool",
]
