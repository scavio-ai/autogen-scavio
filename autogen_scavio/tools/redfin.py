"""Scavio Redfin tools for AutoGen.

3 endpoints. 1 credit flat on all three endpoints.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_redfin_search_tool() -> FunctionTool:
    """Create a Scavio Redfin search tool."""

    async def scavio_redfin_search(
        location: Annotated[
            str | None,
            "A redfin.com region URL (/city/, /neighborhood/, /county/, /zipcode/) or "
            "a bare 5-digit ZIP (1-500 characters). CITY NAMES ARE NOT ACCEPTED - "
            "Redfin's own name lookup is blocked to us; use region_id + region_type "
            "instead.",
        ] = None,
        region_id: Annotated[
            int | None,
            "Redfin internal region id (>= 1), used together with region_type. NOT a "
            "ZIP code - the two are different number spaces and a ZIP here resolves "
            "to another city rather than failing.",
        ] = None,
        region_type: Annotated[
            Literal[1, 2, 5, 6] | None,
            "Region kind that region_id belongs to: 1 neighborhood, 2 ZIP, 5 county, "
            "6 city. Must be sent together with region_id or both are ignored in "
            "favour of location.",
        ] = None,
        listing_status: Annotated[
            Literal["for_sale", "sold", "for_rent"] | None,
            "Market to search. Defaults to 'for_sale'.",
        ] = None,
        sold_within_days: Annotated[
            int | None,
            "Sold within the last N days (>= 1). REJECTED unless "
            "listing_status='sold', where it defaults to 90.",
        ] = None,
        page: Annotated[
            int | None,
            "Results page, 1-based; page size is whatever limit is set to. No upper "
            "bound.",
        ] = None,
        limit: Annotated[
            int | None,
            "Listings per page, 1-350. Defaults to 100.",
        ] = None,
        sort: Annotated[
            Literal[
                "recommended", "price_low", "price_high", "newest", "oldest",
                "sqft_low", "sqft_high", "price_per_sqft_low", "price_per_sqft_high",
            ]
            | None,
            "Result sort order. Defaults to 'recommended', Redfin's own ranking.",
        ] = None,
        min_price: Annotated[
            float | None,
            "Minimum price, inclusive (>= 0). Monthly rent when "
            "listing_status='for_rent'.",
        ] = None,
        max_price: Annotated[
            float | None,
            "Maximum price, inclusive (>= 0). Monthly rent when "
            "listing_status='for_rent'.",
        ] = None,
        beds_min: Annotated[
            int | None,
            "Minimum bedrooms (whole number >= 0); fractional values are rejected.",
        ] = None,
        beds_max: Annotated[
            int | None,
            "Maximum bedrooms (whole number >= 0); fractional values are rejected.",
        ] = None,
        baths_min: Annotated[
            int | None,
            "Minimum bathrooms (whole number >= 0). WHOLE BATHS ONLY - 1.5 is "
            "rejected rather than silently truncated to 1. There is no baths_max.",
        ] = None,
        sqft_min: Annotated[
            int | None,
            "Minimum living area in square feet (whole number >= 0).",
        ] = None,
        sqft_max: Annotated[
            int | None,
            "Maximum living area in square feet (whole number >= 0).",
        ] = None,
        lot_size_min: Annotated[
            int | None,
            "Minimum lot size in square feet (whole number >= 0). There is no "
            "lot_size_max.",
        ] = None,
        year_built_min: Annotated[
            int | None,
            "Earliest year built (whole number >= 0).",
        ] = None,
        year_built_max: Annotated[
            int | None,
            "Latest year built (whole number >= 0).",
        ] = None,
        max_hoa: Annotated[
            float | None,
            "Maximum monthly HOA fee in dollars (>= 0).",
        ] = None,
        property_type: Annotated[
            Literal[
                "house", "condo", "townhouse", "multi_family", "land", "other", "co_op",
            ]
            | None,
            "Restrict to one property type.",
        ] = None,
        has_pool: Annotated[bool | None, "Only listings with a pool."] = None,
        max_days_on_market: Annotated[
            int | None,
            "Listed at most N days ago (whole number >= 0). Cannot be combined with "
            "min_days_on_market - Redfin expresses both bounds through one param.",
        ] = None,
        min_days_on_market: Annotated[
            int | None,
            "Listed at least N days ago (whole number >= 0). Cannot be combined with "
            "max_days_on_market.",
        ] = None,
    ) -> str:
        """Redfin listings: price, price per sqft, beds, baths, living area, lot size,
        year built, coordinates, listing remarks, full photo galleries.

        Parameter rule: location OR (region_id AND region_type); region halves paired;
        max/min_days_on_market mutually exclusive; sold_within_days requires
        listing_status=sold.

        Pagination: page + limit - up to 350 per page.

        Args:
            location: A redfin.com region URL (/city/, /neighborhood/, /county/,
                /zipcode/) or a bare 5-digit ZIP (1-500 characters). CITY NAMES ARE NOT
                ACCEPTED - Redfin's own name lookup is blocked to us; use region_id +
                region_type instead.
            region_id: Redfin internal region id (>= 1), used together with region_type.
                NOT a ZIP code - the two are different number spaces and a ZIP here
                resolves to another city rather than failing.
            region_type: Region kind that region_id belongs to: 1 neighborhood, 2 ZIP, 5
                county, 6 city. Must be sent together with region_id or both are ignored
                in favour of location.
            listing_status: Market to search. Defaults to 'for_sale'.
            sold_within_days: Sold within the last N days (>= 1). REJECTED unless
                listing_status='sold', where it defaults to 90.
            page: Results page, 1-based; page size is whatever limit is set to. No upper
                bound.
            limit: Listings per page, 1-350. Defaults to 100.
            sort: Result sort order. Defaults to 'recommended', Redfin's own ranking.
            min_price: Minimum price, inclusive (>= 0). Monthly rent when
                listing_status='for_rent'.
            max_price: Maximum price, inclusive (>= 0). Monthly rent when
                listing_status='for_rent'.
            beds_min: Minimum bedrooms (whole number >= 0); fractional values are
                rejected.
            beds_max: Maximum bedrooms (whole number >= 0); fractional values are
                rejected.
            baths_min: Minimum bathrooms (whole number >= 0). WHOLE BATHS ONLY - 1.5 is
                rejected rather than silently truncated to 1. There is no baths_max.
            sqft_min: Minimum living area in square feet (whole number >= 0).
            sqft_max: Maximum living area in square feet (whole number >= 0).
            lot_size_min: Minimum lot size in square feet (whole number >= 0). There is
                no lot_size_max.
            year_built_min: Earliest year built (whole number >= 0).
            year_built_max: Latest year built (whole number >= 0).
            max_hoa: Maximum monthly HOA fee in dollars (>= 0).
            property_type: Restrict to one property type.
            has_pool: Only listings with a pool.
            max_days_on_market: Listed at most N days ago (whole number >= 0). Cannot be
                combined with min_days_on_market - Redfin expresses both bounds through
                one param.
            min_days_on_market: Listed at least N days ago (whole number >= 0). Cannot
                be combined with max_days_on_market.

        Returns:
            JSON string with listings: price, price per sqft, beds, baths, living area,
            lot size, year built, coordinates, listing remarks, days on market, full
            photo galleries. Up to 350 per page.
        """
        client = get_async_client()

        params: dict = {
            "location": location,
            "region_id": region_id,
            "region_type": region_type,
            "listing_status": listing_status,
            "sold_within_days": sold_within_days,
            "page": page,
            "limit": limit,
            "sort": sort,
            "min_price": min_price,
            "max_price": max_price,
            "beds_min": beds_min,
            "beds_max": beds_max,
            "baths_min": baths_min,
            "sqft_min": sqft_min,
            "sqft_max": sqft_max,
            "lot_size_min": lot_size_min,
            "year_built_min": year_built_min,
            "year_built_max": year_built_max,
            "max_hoa": max_hoa,
            "property_type": property_type,
            "has_pool": has_pool,
            "max_days_on_market": max_days_on_market,
            "min_days_on_market": min_days_on_market,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.redfin.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_redfin_search,
        description=(
            "Redfin listings: price, price per sqft, beds, baths, living area, lot "
            "size, year built, coordinates, listing remarks and full photo galleries, "
            "for sale, sold or for rent. Up to 350 per page. Provide location, or "
            "region_id together with region_type. Costs 1 credit."
        ),
    )


def create_redfin_property_tool() -> FunctionTool:
    """Create a Scavio Redfin property tool."""

    async def scavio_redfin_property(
        property_id: Annotated[
            str,
            "Redfin property id, or any redfin.com listing URL carrying one (1-500 "
            "characters).",
        ],
    ) -> str:
        """One Redfin listing in full: price, Redfin Estimate and rental estimate,
        complete MLS fact sheet, price and tax history, agents, schools, climate risk,
        comparable sales, photos.

        Args:
            property_id: Redfin property id, or any redfin.com listing URL carrying one
                (1-500 characters).

        Returns:
            JSON string with one listing in full: price, Redfin Estimate and rental
            estimate, complete MLS fact sheet, price and tax history, listing agents,
            open houses, schools, climate risk, walkability and location scores, sun
            exposure, monthly weather, permits, zoning, comparable sales, photos.
        """
        client = get_async_client()

        params: dict = {
            "property_id": property_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.redfin.property(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_redfin_property,
        description=(
            "One Redfin listing in full: price, Redfin Estimate and rental estimate, "
            "complete MLS fact sheet, price and tax history, listing agents, open "
            "houses, schools, climate risk, walkability, sun exposure, monthly "
            "weather, permits, zoning, comparable sales and photos. Costs 1 credit."
        ),
    )


def create_redfin_market_tool() -> FunctionTool:
    """Create a Scavio Redfin market tool."""

    async def scavio_redfin_market(
        location: Annotated[
            str | None,
            "A redfin.com region URL (/city/, /neighborhood/, /county/, /zipcode/) or "
            "a bare 5-digit ZIP (1-500 characters). City names are not accepted.",
        ] = None,
        region_id: Annotated[
            int | None,
            "Redfin internal region id (>= 1), used together with region_type. Not a "
            "ZIP code.",
        ] = None,
        region_type: Annotated[
            Literal[1, 2, 5, 6] | None,
            "Region kind that region_id belongs to: 1 neighborhood, 2 ZIP, 5 county, "
            "6 city. Must be sent together with region_id or both are ignored in "
            "favour of location.",
        ] = None,
    ) -> str:
        """Redfin housing-market stats for a region: median list and sale price, price
        per sqft, sale-to-list ratio, average offers and days on market, YoY movement,
        0-100 compete score, live inventory.

        Parameter rule: location OR (region_id AND region_type); region halves paired.

        Args:
            location: A redfin.com region URL (/city/, /neighborhood/, /county/,
                /zipcode/) or a bare 5-digit ZIP (1-500 characters). City names are not
                accepted.
            region_id: Redfin internal region id (>= 1), used together with region_type.
                Not a ZIP code.
            region_type: Region kind that region_id belongs to: 1 neighborhood, 2 ZIP, 5
                county, 6 city. Must be sent together with region_id or both are ignored
                in favour of location.

        Returns:
            JSON string with housing-market stats for a region: median list and sale
            price, price per sqft, sale-to-list ratio, average offers and days on
            market, YoY movement, Redfin's 0-100 compete score, live inventory by
            property type, median price and active listings per bedroom count, Redfin
            agent presence and aggregate rating.
        """
        client = get_async_client()

        params: dict = {
            "location": location,
            "region_id": region_id,
            "region_type": region_type,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.redfin.market(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_redfin_market,
        description=(
            "Redfin housing-market stats for a region: median list and sale price, "
            "price per sqft, sale-to-list ratio, average offers and days on market, "
            "YoY movement, 0-100 compete score, live inventory by property type and "
            "by bedroom count, and Redfin agent presence. Provide location, or "
            "region_id together with region_type. Costs 1 credit."
        ),
    )
