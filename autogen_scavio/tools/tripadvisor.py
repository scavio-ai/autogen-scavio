"""Scavio Tripadvisor tools for AutoGen.

4 endpoints. 2 credits flat on all four endpoints.

LOOKUP FIRST: create_tripadvisor_locations_tool is the entry point. Every other
Tripadvisor endpoint is keyed by an id that only exists inside Tripadvisor's own URLs,
so a caller holding a name has to resolve it here before anything else will answer.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_tripadvisor_locations_tool() -> FunctionTool:
    """Create a Scavio Tripadvisor locations tool."""

    async def scavio_tripadvisor_locations(
        query: Annotated[str, "Place or business name to resolve (1-120 characters)."],
        limit: Annotated[
            int | None,
            "Rows to return, 1-20 (default 12). Sizes the response only; there is no "
            "paging here.",
        ] = None,
    ) -> str:
        """START HERE. Resolve a place or business NAME to the TripAdvisor geo_id /
        location_id pair every other endpoint needs.

        Args:
            query: Place or business name to resolve (1-120 characters).
            limit: Rows to return, 1-20 (default 12). Sizes the response only; there is
                no paging here.

        Returns:
            JSON string with lOOKUP: resolves a place or business NAME to TripAdvisor
            geo_id / location_id pairs. Start here.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.tripadvisor.locations(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_tripadvisor_locations,
        description=(
            "START HERE: resolve a place or business NAME to the TripAdvisor geo_id / "
            "location_id pair every other TripAdvisor endpoint is keyed by. Up to 20 "
            "rows. Costs 2 credits."
        ),
    )


def create_tripadvisor_search_tool() -> FunctionTool:
    """Create a Scavio Tripadvisor search tool."""

    async def scavio_tripadvisor_search(
        geo_id: Annotated[
            str | None,
            "TripAdvisor geo id (1-500 characters): 30196, g30196, or a URL carrying "
            "one. Required unless url is given.",
        ] = None,
        category: Annotated[
            Literal["restaurants", "hotels", "attractions"] | None,
            "Listing family to search (default 'restaurants').",
        ] = None,
        page: Annotated[
            int | None,
            "Results page, 1-based. 30 locations per page; a page beyond the last is "
            "a 404, not an empty result.",
        ] = None,
        url: Annotated[
            str | None,
            "Full tripadvisor.com listing URL (1-500 characters), as an alternative "
            "to geo_id; country sites are accepted.",
        ] = None,
    ) -> str:
        """Restaurants / hotels / attractions in a TripAdvisor geo, TripAdvisor-ranked;
        each row carries the location_id + geo_id pair.

        Parameter rule: geo_id or url is required.

        Pagination: page - 30 locations per page; a page beyond the last is a 404, not
        an empty result.

        Args:
            geo_id: TripAdvisor geo id (1-500 characters): 30196, g30196, or a URL
                carrying one. Required unless url is given.
            category: Listing family to search (default 'restaurants').
            page: Results page, 1-based. 30 locations per page; a page beyond the last
                is a 404, not an empty result.
            url: Full tripadvisor.com listing URL (1-500 characters), as an alternative
                to geo_id; country sites are accepted.

        Returns:
            JSON string with restaurants / hotels / attractions in a geo,
            TripAdvisor-ranked: rating, review count, price band, address, coordinates,
            phone, hours, Travelers' Choice badge; each row carries the location_id +
            geo_id pair.
        """
        client = get_async_client()

        params: dict = {
            "geo_id": geo_id,
            "category": category,
            "page": page,
            "url": url,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.tripadvisor.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_tripadvisor_search,
        description=(
            "Restaurants, hotels or attractions in a TripAdvisor geo, "
            "TripAdvisor-ranked: rating, review count, price band, address, "
            "coordinates, phone, hours, Travelers' Choice badge; each row carries the "
            "location_id + geo_id pair. 30 locations per page. Provide geo_id or url. "
            "Costs 2 credits."
        ),
    )


def create_tripadvisor_location_tool() -> FunctionTool:
    """Create a Scavio Tripadvisor location tool."""

    async def scavio_tripadvisor_location(
        location_id: Annotated[
            str | None,
            "TripAdvisor location id (1-500 characters): 1899234, d1899234, or a full "
            "_Review URL. Required unless url is given.",
        ] = None,
        geo_id: Annotated[
            str | None,
            "Geo the location sits in; required when location_id is a bare d-id.",
        ] = None,
        category: Annotated[
            Literal["restaurants", "hotels", "attractions"] | None,
            "Location family (default 'restaurants'); match the location's own type.",
        ] = None,
        url: Annotated[
            str | None,
            "Full tripadvisor.com _Review URL (1-500 characters), as an alternative "
            "to location_id.",
        ] = None,
    ) -> str:
        """One TripAdvisor location in full: rating histogram, sub-ratings, city
        ranking, amenities, contact, photos, and the FIRST PAGE OF REVIEWS.

        Parameter rule: location_id or url is required; the transport additionally
        requires a geo when a bare d-id is sent.

        Args:
            location_id: TripAdvisor location id (1-500 characters): 1899234, d1899234,
                or a full _Review URL. Required unless url is given.
            geo_id: Geo the location sits in; required when location_id is a bare d-id.
            category: Location family (default 'restaurants'); match the location's own
                type.
            url: Full tripadvisor.com _Review URL (1-500 characters), as an alternative
                to location_id.

        Returns:
            JSON string with one location in full: rating, review histogram and
            per-aspect sub-ratings, city ranking, price band, cuisines, amenities,
            address, coordinates, contact, photos, and the FIRST PAGE OF REVIEWS.
        """
        client = get_async_client()

        params: dict = {
            "location_id": location_id,
            "geo_id": geo_id,
            "category": category,
            "url": url,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.tripadvisor.location(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_tripadvisor_location,
        description=(
            "One TripAdvisor location in full: rating, review histogram and "
            "per-aspect sub-ratings, city ranking, price band, cuisines, amenities, "
            "address, coordinates, contact, photos, and the FIRST PAGE OF REVIEWS. "
            "Provide location_id or url. Costs 2 credits."
        ),
    )


def create_tripadvisor_reviews_tool() -> FunctionTool:
    """Create a Scavio Tripadvisor reviews tool."""

    async def scavio_tripadvisor_reviews(
        location_id: Annotated[
            str | None,
            "TripAdvisor location id (1-500 characters): 1899234, d1899234, or a full "
            "_Review URL. Required unless url is given.",
        ] = None,
        geo_id: Annotated[
            str | None,
            "Geo the location sits in; required when location_id is a bare d-id.",
        ] = None,
        category: Annotated[
            Literal["restaurants", "hotels", "attractions"] | None,
            "Location family (default 'restaurants'). It sets the page size, so it "
            "must match the location's own type on any page past the first.",
        ] = None,
        url: Annotated[
            str | None,
            "Full tripadvisor.com _Review URL (1-500 characters), as an alternative "
            "to location_id.",
        ] = None,
        page: Annotated[
            int | None,
            "Reviews page, 1-based. 15 per page for restaurants, 10 for hotels and "
            "attractions; past the last page is a 404.",
        ] = None,
    ) -> str:
        """A page of TripAdvisor reviews: rating, trip date and type, reviewer home town
        and contribution count, management response.

        Parameter rule: location_id or url is required.

        Pagination: page - 15 per page for restaurants, 10 for hotels and attractions,
        so `category` must match the location's own type on any page past the first.

        Args:
            location_id: TripAdvisor location id (1-500 characters): 1899234, d1899234,
                or a full _Review URL. Required unless url is given.
            geo_id: Geo the location sits in; required when location_id is a bare d-id.
            category: Location family (default 'restaurants'). It sets the page size, so
                it must match the location's own type on any page past the first.
            url: Full tripadvisor.com _Review URL (1-500 characters), as an alternative
                to location_id.
            page: Reviews page, 1-based. 15 per page for restaurants, 10 for hotels and
                attractions; past the last page is a 404.

        Returns:
            JSON string with a page of reviews: rating, trip date and type, reviewer
            home town and contribution count, management response.
        """
        client = get_async_client()

        params: dict = {
            "location_id": location_id,
            "geo_id": geo_id,
            "category": category,
            "url": url,
            "page": page,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.tripadvisor.reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_tripadvisor_reviews,
        description=(
            "A page of TripAdvisor reviews: rating, trip date and type, reviewer home "
            "town and contribution count, management response. Page 1 already rides "
            "along in location(), so use this to page PAST it; consecutive pages can "
            "repeat one review at the boundary, so de-duplicate on review_id. Provide "
            "location_id or url. Costs 2 credits."
        ),
    )
