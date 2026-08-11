"""Scavio Walmart tools for AutoGen.

7 endpoints. BODY-PRICED, not flat: search and category cost 1 credit on domain 'com' or
'ca' and 2 credits on 'com.mx'. The other five endpoints take no domain, so they are
always 1 credit.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list


def create_walmart_search_tool(max_results: int = 5) -> FunctionTool:
    """Create a Scavio Walmart search tool."""

    async def scavio_walmart_search(
        query: Annotated[str, "Product search query (1-500 characters)."],
        domain: Annotated[
            Literal["com", "ca", "com.mx"] | None,
            "Marketplace: 'com' (US, default, 1 credit), 'ca' (1 credit), 'com.mx' (2 "
            "credits). Sets the currency and product URLs of the response.",
        ] = None,
        page: Annotated[
            int | None,
            "Results page, 1-based (integer >= 1). One page per call.",
        ] = None,
        start_page: Annotated[
            int | None,
            "Deprecated alias for page; send page instead.",
        ] = None,
        sort_by: Annotated[
            Literal[
                "best_match", "price_low", "price_high", "best_seller", "rating_high",
                "new",
            ]
            | None,
            "Result sort order. Defaults to 'best_match'.",
        ] = None,
        min_price: Annotated[
            float | None,
            "Minimum price filter in the marketplace's own currency; decimals allowed "
            "(e.g. 19.99).",
        ] = None,
        max_price: Annotated[
            float | None,
            "Maximum price filter in the marketplace's own currency; decimals allowed "
            "(e.g. 199.5).",
        ] = None,
        fulfillment_speed: Annotated[
            Literal["today", "tomorrow"] | None,
            "Only items deliverable today, or by tomorrow. '2_days' and 'anytime' are "
            "not accepted - for anytime, omit this parameter.",
        ] = None,
        fulfillment_type: Annotated[
            Literal["in_store"] | None,
            "Set to 'in_store' to return only items available for in-store pickup.",
        ] = None,
    ) -> str:
        """Search Walmart and get structured product rows (products[] + products_count +
        location).

        Pagination: page (integer >= 1); start_page is a deprecated alias.

        Args:
            query: Product search query (1-500 characters).
            domain: Marketplace: 'com' (US, default, 1 credit), 'ca' (1 credit),
                'com.mx' (2 credits). Sets the currency and product URLs of the
                response.
            page: Results page, 1-based (integer >= 1). One page per call.
            start_page: Deprecated alias for page; send page instead.
            sort_by: Result sort order. Defaults to 'best_match'.
            min_price: Minimum price filter in the marketplace's own currency; decimals
                allowed (e.g. 19.99).
            max_price: Maximum price filter in the marketplace's own currency; decimals
                allowed (e.g. 199.5).
            fulfillment_speed: Only items deliverable today, or by tomorrow. '2_days'
                and 'anytime' are not accepted - for anytime, omit this parameter.
            fulfillment_type: Set to 'in_store' to return only items available for
                in-store pickup.

        Returns:
            JSON string with structured Walmart search results (products array +
            products_count + location).
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "domain": domain,
            "page": page,
            "start_page": start_page,
            "sort_by": sort_by,
            "min_price": min_price,
            "max_price": max_price,
            "fulfillment_speed": fulfillment_speed,
            "fulfillment_type": fulfillment_type,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.walmart.search(**params)

        truncate_list(raw, ['data', 'products'], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_walmart_search,
        description=(
            "Search Walmart and get structured product rows (products, products_count "
            "and the store the results were priced against). Costs 1 credit on domain "
            "'com' or 'ca' and 2 credits on 'com.mx'."
        ),
    )


def create_walmart_product_tool() -> FunctionTool:
    """Create a Scavio Walmart product tool."""

    async def scavio_walmart_product(
        product_id: Annotated[str, "Walmart item id (usItemId), e.g. '13544111159'."],
    ) -> str:
        """Full Walmart product detail: price, rating, images, specifications,
        availability, seller.

        Args:
            product_id: Walmart item id (usItemId), e.g. '13544111159'.

        Returns:
            JSON string with full product details: price, rating, images,
            specifications, availability, seller.
        """
        client = get_async_client()

        params: dict = {
            "product_id": product_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.walmart.product(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_walmart_product,
        description=(
            "Full detail for a single Walmart product: price, rating, images, "
            "specifications, availability and seller. US marketplace only - "
            "walmart.ca product pages could not be fetched at all, so this endpoint "
            "takes no domain. Costs 1 credit. Walmart is body-priced through "
            "`domain`, but this endpoint takes no domain, so it is always 1."
        ),
    )


def create_walmart_reviews_tool() -> FunctionTool:
    """Create a Scavio Walmart reviews tool."""

    async def scavio_walmart_reviews(
        product_id: Annotated[str, "Walmart item id (usItemId), e.g. '13544111159'."],
        page: Annotated[
            int | None,
            "Reviews page, 1-based (integer >= 1). 10 reviews per page.",
        ] = None,
        sort: Annotated[
            Literal[
                "relevancy", "submission-desc", "submission-asc", "rating-desc",
                "rating-asc", "helpful-desc",
            ]
            | None,
            "Review sort order. Omit for Walmart's own default ordering.",
        ] = None,
    ) -> str:
        """Customer reviews with ratings, text, author, date and the rating breakdown.

        Pagination: page (10 reviews per page).

        Args:
            product_id: Walmart item id (usItemId), e.g. '13544111159'.
            page: Reviews page, 1-based (integer >= 1). 10 reviews per page.
            sort: Review sort order. Omit for Walmart's own default ordering.

        Returns:
            JSON string with customer reviews with ratings, text, author, date and the
            rating breakdown; 10 per page.
        """
        client = get_async_client()

        params: dict = {
            "product_id": product_id,
            "page": page,
            "sort": sort,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.walmart.reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_walmart_reviews,
        description=(
            "Customer reviews for a Walmart product with ratings, text, author, date "
            "and the rating breakdown. 10 reviews per page; paginate with page. Costs "
            "1 credit. Walmart is body-priced through `domain`, but this endpoint "
            "takes no domain, so it is always 1."
        ),
    )


def create_walmart_category_tool() -> FunctionTool:
    """Create a Scavio Walmart category tool."""

    async def scavio_walmart_category(
        category_id: Annotated[
            str,
            "Walmart category id: either a leaf id ('1095191') or the full "
            "underscore-joined path ('3944_133251_1095191'). Both are accepted.",
        ],
        domain: Annotated[
            Literal["com", "ca", "com.mx"] | None,
            "Marketplace: 'com' (US, default, 1 credit), 'ca' (1 credit), 'com.mx' (2 "
            "credits). Sets the currency and product URLs of the response.",
        ] = None,
        page: Annotated[
            int | None,
            "Results page, 1-based (integer >= 1). One page per call.",
        ] = None,
        limit: Annotated[
            int | None,
            "Trim the returned products to at most this many (integer >= 1). Applied "
            "after fetching, so it does not reduce the credit cost of the call.",
        ] = None,
        sort_by: Annotated[
            Literal[
                "best_match", "price_low", "price_high", "best_seller", "rating_high",
                "new",
            ]
            | None,
            "Result sort order. Defaults to 'best_match'.",
        ] = None,
        min_price: Annotated[
            float | None,
            "Minimum price filter in the marketplace's own currency; decimals allowed "
            "(e.g. 19.99).",
        ] = None,
        max_price: Annotated[
            float | None,
            "Maximum price filter in the marketplace's own currency; decimals allowed "
            "(e.g. 199.5).",
        ] = None,
        fulfillment_speed: Annotated[
            Literal["today", "tomorrow"] | None,
            "Only items deliverable today, or by tomorrow. '2_days' and 'anytime' are "
            "not accepted - for anytime, omit this parameter.",
        ] = None,
    ) -> str:
        """Products within a Walmart category, same product shape as search.

        Pagination: page; `limit` trims after fetching and does NOT reduce cost.

        Args:
            category_id: Walmart category id: either a leaf id ('1095191') or the full
                underscore-joined path ('3944_133251_1095191'). Both are accepted.
            domain: Marketplace: 'com' (US, default, 1 credit), 'ca' (1 credit),
                'com.mx' (2 credits). Sets the currency and product URLs of the
                response.
            page: Results page, 1-based (integer >= 1). One page per call.
            limit: Trim the returned products to at most this many (integer >= 1).
                Applied after fetching, so it does not reduce the credit cost of the
                call.
            sort_by: Result sort order. Defaults to 'best_match'.
            min_price: Minimum price filter in the marketplace's own currency; decimals
                allowed (e.g. 19.99).
            max_price: Maximum price filter in the marketplace's own currency; decimals
                allowed (e.g. 199.5).
            fulfillment_speed: Only items deliverable today, or by tomorrow. '2_days'
                and 'anytime' are not accepted - for anytime, omit this parameter.

        Returns:
            JSON string with products within a category, same product shape as search.
        """
        client = get_async_client()

        params: dict = {
            "category_id": category_id,
            "domain": domain,
            "page": page,
            "limit": limit,
            "sort_by": sort_by,
            "min_price": min_price,
            "max_price": max_price,
            "fulfillment_speed": fulfillment_speed,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.walmart.category(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_walmart_category,
        description=(
            "Products within a Walmart category, in the same product shape as search. "
            "Costs 1 credit on domain 'com' or 'ca' and 2 credits on 'com.mx'; "
            "`limit` trims the response after fetching and never reduces the cost."
        ),
    )


def create_walmart_offers_tool() -> FunctionTool:
    """Create a Scavio Walmart offers tool."""

    async def scavio_walmart_offers(
        product_id: Annotated[str, "Walmart item id (usItemId), e.g. '2979510112'."],
    ) -> str:
        """Seller offers for a product: price, seller, condition, buy-box flag.

        Args:
            product_id: Walmart item id (usItemId), e.g. '2979510112'.

        Returns:
            JSON string with seller offers for a product: price, seller, condition,
            buy-box flag. BUY-BOX SELLER ONLY.
        """
        client = get_async_client()

        params: dict = {
            "product_id": product_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.walmart.offers(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_walmart_offers,
        description=(
            "The buy-box offer for a Walmart product: price, seller, condition and "
            "buy-box flag. BUY-BOX SELLER ONLY - this is not the full offer list, and "
            "there is no way to page through the other sellers. Costs 1 credit. "
            "Walmart is body-priced through `domain`, but this endpoint takes no "
            "domain, so it is always 1."
        ),
    )


def create_walmart_seller_tool() -> FunctionTool:
    """Create a Scavio Walmart seller tool."""

    async def scavio_walmart_seller(
        seller_id: Annotated[
            str,
            "Numeric Walmart catalog seller id, as returned in `seller_catalog_id` on "
            "a product, search or offers response (e.g. '101480084'). The GUID "
            "`seller_id` is not accepted here - it 404s.",
        ],
    ) -> str:
        """Marketplace seller storefront: name, rating, review count, Pro Seller badge,
        business details.

        Args:
            seller_id: Numeric Walmart catalog seller id, as returned in
                `seller_catalog_id` on a product, search or offers response (e.g.
                '101480084'). The GUID `seller_id` is not accepted here - it 404s.

        Returns:
            JSON string with marketplace seller storefront: name, rating, review count,
            Pro Seller badge, business details.
        """
        client = get_async_client()

        params: dict = {
            "seller_id": seller_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.walmart.seller(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_walmart_seller,
        description=(
            "Marketplace seller storefront: name, rating, review count, Pro Seller "
            "badge and business details. Costs 1 credit. Walmart is body-priced "
            "through `domain`, but this endpoint takes no domain, so it is always 1."
        ),
    )


def create_walmart_seller_products_tool() -> FunctionTool:
    """Create a Scavio Walmart seller products tool."""

    async def scavio_walmart_seller_products(
        seller_id: Annotated[
            str,
            "Numeric Walmart catalog seller id, as returned in `seller_catalog_id` on "
            "a product, search or offers response (e.g. '101480084'). The GUID "
            "`seller_id` 404s.",
        ],
    ) -> str:
        """A seller's catalog; ~40 items server-rendered, total_count is the real
        catalog size.

        Args:
            seller_id: Numeric Walmart catalog seller id, as returned in
                `seller_catalog_id` on a product, search or offers response (e.g.
                '101480084'). The GUID `seller_id` 404s.

        Returns:
            JSON string with a seller's catalog; ~40 items server-rendered, total_count
            is the real catalog size.
        """
        client = get_async_client()

        params: dict = {
            "seller_id": seller_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.walmart.seller_products(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_walmart_seller_products,
        description=(
            "A marketplace seller's catalog. Roughly the first 40 items are "
            "server-rendered and returned; total_count reports the seller's real "
            "catalog size. There is no pagination - the rest of the catalog is not "
            "reachable. Costs 1 credit. Walmart is body-priced through `domain`, but "
            "this endpoint takes no domain, so it is always 1."
        ),
    )
