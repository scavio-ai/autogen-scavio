"""Scavio eBay tools for AutoGen.

3 endpoints. 1 credit flat on all three endpoints.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_ebay_search_tool() -> FunctionTool:
    """Create a Scavio eBay search tool."""

    async def scavio_ebay_search(
        query: Annotated[
            str | None,
            "Keyword to search (1-500 characters). Optional: a seller-only search "
            "pages that seller's whole catalogue.",
        ] = None,
        seller: Annotated[
            str | None,
            "Restrict results to one seller's listings (1-64 characters), as in "
            "ebay.com/usr/<name>. Can be sent with no query.",
        ] = None,
        page: Annotated[int | None, "Results page, 1-based."] = None,
        sort_by: Annotated[
            Literal[
                "best_match", "ending_soonest", "newly_listed", "price_low",
                "price_high",
            ]
            | None,
            "Result sort order. Defaults to 'best_match'. eBay's 'Distance: nearest "
            "first' is deliberately unsupported (it ranks against our proxy exit, not "
            "the caller).",
        ] = None,
        min_price: Annotated[
            float | None,
            "Minimum price, inclusive. Must be 0 or greater.",
        ] = None,
        max_price: Annotated[
            float | None,
            "Maximum price, inclusive. Must be 0 or greater.",
        ] = None,
        condition: Annotated[
            Literal["new", "open_box", "refurbished", "used", "for_parts"] | None,
            "Item condition filter. 'refurbished' is eBay's parent condition, not one "
            "of its three graded tiers.",
        ] = None,
        buying_format: Annotated[
            Literal["auction", "buy_it_now", "best_offer"] | None,
            "Listing format: auction, fixed price (buy_it_now), or fixed price "
            "accepting offers (best_offer).",
        ] = None,
        free_shipping: Annotated[
            bool | None,
            "Only listings with free shipping.",
        ] = None,
        sold: Annotated[
            bool | None,
            "Search completed listings that actually SOLD, for price research. eBay "
            "publishes no headline count on this view, so total_results is null.",
        ] = None,
        category_id: Annotated[
            str | None,
            "eBay category id; must be numeric (e.g. '112529'). An unrecognised id "
            "returns the UNFILTERED set under a 200.",
        ] = None,
        per_page: Annotated[
            Literal[60, 120, 240] | None,
            "Listings per page: 60, 120 or 240 only. Defaults to 60; eBay silently "
            "falls back to 60 for anything else.",
        ] = None,
    ) -> str:
        """Search live or SOLD eBay listings: price, condition, bids, shipping, seller,
        feedback.

        Parameter rule: query or seller is required.

        Pagination: page; per_page accepts ONLY 60, 120 or 240 (silent fallback to 60).

        Args:
            query: Keyword to search (1-500 characters). Optional: a seller-only search
                pages that seller's whole catalogue.
            seller: Restrict results to one seller's listings (1-64 characters), as in
                ebay.com/usr/<name>. Can be sent with no query.
            page: Results page, 1-based.
            sort_by: Result sort order. Defaults to 'best_match'. eBay's 'Distance:
                nearest first' is deliberately unsupported (it ranks against our proxy
                exit, not the caller).
            min_price: Minimum price, inclusive. Must be 0 or greater.
            max_price: Maximum price, inclusive. Must be 0 or greater.
            condition: Item condition filter. 'refurbished' is eBay's parent condition,
                not one of its three graded tiers.
            buying_format: Listing format: auction, fixed price (buy_it_now), or fixed
                price accepting offers (best_offer).
            free_shipping: Only listings with free shipping.
            sold: Search completed listings that actually SOLD, for price research. eBay
                publishes no headline count on this view, so total_results is null.
            category_id: eBay category id; must be numeric (e.g. '112529'). An
                unrecognised id returns the UNFILTERED set under a 200.
            per_page: Listings per page: 60, 120 or 240 only. Defaults to 60; eBay
                silently falls back to 60 for anything else.

        Returns:
            JSON string with structured listing results: price, condition, bids,
            shipping, seller, feedback (+ count / total_results).
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "seller": seller,
            "page": page,
            "sort_by": sort_by,
            "min_price": min_price,
            "max_price": max_price,
            "condition": condition,
            "buying_format": buying_format,
            "free_shipping": free_shipping,
            "sold": sold,
            "category_id": category_id,
            "per_page": per_page,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.ebay.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_ebay_search,
        description=(
            "Search live or SOLD eBay listings: price, condition, bids, shipping, "
            "seller, feedback. Provide query or seller; per_page accepts only 60, 120 "
            "or 240. Costs 1 credit."
        ),
    )


def create_ebay_product_tool() -> FunctionTool:
    """Create a Scavio eBay product tool."""

    async def scavio_ebay_product(
        item_id: Annotated[
            str,
            "eBay item number (e.g. '168591664725'), or a full ebay.com/itm/... "
            "listing URL; tracking parameters on a pasted URL are discarded.",
        ],
    ) -> str:
        """One eBay listing in full: price, condition, images, item specifics, shipping,
        returns, auction state, seller.

        Args:
            item_id: eBay item number (e.g. '168591664725'), or a full ebay.com/itm/...
                listing URL; tracking parameters on a pasted URL are discarded.

        Returns:
            JSON string with one listing in full: price, condition, images, item
            specifics, shipping, returns, auction state, seller.
        """
        client = get_async_client()

        params: dict = {
            "item_id": item_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.ebay.product(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_ebay_product,
        description=(
            "One eBay listing in full: price, condition, images, item specifics, "
            "shipping, returns, auction state, seller. Costs 1 credit."
        ),
    )


def create_ebay_seller_tool() -> FunctionTool:
    """Create a Scavio eBay seller tool."""

    async def scavio_ebay_seller(
        seller: Annotated[
            str,
            "eBay username as it appears in ebay.com/usr/<name> (1-64 characters), "
            "which is what seller_name on a search or product result returns.",
        ],
    ) -> str:
        """eBay seller profile card: store name, feedback score and %, items sold,
        followers, location, categories.

        Args:
            seller: eBay username as it appears in ebay.com/usr/<name> (1-64
                characters), which is what seller_name on a search or product result
                returns.

        Returns:
            JSON string with seller profile card: store name, feedback score and %,
            items sold, followers, location, categories.
        """
        client = get_async_client()

        params: dict = {
            "seller": seller,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.ebay.seller(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_ebay_seller,
        description=(
            "eBay seller profile card: store name, feedback score and %, items sold, "
            "followers, location, categories. Profile only: page a catalogue with "
            "search(seller=...). Costs 1 credit."
        ),
    )
