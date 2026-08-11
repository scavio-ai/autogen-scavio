"""Scavio Zillow tools for AutoGen.

3 endpoints. 1 credit flat on all three endpoints.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_zillow_search_tool() -> FunctionTool:
    """Create a Scavio Zillow search tool."""

    async def scavio_zillow_search(
        location: Annotated[
            str,
            "Region to search (1-200 characters): a Zillow slug ('austin-tx'), a "
            "human form ('Austin, TX'), a ZIP, or a pasted zillow.com search URL. A "
            "ZIP works alone but cannot be combined with a filter or sort; an "
            "unresolvable region is a 404.",
        ],
        listing_status: Annotated[
            Literal["for_sale", "for_rent", "sold"] | None,
            "Which listings to return. Defaults to 'for_sale'.",
        ] = None,
        page: Annotated[int | None, "Results page, 1-based."] = None,
        sort: Annotated[
            Literal[
                "relevance", "recommended", "newest", "price_low", "price_high",
                "payment_low", "payment_high", "beds", "baths", "sqft", "lot_size",
                "zestimate_low", "zestimate_high", "recent_change",
            ]
            | None,
            "Result sort order. Sorts that rank against a signed-in profile "
            "(saved/featured/personalised) are unsupported - we are never signed in.",
        ] = None,
        min_price: Annotated[
            float | None,
            "Minimum price, inclusive (0 or greater). On listing_status='for_rent' "
            "this is MONTHLY RENT - Zillow files rent under its payment filter.",
        ] = None,
        max_price: Annotated[
            float | None,
            "Maximum price, inclusive (0 or greater). On listing_status='for_rent' "
            "this is MONTHLY RENT.",
        ] = None,
        beds_min: Annotated[
            int | None,
            "Minimum bedrooms; whole number, 0 or greater.",
        ] = None,
        beds_max: Annotated[
            int | None,
            "Maximum bedrooms; whole number, 0 or greater.",
        ] = None,
        baths_min: Annotated[
            float | None,
            "Minimum bathrooms, 0 or greater. Half-baths are allowed (1.5).",
        ] = None,
        baths_max: Annotated[
            float | None,
            "Maximum bathrooms, 0 or greater. Half-baths are allowed (1.5).",
        ] = None,
        sqft_min: Annotated[
            int | None,
            "Minimum living area in square feet; whole number, 0 or greater.",
        ] = None,
        sqft_max: Annotated[
            int | None,
            "Maximum living area in square feet; whole number, 0 or greater.",
        ] = None,
        lot_size_min: Annotated[
            int | None,
            "Minimum lot size in square feet; whole number, 0 or greater.",
        ] = None,
        lot_size_max: Annotated[
            int | None,
            "Maximum lot size in square feet; whole number, 0 or greater.",
        ] = None,
        year_built_min: Annotated[
            int | None,
            "Earliest year built; whole number, 0 or greater.",
        ] = None,
        year_built_max: Annotated[
            int | None,
            "Latest year built; whole number, 0 or greater.",
        ] = None,
        max_hoa: Annotated[
            float | None,
            "Maximum monthly HOA fee in dollars, 0 or greater.",
        ] = None,
        home_type: Annotated[
            Literal[
                "houses", "townhomes", "multi_family", "condos", "apartments",
                "manufactured", "lots_land",
            ]
            | None,
            "Property type filter.",
        ] = None,
        days_on_zillow: Annotated[
            Literal["1", "7", "14", "30", "90", "6m", "12m", "24m", "36m"] | None,
            "Listed - or, with listing_status='sold', sold - within the last N days. "
            "Closed enum: an unrecognised value returns the UNFILTERED set under a "
            "200.",
        ] = None,
        keywords: Annotated[
            str | None,
            "Free-text match against the listing description (1-200 characters).",
        ] = None,
        has_pool: Annotated[bool | None, "Only listings with a pool."] = None,
        has_garage: Annotated[bool | None, "Only listings with a garage."] = None,
        has_air_conditioning: Annotated[
            bool | None,
            "Only listings with air conditioning.",
        ] = None,
        is_waterfront: Annotated[bool | None, "Only waterfront listings."] = None,
        has_basement: Annotated[bool | None, "Only listings with a basement."] = None,
        is_new_construction: Annotated[
            bool | None,
            "Only new-construction listings.",
        ] = None,
        has_open_house: Annotated[
            bool | None,
            "Only listings with an upcoming open house.",
        ] = None,
        price_reduced: Annotated[
            bool | None,
            "Only listings whose price was reduced.",
        ] = None,
        is_3d_tour: Annotated[bool | None, "Only listings with a 3D tour."] = None,
    ) -> str:
        """Zillow listings in a region: price, beds, baths, living area, Zestimate,
        coordinates, images, days on market.

        Pagination: page.

        Args:
            location: Region to search (1-200 characters): a Zillow slug ('austin-tx'),
                a human form ('Austin, TX'), a ZIP, or a pasted zillow.com search URL. A
                ZIP works alone but cannot be combined with a filter or sort; an
                unresolvable region is a 404.
            listing_status: Which listings to return. Defaults to 'for_sale'.
            page: Results page, 1-based.
            sort: Result sort order. Sorts that rank against a signed-in profile
                (saved/featured/personalised) are unsupported - we are never signed in.
            min_price: Minimum price, inclusive (0 or greater). On
                listing_status='for_rent' this is MONTHLY RENT - Zillow files rent under
                its payment filter.
            max_price: Maximum price, inclusive (0 or greater). On
                listing_status='for_rent' this is MONTHLY RENT.
            beds_min: Minimum bedrooms; whole number, 0 or greater.
            beds_max: Maximum bedrooms; whole number, 0 or greater.
            baths_min: Minimum bathrooms, 0 or greater. Half-baths are allowed (1.5).
            baths_max: Maximum bathrooms, 0 or greater. Half-baths are allowed (1.5).
            sqft_min: Minimum living area in square feet; whole number, 0 or greater.
            sqft_max: Maximum living area in square feet; whole number, 0 or greater.
            lot_size_min: Minimum lot size in square feet; whole number, 0 or greater.
            lot_size_max: Maximum lot size in square feet; whole number, 0 or greater.
            year_built_min: Earliest year built; whole number, 0 or greater.
            year_built_max: Latest year built; whole number, 0 or greater.
            max_hoa: Maximum monthly HOA fee in dollars, 0 or greater.
            home_type: Property type filter.
            days_on_zillow: Listed - or, with listing_status='sold', sold - within the
                last N days. Closed enum: an unrecognised value returns the UNFILTERED
                set under a 200.
            keywords: Free-text match against the listing description (1-200
                characters).
            has_pool: Only listings with a pool.
            has_garage: Only listings with a garage.
            has_air_conditioning: Only listings with air conditioning.
            is_waterfront: Only waterfront listings.
            has_basement: Only listings with a basement.
            is_new_construction: Only new-construction listings.
            has_open_house: Only listings with an upcoming open house.
            price_reduced: Only listings whose price was reduced.
            is_3d_tour: Only listings with a 3D tour.

        Returns:
            JSON string with listings in a region: price, beds, baths, living area,
            Zestimate, coordinates, images, days on market.
        """
        client = get_async_client()

        params: dict = {
            "location": location,
            "listing_status": listing_status,
            "page": page,
            "sort": sort,
            "min_price": min_price,
            "max_price": max_price,
            "beds_min": beds_min,
            "beds_max": beds_max,
            "baths_min": baths_min,
            "baths_max": baths_max,
            "sqft_min": sqft_min,
            "sqft_max": sqft_max,
            "lot_size_min": lot_size_min,
            "lot_size_max": lot_size_max,
            "year_built_min": year_built_min,
            "year_built_max": year_built_max,
            "max_hoa": max_hoa,
            "home_type": home_type,
            "days_on_zillow": days_on_zillow,
            "keywords": keywords,
            "has_pool": has_pool,
            "has_garage": has_garage,
            "has_air_conditioning": has_air_conditioning,
            "is_waterfront": is_waterfront,
            "has_basement": has_basement,
            "is_new_construction": is_new_construction,
            "has_open_house": has_open_house,
            "price_reduced": price_reduced,
            "is_3d_tour": is_3d_tour,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.zillow.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_zillow_search,
        description=(
            "Zillow listings in a region: price, beds, baths, living area, Zestimate, "
            "coordinates, images, days on market. A bare ZIP works alone but cannot "
            "be combined with a filter or a sort. Costs 1 credit."
        ),
    )


def create_zillow_property_tool() -> FunctionTool:
    """Create a Scavio Zillow property tool."""

    async def scavio_zillow_property(
        zpid: Annotated[
            str,
            "Zillow property id (e.g. '29414894'), a full /homedetails/ URL, or a "
            "rental building URL (zillow.com/apartments/...). The building form is "
            "required for buildings: they have no zpid a caller can see.",
        ],
    ) -> str:
        """Full Zillow listing: price and price history, Zestimate, tax history, RESO
        facts, rooms, schools, open houses, photos.

        Args:
            zpid: Zillow property id (e.g. '29414894'), a full /homedetails/ URL, or a
                rental building URL (zillow.com/apartments/...). The building form is
                required for buildings: they have no zpid a caller can see.

        Returns:
            JSON string with full listing: price and price history, Zestimate, tax
            history, description, RESO facts, rooms, schools, open houses, photos,
            attribution. Rental buildings return floor plans, amenities and unit counts
            instead.
        """
        client = get_async_client()

        params: dict = {
            "zpid": zpid,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.zillow.property(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_zillow_property,
        description=(
            "Full Zillow listing: price and price history, Zestimate, tax history, "
            "RESO facts, rooms, schools, open houses, photos. Rental buildings return "
            "floor plans instead. Costs 1 credit."
        ),
    )


def create_zillow_agent_reviews_tool() -> FunctionTool:
    """Create a Scavio Zillow agent reviews tool."""

    async def scavio_zillow_agent_reviews(
        screen_name: Annotated[
            str,
            "Zillow agent profile screen name as it appears in "
            "zillow.com/profile/<name>/ (1-200 characters, may contain spaces), or a "
            "full profile URL.",
        ],
    ) -> str:
        """A Zillow AGENT's profile and reviews: rating, bodies with sub-ratings,
        specialties, licenses, service areas, sales counts.

        Args:
            screen_name: Zillow agent profile screen name as it appears in
                zillow.com/profile/<name>/ (1-200 characters, may contain spaces), or a
                full profile URL.

        Returns:
            JSON string with an AGENT's profile and reviews: rating, review count,
            bodies with sub-ratings, specialties, languages, licenses, service areas,
            sales counts.
        """
        client = get_async_client()

        params: dict = {
            "screen_name": screen_name,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.zillow.agent_reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_zillow_agent_reviews,
        description=(
            "A Zillow AGENT's profile and reviews: rating, bodies with sub-ratings, "
            "specialties, licenses, service areas, sales counts. Zillow "
            "server-renders the first five. Costs 1 credit."
        ),
    )
