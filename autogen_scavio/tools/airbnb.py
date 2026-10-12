"""Scavio Airbnb tools for AutoGen.

3 endpoints. 1 credit flat on all three endpoints.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_airbnb_search_tool() -> FunctionTool:
    """Create a Scavio Airbnb search tool."""

    async def scavio_airbnb_search(
        location: Annotated[
            str,
            "City, region, ZIP, or a pasted airbnb.com/s/ URL (1-200 characters). An "
            "unresolvable location is a 404.",
        ],
        check_in: Annotated[
            str | None,
            "Check-in date, YYYY-MM-DD. Must be sent with check_out; omitting both "
            "defaults to +30 days and flags dates_are_defaulted in the response.",
        ] = None,
        check_out: Annotated[
            str | None,
            "Check-out date, YYYY-MM-DD. Must be later than check_in; defaults to "
            "check_in plus 5 nights when omitted.",
        ] = None,
        adults: Annotated[int | None, "Adult guests, >= 1."] = None,
        children: Annotated[int | None, "Children aged 2-12, >= 0."] = None,
        infants: Annotated[int | None, "Infants under 2, >= 0."] = None,
        pets: Annotated[int | None, "Pets, >= 0."] = None,
        min_price: Annotated[
            float | None,
            "Minimum price for the WHOLE STAY in `currency`, not per night, >= 0. "
            "Must not exceed max_price.",
        ] = None,
        max_price: Annotated[
            float | None,
            "Maximum price for the WHOLE STAY in `currency`, not per night, >= 0.",
        ] = None,
        room_type: Annotated[
            Literal["entire_home", "private_room", "shared_room", "hotel_room"] | None,
            "Room type. Validated before the scrape, because an unrecognised value "
            "returns the UNFILTERED set under a 200.",
        ] = None,
        min_bedrooms: Annotated[int | None, "Minimum bedrooms, >= 0."] = None,
        min_beds: Annotated[int | None, "Minimum beds, >= 0."] = None,
        min_bathrooms: Annotated[int | None, "Minimum bathrooms, >= 0."] = None,
        superhost: Annotated[bool | None, "Superhost listings only."] = None,
        instant_book: Annotated[bool | None, "Instant Book listings only."] = None,
        guest_favorite: Annotated[bool | None, "Guest Favorite listings only."] = None,
        free_cancellation: Annotated[
            bool | None,
            "Listings with free cancellation only.",
        ] = None,
        amenities: Annotated[
            str | None,
            "Comma-separated amenities (1-200 characters): wifi, air_conditioning, "
            "pool, kitchen, free_parking, washer, self_check_in, tv, or raw numeric "
            "Airbnb amenity ids. An unrecognised NAME is rejected before the scrape.",
        ] = None,
        currency: Annotated[
            str | None,
            "ISO 4217 currency for prices, 3 letters (default 'USD'). Without it "
            "Airbnb picks a currency itself and identical requests can disagree.",
        ] = None,
        page: Annotated[
            int | None,
            "Results page, 1-based. 18 listings per page. Cannot be combined with "
            "cursor.",
        ] = None,
        cursor: Annotated[
            str | None,
            "next_cursor from a previous response (1-500 characters); wins over page, "
            "so sending both is rejected.",
        ] = None,
    ) -> str:
        """Airbnb stays: stay-total and per-night price with the full discount ledger,
        rating, bedrooms/beds/baths, coordinates, badges, images.

        Parameter rule: dates paired and ordered; min_price <= max_price; page XOR
        cursor.

        Pagination: page XOR cursor - `cursor` WINS over `page`, so sending both is
        REJECTED. 18 listings per page.

        Args:
            location: City, region, ZIP, or a pasted airbnb.com/s/ URL (1-200
                characters). An unresolvable location is a 404.
            check_in: Check-in date, YYYY-MM-DD. Must be sent with check_out; omitting
                both defaults to +30 days and flags dates_are_defaulted in the response.
            check_out: Check-out date, YYYY-MM-DD. Must be later than check_in; defaults
                to check_in plus 5 nights when omitted.
            adults: Adult guests, >= 1.
            children: Children aged 2-12, >= 0.
            infants: Infants under 2, >= 0.
            pets: Pets, >= 0.
            min_price: Minimum price for the WHOLE STAY in `currency`, not per night, >=
                0. Must not exceed max_price.
            max_price: Maximum price for the WHOLE STAY in `currency`, not per night, >=
                0.
            room_type: Room type. Validated before the scrape, because an unrecognised
                value returns the UNFILTERED set under a 200.
            min_bedrooms: Minimum bedrooms, >= 0.
            min_beds: Minimum beds, >= 0.
            min_bathrooms: Minimum bathrooms, >= 0.
            superhost: Superhost listings only.
            instant_book: Instant Book listings only.
            guest_favorite: Guest Favorite listings only.
            free_cancellation: Listings with free cancellation only.
            amenities: Comma-separated amenities (1-200 characters): wifi,
                air_conditioning, pool, kitchen, free_parking, washer, self_check_in,
                tv, or raw numeric Airbnb amenity ids. An unrecognised NAME is rejected
                before the scrape.
            currency: ISO 4217 currency for prices, 3 letters (default 'USD'). Without
                it Airbnb picks a currency itself and identical requests can disagree.
            page: Results page, 1-based. 18 listings per page. Cannot be combined with
                cursor.
            cursor: next_cursor from a previous response (1-500 characters); wins over
                page, so sending both is rejected.

        Returns:
            JSON string with stays: stay-total and per-night price with the full
            discount ledger, rating and review count, bedrooms/beds/baths, coordinates,
            badges, images, dates_are_defaulted.
        """
        client = get_async_client()

        params: dict = {
            "location": location,
            "check_in": check_in,
            "check_out": check_out,
            "adults": adults,
            "children": children,
            "infants": infants,
            "pets": pets,
            "min_price": min_price,
            "max_price": max_price,
            "room_type": room_type,
            "min_bedrooms": min_bedrooms,
            "min_beds": min_beds,
            "min_bathrooms": min_bathrooms,
            "superhost": superhost,
            "instant_book": instant_book,
            "guest_favorite": guest_favorite,
            "free_cancellation": free_cancellation,
            "amenities": amenities,
            "currency": currency,
            "page": page,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.airbnb.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_airbnb_search,
        description=(
            "Airbnb stays: stay-total and per-night price with the full discount "
            "ledger, rating and review count, bedrooms/beds/baths, coordinates, "
            "badges, images, dates_are_defaulted. 18 listings per page; page and "
            "cursor are mutually exclusive. Costs 1 credit."
        ),
    )


def create_airbnb_listing_tool() -> FunctionTool:
    """Create a Scavio Airbnb listing tool."""

    async def scavio_airbnb_listing(
        listing_id: Annotated[
            str,
            "Airbnb listing id or a full /rooms/ URL (1-500 characters); query params "
            "are discarded, since they carry someone else's dates.",
        ],
        check_in: Annotated[
            str | None,
            "Check-in date, YYYY-MM-DD. Must be sent with check_out. Does not produce "
            "a price: the room page has no nightly rate.",
        ] = None,
        check_out: Annotated[
            str | None,
            "Check-out date, YYYY-MM-DD. Must be later than check_in and sent "
            "together with it.",
        ] = None,
        adults: Annotated[int | None, "Adult guests, >= 1."] = None,
        children: Annotated[int | None, "Children aged 2-12, >= 0."] = None,
        infants: Annotated[int | None, "Infants under 2, >= 0."] = None,
        pets: Annotated[int | None, "Pets, >= 0."] = None,
        currency: Annotated[
            str | None,
            "ISO 4217 currency, 3 letters (default 'USD').",
        ] = None,
    ) -> str:
        """One Airbnb listing in full: description, capacity, the complete grouped
        amenity list, host profile, house rules, photo tour, and the RATING BREAKDOWN.

        Parameter rule: dates paired and ordered.

        Args:
            listing_id: Airbnb listing id or a full /rooms/ URL (1-500 characters);
                query params are discarded, since they carry someone else's dates.
            check_in: Check-in date, YYYY-MM-DD. Must be sent with check_out. Does not
                produce a price: the room page has no nightly rate.
            check_out: Check-out date, YYYY-MM-DD. Must be later than check_in and sent
                together with it.
            adults: Adult guests, >= 1.
            children: Children aged 2-12, >= 0.
            infants: Infants under 2, >= 0.
            pets: Pets, >= 0.
            currency: ISO 4217 currency, 3 letters (default 'USD').

        Returns:
            JSON string with one listing in full: description, property/room type,
            capacity and room counts, the complete grouped amenity list (including the
            ones the place does NOT have), host profile and stats, house rules with
            parsed check-in/out times, cancellation policy, sleeping arrangements, photo
            tour, every image, and the RATING BREAKDOWN. NO NIGHTLY PRICE.
        """
        client = get_async_client()

        params: dict = {
            "listing_id": listing_id,
            "check_in": check_in,
            "check_out": check_out,
            "adults": adults,
            "children": children,
            "infants": infants,
            "pets": pets,
            "currency": currency,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.airbnb.listing(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_airbnb_listing,
        description=(
            "One Airbnb listing in full: description, property/room type, capacity "
            "and room counts, the complete grouped amenity list (including what the "
            "place does NOT have), host profile and stats, house rules, cancellation "
            "policy, sleeping arrangements, photo tour and the RATING BREAKDOWN. "
            "Carries NO nightly price - prices are search-only. Costs 1 credit."
        ),
    )


def create_airbnb_reviews_tool() -> FunctionTool:
    """Create a Scavio Airbnb reviews tool."""

    async def scavio_airbnb_reviews(
        listing_id: Annotated[
            str,
            "Airbnb listing id or a full /rooms/ URL (1-500 characters).",
        ],
        currency: Annotated[
            str | None,
            "ISO 4217 currency, 3 letters (default 'USD').",
        ] = None,
        limit: Annotated[
            int | None,
            "Reviews to return, 1-50 (default 30). Upstream returns a fixed 7 when no "
            "explicit limit is sent.",
        ] = None,
        offset: Annotated[
            int | None,
            "Reviews to skip before this page, >= 0 (default 0).",
        ] = None,
    ) -> str:
        """Airbnb review BODIES with per-review rating, date, and reviewer
        name/photo/location.

        Pagination: limit + offset.

        Args:
            listing_id: Airbnb listing id or a full /rooms/ URL (1-500 characters).
            currency: ISO 4217 currency, 3 letters (default 'USD').
            limit: Reviews to return, 1-50 (default 30). Upstream returns a fixed 7 when
                no explicit limit is sent.
            offset: Reviews to skip before this page, >= 0 (default 0).

        Returns:
            JSON string with review BODIES with per-review rating, date, and reviewer
            name/photo/location. `count` is the listing's TOTAL review count, `returned`
            is how many this page holds.
        """
        client = get_async_client()

        params: dict = {
            "listing_id": listing_id,
            "currency": currency,
            "limit": limit,
            "offset": offset,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.airbnb.reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_airbnb_reviews,
        description=(
            "Airbnb review BODIES with per-review rating, date and reviewer "
            "name/photo/location, limit/offset paged at up to 50 per call. `count` is "
            "the listing's TOTAL review count, `returned` is how many this page "
            "holds. The rating breakdown lives on listing(), not here. Costs 1 "
            "credit."
        ),
    )
