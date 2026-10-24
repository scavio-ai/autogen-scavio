"""Scavio HEB tools for AutoGen.

3 endpoints. 2 credits per call.
"""

from __future__ import annotations

from typing import Annotated

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_heb_search_tool() -> FunctionTool:
    """Create a Scavio HEB search tool."""

    async def scavio_heb_search(
        query: Annotated[str, "Search keywords, e.g. 'organic milk'."],
        page: Annotated[int | None, "Page, 1-based."] = None,
        page_size: Annotated[
            int | None,
            "Results per page, max 60. Default 30.",
        ] = None,
    ) -> str:
        """Search HEB grocery products by keyword.

        Returns price (cents), list price, sale status, unit price, size, UPC,
        stock, EBT/SNAP eligibility, category, aisle location and product URL.

        Args:
            query: Search keywords.
            page: Page, 1-based.
            page_size: Results per page, max 60. Default 30.

        Returns:
            JSON string with search results.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "page": page,
            "page_size": page_size,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.heb.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_heb_search,
        description=(
            "Search HEB grocery products by keyword. Returns price (cents), "
            "list price, sale status, unit price, size, UPC, stock, EBT/SNAP "
            "eligibility, category, aisle location and product URL. Costs 2 credits."
        ),
    )


def create_heb_product_tool() -> FunctionTool:
    """Create a Scavio HEB product tool."""

    async def scavio_heb_product(
        product_url: Annotated[
            str | None,
            "Full or relative product URL from heb.com, e.g. "
            "'/product-detail/central-market-organics-whole-milk-1-gal/931316'. Preferred.",
        ] = None,
        product_id: Annotated[
            str | None,
            "HEB product id (numeric id at the end of a product URL). Requires slug.",
        ] = None,
        slug: Annotated[
            str | None,
            "Product slug (readable part of the URL). Required with product_id.",
        ] = None,
    ) -> str:
        """Full HEB product detail: nutrition, ingredients, images, coupons, EBT/SNAP.

        Args:
            product_url: Full or relative product URL from heb.com. Preferred.
            product_id: HEB product id. Requires slug.
            slug: Product slug. Required with product_id.

        Returns:
            JSON string with product details.
        """
        client = get_async_client()

        params: dict = {
            "product_url": product_url,
            "product_id": product_id,
            "slug": slug,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.heb.product(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_heb_product,
        description=(
            "Full HEB product detail: nutrition facts, ingredients, description, "
            "images, similar products, coupons, EBT/SNAP eligibility, breadcrumbs, "
            "aisle location. Pass product_url or slug + product_id. Costs 2 credits."
        ),
    )


def create_heb_stores_tool() -> FunctionTool:
    """Create a Scavio HEB stores tool."""

    async def scavio_heb_stores(
        zip: Annotated[
            str | None,
            "5-digit US ZIP code, e.g. '78701'.",
        ] = None,
        city: Annotated[
            str | None,
            "City name, e.g. 'Austin'. Pass zip or city.",
        ] = None,
    ) -> str:
        """Find HEB stores near a US ZIP or city.

        Returns store number, address, phone, hours, pharmacy availability,
        fulfillment channels (curbside, delivery, in-store), distance and store URL.

        Args:
            zip: 5-digit US ZIP code.
            city: City name. Pass zip or city.

        Returns:
            JSON string with store results.
        """
        client = get_async_client()

        params: dict = {"zip": zip, "city": city}
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.heb.stores(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_heb_stores,
        description=(
            "Find HEB stores near a US ZIP code or city. Returns store number, "
            "address, phone, hours, pharmacy availability, fulfillment channels "
            "(curbside, delivery, in-store), distance and store URL. Costs 2 credits."
        ),
    )
