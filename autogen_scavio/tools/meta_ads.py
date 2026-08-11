"""Scavio Meta Ad Library tools for AutoGen.

3 endpoints. 1 credit flat on all three endpoints, and every cursor page is another
credit. Page 1 is 30 ads, each page after it is 10, so walking a whole query costs
roughly one credit per ten ads past the first thirty.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_meta_ads_search_tool() -> FunctionTool:
    """Create a Scavio Meta Ad Library search tool."""

    async def scavio_meta_ads_search(
        query: Annotated[
            str,
            "Keyword to search the ad library for (1-200 characters).",
        ],
        country: Annotated[
            str | None,
            "Ad library country as an exactly 2-character ISO 3166-1 alpha-2 code "
            "(server default 'US').",
        ] = None,
        active_status: Annotated[
            Literal["all", "active", "inactive"] | None,
            "Whether the ad is still running (server default 'all').",
        ] = None,
        ad_type: Annotated[
            Literal["all", "political_and_issue_ads"] | None,
            "Set 'political_and_issue_ads' to expose spend, reach, impressions and "
            "the paid-for-by disclosure; commercial ads leave all four null (server "
            "default 'all').",
        ] = None,
        media_type: Annotated[
            Literal["all", "image", "video", "meme", "image_and_meme", "none"] | None,
            "Creative media filter. Default: no media filter.",
        ] = None,
        search_type: Annotated[
            Literal["keyword_unordered", "keyword_exact_phrase"] | None,
            "How the query is matched (server default 'keyword_unordered').",
        ] = None,
        cursor: Annotated[
            str | None,
            "next_cursor from the previous response: page 1 is 30 ads, every cursor "
            "page is 10. The cursor is a self-contained blob, so ALL other filters "
            "are ignored when it is present.",
        ] = None,
    ) -> str:
        """Search the Meta Ad Library: 30 ads on page 1 with full creative (page name,
        ad copy, headline, CTA, images and videos, platforms, run dates), then
        cursor-paginated.

        Pagination: FULL CURSOR PAGINATION - page 1 = 30 ads via SSR, then 10 per page
        via a GraphQL POST off next_cursor. Walk has_next_page to scrape a whole query.
        THE BIG DIFFERENTIATOR over the $79-399/mo tools - lead with it.

        Args:
            query: Keyword to search the ad library for (1-200 characters).
            country: Ad library country as an exactly 2-character ISO 3166-1 alpha-2
                code (server default 'US').
            active_status: Whether the ad is still running (server default 'all').
            ad_type: Set 'political_and_issue_ads' to expose spend, reach, impressions
                and the paid-for-by disclosure; commercial ads leave all four null
                (server default 'all').
            media_type: Creative media filter. Default: no media filter.
            search_type: How the query is matched (server default 'keyword_unordered').
            cursor: next_cursor from the previous response: page 1 is 30 ads, every
                cursor page is 10. The cursor is a self-contained blob, so ALL other
                filters are ignored when it is present.

        Returns:
            JSON string with 30 ads (page 1) with full creative: page name, ad copy,
            headline, CTA, images and videos, platforms each ran on, run dates, and -
            for political/issue ads - spend, reach, impressions and the paid-for-by
            disclosure. Plus total_results, total_is_capped, has_next_page, next_cursor.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "country": country,
            "active_status": active_status,
            "ad_type": ad_type,
            "media_type": media_type,
            "search_type": search_type,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.meta_ads.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_meta_ads_search,
        description=(
            "Search the Meta Ad Library by keyword: 30 ads on page 1 with the full "
            "creative -- page name, ad copy, headline, CTA, images and videos, the "
            "platforms each ran on and its run dates -- then 10 ads per cursor page, "
            "walking has_next_page to the end of the query. total_results caps at "
            "50000 with total_is_capped true, because Meta only reports '>50,000'; "
            "never present it as an exact count. Every page costs 1 credit."
        ),
    )


def create_meta_ads_advertiser_tool() -> FunctionTool:
    """Create a Scavio Meta Ad Library advertiser tool."""

    async def scavio_meta_ads_advertiser(
        page_id: Annotated[
            str,
            "The advertiser's numeric Facebook Page id (3-25 digits, as a string).",
        ],
        country: Annotated[
            str | None,
            "Ad library country as an exactly 2-character ISO 3166-1 alpha-2 code "
            "(server default 'US').",
        ] = None,
        active_status: Annotated[
            Literal["all", "active", "inactive"] | None,
            "Whether the ad is still running (server default 'all').",
        ] = None,
        ad_type: Annotated[
            Literal["all", "political_and_issue_ads"] | None,
            "Set 'political_and_issue_ads' to expose spend, reach, impressions and "
            "the paid-for-by disclosure; commercial ads leave all four null (server "
            "default 'all').",
        ] = None,
        media_type: Annotated[
            Literal["all", "image", "video", "meme", "image_and_meme", "none"] | None,
            "Creative media filter. Default: no media filter.",
        ] = None,
        cursor: Annotated[
            str | None,
            "next_cursor from the previous response: page 1 is 30 ads, every cursor "
            "page is 10. ALL other filters are ignored when it is present.",
        ] = None,
    ) -> str:
        """Every ad a Facebook Page is running, by numeric page id - 30 ads on page 1
        with the same creative detail as search, cursor-paginated at 10 per page
        thereafter.

        Pagination: cursor -> next_cursor; page 1 = 30 ads, then 10 per page. Walk
        has_next_page.

        Args:
            page_id: The advertiser's numeric Facebook Page id (3-25 digits, as a
                string).
            country: Ad library country as an exactly 2-character ISO 3166-1 alpha-2
                code (server default 'US').
            active_status: Whether the ad is still running (server default 'all').
            ad_type: Set 'political_and_issue_ads' to expose spend, reach, impressions
                and the paid-for-by disclosure; commercial ads leave all four null
                (server default 'all').
            media_type: Creative media filter. Default: no media filter.
            cursor: next_cursor from the previous response: page 1 is 30 ads, every
                cursor page is 10. ALL other filters are ignored when it is present.

        Returns:
            JSON string with every ad a Facebook Page is running, by numeric page id -
            30 ads (page 1) with the same creative detail as search, cursor-paginated at
            10/page thereafter.
        """
        client = get_async_client()

        params: dict = {
            "page_id": page_id,
            "country": country,
            "active_status": active_status,
            "ad_type": ad_type,
            "media_type": media_type,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.meta_ads.advertiser(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_meta_ads_advertiser,
        description=(
            "Every ad a Facebook Page is running, by numeric page id: 30 ads on page "
            "1 with the same creative detail as search(), then 10 ads per cursor "
            "page, walking has_next_page to the end of the advertiser. Every page "
            "costs 1 credit."
        ),
    )


def create_meta_ads_ad_tool() -> FunctionTool:
    """Create a Scavio Meta Ad Library ad tool."""

    async def scavio_meta_ads_ad(
        ad_archive_id: Annotated[str, "Meta ad archive id (3-25 digits, as a string)."],
    ) -> str:
        """One Meta ad in full by archive id: creative, advertiser, run dates,
        platforms, any political disclosure.

        Args:
            ad_archive_id: Meta ad archive id (3-25 digits, as a string).

        Returns:
            JSON string with one ad in full by archive id: creative, advertiser, run
            dates, platforms, any political disclosure.
        """
        client = get_async_client()

        params: dict = {
            "ad_archive_id": ad_archive_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.meta_ads.ad(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_meta_ads_ad,
        description=(
            "One Meta ad in full by archive id: creative, advertiser, run dates, the "
            "platforms it ran on, and the political disclosure when the ad carries "
            "one. Commercial ads leave spend, reach and impressions null. Costs 1 "
            "credit."
        ),
    )
