"""Scavio Yelp tools for AutoGen.

3 endpoints. 2 credits flat on all three endpoints.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_yelp_search_tool() -> FunctionTool:
    """Create a Scavio Yelp search tool."""

    async def scavio_yelp_search(
        term: Annotated[
            str | None,
            "What to look for (1-200 characters): a category ('plumbers'), a dish, or "
            "a business name. Required together with location unless url is given.",
        ] = None,
        location: Annotated[
            str | None,
            "Where to look (1-200 characters): city and region, a full address, or a "
            "postcode. Effectively required - without it Yelp picks a location itself, so the same request can answer about a different metro "
            "run to run.",
        ] = None,
        page: Annotated[
            int | None,
            "Results page, 1-based. Yelp fixes the page size at 10.",
        ] = None,
        sort: Annotated[
            Literal["recommended", "rating", "review_count"] | None,
            "Result ordering (upstream default 'recommended'). Closed enum: Yelp "
            "IGNORES an unrecognised sortby and serves default ranking under a 200, "
            "billing a premium scrape for a sort that never ran.",
        ] = None,
        price: Annotated[
            list[Literal[1, 2, 3, 4]] | None,
            "Price bands to include, 1 ($) to 4 ($$$$); 1-4 values, combined freely - "
            "[1, 2] means $ or $$.",
        ] = None,
        open_now: Annotated[
            bool | None,
            "Only businesses open at the moment of the request.",
        ] = None,
        attributes: Annotated[
            list[str] | None,
            "Raw Yelp filter aliases, max 20, each 1-100 characters "
            "('RestaurantsDelivery', 'GoodForKids', 'WheelchairAccessible'). A "
            "deliberate PASSTHROUGH, not an enum - Yelp's vocabulary runs to ~117 "
            "values per vertical and an alias it does not know is ignored upstream, "
            "returning unfiltered results.",
        ] = None,
        url: Annotated[
            str | None,
            "A full yelp.com/search URL (1-1000 characters) as an alternative to term "
            "+ location; the query, offset and sort are read out of it and the URL is "
            "rebuilt.",
        ] = None,
    ) -> str:
        """Businesses in Yelp's ranked order: rating, review count, price band,
        categories, address, contact rails, hours, photos, review snippet.

        Parameter rule: (term AND location) or url is required.

        Pagination: page - Yelp fixes the page size at 10.

        Args:
            term: What to look for (1-200 characters): a category ('plumbers'), a dish,
                or a business name. Required together with location unless url is given.
            location: Where to look (1-200 characters): city and region, a full address,
                or a postcode. Effectively required - without it Yelp picks a location itself, so the same request can answer about a different
                metro run to run.
            page: Results page, 1-based. Yelp fixes the page size at 10.
            sort: Result ordering (upstream default 'recommended'). Closed enum: Yelp
                IGNORES an unrecognised sortby and serves default ranking under a 200,
                billing a premium scrape for a sort that never ran.
            price: Price bands to include, 1 ($) to 4 ($$$$); 1-4 values, combined
                freely - [1, 2] means $ or $$.
            open_now: Only businesses open at the moment of the request.
            attributes: Raw Yelp filter aliases, max 20, each 1-100 characters
                ('RestaurantsDelivery', 'GoodForKids', 'WheelchairAccessible'). A
                deliberate PASSTHROUGH, not an enum - Yelp's vocabulary runs to ~117
                values per vertical and an alias it does not know is ignored upstream,
                returning unfiltered results.
            url: A full yelp.com/search URL (1-1000 characters) as an alternative to
                term + location; the query, offset and sort are read out of it and the
                URL is rebuilt.

        Returns:
            JSON string with businesses in Yelp's ranked order: rating, review count,
            price band, categories, address, contact rails, hours, photos, review
            snippet; each row carries business_id AND alias. count = the 10-row page,
            total_results = Yelp's headline count.
        """
        client = get_async_client()

        params: dict = {
            "term": term,
            "location": location,
            "page": page,
            "sort": sort,
            "price": price,
            "open_now": open_now,
            "attributes": attributes,
            "url": url,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.yelp.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_yelp_search,
        description=(
            "Businesses in Yelp's ranked order: rating, review count, price band, "
            "categories, address, contact rails, hours, photos and a review snippet; "
            "every row carries both business_id and alias. Yelp fixes the page size "
            "at 10. Provide term and location, or url. Costs 2 credits."
        ),
    )


def create_yelp_business_tool() -> FunctionTool:
    """Create a Scavio Yelp business tool."""

    async def scavio_yelp_business(
        business_id: Annotated[
            str | None,
            "A Yelp business alias ('desnudo-coffee-austin-2'), its opaque encid, or "
            "any yelp.com/biz URL carrying one (1-500 characters). Search rows return "
            "both id forms.",
        ] = None,
        url: Annotated[
            str | None,
            "A full yelp.com/biz URL (1-1000 characters) as an alternative to "
            "business_id.",
        ] = None,
    ) -> str:
        """One Yelp business in full: per-star histogram, price band, address and
        coordinates, hours, amenities, photos, health inspections, Q&A - PLUS the first
        page of reviews at no extra cost.

        Parameter rule: business_id or url is required.

        Args:
            business_id: A Yelp business alias ('desnudo-coffee-austin-2'), its opaque
                encid, or any yelp.com/biz URL carrying one (1-500 characters). Search
                rows return both id forms.
            url: A full yelp.com/biz URL (1-1000 characters) as an alternative to
                business_id.

        Returns:
            JSON string with one business in full: rating + per-star histogram, review
            count, price band, categories, address and coordinates, phone, website and
            menu links, hours and holidays, amenities, photos and videos, popular items,
            health inspections, Q&A, licences, claim status - PLUS the first page of
            reviews at no extra cost.
        """
        client = get_async_client()

        params: dict = {
            "business_id": business_id,
            "url": url,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.yelp.business(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_yelp_business,
        description=(
            "One business in full: rating and per-star histogram, review count, price "
            "band, categories, address and coordinates, phone, website and menu "
            "links, hours and holidays, amenities, photos and videos, popular items, "
            "health inspections, Q&A, licences and claim status - plus the first page "
            "of reviews at no extra cost. Provide business_id or url. Costs 2 "
            "credits."
        ),
    )


def create_yelp_reviews_tool() -> FunctionTool:
    """Create a Scavio Yelp reviews tool."""

    async def scavio_yelp_reviews(
        business_id: Annotated[
            str | None,
            "A Yelp business alias ('desnudo-coffee-austin-2'), its opaque encid, or "
            "any yelp.com/biz URL carrying one (1-500 characters).",
        ] = None,
        url: Annotated[
            str | None,
            "A full yelp.com/biz URL (1-1000 characters) as an alternative to "
            "business_id.",
        ] = None,
        page: Annotated[
            int | None,
            "Reviews page, 1-based, 10 per page. Page 1 duplicates the reviews "
            "business() already returned and costs another 2 credits - start at 2. A "
            "page past the last review is a 404, not an empty result.",
        ] = None,
        sort: Annotated[
            Literal[
                "relevance", "newest", "oldest", "rating_high", "rating_low", "elites",
            ]
            | None,
            "Review ordering (upstream default 'relevance'). Closed enum: Yelp "
            "IGNORES an unrecognised value and serves default ranking under a billed "
            "200.",
        ] = None,
        rating: Annotated[
            Literal[1, 2, 3, 4, 5] | None,
            "Only reviews at this star rating, 1-5. Changes filtered_review_count on "
            "the response, not review_count.",
        ] = None,
    ) -> str:
        """A page of Yelp reviews: rating, full text, language, author profile and
        expertise counts, attached photos, reaction counts, owner response.

        Parameter rule: business_id or url is required.

        Pagination: page - 10 per page; a page past the last is a 404, not an empty
        result.

        Args:
            business_id: A Yelp business alias ('desnudo-coffee-austin-2'), its opaque
                encid, or any yelp.com/biz URL carrying one (1-500 characters).
            url: A full yelp.com/biz URL (1-1000 characters) as an alternative to
                business_id.
            page: Reviews page, 1-based, 10 per page. Page 1 duplicates the reviews
                business() already returned and costs another 2 credits - start at 2. A
                page past the last review is a 404, not an empty result.
            sort: Review ordering (upstream default 'relevance'). Closed enum: Yelp
                IGNORES an unrecognised value and serves default ranking under a billed
                200.
            rating: Only reviews at this star rating, 1-5. Changes filtered_review_count
                on the response, not review_count.

        Returns:
            JSON string with a page of reviews: rating, full text, language, author
            profile and expertise counts, attached photos, reaction counts, owner
            response.
        """
        client = get_async_client()

        params: dict = {
            "business_id": business_id,
            "url": url,
            "page": page,
            "sort": sort,
            "rating": rating,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.yelp.reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_yelp_reviews,
        description=(
            "A page of reviews: rating, full text, language, author profile and "
            "expertise counts, attached photos, reaction counts and owner response. "
            "10 per page. PAGE 1 IS REDUNDANT - it re-fetches the document business() "
            "already returned - so start at page 2. Provide business_id or url. Costs "
            "2 credits."
        ),
    )
