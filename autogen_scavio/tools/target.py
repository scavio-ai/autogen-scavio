"""Scavio Target tools for AutoGen.

4 endpoints. 1 credit flat on all four endpoints.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_target_search_tool() -> FunctionTool:
    """Create a Scavio Target search tool."""

    async def scavio_target_search(
        keyword: Annotated[str, "Search keyword (1-500 characters)."],
        page: Annotated[int | None, "Results page, 1-based."] = None,
        count: Annotated[
            int | None,
            "Results per page, 1-28. Defaults to 24; Target rejects anything above 28 "
            "outright.",
        ] = None,
        sort: Annotated[
            Literal[
                "relevance", "featured", "price_low", "price_high", "rating_high",
                "best_seller", "newest",
            ]
            | None,
            "Result sort order. Defaults to 'relevance'.",
        ] = None,
        store_id: Annotated[
            str | None,
            "Numeric Target store id whose prices and availability the response "
            "reflects. Defaults to '3991', the store target.com uses with no store "
            "context.",
        ] = None,
    ) -> str:
        """Search Target.com: prices, ratings, badges and promotions.

        Pagination: page + count.

        Args:
            keyword: Search keyword (1-500 characters).
            page: Results page, 1-based.
            count: Results per page, 1-28. Defaults to 24; Target rejects anything above
                28 outright.
            sort: Result sort order. Defaults to 'relevance'.
            store_id: Numeric Target store id whose prices and availability the response
                reflects. Defaults to '3991', the store target.com uses with no store
                context.

        Returns:
            JSON string with search results with prices, ratings, badges and promotions.
        """
        client = get_async_client()

        params: dict = {
            "keyword": keyword,
            "page": page,
            "count": count,
            "sort": sort,
            "store_id": store_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.target.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_target_search,
        description=(
            "Search Target.com, the US retailer: prices, ratings, badges and "
            "promotions. Up to 28 results per page; rendered upstream, so expect "
            "around 9 seconds. Costs 1 credit."
        ),
    )


def create_target_category_tool() -> FunctionTool:
    """Create a Scavio Target category tool."""

    async def scavio_target_category(
        category_id: Annotated[
            str,
            "Target category id: the segment after 'N-' in a target.com /c/ URL "
            "(target.com/c/apple/-/N-5xtg6 -> '5xtg6').",
        ],
        page: Annotated[int | None, "Results page, 1-based."] = None,
        count: Annotated[
            int | None,
            "Results per page, 1-28. Defaults to 24; Target rejects anything above 28 "
            "outright.",
        ] = None,
        sort: Annotated[
            Literal[
                "relevance", "featured", "price_low", "price_high", "rating_high",
                "best_seller", "newest",
            ]
            | None,
            "Result sort order. Defaults to 'relevance'.",
        ] = None,
        store_id: Annotated[
            str | None,
            "Numeric Target store id whose prices and availability the response "
            "reflects. Defaults to '3991'.",
        ] = None,
    ) -> str:
        """Products in a Target category, same shape as search plus the category
        breadcrumb.

        Pagination: page + count.

        Args:
            category_id: Target category id: the segment after 'N-' in a target.com /c/
                URL (target.com/c/apple/-/N-5xtg6 -> '5xtg6').
            page: Results page, 1-based.
            count: Results per page, 1-28. Defaults to 24; Target rejects anything above
                28 outright.
            sort: Result sort order. Defaults to 'relevance'.
            store_id: Numeric Target store id whose prices and availability the response
                reflects. Defaults to '3991'.

        Returns:
            JSON string with products in a category, same shape as search plus the
            category breadcrumb.
        """
        client = get_async_client()

        params: dict = {
            "category_id": category_id,
            "page": page,
            "count": count,
            "sort": sort,
            "store_id": store_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.target.category(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_target_category,
        description=(
            "Products in a Target category, same shape as search plus the category "
            "breadcrumb. Up to 28 per page; the slowest Target endpoint at around 37 "
            "seconds. Costs 1 credit."
        ),
    )


def create_target_product_tool() -> FunctionTool:
    """Create a Scavio Target product tool."""

    async def scavio_target_product(
        tcin: Annotated[
            str,
            "Target catalog id (tcin, e.g. '1010453160'). A colour/size child tcin is "
            "answered by its variation parent, with the child present in 'variants'.",
        ],
        store_id: Annotated[
            str | None,
            "Numeric Target store id whose prices and availability the response "
            "reflects. Defaults to '3991'.",
        ] = None,
    ) -> str:
        """Target product details by TCIN: price, rating, images, specifications,
        variants, return policy, fulfillment.

        Args:
            tcin: Target catalog id (tcin, e.g. '1010453160'). A colour/size child tcin
                is answered by its variation parent, with the child present in
                'variants'.
            store_id: Numeric Target store id whose prices and availability the response
                reflects. Defaults to '3991'.

        Returns:
            JSON string with product details: price, rating, images, specifications,
            variants, return policy, fulfillment.
        """
        client = get_async_client()

        params: dict = {
            "tcin": tcin,
            "store_id": store_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.target.product(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_target_product,
        description=(
            "Target product details by TCIN: price, rating, images, specifications, "
            "variants, return policy, fulfillment. seller_id/seller_name are null for "
            "stock sold by Target. Costs 1 credit."
        ),
    )


def create_target_reviews_tool() -> FunctionTool:
    """Create a Scavio Target reviews tool."""

    async def scavio_target_reviews(
        tcin: Annotated[str, "Target catalog id (tcin, e.g. '1010453160')."],
        limit: Annotated[
            int | None,
            "Trim the returned reviews to at most this many (1 or greater). Target "
            "publishes 8 anonymously and offers no paging, so this only trims.",
        ] = None,
        store_id: Annotated[
            str | None,
            "Numeric Target store id whose prices and availability the response "
            "reflects. Defaults to '3991'.",
        ] = None,
    ) -> str:
        """Target reviews with the rating breakdown, per-attribute averages and guest
        photos.

        Args:
            tcin: Target catalog id (tcin, e.g. '1010453160').
            limit: Trim the returned reviews to at most this many (1 or greater). Target
                publishes 8 anonymously and offers no paging, so this only trims.
            store_id: Numeric Target store id whose prices and availability the response
                reflects. Defaults to '3991'.

        Returns:
            JSON string with reviews with the rating breakdown, per-attribute averages
            and guest photos. 8 bodies max, no paging.
        """
        client = get_async_client()

        params: dict = {
            "tcin": tcin,
            "limit": limit,
            "store_id": store_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.target.reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_target_reviews,
        description=(
            "Target reviews with the rating breakdown, per-attribute averages and "
            "guest photos. 8 review bodies maximum and no paging; expect around 40 "
            "seconds. Costs 1 credit."
        ),
    )
