"""AutoGen integration for Scavio Search API."""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import configure
from autogen_scavio.tools.airbnb import (
    create_airbnb_listing_tool,
    create_airbnb_reviews_tool,
    create_airbnb_search_tool,
)
from autogen_scavio.tools.amazon import (
    create_amazon_offers_tool,
    create_amazon_product_tool,
    create_amazon_search_tool,
)
from autogen_scavio.tools.app_store import (
    create_app_store_app_tool,
    create_app_store_reviews_tool,
    create_app_store_search_tool,
)
from autogen_scavio.tools.booking import (
    create_booking_hotel_tool,
    create_booking_reviews_tool,
    create_booking_search_tool,
)
from autogen_scavio.tools.capterra import (
    create_capterra_product_tool,
    create_capterra_reviews_tool,
    create_capterra_search_tool,
)
from autogen_scavio.tools.companies_house import (
    create_companies_house_company_tool,
    create_companies_house_filing_history_tool,
    create_companies_house_officers_tool,
    create_companies_house_search_tool,
)
from autogen_scavio.tools.ebay import (
    create_ebay_product_tool,
    create_ebay_search_tool,
    create_ebay_seller_tool,
)
from autogen_scavio.tools.extract import (
    create_batch_extract_tool,
    create_batch_status_tool,
    create_crawl_status_tool,
    create_crawl_website_tool,
    create_extract_tool,
    create_map_website_tool,
)
from autogen_scavio.tools.g2 import (
    create_g2_product_tool,
    create_g2_reviews_tool,
    create_g2_search_tool,
)
from autogen_scavio.tools.glassdoor import (
    create_glassdoor_companies_tool,
    create_glassdoor_company_tool,
    create_glassdoor_reviews_tool,
    create_glassdoor_salaries_tool,
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
from autogen_scavio.tools.google_ads import (
    create_google_ads_advertisers_tool,
    create_google_ads_creative_tool,
    create_google_ads_search_tool,
)
from autogen_scavio.tools.google_play import (
    create_google_play_app_tool,
    create_google_play_reviews_tool,
    create_google_play_search_tool,
)
from autogen_scavio.tools.home_depot import (
    create_home_depot_product_tool,
    create_home_depot_reviews_tool,
    create_home_depot_search_tool,
)
from autogen_scavio.tools.indeed import (
    create_indeed_company_reviews_tool,
    create_indeed_company_tool,
    create_indeed_job_tool,
    create_indeed_search_tool,
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
from autogen_scavio.tools.kuaishou import (
    create_kuaishou_comment_replies_tool,
    create_kuaishou_profile_tool,
    create_kuaishou_search_live_tool,
    create_kuaishou_search_tool,
    create_kuaishou_search_users_tool,
    create_kuaishou_search_videos_tool,
    create_kuaishou_tag_feed_tool,
    create_kuaishou_trending_tool,
    create_kuaishou_user_live_tool,
    create_kuaishou_user_posts_tool,
    create_kuaishou_user_resolve_tool,
    create_kuaishou_video_comments_tool,
    create_kuaishou_video_tool,
    create_kuaishou_videos_batch_tool,
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
from autogen_scavio.tools.meta_ads import (
    create_meta_ads_ad_tool,
    create_meta_ads_advertiser_tool,
    create_meta_ads_search_tool,
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
from autogen_scavio.tools.redfin import (
    create_redfin_market_tool,
    create_redfin_property_tool,
    create_redfin_search_tool,
)
from autogen_scavio.tools.sec import (
    create_sec_company_tool,
    create_sec_concept_tool,
    create_sec_facts_tool,
    create_sec_filings_tool,
    create_sec_lookup_tool,
    create_sec_search_tool,
)
from autogen_scavio.tools.target import (
    create_target_category_tool,
    create_target_product_tool,
    create_target_reviews_tool,
    create_target_search_tool,
)
from autogen_scavio.tools.threads import (
    create_threads_post_comments_tool,
    create_threads_post_tool,
    create_threads_profile_tool,
    create_threads_search_users_tool,
    create_threads_user_posts_tool,
    create_threads_user_replies_tool,
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
from autogen_scavio.tools.tripadvisor import (
    create_tripadvisor_location_tool,
    create_tripadvisor_locations_tool,
    create_tripadvisor_reviews_tool,
    create_tripadvisor_search_tool,
)
from autogen_scavio.tools.walmart import (
    create_walmart_category_tool,
    create_walmart_offers_tool,
    create_walmart_product_tool,
    create_walmart_reviews_tool,
    create_walmart_search_tool,
    create_walmart_seller_products_tool,
    create_walmart_seller_tool,
)
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
from autogen_scavio.tools.yelp import (
    create_yelp_business_tool,
    create_yelp_reviews_tool,
    create_yelp_search_tool,
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
from autogen_scavio.tools.zillow import (
    create_zillow_agent_reviews_tool,
    create_zillow_property_tool,
    create_zillow_search_tool,
)

__version__ = "0.8.1"

_PROVIDER_MAP: dict[str, list] = {
    "extract": [
        # Not a platform: /api/v1/extract reads ANY url. It leads the list
        # because it is what an agent reaches for when no platform endpoint
        # covers the page in front of it.
        create_extract_tool,
    ],
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
    "walmart": [
        # BODY-PRICED. search and category cost 1 credit on domain 'com' or
        # 'ca' and 2 on 'com.mx'; the other five take no domain and are
        # always 1.
        create_walmart_search_tool,
        create_walmart_product_tool,
        create_walmart_reviews_tool,
        create_walmart_category_tool,
        create_walmart_offers_tool,
        create_walmart_seller_tool,
        create_walmart_seller_products_tool,
    ],
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
    "threads": [
        # BODY-PRICED. profile, user_posts and user_replies cost 2 credits
        # addressed by user_id and 4 by username - the handle has to be
        # resolved through people search first. The other three have no
        # username form and are always 2.
        create_threads_profile_tool,
        create_threads_user_posts_tool,
        create_threads_user_replies_tool,
        create_threads_post_tool,
        create_threads_post_comments_tool,
        create_threads_search_users_tool,
    ],
    "kuaishou": [
        # PRICED PER ENDPOINT, never per platform: profile 10, video 2,
        # videos_batch 40, the four search endpoints 10 each, the rest 1.
        create_kuaishou_profile_tool,
        create_kuaishou_user_posts_tool,
        create_kuaishou_user_live_tool,
        create_kuaishou_user_resolve_tool,
        create_kuaishou_video_tool,
        create_kuaishou_video_comments_tool,
        create_kuaishou_comment_replies_tool,
        create_kuaishou_videos_batch_tool,
        create_kuaishou_search_tool,
        create_kuaishou_search_videos_tool,
        create_kuaishou_search_users_tool,
        create_kuaishou_search_live_tool,
        create_kuaishou_tag_feed_tool,
        create_kuaishou_trending_tool,
    ],
    "ebay": [
        create_ebay_search_tool,
        create_ebay_product_tool,
        create_ebay_seller_tool,
    ],
    "target": [
        create_target_search_tool,
        create_target_category_tool,
        create_target_product_tool,
        create_target_reviews_tool,
    ],
    "home_depot": [
        create_home_depot_search_tool,
        create_home_depot_product_tool,
        create_home_depot_reviews_tool,
    ],
    "zillow": [
        create_zillow_search_tool,
        create_zillow_property_tool,
        create_zillow_agent_reviews_tool,
    ],
    "booking": [
        create_booking_search_tool,
        create_booking_hotel_tool,
        create_booking_reviews_tool,
    ],
    "tripadvisor": [
        # locations() is lookup-first: every other endpoint is keyed by ids
        # that only exist inside Tripadvisor's own URLs.
        create_tripadvisor_locations_tool,
        create_tripadvisor_search_tool,
        create_tripadvisor_location_tool,
        create_tripadvisor_reviews_tool,
    ],
    "indeed": [
        create_indeed_search_tool,
        create_indeed_job_tool,
        create_indeed_company_tool,
        create_indeed_company_reviews_tool,
    ],
    "airbnb": [
        create_airbnb_search_tool,
        create_airbnb_listing_tool,
        create_airbnb_reviews_tool,
    ],
    "glassdoor": [
        # companies() is lookup-first: the other three take an employer_id
        # that only exists inside Glassdoor's /Overview/ URLs.
        create_glassdoor_companies_tool,
        create_glassdoor_company_tool,
        create_glassdoor_reviews_tool,
        create_glassdoor_salaries_tool,
    ],
    "yelp": [
        create_yelp_search_tool,
        create_yelp_business_tool,
        create_yelp_reviews_tool,
    ],
    "app_store": [
        create_app_store_search_tool,
        create_app_store_app_tool,
        create_app_store_reviews_tool,
    ],
    "google_play": [
        create_google_play_search_tool,
        create_google_play_app_tool,
        create_google_play_reviews_tool,
    ],
    "sec": [
        # lookup() is lookup-first: callers hold a ticker, EDGAR is keyed by
        # CIK.
        create_sec_lookup_tool,
        create_sec_company_tool,
        create_sec_filings_tool,
        create_sec_concept_tool,
        create_sec_facts_tool,
        create_sec_search_tool,
    ],
    "redfin": [
        create_redfin_search_tool,
        create_redfin_property_tool,
        create_redfin_market_tool,
    ],
    "companies_house": [
        # search() is lookup-first: everything else is keyed by the company
        # number it returns.
        create_companies_house_search_tool,
        create_companies_house_company_tool,
        create_companies_house_officers_tool,
        create_companies_house_filing_history_tool,
    ],
    "g2": [
        create_g2_search_tool,
        create_g2_product_tool,
        create_g2_reviews_tool,
    ],
    "capterra": [
        create_capterra_search_tool,
        create_capterra_product_tool,
        create_capterra_reviews_tool,
    ],
    "google_ads": [
        # advertisers() is lookup-first: search() and creative() are keyed by
        # the advertiser_id it resolves.
        create_google_ads_advertisers_tool,
        create_google_ads_search_tool,
        create_google_ads_creative_tool,
    ],
    "meta_ads": [
        create_meta_ads_search_tool,
        create_meta_ads_advertiser_tool,
        create_meta_ads_ad_tool,
    ],
    "crawl": [
        # OPT-IN: map, crawl and batch, the multi-page members of the Extract
        # family. Crawl and batch bill per page, so this provider is left out
        # of the default set; pass enable_crawl=True or name it in providers.
        create_map_website_tool,
        create_crawl_website_tool,
        create_crawl_status_tool,
        create_batch_extract_tool,
        create_batch_status_tool,
    ],
}

# Providers loaded only when asked for by name (or enable_crawl=True).
_OPT_IN_PROVIDERS = frozenset({"crawl"})


def create_scavio_tools(
    api_key: str | None = None,
    max_results: int = 5,
    providers: list[str] | None = None,
    enable_crawl: bool = False,
) -> list[FunctionTool]:
    """Create Scavio search tools for AutoGen agents.

    Args:
        api_key: Scavio API key. If None, reads from SCAVIO_API_KEY env var.
        max_results: Default maximum results for search tools.
        providers: List of providers to include (e.g. ["google", "amazon"]).
            Defaults to every provider except the opt-in "crawl" provider.
        enable_crawl: Also include the "crawl" provider: map_website,
            crawl_website, crawl_status, batch_extract and batch_status.

    Returns:
        List of FunctionTool instances ready for use with AutoGen agents.
    """
    configure(api_key)

    selected = list(providers) if providers else [
        p for p in _PROVIDER_MAP if p not in _OPT_IN_PROVIDERS
    ]
    if enable_crawl and "crawl" not in selected:
        selected.append("crawl")
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
    "create_extract_tool",
    "create_map_website_tool",
    "create_crawl_website_tool",
    "create_crawl_status_tool",
    "create_batch_extract_tool",
    "create_batch_status_tool",
    "create_walmart_reviews_tool",
    "create_walmart_category_tool",
    "create_walmart_offers_tool",
    "create_walmart_seller_tool",
    "create_walmart_seller_products_tool",
    "create_threads_profile_tool",
    "create_threads_user_posts_tool",
    "create_threads_user_replies_tool",
    "create_threads_post_tool",
    "create_threads_post_comments_tool",
    "create_threads_search_users_tool",
    "create_kuaishou_profile_tool",
    "create_kuaishou_user_posts_tool",
    "create_kuaishou_user_live_tool",
    "create_kuaishou_user_resolve_tool",
    "create_kuaishou_video_tool",
    "create_kuaishou_video_comments_tool",
    "create_kuaishou_comment_replies_tool",
    "create_kuaishou_videos_batch_tool",
    "create_kuaishou_search_tool",
    "create_kuaishou_search_videos_tool",
    "create_kuaishou_search_users_tool",
    "create_kuaishou_search_live_tool",
    "create_kuaishou_tag_feed_tool",
    "create_kuaishou_trending_tool",
    "create_ebay_search_tool",
    "create_ebay_product_tool",
    "create_ebay_seller_tool",
    "create_target_search_tool",
    "create_target_category_tool",
    "create_target_product_tool",
    "create_target_reviews_tool",
    "create_home_depot_search_tool",
    "create_home_depot_product_tool",
    "create_home_depot_reviews_tool",
    "create_zillow_search_tool",
    "create_zillow_property_tool",
    "create_zillow_agent_reviews_tool",
    "create_booking_search_tool",
    "create_booking_hotel_tool",
    "create_booking_reviews_tool",
    "create_tripadvisor_locations_tool",
    "create_tripadvisor_search_tool",
    "create_tripadvisor_location_tool",
    "create_tripadvisor_reviews_tool",
    "create_indeed_search_tool",
    "create_indeed_job_tool",
    "create_indeed_company_tool",
    "create_indeed_company_reviews_tool",
    "create_airbnb_search_tool",
    "create_airbnb_listing_tool",
    "create_airbnb_reviews_tool",
    "create_glassdoor_companies_tool",
    "create_glassdoor_company_tool",
    "create_glassdoor_reviews_tool",
    "create_glassdoor_salaries_tool",
    "create_yelp_search_tool",
    "create_yelp_business_tool",
    "create_yelp_reviews_tool",
    "create_app_store_search_tool",
    "create_app_store_app_tool",
    "create_app_store_reviews_tool",
    "create_google_play_search_tool",
    "create_google_play_app_tool",
    "create_google_play_reviews_tool",
    "create_sec_lookup_tool",
    "create_sec_company_tool",
    "create_sec_filings_tool",
    "create_sec_concept_tool",
    "create_sec_facts_tool",
    "create_sec_search_tool",
    "create_redfin_search_tool",
    "create_redfin_property_tool",
    "create_redfin_market_tool",
    "create_companies_house_search_tool",
    "create_companies_house_company_tool",
    "create_companies_house_officers_tool",
    "create_companies_house_filing_history_tool",
    "create_g2_search_tool",
    "create_g2_product_tool",
    "create_g2_reviews_tool",
    "create_capterra_search_tool",
    "create_capterra_product_tool",
    "create_capterra_reviews_tool",
    "create_google_ads_advertisers_tool",
    "create_google_ads_search_tool",
    "create_google_ads_creative_tool",
    "create_meta_ads_search_tool",
    "create_meta_ads_advertiser_tool",
    "create_meta_ads_ad_tool",
]
