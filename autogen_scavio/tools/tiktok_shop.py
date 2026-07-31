"""Scavio TikTok Shop tools for AutoGen."""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list

# The two facts every caller has to know about this product area. They are
# repeated in the tool descriptions so an agent reading only the tool manifest
# still sees them.
PRODUCT_COVERAGE_NOTE = (
    "Only about 44% of the product ids returned by scavio_tiktok_shop_search "
    "resolve on this tool. Upstream has no detail data for the rest, so a "
    "not-found result is a normal outcome rather than an error: skip that "
    "product instead of retrying. Search is a listing source, not the first leg "
    "of a reliable search-then-detail pipeline."
)
PRODUCT_PRICE_NOTE = (
    "This tool does NOT return a price -- upstream masks it on the product "
    "page, so price.current and price.original come back null. Exact prices are "
    "returned by scavio_tiktok_shop_search, scavio_tiktok_shop_shop_products and "
    "scavio_tiktok_shop_category_products."
)


def _is_not_found(err: Exception) -> bool:
    """Report whether ``err`` is a TikTok Shop 404.

    A 404 here means the provider answered and there is genuinely no record:
    the id does not resolve, the shop has no products, or the link is dead.
    That is a determinate answer, not a failure, so it is surfaced as a
    structured result rather than raised.
    """
    return getattr(err, "status_code", None) == 404


def _not_found(reason: str, guidance: str) -> str:
    """Serialize the structured not-found result returned instead of raising."""
    return format_response(
        {"data": None, "not_found": True, "reason": reason, "guidance": guidance}
    )


def create_tiktok_shop_search_tool(max_results: int = 10) -> FunctionTool:
    """Create a TikTok Shop product search tool with the given configuration."""

    async def scavio_tiktok_shop_search(
        search: str,
        cursor: str | None = None,
    ) -> str:
        """Search TikTok Shop products by keyword (US catalog only).

        Returns up to 30 product cards per page with exact prices, ratings,
        sold counts and shop details. Paginate with data.next_cursor and dedupe
        by product_id across pages, which can overlap. data.degraded is true
        when the retry budget was exhausted and the page came back short -- a
        thin page, not the end of results.

        Product ids returned here are not guaranteed to resolve on
        scavio_tiktok_shop_product: only about 44% do.

        Args:
            search: Search keyword, 1-200 characters.
            cursor: Opaque cursor from a previous response's data.next_cursor.

        Returns:
            JSON string with the product listing.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "search": search,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.tiktok_shop.search(**params)

        truncate_list(raw, ["data", "products"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_shop_search,
        description=(
            "Search TikTok Shop products by keyword (US catalog only). Returns "
            "up to 30 products per page with exact prices, ratings, sold counts "
            "and shop details. Paginate with data.next_cursor and dedupe by "
            "product_id across pages. Product ids returned here are not "
            "guaranteed to resolve on scavio_tiktok_shop_product: only about "
            "44% do, so treat this as a listing source, not the first leg of a "
            "search-then-detail pipeline. This tool returns exact prices; the "
            "product detail tool does not."
        ),
    )


def create_tiktok_shop_search_suggestions_tool() -> FunctionTool:
    """Create a TikTok Shop keyword suggestion tool."""

    async def scavio_tiktok_shop_search_suggestions(
        search: str,
        region: str | None = None,
    ) -> str:
        """Expand a partial TikTok Shop query into keyword suggestions.

        Returns data.suggestions, a list of plain strings -- upstream provides
        no search volume and no score, so none is invented. Suggestions are not
        guaranteed prefix matches: a misspelling returns typo corrections, and
        results can include brand and shop names.

        Args:
            search: Partial search keyword, 1-100 characters.
            region: Marketplace region (US, GB, SG, MY, PH, TH, VN, ID).

        Returns:
            JSON string with the suggestion list.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "search": search,
            "region": region,
        }.items() if v is not None}

        raw = await client.tiktok_shop.search_suggestions(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_shop_search_suggestions,
        description=(
            "Keyword autocomplete and expansion for a partial TikTok Shop "
            "query, across 8 marketplace regions. Returns a plain list of "
            "suggestion strings with no search volume or score. Suggestions are "
            "not guaranteed prefix matches: a misspelling returns typo "
            "corrections, and results can include brand and shop names."
        ),
    )


def create_tiktok_shop_product_tool() -> FunctionTool:
    """Create a TikTok Shop product detail tool."""

    async def scavio_tiktok_shop_product(
        product_id: str,
        region: str | None = None,
    ) -> str:
        """Fetch full TikTok Shop product detail.

        Returns description, images, variants with stock, shipping, the full
        shop profile, category path, breadcrumbs and up to 3 top reviews.

        Two limits worth knowing: this resolves only about 44% of the product
        ids scavio_tiktok_shop_search returns -- a not-found result is a normal
        outcome, so skip the product instead of retrying -- and it carries no
        price at all, because upstream masks the digits on the product page.
        Exact prices come from scavio_tiktok_shop_search,
        scavio_tiktok_shop_shop_products or scavio_tiktok_shop_category_products.

        Args:
            product_id: TikTok Shop product id, 6-25 digits.
            region: Marketplace region (US, GB, SG, MY, PH, TH, VN, ID).

        Returns:
            JSON string with the product detail, or a structured not-found
            result.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "product_id": product_id,
            "region": region,
        }.items() if v is not None}

        try:
            raw = await client.tiktok_shop.product(**params)
        except Exception as err:
            if _is_not_found(err):
                return _not_found(
                    "No TikTok Shop detail data upstream for product "
                    f"'{product_id}': {err}",
                    PRODUCT_COVERAGE_NOTE + " " + PRODUCT_PRICE_NOTE,
                )
            raise

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_shop_product,
        description=(
            "Fetch full TikTok Shop product detail: description, images, "
            "variants with stock, shipping, shop profile, category path and top "
            "reviews. " + PRODUCT_PRICE_NOTE + " " + PRODUCT_COVERAGE_NOTE
            + " A not-found answer comes back as data null with not_found true; "
            "treat it as a normal result and move on."
        ),
    )


def create_tiktok_shop_product_reviews_tool(max_results: int = 20) -> FunctionTool:
    """Create a TikTok Shop product reviews tool with the given configuration."""

    async def scavio_tiktok_shop_product_reviews(
        product_id: str,
        page: int | None = None,
        page_size: int | None = None,
        sort: str | None = None,
        rating: int | None = None,
        has_media: bool | None = None,
        verified_only: bool | None = None,
        region: str | None = None,
    ) -> str:
        """Fetch paginated TikTok Shop product reviews.

        Returns review text, images, star histogram, verified-purchase and
        incentivized flags, up to 200 rows per call. data.total_reviews drifts
        between calls minutes apart and must not be used to compute a page
        count -- page with data.has_more instead. Reviewer names arrive
        pre-masked by the platform and image URLs are signed and expire.

        Args:
            product_id: TikTok Shop product id, 6-25 digits.
            page: 1-based page number, 1-500.
            page_size: Reviews per page, 1-200.
            sort: "relevant" (text-complete, image-heavy) or "recent" (fresher
                but far more text-sparse).
            rating: Only reviews with this star rating, 1-5.
            has_media: Only reviews with a photo or video.
            verified_only: Only verified purchases. Upstream allows one filter
                at a time, so this is ignored when has_media is true.
            region: Marketplace region (US, GB, SG, MY, PH, TH, VN, ID).

        Returns:
            JSON string with the review page.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "product_id": product_id,
            "page": page,
            "page_size": page_size,
            "sort": sort,
            "rating": rating,
            "has_media": has_media,
            "verified_only": verified_only,
            "region": region,
        }.items() if v is not None}

        raw = await client.tiktok_shop.product_reviews(**params)

        truncate_list(raw, ["data", "reviews"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_shop_product_reviews,
        description=(
            "Fetch paginated TikTok Shop product reviews with text, images, "
            "star histogram and verified-purchase flags, up to 200 per call. "
            "data.total_reviews drifts between calls and must not be used to "
            "compute a page count; page with data.has_more instead. "
            "sort='recent' is fresher but far more text-sparse than the default "
            "'relevant'. Reviewer names are pre-masked by the platform and "
            "image URLs are signed and expire."
        ),
    )


def create_tiktok_shop_categories_tool() -> FunctionTool:
    """Create a TikTok Shop category tree tool."""

    async def scavio_tiktok_shop_categories() -> str:
        """Fetch the global TikTok Shop category tree.

        Returns 28 top-level categories, 240 nodes, exactly two levels deep --
        that is all upstream provides, the depth is not faked. Category ids are
        identical in every region and names are always English, so this tool
        takes no parameters. The tree is stable: cache it rather than calling it
        per request.

        Returns:
            JSON string with the category tree.
        """
        client = get_async_client()

        raw = await client.tiktok_shop.categories()

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_shop_categories,
        description=(
            "Fetch the global TikTok Shop category tree: 28 top-level "
            "categories, 240 nodes, two levels deep. Category ids are identical "
            "in every region and names are always English, so this tool takes "
            "no parameters. Feed a category_id from here into "
            "scavio_tiktok_shop_category_products. The tree is stable; cache it."
        ),
    )


def create_tiktok_shop_category_products_tool(max_results: int = 10) -> FunctionTool:
    """Create a TikTok Shop category listing tool with the given configuration."""

    async def scavio_tiktok_shop_category_products(
        category_id: str,
        cursor: str | None = None,
        region: str | None = None,
    ) -> str:
        """List TikTok Shop products under a category id, with exact prices.

        Page size is inconsistent upstream (15 to 20 per page), so always
        paginate with data.next_cursor rather than assuming a fixed size.
        Category listings are shallow: after a few pages the source stops
        returning new products and has_more turns false, which is the end of the
        listing rather than an error.

        Args:
            category_id: Category id from scavio_tiktok_shop_categories.
            cursor: Opaque cursor from a previous response's data.next_cursor.
            region: Marketplace region. US and GB only.

        Returns:
            JSON string with the product listing, or a structured not-found
            result.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "category_id": category_id,
            "cursor": cursor,
            "region": region,
        }.items() if v is not None}

        try:
            raw = await client.tiktok_shop.category_products(**params)
        except Exception as err:
            if _is_not_found(err):
                return _not_found(
                    f"No TikTok Shop products found for category "
                    f"'{category_id}': {err}",
                    "Check the category_id against "
                    "scavio_tiktok_shop_categories. Category listings are "
                    "served for US and GB only.",
                )
            raise

        truncate_list(raw, ["data", "products"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_shop_category_products,
        description=(
            "List TikTok Shop products under a category id from "
            "scavio_tiktok_shop_categories, with exact prices. US and GB only. "
            "Page size is inconsistent upstream (15 to 20 per page), so "
            "paginate with data.next_cursor and never assume a fixed size. "
            "Listings are shallow: has_more turning false after a few pages is "
            "the end of the listing, not an error. This tool returns exact "
            "prices; the product detail tool does not."
        ),
    )


def create_tiktok_shop_shop_products_tool(max_results: int = 10) -> FunctionTool:
    """Create a TikTok Shop seller catalog tool with the given configuration."""

    async def scavio_tiktok_shop_shop_products(
        shop_id: str,
        cursor: str | None = None,
        region: str | None = None,
    ) -> str:
        """Fetch a TikTok Shop seller's product catalog, with exact prices.

        Returns 30 product cards per page. data.shop carries only the shop id,
        name and logo: follower count, shop location and shop-level rating are
        not available from this endpoint -- scavio_tiktok_shop_product has the
        full shop profile.

        Args:
            shop_id: TikTok Shop seller id, 6-25 digits.
            cursor: Opaque cursor from a previous response's data.next_cursor.
            region: Marketplace region (US, GB, SG, MY, PH, TH, VN, ID).

        Returns:
            JSON string with the product listing, or a structured not-found
            result.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "shop_id": shop_id,
            "cursor": cursor,
            "region": region,
        }.items() if v is not None}

        try:
            raw = await client.tiktok_shop.shop_products(**params)
        except Exception as err:
            if _is_not_found(err):
                return _not_found(
                    f"No TikTok Shop products found for shop '{shop_id}': {err}",
                    "Check the shop_id, or resolve a storefront URL with "
                    "scavio_tiktok_shop_resolve first.",
                )
            raise

        truncate_list(raw, ["data", "products"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_shop_shop_products,
        description=(
            "Fetch a TikTok Shop seller's product catalog, 30 per page, with "
            "exact prices. Paginate with data.next_cursor. Shop follower count, "
            "location and shop-level rating are not available here -- use "
            "scavio_tiktok_shop_product for the full shop profile. This tool "
            "returns exact prices; the product detail tool does not."
        ),
    )


def create_tiktok_shop_resolve_tool() -> FunctionTool:
    """Create a TikTok Shop URL resolution tool."""

    async def scavio_tiktok_shop_resolve(url: str) -> str:
        """Resolve a TikTok Shop URL or share link to a product_id or shop_id.

        Returns data.type ("product" or "shop"), the id, a canonical
        https://shop.tiktok.com/... URL, and resolved_by ("url_pattern" when the
        id was read straight out of the link, "share_link" when the link had to
        be followed). A dead or expired share link comes back as a structured
        not-found result.

        Args:
            url: A TikTok Shop URL or share link. Accepted: shop.tiktok.com
                product or store pages, tiktok.com/view/product or /view/shop
                links, affiliate-*.tiktok.com share links, and vt.tiktok.com or
                tiktok.com/t short links.

        Returns:
            JSON string with the resolved reference, or a structured not-found
            result.
        """
        client = get_async_client()

        try:
            raw = await client.tiktok_shop.resolve(url=url)
        except Exception as err:
            if _is_not_found(err):
                return _not_found(
                    f"Could not resolve '{url}': {err}",
                    "The link may have expired or may not point to a product "
                    "or shop. Try the canonical shop.tiktok.com URL instead.",
                )
            raise

        return format_response(raw)

    return FunctionTool(
        scavio_tiktok_shop_resolve,
        description=(
            "Resolve any TikTok Shop URL or share link to a product_id or "
            "shop_id, ready to pass to the other TikTok Shop tools. Accepts "
            "shop.tiktok.com product and store pages, tiktok.com/view links, "
            "affiliate share links and vt.tiktok.com short links. Returns the "
            "id, a canonical https URL and whether it was read from the URL "
            "pattern or by following the share link. A dead link comes back as "
            "not_found."
        ),
    )
