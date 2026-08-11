"""Scavio Apple App Store tools for AutoGen.

3 endpoints. 1 credit flat on all three endpoints - this is Apple's official iTunes JSON
API.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_app_store_search_tool() -> FunctionTool:
    """Create a Scavio Apple App Store search tool."""

    async def scavio_app_store_search(
        term: Annotated[
            str,
            "What to search for (1-500 characters). Apple matches an app name, a "
            "keyword OR a publisher name, so searching a developer returns their "
            "catalogue.",
        ],
        limit: Annotated[
            int | None,
            "Apps to return, 1-200 (default 25). The ONLY lever on result volume: the "
            "search API has no pagination and every offset spelling is silently "
            "ignored.",
        ] = None,
        country: Annotated[
            str | None,
            "Two-letter ISO storefront code (default 'us'); decides price, currency, "
            "localised title and whether the app is sold there at all. Anything that "
            "is not exactly two letters is rejected with a free 400.",
        ] = None,
        entity: Annotated[
            Literal["software", "ipad_software", "mac_software"] | None,
            "Which catalogue to search: iPhone/iPad apps ('software', the default), "
            "iPad apps, or Mac App Store apps. These are separate stores, not a "
            "filter - Mac rows carry no iPad/Apple TV screenshots, advisories, "
            "features, supported devices or Game Center flag, returning them empty "
            "rather than absent.",
        ] = None,
        lang: Annotated[
            str | None,
            "Listing text language as a five-letter code ('en_us', 'ja_jp'); any "
            "other shape is rejected. Independent of country: the storefront sets the "
            "price, this sets the words.",
        ] = None,
    ) -> str:
        """Up to 200 fully-shaped App Store apps (the same 43-field row as /app).
        Doubles as a bulk metadata fetch and a publisher lookup.

        Args:
            term: What to search for (1-500 characters). Apple matches an app name, a
                keyword OR a publisher name, so searching a developer returns their
                catalogue.
            limit: Apps to return, 1-200 (default 25). The ONLY lever on result volume:
                the search API has no pagination and every offset spelling is silently
                ignored.
            country: Two-letter ISO storefront code (default 'us'); decides price,
                currency, localised title and whether the app is sold there at all.
                Anything that is not exactly two letters is rejected with a free 400.
            entity: Which catalogue to search: iPhone/iPad apps ('software', the
                default), iPad apps, or Mac App Store apps. These are separate stores,
                not a filter - Mac rows carry no iPad/Apple TV screenshots, advisories,
                features, supported devices or Game Center flag, returning them empty
                rather than absent.
            lang: Listing text language as a five-letter code ('en_us', 'ja_jp'); any
                other shape is rejected. Independent of country: the storefront sets the
                price, this sets the words.

        Returns:
            JSON string with up to 200 fully-shaped apps (same row as /app). No
            pagination.
        """
        client = get_async_client()

        params: dict = {
            "term": term,
            "limit": limit,
            "country": country,
            "entity": entity,
            "lang": lang,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.app_store.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_app_store_search,
        description=(
            "Search the App Store and get up to 200 fully-shaped app rows - the same "
            "43-field row as app() - so a search doubles as a bulk metadata fetch and "
            "as a publisher lookup. NO PAGINATION: raise limit, there is no second "
            "page. Costs 1 credit."
        ),
    )


def create_app_store_app_tool() -> FunctionTool:
    """Create a Scavio Apple App Store app tool."""

    async def scavio_app_store_app(
        app_id: Annotated[
            str,
            "App Store id - the digits after 'id' in an apps.apple.com URL - or the "
            "app's bundle id ('notion.id', 'com.burbn.instagram'); both resolve to "
            "the identical payload. 1-255 characters matching "
            "^[A-Za-z0-9][A-Za-z0-9._-]*$, so a pasted apps.apple.com URL is rejected "
            "with a free 400. An id Apple cannot resolve is a billed 404.",
        ],
        country: Annotated[
            str | None,
            "Two-letter ISO storefront code (default 'us'); decides price, currency, "
            "localised title and whether the app is sold there at all. Anything that "
            "is not exactly two letters is rejected with a free 400.",
        ] = None,
    ) -> str:
        """Full App Store listing: title, description, developer identity, price,
        all-time and current-version ratings, release notes, genres, advisories,
        screenshots, size, minimum OS, supported devices.

        Args:
            app_id: App Store id - the digits after 'id' in an apps.apple.com URL - or
                the app's bundle id ('notion.id', 'com.burbn.instagram'); both resolve
                to the identical payload. 1-255 characters matching
                ^[A-Za-z0-9][A-Za-z0-9._-]*$, so a pasted apps.apple.com URL is rejected
                with a free 400. An id Apple cannot resolve is a billed 404.
            country: Two-letter ISO storefront code (default 'us'); decides price,
                currency, localised title and whether the app is sold there at all.
                Anything that is not exactly two letters is rejected with a free 400.

        Returns:
            JSON string with full listing: title, description, developer/seller
            identity, price and currency, all-time and current-version ratings, version
            and release notes, genres, content rating and advisories, icons at three
            sizes, screenshots, download size, minimum OS, languages, supported devices,
            Game Center and VPP flags.
        """
        client = get_async_client()

        params: dict = {
            "app_id": app_id,
            "country": country,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.app_store.app(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_app_store_app,
        description=(
            "Full App Store listing: title, description, developer and seller "
            "identity, price and currency, all-time and current-version ratings, "
            "version and release notes, genres, content rating and advisories, icons "
            "at three sizes, screenshots, download size, minimum OS, languages, "
            "supported devices and the Game Center and VPP flags. Costs 1 credit."
        ),
    )


def create_app_store_reviews_tool() -> FunctionTool:
    """Create a Scavio Apple App Store reviews tool."""

    async def scavio_app_store_reviews(
        app_id: Annotated[
            str,
            "App Store id, NUMERIC ONLY - unlike app(), the reviews feed has no "
            "bundle-id form.",
        ],
        country: Annotated[
            str | None,
            "Two-letter ISO storefront code (default 'us'). Anything that is not "
            "exactly two letters is rejected with a free 400. Ask a different country "
            "to reach past the 500-review ceiling.",
        ] = None,
        page: Annotated[
            int | None,
            "Reviews page, 1-10, 50 reviews each (default 1). Apple hard-stops at "
            "page 10.",
        ] = None,
        sort: Annotated[
            Literal["most_recent", "most_helpful"] | None,
            "Review ordering (default 'most_recent'). The choice decides whether the "
            "vote fields mean anything: under most_recent almost every review is too "
            "new to have been voted on and returns zeroes, while most_helpful returns "
            "them densely populated.",
        ] = None,
    ) -> str:
        """A page of App Store reviews: star rating, title, full text, author, and the
        APP VERSION it was written against.

        Pagination: page 1..10 at 50 per page - a HARD STOP at page 10 (500 reviews per
        storefront is Apple's anonymous ceiling). Reach further by asking a different
        `country`.

        Args:
            app_id: App Store id, NUMERIC ONLY - unlike app(), the reviews feed has no
                bundle-id form.
            country: Two-letter ISO storefront code (default 'us'). Anything that is not
                exactly two letters is rejected with a free 400. Ask a different country
                to reach past the 500-review ceiling.
            page: Reviews page, 1-10, 50 reviews each (default 1). Apple hard-stops at
                page 10.
            sort: Review ordering (default 'most_recent'). The choice decides whether
                the vote fields mean anything: under most_recent almost every review is
                too new to have been voted on and returns zeroes, while most_helpful
                returns them densely populated.

        Returns:
            JSON string with a page of reviews: star rating, title, full text, author,
            and the APP VERSION it was written against.
        """
        client = get_async_client()

        params: dict = {
            "app_id": app_id,
            "country": country,
            "page": page,
            "sort": sort,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.app_store.reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_app_store_reviews,
        description=(
            "A page of App Store reviews: star rating, title, full text, author and "
            "the APP VERSION the review was written against. 50 per page, "
            "hard-stopped at page 10 - 500 reviews per storefront is Apple's "
            "anonymous ceiling. This endpoint cannot 404: an unknown id and a real "
            "app with no reviews return the same empty feed. Costs 1 credit."
        ),
    )
