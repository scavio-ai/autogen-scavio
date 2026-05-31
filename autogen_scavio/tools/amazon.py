"""Scavio Amazon tools for AutoGen."""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list


def create_amazon_search_tool(
    max_results: int = 5,
    pages: int | None = None,
    autoselect_variant: bool | None = None,
) -> FunctionTool:
    """Create an Amazon search tool with the given configuration."""

    async def scavio_amazon_search(
        query: str,
        domain: str = "com",
        sort_by: str | None = None,
        start_page: int | None = None,
        category_id: str | None = None,
        merchant_id: str | None = None,
        language: str | None = None,
        currency: str | None = None,
        device: str | None = None,
        zip_code: str | None = None,
    ) -> str:
        """Search Amazon product listings using the Scavio API.

        Args:
            query: The product search query.
            domain: Amazon domain suffix (e.g. "com", "co.uk", "de").
            sort_by: Sort order for results.
            start_page: Page number to start from.
            category_id: Filter by Amazon category ID.
            merchant_id: Filter by merchant/seller ID.
            language: Language code for results.
            currency: Currency code for prices.
            device: Device type for the request.
            zip_code: ZIP code for localized pricing/availability.

        Returns:
            JSON string with product names, prices, ratings, ASINs,
            and availability.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "domain": domain,
        }
        if sort_by is not None:
            params["sort_by"] = sort_by
        if start_page is not None:
            params["start_page"] = start_page
        if pages is not None:
            params["pages"] = pages
        if category_id is not None:
            params["category_id"] = category_id
        if merchant_id is not None:
            params["merchant_id"] = merchant_id
        if language is not None:
            params["language"] = language
        if currency is not None:
            params["currency"] = currency
        if device is not None:
            params["device"] = device
        if zip_code is not None:
            params["zip_code"] = zip_code
        if autoselect_variant is not None:
            params["autoselect_variant"] = autoselect_variant

        raw = await client.amazon.search(**params)

        truncate_list(raw, ["data", "products"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_amazon_search,
        description=(
            "Search Amazon product listings. Returns product names, "
            "prices, ratings, ASINs, and availability."
        ),
    )


def create_amazon_product_tool() -> FunctionTool:
    """Create an Amazon product detail tool."""

    async def scavio_amazon_product(
        asin: str,
        domain: str = "com",
        language: str | None = None,
        currency: str | None = None,
        device: str | None = None,
        zip_code: str | None = None,
        autoselect_variant: bool | None = None,
    ) -> str:
        """Fetch full details for a specific Amazon product by ASIN code.

        Args:
            asin: The Amazon Standard Identification Number for the product.
            domain: Amazon domain suffix (e.g. "com", "co.uk", "de").
            language: Language code for the response.
            currency: Currency code for prices.
            device: Device type for the request.
            zip_code: ZIP code for localized pricing/availability.
            autoselect_variant: Whether to auto-select the default variant.

        Returns:
            JSON string with full product details including title,
            description, pricing, images, and specifications.
        """
        client = get_async_client()

        params: dict = {
            "asin": asin,
            "domain": domain,
        }
        if language is not None:
            params["language"] = language
        if currency is not None:
            params["currency"] = currency
        if device is not None:
            params["device"] = device
        if zip_code is not None:
            params["zip_code"] = zip_code
        if autoselect_variant is not None:
            params["autoselect_variant"] = autoselect_variant

        raw = await client.amazon.product(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_amazon_product,
        description=(
            "Fetch full details for a specific Amazon product by ASIN code."
        ),
    )
