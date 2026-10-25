"""Scavio Decathlon tools for AutoGen.

2 endpoints. 2 credits per call. Supports 7 country domains:
FR, ES, IT, IN, UK, PT and NET (international).
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_decathlon_search_tool() -> FunctionTool:
    """Create a Scavio Decathlon search tool."""

    async def scavio_decathlon_search(
        query: Annotated[str, "Search keywords, e.g. 'running shoes'."],
        country: Annotated[
            Literal["fr", "es", "it", "in", "uk", "pt", "net"],
            "Country domain.",
        ],
        page: Annotated[int | None, "Page, 1-based."] = None,
    ) -> str:
        """Search Decathlon products by keyword across 7 country domains.

        Returns product name, brand, price (cents), currency, availability,
        rating, review count and image.

        Args:
            query: Search keywords.
            country: Country domain.
            page: Page, 1-based.

        Returns:
            JSON string with search results.
        """
        client = get_async_client()

        params: dict = {"query": query, "country": country, "page": page}
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.decathlon.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_decathlon_search,
        description=(
            "Search Decathlon products by keyword across 7 country domains "
            "(FR, ES, IT, IN, UK, PT, NET). Returns product name, brand, "
            "price (cents), currency, availability, rating, review count and "
            "image. Costs 2 credits."
        ),
    )


def create_decathlon_product_tool() -> FunctionTool:
    """Create a Scavio Decathlon product tool."""

    async def scavio_decathlon_product(
        country: Annotated[
            Literal["fr", "es", "it", "in", "uk", "pt", "net"],
            "Country domain.",
        ],
        product_url: Annotated[
            str | None,
            "Full or relative product URL from any Decathlon domain. Preferred.",
        ] = None,
        product_id: Annotated[
            str | None,
            "Decathlon numeric product ID (from the /p/{slug}/{id}/... URL pattern).",
        ] = None,
    ) -> str:
        """Full Decathlon product detail: description, images, SKU, price, variants, rating.

        Args:
            country: Country domain.
            product_url: Full or relative product URL. Preferred.
            product_id: Decathlon numeric product ID.

        Returns:
            JSON string with product details.
        """
        client = get_async_client()

        params: dict = {
            "country": country,
            "product_url": product_url,
            "product_id": product_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.decathlon.product(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_decathlon_product,
        description=(
            "Full Decathlon product detail by URL or product ID: description, "
            "images, SKU, GTIN, color, price (cents), list price, availability, "
            "offers/variants, rating, review count, category and breadcrumbs. "
            "Supports all 7 country domains. Costs 2 credits."
        ),
    )
