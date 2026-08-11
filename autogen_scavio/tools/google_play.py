"""Scavio Google Play tools for AutoGen.

3 endpoints. 2 credits flat on all three endpoints. This is NOT the 1-credit Google SERP
price: Google Play is a separate namespace partly because it is a separate, dearer
scrape.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_google_play_search_tool() -> FunctionTool:
    """Create a Scavio Google Play search tool."""

    async def scavio_google_play_search(
        query: Annotated[
            str,
            "What to search the store for (1-200 characters): an app name, a "
            "publisher, or a category phrase. Apps only - games are folded into the "
            "apps vertical, but books and films use a different card shape and are "
            "not covered.",
        ],
        hl: Annotated[
            str | None,
            "UI language, 2-20 characters (default 'en'). Changes the STOREFRONT, not "
            "only the strings: at hl=pt-BR the title, description, install formatting "
            "and content rating all move with it. Play silently falls back to English "
            "on a value it does not serve.",
        ] = None,
        gl: Annotated[
            str | None,
            "Country code, 2-10 characters (default 'us'), deciding which "
            "storefront's price and availability are returned. Play silently falls "
            "back to the US storefront on a country it does not serve.",
        ] = None,
    ) -> str:
        """Ranked Google Play apps: package name, title, developer, rating, install
        count, price and IAP range, content rating, icon, screenshots.

        Args:
            query: What to search the store for (1-200 characters): an app name, a
                publisher, or a category phrase. Apps only - games are folded into the
                apps vertical, but books and films use a different card shape and are
                not covered.
            hl: UI language, 2-20 characters (default 'en'). Changes the STOREFRONT, not
                only the strings: at hl=pt-BR the title, description, install formatting
                and content rating all move with it. Play silently falls back to English
                on a value it does not serve.
            gl: Country code, 2-10 characters (default 'us'), deciding which
                storefront's price and availability are returned. Play silently falls
                back to the US storefront on a country it does not serve.

        Returns:
            JSON string with ranked apps: package name, title, developer, rating,
            install count, price and IAP range, content rating, icon, screenshots. A
            branded query returns the hero card as result 1 projected to the same row
            shape, plus Play's related-query rail.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "hl": hl,
            "gl": gl,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.google_play.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_google_play_search,
        description=(
            "Ranked Google Play apps: package name, title, developer, rating, install "
            "count, price and IAP range, content rating, icon and screenshots. A "
            "branded query returns the hero card as result 1 in the same row shape, "
            "plus Play's related-query rail. NO PAGINATION - one shelf of about 30 "
            "apps. Costs 2 credits."
        ),
    )


def create_google_play_app_tool() -> FunctionTool:
    """Create a Scavio Google Play app tool."""

    async def scavio_google_play_app(
        app_id: Annotated[
            str,
            "Android package name ('com.spotify.music') or any play.google.com URL "
            "carrying one in its id param (1-500 characters).",
        ],
        hl: Annotated[
            str | None,
            "UI language, 2-20 characters (default 'en'). Changes the STOREFRONT, not "
            "only the strings: title, description, install formatting and content "
            "rating all move with it. Play silently falls back to English on a value "
            "it does not serve.",
        ] = None,
        gl: Annotated[
            str | None,
            "Country code, 2-10 characters (default 'us'), deciding which "
            "storefront's price and availability are returned. Play silently falls "
            "back to the US storefront on a country it does not serve.",
        ] = None,
    ) -> str:
        """Full Google Play store listing: installs (incl. the REAL unrendered count),
        star histogram, developer identity, IAPs, permission tree, Data safety table,
        the 20 server-rendered reviews.

        Args:
            app_id: Android package name ('com.spotify.music') or any play.google.com
                URL carrying one in its id param (1-500 characters).
            hl: UI language, 2-20 characters (default 'en'). Changes the STOREFRONT, not
                only the strings: title, description, install formatting and content
                rating all move with it. Play silently falls back to English on a value
                it does not serve.
            gl: Country code, 2-10 characters (default 'us'), deciding which
                storefront's price and availability are returned. Play silently falls
                back to the US storefront on a country it does not serve.

        Returns:
            JSON string with full store listing: installs (incl. the real unrendered
            count), rating and star histogram, description, developer identity and legal
            contact, price and IAPs, categories and gameplay tags, screenshots and
            trailer, version and Android requirement, release/update dates, changelog,
            full permission tree, Data safety table, the 20 server-rendered reviews,
            similar-apps and more-by-developer rails.
        """
        client = get_async_client()

        params: dict = {
            "app_id": app_id,
            "hl": hl,
            "gl": gl,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.google_play.app(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_google_play_app,
        description=(
            "Full Google Play store listing: installs including the REAL count Play "
            "publishes but never renders, rating and star histogram, description, "
            "developer identity and legal contact, price and IAPs, categories and "
            "gameplay tags, screenshots and trailer, version and Android requirement, "
            "release and update dates, changelog, the full permission tree, the Data "
            "safety table, the 20 server-rendered reviews and the similar-apps and "
            "more-by-developer rails. Costs 2 credits."
        ),
    )


def create_google_play_reviews_tool() -> FunctionTool:
    """Create a Scavio Google Play reviews tool."""

    async def scavio_google_play_reviews(
        app_id: Annotated[
            str,
            "Android package name ('com.spotify.music') or any play.google.com URL "
            "carrying one in its id param (1-500 characters).",
        ],
        sort: Annotated[
            Literal["relevance", "newest", "rating"] | None,
            "Review ordering (default 'newest'). Closed enum. The cursor encodes the "
            "sort, so keep this identical when paging.",
        ] = None,
        count: Annotated[
            int | None,
            "Reviews to return, 1-200 (default 50); 200 is our cap, not Play's. Play "
            "honours more, but a single page that large is megabytes for one credit - "
            "page with cursor instead.",
        ] = None,
        cursor: Annotated[
            str | None,
            "Continuation token from a prior response's next_cursor (1-4000 "
            "characters). Opaque and SINGLE-USE, and it encodes the sort as well as "
            "the position - send it back with the SAME sort it came from. A cursor "
            "past the last review is a 404, not an empty page.",
        ] = None,
        hl: Annotated[
            str | None,
            "UI language, 2-20 characters (default 'en'). Changes the STOREFRONT, not "
            "only the strings. Play silently falls back to English on a value it does "
            "not serve.",
        ] = None,
        gl: Annotated[
            str | None,
            "Country code, 2-10 characters (default 'us'), deciding which "
            "storefront's price and availability are returned. Play silently falls "
            "back to the US storefront on a country it does not serve.",
        ] = None,
    ) -> str:
        """A page of Google Play reviews: star score, full text, author, thumbs-up
        count, developer reply, and the APP VERSION the reviewer was running.

        Pagination: cursor -> next_cursor. The cursor is OPAQUE, SINGLE-USE, and encodes
        the SORT as well as the position - send it back with the SAME `sort` it came
        from. A cursor past the last review is a 404, not an empty page.

        Args:
            app_id: Android package name ('com.spotify.music') or any play.google.com
                URL carrying one in its id param (1-500 characters).
            sort: Review ordering (default 'newest'). Closed enum. The cursor encodes
                the sort, so keep this identical when paging.
            count: Reviews to return, 1-200 (default 50); 200 is our cap, not Play's.
                Play honours more, but a single page that large is megabytes for one
                credit - page with cursor instead.
            cursor: Continuation token from a prior response's next_cursor (1-4000
                characters). Opaque and SINGLE-USE, and it encodes the sort as well as
                the position - send it back with the SAME sort it came from. A cursor
                past the last review is a 404, not an empty page.
            hl: UI language, 2-20 characters (default 'en'). Changes the STOREFRONT, not
                only the strings. Play silently falls back to English on a value it does
                not serve.
            gl: Country code, 2-10 characters (default 'us'), deciding which
                storefront's price and availability are returned. Play silently falls
                back to the US storefront on a country it does not serve.

        Returns:
            JSON string with a page of reviews: star score, full text, author, thumbs-up
            count, developer reply, and the APP VERSION the reviewer was running. Paged
            via next_cursor.
        """
        client = get_async_client()

        params: dict = {
            "app_id": app_id,
            "sort": sort,
            "count": count,
            "cursor": cursor,
            "hl": hl,
            "gl": gl,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.google_play.reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_google_play_reviews,
        description=(
            "A page of Google Play reviews: star score, full text, author, thumbs-up "
            "count, developer reply and the APP VERSION the reviewer was running. "
            "Paged by cursor, up to 200 per call. app() already returns the 20 "
            "reviews Play server-renders; use this to page past them or sort "
            "differently. Costs 2 credits."
        ),
    )
