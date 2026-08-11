"""Scavio Google Ads Transparency tools for AutoGen.

3 endpoints. 1 credit flat on all three endpoints.

LOOKUP FIRST: create_google_ads_advertisers_tool is the entry point. Every other Google
Ads Transparency endpoint is keyed by an id that only exists inside Google Ads
Transparency's own URLs, so a caller holding a name has to resolve it here before
anything else will answer.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_google_ads_advertisers_tool() -> FunctionTool:
    """Create a Scavio Google Ads Transparency advertisers tool."""

    async def scavio_google_ads_advertisers(
        query: Annotated[str, "Brand name or domain to resolve (1-200 characters)."],
        region: Annotated[
            str | None,
            "ISO 3166-1 alpha-2 country ('US', 'GB', 'DE') or a Google geo criteria "
            "id as a string (2-12 characters). Default: no region filter.",
        ] = None,
        limit: Annotated[
            int | None,
            "Rows per arm (1-20; server default 10). Advertisers and domains are "
            "capped separately, so a name query can return up to twice this many "
            "rows.",
        ] = None,
    ) -> str:
        """START HERE. Resolve a brand name or domain to the advertiser_id /search and
        /creative are keyed by. Returns `advertiser` rows (id, verified name,
        verification country, total ad count as a RANGE) and `domain` rows.

        Args:
            query: Brand name or domain to resolve (1-200 characters).
            region: ISO 3166-1 alpha-2 country ('US', 'GB', 'DE') or a Google geo
                criteria id as a string (2-12 characters). Default: no region filter.
            limit: Rows per arm (1-20; server default 10). Advertisers and domains are
                capped separately, so a name query can return up to twice this many
                rows.

        Returns:
            JSON string with lOOKUP: two row kinds in one list - `advertiser` rows carry
            the id, verified name, verification country and total ad count as a range;
            `domain` rows carry a website. A name query returns both; a domain-shaped
            query returns domains only. NO PAGINATION.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "region": region,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.google_ads.advertisers(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_google_ads_advertisers,
        description=(
            "Resolve a brand name or domain to the advertiser_id that search() and "
            "creative() are keyed by. Returns two row kinds in one list: 'advertiser' "
            "rows carrying the id, verified name, verification country and total ad "
            "count as a range, and 'domain' rows carrying a website. A name query "
            "returns both kinds; a domain-shaped query returns domains only. "
            "Autocomplete-backed, roughly 20 rows per arm, and it does not paginate. "
            "Costs 1 credit."
        ),
    )


def create_google_ads_search_tool() -> FunctionTool:
    """Create a Scavio Google Ads Transparency search tool."""

    async def scavio_google_ads_search(
        domain: Annotated[
            str | None,
            "Advertiser website (1-253 characters): bare host, www host or full URL, "
            "reduced to the registrable host. The only way to get `domain` back on "
            "each row.",
        ] = None,
        advertiser_id: Annotated[
            str | None,
            "Google advertiser id, e.g. 'AR16735076323512287233' (3-40 characters). "
            "The shape is checked before any request, so a typo costs no credits. "
            "Querying by id drops `domain` from every row.",
        ] = None,
        region: Annotated[
            str | None,
            "ISO 3166-1 alpha-2 country ('US', 'GB', 'DE') or a Google geo criteria "
            "id as a string (2-12 characters). Scopes the deep links on every row, "
            "and the same advertiser can share zero creatives between two countries. "
            "Default: worldwide.",
        ] = None,
        format: Annotated[
            Literal["text", "image", "video"] | None,
            "Creative format. The three sets are disjoint -- an advertiser's text, "
            "image and video ads share no creatives. Default: all formats.",
        ] = None,
        platform: Annotated[
            Literal["play", "maps", "search", "shopping", "youtube"] | None,
            "Google surface the ad ran on. Default: all surfaces.",
        ] = None,
        topic: Annotated[
            Literal["all", "political"] | None,
            "Ad topic (server default 'all').",
        ] = None,
        limit: Annotated[
            int | None,
            "Ads per page (1-100; server default 40). 100 is a hard upstream ceiling, "
            "not our policy: Google answers a larger request with zero rows rather "
            "than an error.",
        ] = None,
        cursor: Annotated[
            str | None,
            "next_cursor from the previous response (1-4000 characters), 100 ads per "
            "page. Re-send the same filters alongside it; next_cursor is null once "
            "exhausted.",
        ] = None,
    ) -> str:
        """Every ad Google is running for one advertiser: the creative, advertiser id
        and name, format, first/last seen dates, days actually run, plus
        total_ads_min/total_ads_max.

        Parameter rule: domain or advertiser_id is required.

        Pagination: cursor -> next_cursor, 100 per page. Re-send the SAME filters
        alongside the cursor.

        Args:
            domain: Advertiser website (1-253 characters): bare host, www host or full
                URL, reduced to the registrable host. The only way to get `domain` back
                on each row.
            advertiser_id: Google advertiser id, e.g. 'AR16735076323512287233' (3-40
                characters). The shape is checked before any request, so a typo costs no
                credits. Querying by id drops `domain` from every row.
            region: ISO 3166-1 alpha-2 country ('US', 'GB', 'DE') or a Google geo
                criteria id as a string (2-12 characters). Scopes the deep links on
                every row, and the same advertiser can share zero creatives between two
                countries. Default: worldwide.
            format: Creative format. The three sets are disjoint -- an advertiser's
                text, image and video ads share no creatives. Default: all formats.
            platform: Google surface the ad ran on. Default: all surfaces.
            topic: Ad topic (server default 'all').
            limit: Ads per page (1-100; server default 40). 100 is a hard upstream
                ceiling, not our policy: Google answers a larger request with zero rows
                rather than an error.
            cursor: next_cursor from the previous response (1-4000 characters), 100 ads
                per page. Re-send the same filters alongside it; next_cursor is null
                once exhausted.

        Returns:
            JSON string with every ad Google is running for one advertiser: the creative
            (archived image, rich-media bundle, Google's renderer link, dimensions),
            advertiser id and name, format, first/last seen dates, days actually run,
            plus total_ads_min/total_ads_max and next_cursor.
        """
        client = get_async_client()

        params: dict = {
            "domain": domain,
            "advertiser_id": advertiser_id,
            "region": region,
            "format": format,
            "platform": platform,
            "topic": topic,
            "limit": limit,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.google_ads.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_google_ads_search,
        description=(
            "Every ad Google Ads Transparency holds for one advertiser: the creative "
            "(archived image, rich-media bundle, Google's renderer link, dimensions), "
            "advertiser id and name, format, first and last seen dates and days "
            "actually run, plus total_ads_min and total_ads_max -- Google publishes "
            "the advertiser's ad total as a range, never an exact figure. Up to 100 "
            "ads per page (server default 40); paginate by sending next_cursor back "
            "as cursor alongside the SAME filters. Provide domain or advertiser_id. "
            "Costs 1 credit."
        ),
    )


def create_google_ads_creative_tool() -> FunctionTool:
    """Create a Scavio Google Ads Transparency creative tool."""

    async def scavio_google_ads_creative(
        advertiser_id: Annotated[
            str,
            "Google advertiser id, e.g. 'AR16735076323512287233' (3-40 characters).",
        ],
        creative_id: Annotated[
            str,
            "Creative id (3-40 characters). It must belong to the advertiser_id sent "
            "with it -- the lookup is keyed by the pair and a mismatched pair is a "
            "404.",
        ],
    ) -> str:
        """One Google ad creative in full and the ONLY endpoint carrying its history:
        every size variation, the impression bucket, the per-region breakdown with
        first/last shown dates and a per-surface impression split, and the funder
        disclosure on political ads.

        Args:
            advertiser_id: Google advertiser id, e.g. 'AR16735076323512287233' (3-40
                characters).
            creative_id: Creative id (3-40 characters). It must belong to the
                advertiser_id sent with it -- the lookup is keyed by the pair and a
                mismatched pair is a 404.

        Returns:
            JSON string with one creative in full and the ONLY endpoint carrying its
            history: every size variation of the asset, the impression bucket, the
            per-region breakdown with first/last shown dates and a per-surface
            impression split inside each region, the format, Google's category label,
            and the funder disclosure on political ads.
        """
        client = get_async_client()

        params: dict = {
            "advertiser_id": advertiser_id,
            "creative_id": creative_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.google_ads.creative(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_google_ads_creative,
        description=(
            "One creative in full, and the only endpoint carrying its history: every "
            "size variation of the asset, the impression bucket, the per-region "
            "breakdown with first and last shown dates and a per-surface impression "
            "split inside each region, the format, Google's category label and the "
            "funder disclosure on political ads. Impressions and first_shown are "
            "EEA-only (DSA-compelled) and come back null for US creatives, and an "
            "impression bucket may carry only a lower or only an upper bound. Costs 1 "
            "credit."
        ),
    )
