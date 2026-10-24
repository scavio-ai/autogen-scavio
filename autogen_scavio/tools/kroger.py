"""Scavio Kroger tools for AutoGen.

2 endpoints. 2 credits per call. Kroger operates Kroger, Ralphs, Fred Meyer,
Harris Teeter, King Soopers, Fry's and other banners.
"""

from __future__ import annotations

from typing import Annotated

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_kroger_search_tool() -> FunctionTool:
    """Create a Scavio Kroger search tool."""

    async def scavio_kroger_search(
        query: Annotated[str, "Search keywords, e.g. 'organic milk'."],
        page: Annotated[int | None, "Page, 1-based."] = None,
    ) -> str:
        """Search Kroger grocery products by keyword.

        Kroger operates Kroger, Ralphs, Fred Meyer, Harris Teeter, King Soopers,
        Fry's and other banners. Returns price (cents), promo price, n-for deals,
        unit price, size, UPC, stock, SNAP eligibility, dietary info, rating and
        category.

        Args:
            query: Search keywords.
            page: Page, 1-based.

        Returns:
            JSON string with search results.
        """
        client = get_async_client()

        params: dict = {"query": query, "page": page}
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kroger.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kroger_search,
        description=(
            "Search Kroger grocery products by keyword. Kroger operates Kroger, "
            "Ralphs, Fred Meyer, Harris Teeter, King Soopers, Fry's and other "
            "banners. Returns price (cents), promo price, n-for deals, unit price, "
            "size, UPC, stock, SNAP eligibility, dietary info, rating and category. "
            "Costs 2 credits."
        ),
    )


def create_kroger_product_tool() -> FunctionTool:
    """Create a Scavio Kroger product tool."""

    async def scavio_kroger_product(
        product_url: Annotated[
            str | None,
            "Full or relative product URL from kroger.com, e.g. "
            "'/p/kroger-2-reduced-fat-milk-gallon/0001111041700'. Preferred.",
        ] = None,
        upc: Annotated[
            str | None,
            "Kroger product UPC (from search or product URLs: /p/{slug}/{upc}).",
        ] = None,
        slug: Annotated[
            str | None,
            "Product slug for readable URL. Optional with upc.",
        ] = None,
    ) -> str:
        """Full Kroger product detail: nutrition, allergens, dietary flags, rating, stock.

        Args:
            product_url: Full or relative product URL from kroger.com. Preferred.
            upc: Kroger product UPC.
            slug: Product slug. Optional with upc.

        Returns:
            JSON string with product details.
        """
        client = get_async_client()

        params: dict = {
            "product_url": product_url,
            "upc": upc,
            "slug": slug,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.kroger.product(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_kroger_product,
        description=(
            "Full Kroger product detail by URL or UPC: nutrition facts, allergens, "
            "ingredients, nutrients with daily values, description, images, rating "
            "distribution, store aisle location, stock level, dietary flags, SNAP "
            "eligibility, dimensions and country of origin. Costs 2 credits."
        ),
    )
