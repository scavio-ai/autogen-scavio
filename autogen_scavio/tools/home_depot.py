"""Scavio Home Depot tools for AutoGen.

3 endpoints. 2 credits flat on all three endpoints.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_home_depot_search_tool() -> FunctionTool:
    """Create a Scavio Home Depot search tool."""

    async def scavio_home_depot_search(
        query: Annotated[str, "Search keyword (1-500 characters)."],
        page: Annotated[
            int | None,
            "Results page, 1-based. Home Depot serves 12 products per page and offers "
            "no way to change that, so paging is the only way to read further.",
        ] = None,
        sort_by: Annotated[
            Literal[
                "best_match", "top_sellers", "top_rated", "price_low", "price_high",
            ]
            | None,
            "Result sort order. Defaults to 'best_match'. Closed enum: Home Depot "
            "answers an unknown sort with an empty page that is still billed. "
            "'Newest' is absent - it is rejected on keyword search.",
        ] = None,
        min_price: Annotated[
            float | None,
            "Minimum price, inclusive. Must be 0 or greater.",
        ] = None,
        max_price: Annotated[
            float | None,
            "Maximum price, inclusive. Must be 0 or greater.",
        ] = None,
    ) -> str:
        """Search Home Depot: price and promotions, brand and model, ratings, badges,
        per-store pickup/delivery.

        Pagination: page - page size is FIXED at 12 and cannot be changed.

        Args:
            query: Search keyword (1-500 characters).
            page: Results page, 1-based. Home Depot serves 12 products per page and
                offers no way to change that, so paging is the only way to read further.
            sort_by: Result sort order. Defaults to 'best_match'. Closed enum: Home
                Depot answers an unknown sort with an empty page that is still billed.
                'Newest' is absent - it is rejected on keyword search.
            min_price: Minimum price, inclusive. Must be 0 or greater.
            max_price: Maximum price, inclusive. Must be 0 or greater.

        Returns:
            JSON string with search results: price and promotions, brand and model,
            ratings, badges, per-store pickup/delivery.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "page": page,
            "sort_by": sort_by,
            "min_price": min_price,
            "max_price": max_price,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.home_depot.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_home_depot_search,
        description=(
            "Search Home Depot: price and promotions, brand and model, ratings, "
            "badges, per-store pickup/delivery. Page size is fixed at 12 and cannot "
            "be changed. Costs 2 credits."
        ),
    )


def create_home_depot_product_tool() -> FunctionTool:
    """Create a Scavio Home Depot product tool."""

    async def scavio_home_depot_product(
        item_id: Annotated[
            str,
            "Home Depot item id (e.g. '325479354'), or a full homedepot.com/p/... "
            "product URL; tracking parameters on a pasted URL are discarded.",
        ],
    ) -> str:
        """Full Home Depot item detail: pricing, images and videos, spec table,
        dimensions, bullets, documents, return policy.

        Args:
            item_id: Home Depot item id (e.g. '325479354'), or a full
                homedepot.com/p/... product URL; tracking parameters on a pasted URL are
                discarded.

        Returns:
            JSON string with full item detail: pricing and promotions, images and
            videos, spec table, dimensions, bullets, documents, return policy.
        """
        client = get_async_client()

        params: dict = {
            "item_id": item_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.home_depot.product(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_home_depot_product,
        description=(
            "Full Home Depot item detail: pricing, images and videos, spec table, "
            "dimensions, bullets, documents, return policy. Carries a 10-review "
            "preview only. Costs 2 credits."
        ),
    )


def create_home_depot_reviews_tool() -> FunctionTool:
    """Create a Scavio Home Depot reviews tool."""

    async def scavio_home_depot_reviews(
        item_id: Annotated[
            str,
            "Home Depot item id (e.g. '325479354'), or a full homedepot.com/p/... "
            "product URL; tracking parameters on a pasted URL are discarded.",
        ],
        page: Annotated[
            int | None,
            "Reviews page, 1-based. 30 reviews per page; 'total_pages' in the "
            "response is the last one that exists, and asking past it is a 404.",
        ] = None,
    ) -> str:
        """One page of full Home Depot review bodies, rating distribution, per-attribute
        ratings, photos, seller responses.

        Pagination: page - 30 per page; total_pages is the last that exists and asking
        past it is a 404.

        Args:
            item_id: Home Depot item id (e.g. '325479354'), or a full
                homedepot.com/p/... product URL; tracking parameters on a pasted URL are
                discarded.
            page: Reviews page, 1-based. 30 reviews per page; 'total_pages' in the
                response is the last one that exists, and asking past it is a 404.

        Returns:
            JSON string with one page of full review bodies, the rating distribution,
            per-attribute ratings, photos and seller responses.
        """
        client = get_async_client()

        params: dict = {
            "item_id": item_id,
            "page": page,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.home_depot.reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_home_depot_reviews,
        description=(
            "One page of full Home Depot review bodies, the rating distribution, "
            "per-attribute ratings, photos and seller responses. 30 reviews per page. "
            "Costs 2 credits."
        ),
    )
