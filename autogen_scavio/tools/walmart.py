"""Scavio Walmart tools for AutoGen."""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list


def create_walmart_search_tool(max_results: int = 5) -> FunctionTool:
    """Create a Walmart search tool with the given configuration."""

    async def scavio_walmart_search(
        query: str,
        domain: str | None = None,
        device: str | None = None,
        sort_by: str | None = None,
        start_page: int | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        fulfillment_speed: str | None = None,
        fulfillment_type: str | None = None,
        delivery_zip: str | None = None,
        store_id: str | None = None,
    ) -> str:
        """Search Walmart product listings using the Scavio API.

        Args:
            query: The search query string.
            domain: Walmart domain to search (e.g. "com", "ca").
            device: Device type for results (e.g. "desktop", "mobile").
            sort_by: Sort order for results (e.g. "best_match", "price_low", "price_high").
            start_page: Page number to start results from.
            min_price: Minimum price filter.
            max_price: Maximum price filter.
            fulfillment_speed: Filter by fulfillment speed (e.g. "nextday", "twoday").
            fulfillment_type: Filter by fulfillment type (e.g. "pickup", "shipping").
            delivery_zip: ZIP code for delivery availability filtering.
            store_id: Walmart store ID for local inventory filtering.

        Returns:
            JSON string with Walmart search results including product names,
            prices, ratings, and fulfillment options.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "domain": domain,
            "device": device,
            "sort_by": sort_by,
            "start_page": start_page,
            "min_price": min_price,
            "max_price": max_price,
            "fulfillment_speed": fulfillment_speed,
            "fulfillment_type": fulfillment_type,
            "delivery_zip": delivery_zip,
            "store_id": store_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.walmart.search(**params)

        truncate_list(raw, ["data", "products"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_walmart_search,
        description=(
            "Search Walmart product listings. Returns product names, "
            "prices, ratings, and fulfillment options."
        ),
    )


def create_walmart_product_tool() -> FunctionTool:
    """Create a Walmart product detail tool."""

    async def scavio_walmart_product(
        product_id: str,
        domain: str | None = None,
        device: str | None = None,
        delivery_zip: str | None = None,
        store_id: str | None = None,
    ) -> str:
        """Fetch full details for a specific Walmart product by product ID.

        Args:
            product_id: The Walmart product ID to retrieve details for.
            domain: Walmart domain (e.g. "com", "ca").
            device: Device type (e.g. "desktop", "mobile").
            delivery_zip: ZIP code for delivery availability info.
            store_id: Walmart store ID for local availability info.

        Returns:
            JSON string with full product details including name, price,
            description, reviews, and availability.
        """
        client = get_async_client()

        params: dict = {
            "product_id": product_id,
            "domain": domain,
            "device": device,
            "delivery_zip": delivery_zip,
            "store_id": store_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.walmart.product(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_walmart_product,
        description="Fetch full details for a specific Walmart product by product ID.",
    )
