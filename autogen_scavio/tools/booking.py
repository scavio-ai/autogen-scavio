"""Scavio Booking.com tools for AutoGen.

3 endpoints. 1 credit flat on all three endpoints.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_booking_search_tool() -> FunctionTool:
    """Create a Scavio Booking.com search tool."""

    async def scavio_booking_search(
        destination: Annotated[
            str | None,
            "Destination to search, e.g. 'Paris' (1-200 characters). Required unless "
            "dest_id is given.",
        ] = None,
        dest_id: Annotated[
            str | None,
            "Numeric Booking.com destination id, as an alternative to destination.",
        ] = None,
        dest_type: Annotated[
            Literal[
                "city", "region", "country", "district", "landmark", "airport", "hotel",
            ]
            | None,
            "What dest_id refers to. Requires dest_id and is rejected without it, "
            "because Booking silently ignores a lone dest_type.",
        ] = None,
        page: Annotated[
            int | None,
            "Results page, 1-based. 25 properties per page, 1 credit each.",
        ] = None,
        sort_by: Annotated[
            Literal[
                "popularity", "price_low", "price_high", "stars_high", "stars_low",
                "stars_and_price", "distance", "review_score",
            ]
            | None,
            "Result sort order (default 'popularity').",
        ] = None,
        min_price: Annotated[
            float | None,
            "Minimum price PER NIGHT in `currency`, >= 0. Must not exceed max_price.",
        ] = None,
        max_price: Annotated[
            float | None,
            "Maximum price PER NIGHT in `currency`, >= 0.",
        ] = None,
        stars: Annotated[
            list[int] | None,
            "Star ratings to include, each 1-5, 1-5 values, OR'd together (e.g. [4, "
            "5]).",
        ] = None,
        min_review_score: Annotated[
            Literal["6", "7", "8", "9"] | None,
            "Minimum guest review score. Only '6', '7', '8' and '9' exist upstream; "
            "any other threshold is silently dropped.",
        ] = None,
        property_type: Annotated[
            Literal[
                "apartments", "hostels", "hotels", "motels", "resorts",
                "bed_and_breakfasts", "villas", "campgrounds", "vacation_homes",
                "lodges", "homestays",
            ]
            | int
            | None,
            "Accommodation type by name, or a raw numeric Booking accommodation-type "
            "id (>= 1).",
        ] = None,
        free_cancellation: Annotated[
            bool | None,
            "Only properties offering free cancellation.",
        ] = None,
        no_prepayment: Annotated[
            bool | None,
            "Only properties that take no prepayment.",
        ] = None,
        breakfast_included: Annotated[
            bool | None,
            "Only rates that include breakfast.",
        ] = None,
        checkin: Annotated[
            str | None,
            "Check-in date, YYYY-MM-DD. Must be sent together with checkout: a lone "
            "checkin is ignored and Booking prices a default range of its own.",
        ] = None,
        checkout: Annotated[
            str | None,
            "Check-out date, YYYY-MM-DD. Must be later than checkin and sent together "
            "with it.",
        ] = None,
        adults: Annotated[int | None, "Adult guests, >= 1 (default 2)."] = None,
        children_ages: Annotated[
            list[int] | None,
            "AGES of accompanying children, each 0-17, max 10 entries. Ages, not a "
            "count.",
        ] = None,
        rooms: Annotated[int | None, "Rooms required, >= 1 (default 1)."] = None,
        currency: Annotated[
            str | None,
            "ISO 4217 currency for prices, 3 letters (default 'USD'). Without it "
            "Booking picks a currency itself and identical requests can disagree.",
        ] = None,
    ) -> str:
        """Booking.com properties for a destination and stay: live nightly price, review
        score, star rating, room type, deal badges.

        Parameter rule: destination or dest_id required; dest_type requires dest_id;
        min_price <= max_price; checkin/checkout paired and ordered.

        Pagination: page - 25 properties per page.

        Args:
            destination: Destination to search, e.g. 'Paris' (1-200 characters).
                Required unless dest_id is given.
            dest_id: Numeric Booking.com destination id, as an alternative to
                destination.
            dest_type: What dest_id refers to. Requires dest_id and is rejected without
                it, because Booking silently ignores a lone dest_type.
            page: Results page, 1-based. 25 properties per page, 1 credit each.
            sort_by: Result sort order (default 'popularity').
            min_price: Minimum price PER NIGHT in `currency`, >= 0. Must not exceed
                max_price.
            max_price: Maximum price PER NIGHT in `currency`, >= 0.
            stars: Star ratings to include, each 1-5, 1-5 values, OR'd together (e.g.
                [4, 5]).
            min_review_score: Minimum guest review score. Only '6', '7', '8' and '9'
                exist upstream; any other threshold is silently dropped.
            property_type: Accommodation type by name, or a raw numeric Booking
                accommodation-type id (>= 1).
            free_cancellation: Only properties offering free cancellation.
            no_prepayment: Only properties that take no prepayment.
            breakfast_included: Only rates that include breakfast.
            checkin: Check-in date, YYYY-MM-DD. Must be sent together with checkout: a
                lone checkin is ignored and Booking prices a default range of its own.
            checkout: Check-out date, YYYY-MM-DD. Must be later than checkin and sent
                together with it.
            adults: Adult guests, >= 1 (default 2).
            children_ages: AGES of accompanying children, each 0-17, max 10 entries.
                Ages, not a count.
            rooms: Rooms required, >= 1 (default 1).
            currency: ISO 4217 currency for prices, 3 letters (default 'USD'). Without
                it Booking picks a currency itself and identical requests can disagree.

        Returns:
            JSON string with properties for a destination and stay: live nightly price,
            review score, star rating, location, room type, deal badges.
        """
        client = get_async_client()

        params: dict = {
            "destination": destination,
            "dest_id": dest_id,
            "dest_type": dest_type,
            "page": page,
            "sort_by": sort_by,
            "min_price": min_price,
            "max_price": max_price,
            "stars": stars,
            "min_review_score": min_review_score,
            "property_type": property_type,
            "free_cancellation": free_cancellation,
            "no_prepayment": no_prepayment,
            "breakfast_included": breakfast_included,
            "checkin": checkin,
            "checkout": checkout,
            "adults": adults,
            "children_ages": children_ages,
            "rooms": rooms,
            "currency": currency,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.booking.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_booking_search,
        description=(
            "Booking.com properties for a destination and stay: live nightly price, "
            "review score, star rating, location, room type, deal badges. 25 "
            "properties per page. Provide destination or dest_id. Costs 1 credit."
        ),
    )


def create_booking_hotel_tool() -> FunctionTool:
    """Create a Scavio Booking.com hotel tool."""

    async def scavio_booking_hotel(
        hotel: Annotated[
            str,
            "Booking.com property URL or the bare page slug (1-500 characters); query "
            "params are discarded.",
        ],
        country_code: Annotated[
            str | None,
            "Two-letter country code for the property page (default 'us'). Only "
            "consulted for a bare slug, where a wrong one is a real, BILLED 404.",
        ] = None,
        checkin: Annotated[
            str | None,
            "Check-in date, YYYY-MM-DD. Must be sent together with checkout; omitting "
            "both prices a two-night range Booking chose, echoed back in the "
            "response.",
        ] = None,
        checkout: Annotated[
            str | None,
            "Check-out date, YYYY-MM-DD. Must be later than checkin and sent together "
            "with it.",
        ] = None,
        adults: Annotated[int | None, "Adult guests, >= 1 (default 2)."] = None,
        children_ages: Annotated[
            list[int] | None,
            "AGES of accompanying children, each 0-17, max 10 entries. Ages, not a "
            "count.",
        ] = None,
        rooms: Annotated[int | None, "Rooms required, >= 1 (default 1)."] = None,
        currency: Annotated[
            str | None,
            "ISO 4217 currency for prices, 3 letters (default 'USD'). Without it "
            "Booking picks a currency itself and identical requests can disagree.",
        ] = None,
    ) -> str:
        """One Booking.com property in full: rooms and rate plans, facilities, house
        rules, policies, images, review scores.

        Parameter rule: checkin/checkout paired and ordered.

        Args:
            hotel: Booking.com property URL or the bare page slug (1-500 characters);
                query params are discarded.
            country_code: Two-letter country code for the property page (default 'us').
                Only consulted for a bare slug, where a wrong one is a real, BILLED 404.
            checkin: Check-in date, YYYY-MM-DD. Must be sent together with checkout;
                omitting both prices a two-night range Booking chose, echoed back in the
                response.
            checkout: Check-out date, YYYY-MM-DD. Must be later than checkin and sent
                together with it.
            adults: Adult guests, >= 1 (default 2).
            children_ages: AGES of accompanying children, each 0-17, max 10 entries.
                Ages, not a count.
            rooms: Rooms required, >= 1 (default 1).
            currency: ISO 4217 currency for prices, 3 letters (default 'USD'). Without
                it Booking picks a currency itself and identical requests can disagree.

        Returns:
            JSON string with one property in full: rooms and rate plans, facilities,
            house rules, check-in windows, policies, images, location, review scores -
            priced for the stay asked for.
        """
        client = get_async_client()

        params: dict = {
            "hotel": hotel,
            "country_code": country_code,
            "checkin": checkin,
            "checkout": checkout,
            "adults": adults,
            "children_ages": children_ages,
            "rooms": rooms,
            "currency": currency,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.booking.hotel(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_booking_hotel,
        description=(
            "One Booking.com property in full: rooms and rate plans, facilities, "
            "house rules, check-in windows, policies, images, location and review "
            "scores, priced for the stay asked for. Chaining the `url` a search row "
            "returns is cheaper than a bare slug. Costs 1 credit."
        ),
    )


def create_booking_reviews_tool() -> FunctionTool:
    """Create a Scavio Booking.com reviews tool."""

    async def scavio_booking_reviews(
        hotel: Annotated[
            str,
            "Booking.com property URL or the bare page slug (1-500 characters); query "
            "params are discarded.",
        ],
        country_code: Annotated[
            str | None,
            "Two-letter country code for the property page (default 'us'). Only "
            "consulted for a bare slug, where a wrong one is a real, BILLED 404.",
        ] = None,
        checkin: Annotated[
            str | None,
            "Check-in date, YYYY-MM-DD. Must be sent together with checkout; it "
            "prices the stay the review page is rendered for.",
        ] = None,
        checkout: Annotated[
            str | None,
            "Check-out date, YYYY-MM-DD. Must be later than checkin and sent together "
            "with it.",
        ] = None,
        adults: Annotated[int | None, "Adult guests, >= 1 (default 2)."] = None,
        children_ages: Annotated[
            list[int] | None,
            "AGES of accompanying children, each 0-17, max 10 entries. Ages, not a "
            "count.",
        ] = None,
        rooms: Annotated[int | None, "Rooms required, >= 1 (default 1)."] = None,
        currency: Annotated[
            str | None,
            "ISO 4217 currency for prices, 3 letters (default 'USD').",
        ] = None,
    ) -> str:
        """Booking.com guest reviews with the score breakdown by category and Booking's
        own praise/complaint summary.

        Parameter rule: checkin/checkout paired and ordered.

        Args:
            hotel: Booking.com property URL or the bare page slug (1-500 characters);
                query params are discarded.
            country_code: Two-letter country code for the property page (default 'us').
                Only consulted for a bare slug, where a wrong one is a real, BILLED 404.
            checkin: Check-in date, YYYY-MM-DD. Must be sent together with checkout; it
                prices the stay the review page is rendered for.
            checkout: Check-out date, YYYY-MM-DD. Must be later than checkin and sent
                together with it.
            adults: Adult guests, >= 1 (default 2).
            children_ages: AGES of accompanying children, each 0-17, max 10 entries.
                Ages, not a count.
            rooms: Rooms required, >= 1 (default 1).
            currency: ISO 4217 currency for prices, 3 letters (default 'USD').

        Returns:
            JSON string with guest reviews with the score breakdown by category and
            Booking's own praise/complaint summary. total_count is the whole history;
            count is this response.
        """
        client = get_async_client()

        params: dict = {
            "hotel": hotel,
            "country_code": country_code,
            "checkin": checkin,
            "checkout": checkout,
            "adults": adults,
            "children_ages": children_ages,
            "rooms": rooms,
            "currency": currency,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.booking.reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_booking_reviews,
        description=(
            "Booking.com guest reviews for a property with the score breakdown by "
            "category and Booking's own praise/complaint summary. No page param: "
            "total_count is the whole review history, count is what this response "
            "holds. Costs 1 credit."
        ),
    )
