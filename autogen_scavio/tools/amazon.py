"""Scavio Amazon tools for AutoGen.

The Amazon API moved to a new upstream provider in 2026-07 and the request
surface shrank. ``sort_by``, ``pages``, ``category_id``, ``merchant_id``,
``language``, ``currency``, ``device``, ``zip_code`` and
``autoselect_variant`` are gone. They are removed rather than kept as silent
no-ops: ``sort_by`` was verified against the marketplace and every sort value
returns the identical unordered set, so a tool signature promising a sort is a
promise the API cannot keep. AutoGen derives the model-facing schema from the
signature and docstring, so a dead param here is a dead param the model plans
against.

``country`` (ISO 3166-1 alpha-2) replaces the old ``domain`` suffix. The API
still accepts ``domain`` as a deprecated alias, but these tools only speak
``country``.
"""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list

_COUNTRY_DOC = (
    "Marketplace country code (ISO 3166-1 alpha-2), not a domain: "
    '"us" (default), "gb" (the UK is gb, not uk), "ca", "de", "fr", "es", '
    '"it", "jp", "in", "au", "br", "mx", "nl", "pl", "se", "sg", "ae", '
    '"sa", "eg", "cn", "be", "tr". An unknown code falls back to us.'
)


def create_amazon_search_tool(max_results: int = 5) -> FunctionTool:
    """Create an Amazon search tool with the given configuration."""

    async def scavio_amazon_search(
        query: str,
        country: str | None = None,
        page: int | None = None,
    ) -> str:
        """Search Amazon product listings using the Scavio API.

        Results are NOT sorted and cannot be sorted or filtered by category,
        merchant or price - rank them yourself.

        Args:
            query: The product search query.
            country: Marketplace country code. See the module docstring.
            page: Result page, 1-based. One page per call, 1 credit each.

        Returns:
            JSON string with asin, title, url, image, price, currency, rating,
            reviews_count, is_sponsored, position, badge, sales_volume and
            delivery per product. reviews_count is Amazon's rounded display
            value and is approximate above 1000.
        """
        client = get_async_client()

        params: dict = {"query": query}
        if country is not None:
            params["country"] = country
        if page is not None:
            params["page"] = page

        raw = await client.amazon.search(**params)

        truncate_list(raw, ["data", "products"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_amazon_search,
        description=(
            "Search Amazon product listings (1 credit). Returns product "
            "titles, prices, ratings, ASINs, badges and delivery estimates. "
            "Results are unsorted and cannot be filtered."
        ),
    )


def create_amazon_product_tool() -> FunctionTool:
    """Create an Amazon product detail tool."""

    async def scavio_amazon_product(
        asin: str,
        country: str | None = None,
    ) -> str:
        """Fetch full details for a specific Amazon product by ASIN code.

        Args:
            asin: The Amazon Standard Identification Number for the product.
            country: Marketplace country code. See the module docstring.

        Returns:
            JSON string with title, brand, description, features, price,
            list_price, rating, reviews_count, availability, images,
            best_sellers_rank and specifications. `price` is the buy-box price
            only - use scavio_amazon_offers for competing sellers. `reviews`
            is review metadata with no review text.
        """
        client = get_async_client()

        params: dict = {"asin": asin}
        if country is not None:
            params["country"] = country

        raw = await client.amazon.product(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_amazon_product,
        description=(
            "Fetch full details for a specific Amazon product by ASIN code (1 "
            "credit)."
        ),
    )


def create_amazon_offers_tool(max_results: int = 20) -> FunctionTool:
    """Create an Amazon seller-offer tool."""

    async def scavio_amazon_offers(
        asin: str,
        country: str | None = None,
    ) -> str:
        """List every seller offer for an Amazon ASIN.

        Args:
            asin: The Amazon Standard Identification Number for the product.
            country: Marketplace country code. See the module docstring.

        Returns:
            JSON string with condition, seller_name, ships_from,
            is_buy_box_winner, is_prime, price, list_price, shipping_price and
            discount_percentage per offer. `price` excludes shipping_price and
            the buy-box winner is not always the cheapest offer. Page 1 only.
            An ASIN sold only by Amazon returns an empty offers list plus a
            `note` - that is a normal answer, not an error.
        """
        client = get_async_client()

        params: dict = {"asin": asin}
        if country is not None:
            params["country"] = country

        raw = await client.amazon.offers(**params)

        truncate_list(raw, ["data", "offers"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_amazon_offers,
        description=(
            "List every seller offer for an Amazon ASIN: price, seller, "
            "condition, shipping, and which offer holds the buy box (1 "
            "credit)."
        ),
    )
