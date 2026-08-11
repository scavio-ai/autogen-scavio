"""Scavio G2 Software Reviews tools for AutoGen.

3 endpoints. 5 credits flat on all three endpoints - the dearest platform Scavio serves.
Budget for it before looping over a product list.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_g2_search_tool() -> FunctionTool:
    """Create a Scavio G2 Software Reviews search tool."""

    async def scavio_g2_search(
        query: Annotated[
            str | None,
            "Search term (1-200 characters). Provide this or url.",
        ] = None,
        page: Annotated[
            int | None,
            "1-based page number; page size follows limit (server default 20). G2 "
            "keeps paginating well past its own widget's page links.",
        ] = None,
        limit: Annotated[
            int | None,
            "Results per page (1-100; server default 20). The 100 ceiling is ours, to "
            "keep a single request inside the 60s deadline; G2 itself paginates at "
            "any size.",
        ] = None,
        sort: Annotated[
            Literal["relevance", "popular", "alphabetical", "rating"] | None,
            "Result sort order (server default 'relevance'). Closed enum: G2 silently "
            "accepts an unknown sort and answers 200 with an unstated ordering.",
        ] = None,
        rating: Annotated[
            Literal[1, 2, 3, 4, 5] | None,
            "Only products at or above this star rating (1-5, sent as an integer). "
            "Omit for no rating floor.",
        ] = None,
        url: Annotated[
            str | None,
            "Full g2.com/search URL, as an alternative to query (1-1000 characters; "
            "the host is checked by the transport).",
        ] = None,
    ) -> str:
        """Search G2 for B2B software products: star rating, review count, vendor,
        categories, seller description, logo; each row carries product_id and slug.

        Parameter rule: query or url is required.

        Pagination: page + limit - `limit` capped at 100 on our side; G2 itself keeps
        paginating at any size.

        Args:
            query: Search term (1-200 characters). Provide this or url.
            page: 1-based page number; page size follows limit (server default 20). G2
                keeps paginating well past its own widget's page links.
            limit: Results per page (1-100; server default 20). The 100 ceiling is ours,
                to keep a single request inside the 60s deadline; G2 itself paginates at
                any size.
            sort: Result sort order (server default 'relevance'). Closed enum: G2
                silently accepts an unknown sort and answers 200 with an unstated
                ordering.
            rating: Only products at or above this star rating (1-5, sent as an
                integer). Omit for no rating floor.
            url: Full g2.com/search URL, as an alternative to query (1-1000 characters;
                the host is checked by the transport).

        Returns:
            JSON string with ranked software products: star rating, review count,
            vendor, categories, seller description, logo; each row carries product_id
            and slug. Plus total_results and total_by_type.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "page": page,
            "limit": limit,
            "sort": sort,
            "rating": rating,
            "url": url,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.g2.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_g2_search,
        description=(
            "Search G2, the B2B software review site, for products: star rating, "
            "review count, vendor, categories, seller description and logo, with "
            "product_id and slug on every row. Up to 100 results per page (server "
            "default 20) and page-paginated; total_results is G2's Products-tab "
            "headline and caps at 10000, while total_by_type splits the query across "
            "products, sellers, categories and discussions. Provide query or url. "
            "Costs 5 credits."
        ),
    )


def create_g2_product_tool() -> FunctionTool:
    """Create a Scavio G2 Software Reviews product tool."""

    async def scavio_g2_product(
        product_id: Annotated[
            str | None,
            "G2 product slug ('notion') or the numeric G2 id ('82623') as a string "
            "(1-200 characters); both resolve on the same upstream path.",
        ] = None,
        url: Annotated[
            str | None,
            "Full g2.com product URL, as an alternative to product_id (1-1000 "
            "characters).",
        ] = None,
    ) -> str:
        """Full G2 software profile: rating and per-star histogram, vendor, pricing
        editions with parsed amounts, feature groups, integrations, alternatives,
        comparisons, and G2's AI-derived pros and cons.

        Parameter rule: product_id or url is required.

        Args:
            product_id: G2 product slug ('notion') or the numeric G2 id ('82623') as a
                string (1-200 characters); both resolve on the same upstream path.
            url: Full g2.com product URL, as an alternative to product_id (1-1000
                characters).

        Returns:
            JSON string with full profile: rating and per-star histogram, review count,
            vendor, description and seller website, pricing editions with parsed
            amounts, feature groups, categories and breadcrumbs, supported languages,
            integrations, alternatives, head-to-head comparisons, media, community
            discussions, and G2's AI-derived pros and cons. NO REVIEW TEXT.
        """
        client = get_async_client()

        params: dict = {
            "product_id": product_id,
            "url": url,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.g2.product(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_g2_product,
        description=(
            "Full G2 product profile: rating with per-star histogram, review count, "
            "vendor, description and seller website, pricing editions with parsed "
            "amounts, feature groups, categories and breadcrumbs, supported "
            "languages, integrations, alternatives, head-to-head comparisons, media, "
            "community discussions and G2's AI-derived pros and cons. Carries NO "
            "review text at all -- G2 loads review bodies in a separate frame, so "
            "call reviews() for those. Provide product_id or url. Costs 5 credits."
        ),
    )


def create_g2_reviews_tool() -> FunctionTool:
    """Create a Scavio G2 Software Reviews reviews tool."""

    async def scavio_g2_reviews(
        product_id: Annotated[
            str | None,
            "G2 product slug or numeric G2 id as a string (1-200 characters).",
        ] = None,
        url: Annotated[
            str | None,
            "Full g2.com reviews URL, as an alternative to product_id (1-1000 "
            "characters).",
        ] = None,
        page: Annotated[
            int | None,
            "1-based page number; fixed at 10 reviews per page.",
        ] = None,
        sort: Annotated[
            Literal["relevance", "newest", "most_helpful", "rating_high", "rating_low"]
            | None,
            "Review sort order (server default 'relevance'). Closed enum: an unknown "
            "sort is silently accepted upstream and never runs.",
        ] = None,
        rating: Annotated[
            Literal[1, 2, 3, 4, 5] | None,
            "Only reviews in this star bucket (1-5, sent as an integer). Buckets are "
            "half- star-inclusive: 1 returns 0, 0.5 and 1-star reviews.",
        ] = None,
        company_size: Annotated[
            Literal["small_business", "mid_market", "enterprise"] | None,
            "Reviewer company size: small_business is 50 employees or fewer, "
            "mid_market 51-1000, enterprise over 1000. Closed enum -- an unknown "
            "value matches nothing and returns a billed 'Reviews (0)'.",
        ] = None,
        role: Annotated[
            Literal[
                "user", "administrator", "executive_sponsor", "internal_consultant",
                "consultant", "agency", "industry_analyst",
            ]
            | None,
            "Reviewer role. Closed enum -- an unknown value matches nothing rather "
            "than erroring.",
        ] = None,
        region: Annotated[
            Literal[
                "north_america", "europe", "asia", "latin_america", "anz",
                "middle_east", "africa",
            ]
            | None,
            "Reviewer region. Closed enum -- an unknown value matches nothing rather "
            "than erroring.",
        ] = None,
        query: Annotated[
            str | None,
            "Full-text search within this product's reviews (1-200 characters); "
            "narrows the review list AND every facet count.",
        ] = None,
    ) -> str:
        """A page of G2 software reviews: rating, title, likes/dislikes, problems
        solved, reviewer job title, industry and company size, validated/incentivized
        flags - PLUS exact per-star counts and faceted counts.

        Parameter rule: product_id or url is required.

        Pagination: page - fixed at 10 per page and paginates well past the 10 pages
        G2's own widget links to.

        Args:
            product_id: G2 product slug or numeric G2 id as a string (1-200 characters).
            url: Full g2.com reviews URL, as an alternative to product_id (1-1000
                characters).
            page: 1-based page number; fixed at 10 reviews per page.
            sort: Review sort order (server default 'relevance'). Closed enum: an
                unknown sort is silently accepted upstream and never runs.
            rating: Only reviews in this star bucket (1-5, sent as an integer). Buckets
                are half- star-inclusive: 1 returns 0, 0.5 and 1-star reviews.
            company_size: Reviewer company size: small_business is 50 employees or
                fewer, mid_market 51-1000, enterprise over 1000. Closed enum -- an
                unknown value matches nothing and returns a billed 'Reviews (0)'.
            role: Reviewer role. Closed enum -- an unknown value matches nothing rather
                than erroring.
            region: Reviewer region. Closed enum -- an unknown value matches nothing
                rather than erroring.
            query: Full-text search within this product's reviews (1-200 characters);
                narrows the review list AND every facet count.

        Returns:
            JSON string with a page of reviews: rating, title, likes/dislikes, problems
            solved, reviewer job title, industry and company size,
            validated/incentivized flags - PLUS exact per-star counts, pros and cons
            with per-theme counts, and company-size / role / industry / region /
            category facets with counts.
        """
        client = get_async_client()

        params: dict = {
            "product_id": product_id,
            "url": url,
            "page": page,
            "sort": sort,
            "rating": rating,
            "company_size": company_size,
            "role": role,
            "region": region,
            "query": query,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.g2.reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_g2_reviews,
        description=(
            "A page of G2 reviews: rating, title, likes and dislikes, problems "
            "solved, reviewer job title, industry and company size, validated and "
            "incentivized flags -- plus what the profile page has no form of: exact "
            "per-star counts, pros and cons with per-theme counts, and company-size, "
            "role, industry, region and category facets with counts. Fixed at 10 "
            "reviews per page and paginates well past the 10 pages G2's own widget "
            "links to. Provide product_id or url. Costs 5 credits."
        ),
    )
