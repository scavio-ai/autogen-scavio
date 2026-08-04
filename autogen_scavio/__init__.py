"""AutoGen integration for Scavio Search API."""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import configure
from autogen_scavio.tools.amazon import (
    create_amazon_offers_tool,
    create_amazon_product_tool,
    create_amazon_search_tool,
)
from autogen_scavio.tools.google import (
    create_google_ai_mode_tool,
    create_google_flights_tool,
    create_google_hotels_detail_tool,
    create_google_hotels_tool,
    create_google_maps_place_tool,
    create_google_maps_reviews_tool,
    create_google_maps_search_tool,
    create_google_news_tool,
    create_google_shopping_product_tool,
    create_google_shopping_stores_tool,
    create_google_shopping_tool,
    create_google_trending_tool,
    create_google_trends_tool,
    create_web_search_tool,
)
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
from autogen_scavio.tools.linkedin import (
    create_linkedin_company_posts_tool,
    create_linkedin_company_tool,
    create_linkedin_job_tool,
    create_linkedin_person_about_tool,
    create_linkedin_person_posts_tool,
    create_linkedin_person_tool,
    create_linkedin_post_comments_tool,
    create_linkedin_post_tool,
    create_linkedin_search_jobs_tool,
)
from autogen_scavio.tools.reddit import (
    create_reddit_comment_replies_tool,
    create_reddit_popular_tool,
    create_reddit_post_comments_tool,
    create_reddit_post_tool,
    create_reddit_search_suggestions_tool,
    create_reddit_search_tool,
    create_reddit_subreddit_posts_tool,
    create_reddit_subreddit_tool,
    create_reddit_trending_tool,
    create_reddit_user_comments_tool,
    create_reddit_user_posts_tool,
    create_reddit_user_tool,
)
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
from autogen_scavio.tools.tiktok_shop import (
    create_tiktok_shop_categories_tool,
    create_tiktok_shop_category_products_tool,
    create_tiktok_shop_product_reviews_tool,
    create_tiktok_shop_product_tool,
    create_tiktok_shop_resolve_tool,
    create_tiktok_shop_search_suggestions_tool,
    create_tiktok_shop_search_tool,
    create_tiktok_shop_shop_products_tool,
)
from autogen_scavio.tools.walmart import create_walmart_product_tool, create_walmart_search_tool
from autogen_scavio.tools.x import (
    create_x_search_tool,
    create_x_trending_tool,
    create_x_tweet_comments_tool,
    create_x_tweet_retweeters_tool,
    create_x_tweet_tool,
    create_x_user_followers_tool,
    create_x_user_followings_tool,
    create_x_user_media_tool,
    create_x_user_replies_tool,
    create_x_user_tool,
    create_x_user_tweets_tool,
)
from autogen_scavio.tools.youtube import (
    create_youtube_channel_community_tool,
    create_youtube_channel_resolve_tool,
    create_youtube_channel_search_tool,
    create_youtube_channel_shorts_tool,
    create_youtube_channel_tool,
    create_youtube_channel_videos_tool,
    create_youtube_comment_replies_tool,
    create_youtube_comments_tool,
    create_youtube_metadata_tool,
    create_youtube_related_tool,
    create_youtube_search_tool,
    create_youtube_shorts_tool,
    create_youtube_streams_tool,
    create_youtube_suggestions_tool,
    create_youtube_transcript_tool,
    create_youtube_video_tool,
)

__version__ = "0.6.0"

_PROVIDER_MAP: dict[str, list] = {
    "google": [
        # Google v1 was retired on 2026-08-04 and answers 410. Every tool here
        # is a v2 endpoint (/api/v2/google/...) and takes v2 params natively:
        # gl, hl, start, google_domain, device. start is a zero-based result
        # offset, not a page number.
        create_web_search_tool,
        create_google_ai_mode_tool,
        create_google_maps_search_tool,
        create_google_maps_place_tool,
        create_google_maps_reviews_tool,
        create_google_shopping_tool,
        create_google_shopping_product_tool,
        create_google_shopping_stores_tool,
        create_google_flights_tool,
        create_google_hotels_tool,
        create_google_hotels_detail_tool,
        create_google_news_tool,
        create_google_trends_tool,
        create_google_trending_tool,
    ],
    "amazon": [
        create_amazon_search_tool,
        create_amazon_product_tool,
        create_amazon_offers_tool,
    ],
    "youtube": [
        create_youtube_search_tool,
        create_youtube_shorts_tool,
        create_youtube_suggestions_tool,
        create_youtube_video_tool,
        # create_youtube_metadata_tool is a deprecated alias of the video tool
        # (same endpoint, same response). It stays importable for existing
        # callers but is not loaded by default.
        create_youtube_comments_tool,
        create_youtube_comment_replies_tool,
        create_youtube_transcript_tool,
        create_youtube_related_tool,
        create_youtube_channel_search_tool,
        create_youtube_channel_tool,
        create_youtube_channel_videos_tool,
        create_youtube_channel_shorts_tool,
        create_youtube_channel_community_tool,
        create_youtube_channel_resolve_tool,
        create_youtube_streams_tool,
    ],
    "walmart": [create_walmart_search_tool, create_walmart_product_tool],
    "reddit": [
        create_reddit_search_tool,
        create_reddit_search_suggestions_tool,
        create_reddit_post_tool,
        create_reddit_post_comments_tool,
        create_reddit_comment_replies_tool,
        create_reddit_subreddit_tool,
        create_reddit_subreddit_posts_tool,
        create_reddit_user_tool,
        create_reddit_user_posts_tool,
        create_reddit_user_comments_tool,
        create_reddit_popular_tool,
        create_reddit_trending_tool,
    ],
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
    "tiktok_shop": [
        create_tiktok_shop_search_tool,
        create_tiktok_shop_search_suggestions_tool,
        create_tiktok_shop_product_tool,
        create_tiktok_shop_product_reviews_tool,
        create_tiktok_shop_categories_tool,
        create_tiktok_shop_category_products_tool,
        create_tiktok_shop_shop_products_tool,
        create_tiktok_shop_resolve_tool,
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
    "x": [
        create_x_search_tool,
        create_x_tweet_tool,
        create_x_tweet_comments_tool,
        create_x_tweet_retweeters_tool,
        create_x_user_tool,
        create_x_user_tweets_tool,
        create_x_user_replies_tool,
        create_x_user_media_tool,
        create_x_user_followers_tool,
        create_x_user_followings_tool,
        create_x_trending_tool,
    ],
    "linkedin": [
        # Nine live endpoints. person/contact, company/people, company/jobs,
        # search/people and search/posts were retired upstream and only answer
        # 410, so they are not wrapped as tools.
        create_linkedin_person_tool,
        create_linkedin_person_about_tool,
        create_linkedin_person_posts_tool,
        create_linkedin_company_tool,
        create_linkedin_company_posts_tool,
        create_linkedin_search_jobs_tool,
        create_linkedin_job_tool,
        create_linkedin_post_tool,
        create_linkedin_post_comments_tool,
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
    "create_google_ai_mode_tool",
    "create_google_maps_search_tool",
    "create_google_maps_place_tool",
    "create_google_maps_reviews_tool",
    "create_google_shopping_tool",
    "create_google_shopping_product_tool",
    "create_google_shopping_stores_tool",
    "create_google_flights_tool",
    "create_google_hotels_tool",
    "create_google_hotels_detail_tool",
    "create_google_news_tool",
    "create_google_trends_tool",
    "create_google_trending_tool",
    "create_amazon_search_tool",
    "create_amazon_product_tool",
    "create_amazon_offers_tool",
    "create_youtube_search_tool",
    "create_youtube_shorts_tool",
    "create_youtube_suggestions_tool",
    "create_youtube_video_tool",
    "create_youtube_metadata_tool",
    "create_youtube_comments_tool",
    "create_youtube_comment_replies_tool",
    "create_youtube_transcript_tool",
    "create_youtube_related_tool",
    "create_youtube_channel_search_tool",
    "create_youtube_channel_tool",
    "create_youtube_channel_videos_tool",
    "create_youtube_channel_shorts_tool",
    "create_youtube_channel_community_tool",
    "create_youtube_channel_resolve_tool",
    "create_youtube_streams_tool",
    "create_walmart_search_tool",
    "create_walmart_product_tool",
    "create_reddit_search_tool",
    "create_reddit_search_suggestions_tool",
    "create_reddit_post_tool",
    "create_reddit_post_comments_tool",
    "create_reddit_comment_replies_tool",
    "create_reddit_subreddit_tool",
    "create_reddit_subreddit_posts_tool",
    "create_reddit_user_tool",
    "create_reddit_user_posts_tool",
    "create_reddit_user_comments_tool",
    "create_reddit_popular_tool",
    "create_reddit_trending_tool",
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
    "create_tiktok_shop_search_tool",
    "create_tiktok_shop_search_suggestions_tool",
    "create_tiktok_shop_product_tool",
    "create_tiktok_shop_product_reviews_tool",
    "create_tiktok_shop_categories_tool",
    "create_tiktok_shop_category_products_tool",
    "create_tiktok_shop_shop_products_tool",
    "create_tiktok_shop_resolve_tool",
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
    "create_x_search_tool",
    "create_x_tweet_tool",
    "create_x_tweet_comments_tool",
    "create_x_tweet_retweeters_tool",
    "create_x_user_tool",
    "create_x_user_tweets_tool",
    "create_x_user_replies_tool",
    "create_x_user_media_tool",
    "create_x_user_followers_tool",
    "create_x_user_followings_tool",
    "create_x_trending_tool",
    "create_linkedin_person_tool",
    "create_linkedin_person_about_tool",
    "create_linkedin_person_posts_tool",
    "create_linkedin_company_tool",
    "create_linkedin_company_posts_tool",
    "create_linkedin_search_jobs_tool",
    "create_linkedin_job_tool",
    "create_linkedin_post_tool",
    "create_linkedin_post_comments_tool",
]
