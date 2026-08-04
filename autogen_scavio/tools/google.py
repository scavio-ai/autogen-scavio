"""Scavio Google tools for AutoGen.

Every tool here calls the v2 Google family (/api/v2/google/...), which costs
1 credit per call. Google v1 was retired on 2026-08-04 and answers 410, so its
params (country_code, language, page) are gone: v2 takes gl, hl and start, and
start is a zero-based result OFFSET, not a page number (0 = page 1, 10 = page
2). Google responses are FLAT -- the payload sits at the top level, there is no
data wrapper.
"""

from __future__ import annotations

from typing import Any

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list

# Result blocks the max_results cap applies to. All are v2 response keys.
_RESULT_LISTS = ("organic_results", "local_results", "top_stories", "video_results")


def _drop_none(params: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in params.items() if v is not None}


def _cap(raw: dict[str, Any], keys: tuple[str, ...], max_results: int) -> None:
    """Truncate top-level list blocks of a flat Google response in place."""
    for key in keys:
        truncate_list(raw, [key], max_results)


def create_web_search_tool(
    max_results: int = 5,
    include_knowledge_graph: bool = True,
    include_questions: bool = True,
    include_related: bool = False,
    include_ai_overview: bool = True,
    include_local_results: bool = False,
    include_top_stories: bool = False,
    include_top_ads: bool = False,
    include_bottom_ads: bool = False,
) -> FunctionTool:
    """Create a web search tool with the given configuration."""

    async def scavio_web_search(
        query: str,
        gl: str | None = None,
        hl: str | None = None,
        start: int | None = None,
        google_domain: str | None = None,
        device: str | None = None,
        location: str | None = None,
        uule: str | None = None,
        lr: str | None = None,
        cr: str | None = None,
        safe: str | None = None,
        nfpr: bool | None = None,
        filter: str | None = None,
        time_period: str | None = None,
    ) -> str:
        """Search Google using the Scavio API.

        Args:
            query: The search query string.
            gl: Country of the search (ISO 3166-1 alpha-2), e.g. "us".
            hl: UI language (ISO 639-1), e.g. "en".
            start: Zero-based result offset, NOT a page number. 0 is page 1,
                10 is page 2, 20 is page 3, up to 990.
            google_domain: Google domain to query, e.g. "google.co.uk".
            device: Device type, "desktop" or "mobile".
            location: Canonical location name, converted to a UULE upstream.
            uule: Pre-encoded UULE; takes priority over location.
            lr: Language restriction, e.g. "lang_en".
            cr: Country restriction, e.g. "countryUS".
            safe: Set to "active" for SafeSearch. That is the only value.
            nfpr: Disable spelling correction / auto-fixes when True.
            filter: "0" disables the similar/omitted-results filter, "1"
                keeps it. String literals, not numbers.
            time_period: Recency filter, one of "last_hour", "last_day",
                "last_week", "last_month", "last_year".

        Returns:
            JSON string with a flat response: organic_results (title, link,
            snippet), the knowledge graph, related questions and the AI
            Overview when available. There is no data wrapper.
        """
        client = get_async_client()

        params = _drop_none(
            {
                "query": query,
                "gl": gl,
                "hl": hl,
                "start": start,
                "google_domain": google_domain,
                "device": device,
                "location": location,
                "uule": uule,
                "lr": lr,
                "cr": cr,
                "safe": safe,
                "nfpr": nfpr,
                "filter": filter,
                "time_period": time_period,
            }
        )
        if not include_ai_overview:
            # Skip the server-side follow-up call that resolves a deferred AI
            # Overview when the block is going to be dropped anyway.
            params["resolve_ai_overview"] = False

        raw = await client.google.search(**params)

        _cap(raw, _RESULT_LISTS, max_results)

        # Pop disabled include_* sections
        if not include_knowledge_graph:
            raw.pop("knowledge_graph", None)
        if not include_questions:
            raw.pop("related_questions", None)
        if not include_related:
            raw.pop("related_searches", None)
        if not include_ai_overview:
            raw.pop("ai_overview", None)
        if not include_local_results:
            raw.pop("local_results", None)
            raw.pop("local_map", None)
        if not include_top_stories:
            raw.pop("top_stories", None)
        if not include_top_ads:
            raw.pop("top_ads", None)
        if not include_bottom_ads:
            raw.pop("bottom_ads", None)

        return format_response(raw)

    return FunctionTool(
        scavio_web_search,
        description=(
            "Search Google via the Scavio API (1 credit). Returns organic "
            "results with titles, links, and snippets, plus the knowledge "
            "graph, related questions, and the AI Overview when available. "
            "Page with start, a zero-based offset: 0, 10, 20."
        ),
    )


def create_google_ai_mode_tool(max_results: int = 5) -> FunctionTool:
    """Create a Google AI Mode tool with the given configuration."""

    async def scavio_google_ai_mode(
        query: str,
        gl: str | None = None,
        hl: str | None = None,
        google_domain: str | None = None,
        device: str | None = None,
        location: str | None = None,
        uule: str | None = None,
        safe: str | None = None,
    ) -> str:
        """Run a query through Google AI Mode and get the generated answer.

        Args:
            query: The question to answer.
            gl: Country of the search (ISO 3166-1 alpha-2), e.g. "us".
            hl: UI language (ISO 639-1), e.g. "en".
            google_domain: Google domain to query, e.g. "google.co.uk".
            device: Device type, "desktop" or "mobile".
            location: Canonical location name, converted to a UULE upstream.
            uule: Pre-encoded UULE; takes priority over location.
            safe: Set to "active" for SafeSearch. That is the only value.

        Returns:
            JSON string with a flat response: text_blocks (the answer),
            references (cited sources) and shopping_results. There is no
            start / pagination on this endpoint.
        """
        client = get_async_client()

        params = _drop_none(
            {
                "query": query,
                "gl": gl,
                "hl": hl,
                "google_domain": google_domain,
                "device": device,
                "location": location,
                "uule": uule,
                "safe": safe,
            }
        )

        raw = await client.google.ai_mode(**params)

        _cap(raw, ("references", "shopping_results"), max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_google_ai_mode,
        description=(
            "Ask Google AI Mode a question (1 credit). Returns the generated "
            "answer as text_blocks plus the references it cites."
        ),
    )


def create_google_maps_search_tool(max_results: int = 5) -> FunctionTool:
    """Create a Google Maps search tool with the given configuration."""

    async def scavio_google_maps_search(
        query: str,
        gl: str | None = None,
        hl: str | None = None,
        ll: str | None = None,
        start: int | None = None,
        google_domain: str | None = None,
    ) -> str:
        """Search Google Maps for places and local businesses.

        Args:
            query: What to look for, e.g. "coffee shops in Brooklyn".
            gl: Country of the search (ISO 3166-1 alpha-2), e.g. "us".
            hl: UI language (ISO 639-1), e.g. "en".
            ll: Map center as "@lat,lng,zoomz", e.g. "@40.7128,-74.0060,13z".
                Maps localizes by map center, not by gl. When omitted, a
                centroid is derived from gl.
            start: Zero-based result offset; must be a multiple of 20.
            google_domain: Google domain to query, e.g. "google.co.uk".

        Returns:
            JSON string with a flat response: local_results with names,
            addresses, ratings, phone numbers, place_id and data_id.
        """
        client = get_async_client()

        params = _drop_none(
            {
                "query": query,
                "gl": gl,
                "hl": hl,
                "ll": ll,
                "start": start,
                "google_domain": google_domain,
            }
        )

        raw = await client.google.maps_search(**params)

        _cap(raw, ("local_results",), max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_google_maps_search,
        description=(
            "Search Google Maps for local businesses and places (1 credit). "
            "Returns local_results with addresses, ratings, phone numbers and "
            "the place_id / data_id used by the place and reviews tools."
        ),
    )


def create_google_maps_place_tool() -> FunctionTool:
    """Create a Google Maps place details tool."""

    async def scavio_google_maps_place(
        place_id: str | None = None,
        data_cid: str | None = None,
    ) -> str:
        """Fetch full details for one Google Maps place.

        Args:
            place_id: Google place id ("ChIJ..."). Provide this or data_cid.
            data_cid: Numeric Google CID. Provide this or place_id.

        Returns:
            JSON string with a flat response: place_results with the address,
            hours, phone, website, rating and review count.
        """
        client = get_async_client()

        params = _drop_none({"place_id": place_id, "data_cid": data_cid})

        raw = await client.google.maps_place(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_google_maps_place,
        description=(
            "Fetch full details for one Google Maps place by place_id or "
            "data_cid (1 credit)."
        ),
    )


def create_google_maps_reviews_tool(max_results: int = 10) -> FunctionTool:
    """Create a Google Maps reviews tool with the given configuration."""

    async def scavio_google_maps_reviews(
        data_id: str | None = None,
        place_id: str | None = None,
        num: int | None = None,
        next_page_token: str | None = None,
        sort_by: str | None = None,
        gl: str | None = None,
        hl: str | None = None,
        google_domain: str | None = None,
    ) -> str:
        """Fetch reviews for a Google Maps place.

        Args:
            data_id: Place data id, form "0xHEX:0xHEX". Provide this or place_id.
            place_id: Google place id ("ChIJ..."). Provide this or data_id.
            num: Reviews per call, 1 to 20.
            next_page_token: Pagination cursor from a prior response.
            sort_by: Sort order, one of "relevance", "newest",
                "highest_rating", "lowest_rating".
            gl: Country of the search (ISO 3166-1 alpha-2), e.g. "us".
            hl: UI language (ISO 639-1), e.g. "en".
            google_domain: Google domain to query, e.g. "google.co.uk".

        Returns:
            JSON string with a flat response: reviews with rating, text,
            author and date, plus place_info, topics and pagination.
        """
        client = get_async_client()

        params = _drop_none(
            {
                "data_id": data_id,
                "place_id": place_id,
                "num": num,
                "next_page_token": next_page_token,
                "sort_by": sort_by,
                "gl": gl,
                "hl": hl,
                "google_domain": google_domain,
            }
        )

        raw = await client.google.maps_reviews(**params)

        _cap(raw, ("reviews",), max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_google_maps_reviews,
        description=(
            "Fetch Google Maps reviews for a place by data_id or place_id "
            "(1 credit). Up to 20 per call; page with next_page_token."
        ),
    )


def create_google_shopping_tool(max_results: int = 5) -> FunctionTool:
    """Create a Google Shopping search tool with the given configuration."""

    async def scavio_google_shopping(
        query: str,
        gl: str | None = None,
        hl: str | None = None,
        start: int | None = None,
        device: str | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        sort_by: int | None = None,
        free_shipping: bool | None = None,
        on_sale: bool | None = None,
        shoprs: str | None = None,
        google_domain: str | None = None,
        location: str | None = None,
        uule: str | None = None,
    ) -> str:
        """Search Google Shopping for products and prices.

        Args:
            query: The product search query.
            gl: Country of the search (ISO 3166-1 alpha-2), e.g. "us".
            hl: UI language (ISO 639-1), e.g. "en".
            start: Zero-based result offset; follow pagination.next.
            device: Device type, "desktop" or "mobile".
            min_price: Minimum price filter.
            max_price: Maximum price filter.
            sort_by: 0 relevance, 1 price ascending, 2 price descending.
                A number here; the product tool uses a string instead.
            free_shipping: Only products with free shipping.
            on_sale: Only products on sale.
            shoprs: Opaque filter token lifted from filters in a prior response.
            google_domain: Google domain to query, e.g. "google.co.uk".
            location: Canonical location name, converted to a UULE upstream.
            uule: Pre-encoded UULE; takes priority over location.

        Returns:
            JSON string with a flat response: shopping_results with titles,
            prices, sellers and the catalog_id used by the product tool.
        """
        client = get_async_client()

        params = _drop_none(
            {
                "query": query,
                "gl": gl,
                "hl": hl,
                "start": start,
                "device": device,
                "min_price": min_price,
                "max_price": max_price,
                "sort_by": sort_by,
                "free_shipping": free_shipping,
                "on_sale": on_sale,
                "shoprs": shoprs,
                "google_domain": google_domain,
                "location": location,
                "uule": uule,
            }
        )

        raw = await client.google.shopping(**params)

        _cap(raw, ("shopping_results",), max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_google_shopping,
        description=(
            "Search Google Shopping for products and prices (1 credit). "
            "Returns shopping_results with prices, sellers and catalog ids."
        ),
    )


def create_google_shopping_product_tool() -> FunctionTool:
    """Create a Google Shopping product details tool."""

    async def scavio_google_shopping_product(
        catalog_id: str | None = None,
        query: str | None = None,
        immersive_product_page_token: str | None = None,
        page_token: str | None = None,
        product_id: str | None = None,
        device: str | None = None,
        sort_by: str | None = None,
        load_all_stores: bool | None = None,
        more_stores: bool | None = None,
        gl: str | None = None,
        hl: str | None = None,
        google_domain: str | None = None,
        location: str | None = None,
        uule: str | None = None,
    ) -> str:
        """Fetch a Google Shopping product page with its seller offers.

        Args:
            catalog_id: Durable product catalog id. Requires query as well.
            query: The search query the product came from. Mandatory whenever
                catalog_id is set.
            immersive_product_page_token: Token from a shopping result.
            page_token: Alias of immersive_product_page_token.
            product_id: Product id, an alternative driver.
            device: Device type, "desktop", "mobile" or "tablet". This is the
                only Google endpoint that accepts "tablet".
            sort_by: Seller sort, one of "base_price", "total_price",
                "promotion", "seller_rating". A string here; the shopping
                search tool uses a number instead.
            load_all_stores: Load every seller rather than the first page.
            more_stores: Request the extended seller list.
            gl: Country of the search (ISO 3166-1 alpha-2), e.g. "us".
            hl: UI language (ISO 639-1), e.g. "en".
            google_domain: Google domain to query, e.g. "google.co.uk".
            location: Canonical location name, converted to a UULE upstream.
            uule: Pre-encoded UULE; takes priority over location.

        Returns:
            JSON string with a flat response: product_results with specs,
            ratings and product_results.stores, the seller list.
        """
        client = get_async_client()

        params = _drop_none(
            {
                "catalog_id": catalog_id,
                "query": query,
                "immersive_product_page_token": immersive_product_page_token,
                "page_token": page_token,
                "product_id": product_id,
                "device": device,
                "sort_by": sort_by,
                "load_all_stores": load_all_stores,
                "more_stores": more_stores,
                "gl": gl,
                "hl": hl,
                "google_domain": google_domain,
                "location": location,
                "uule": uule,
            }
        )

        raw = await client.google.shopping_product(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_google_shopping_product,
        description=(
            "Fetch a Google Shopping product with its seller offers "
            "(1 credit). Needs one of catalog_id (with query), "
            "immersive_product_page_token, page_token or product_id."
        ),
    )


def create_google_shopping_stores_tool(max_results: int = 10) -> FunctionTool:
    """Create a Google Shopping product stores tool."""

    async def scavio_google_shopping_stores(
        catalog_id: str,
        next_page_token: str,
    ) -> str:
        """Fetch the next page of sellers for a Google Shopping product.

        Args:
            catalog_id: The same catalog_id used on the product call.
            next_page_token: Continuation cursor from a prior response.

        Returns:
            JSON string with a flat response: product_results.stores, more
            sellers for the product.
        """
        client = get_async_client()

        raw = await client.google.shopping_stores(
            catalog_id=catalog_id,
            next_page_token=next_page_token,
        )

        truncate_list(raw, ["product_results", "stores"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_google_shopping_stores,
        description=(
            "Page through the sellers of a Google Shopping product "
            "(1 credit). The pagination leg of the shopping product tool."
        ),
    )


def create_google_flights_tool(max_results: int = 5) -> FunctionTool:
    """Create a Google Flights tool with the given configuration."""

    async def scavio_google_flights(
        departure_id: str,
        arrival_id: str,
        outbound_date: str,
        type: int | None = None,
        return_date: str | None = None,
        adults: int | None = None,
        children: int | None = None,
        infants_in_seat: int | None = None,
        infants_on_lap: int | None = None,
        travel_class: int | None = None,
        stops: int | None = None,
        sort_by: int | None = None,
        include_airlines: str | None = None,
        exclude_airlines: str | None = None,
        gl: str | None = None,
        hl: str | None = None,
        currency: str | None = None,
    ) -> str:
        """Search Google Flights for itineraries and prices.

        Args:
            departure_id: Origin IATA code, e.g. "JFK". Comma-separated
                multiples are allowed.
            arrival_id: Destination IATA code. Comma-separated multiples are
                allowed.
            outbound_date: Outbound date as "YYYY-MM-DD".
            type: 1 round trip, 2 one way, 3 multi-city.
            return_date: Return date as "YYYY-MM-DD". Required when type is 1.
            adults: Number of adults, 1 to 9.
            children: Number of children, 0 to 9.
            infants_in_seat: Infants in their own seat, 0 to 4.
            infants_on_lap: Infants on a lap, 0 to 4.
            travel_class: 1 economy, 2 premium, 3 business, 4 first.
            stops: 0 any, 1 nonstop, 2 one stop or fewer, 3 two stops or fewer.
            sort_by: 1 top, 2 price, 3 departure, 4 arrival, 5 duration,
                6 emissions.
            include_airlines: Comma-separated airline or alliance codes.
            exclude_airlines: Comma-separated airline or alliance codes.
            gl: Country of the search (ISO 3166-1 alpha-2), e.g. "us".
            hl: UI language (ISO 639-1), e.g. "en".
            currency: Currency code (ISO 4217), e.g. "USD".

        Returns:
            JSON string with a flat response: best_flights and other_flights
            with legs, durations, airlines and prices.
        """
        client = get_async_client()

        params = _drop_none(
            {
                "departure_id": departure_id,
                "arrival_id": arrival_id,
                "outbound_date": outbound_date,
                "type": type,
                "return_date": return_date,
                "adults": adults,
                "children": children,
                "infants_in_seat": infants_in_seat,
                "infants_on_lap": infants_on_lap,
                "travel_class": travel_class,
                "stops": stops,
                "sort_by": sort_by,
                "include_airlines": include_airlines,
                "exclude_airlines": exclude_airlines,
                "gl": gl,
                "hl": hl,
                "currency": currency,
            }
        )

        raw = await client.google.flights(**params)

        _cap(raw, ("best_flights", "other_flights"), max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_google_flights,
        description=(
            "Search Google Flights for itineraries and prices (1 credit). "
            "Returns best_flights and other_flights."
        ),
    )


def create_google_hotels_tool(max_results: int = 5) -> FunctionTool:
    """Create a Google Hotels tool with the given configuration."""

    async def scavio_google_hotels(
        query: str,
        check_in_date: str,
        check_out_date: str,
        gl: str | None = None,
        hl: str | None = None,
        currency: str | None = None,
        sort_by: int | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        rating: int | None = None,
        hotel_class: str | None = None,
        amenities: str | None = None,
        property_types: str | None = None,
        free_cancellation: bool | None = None,
        eco_certified: bool | None = None,
        special_offers: bool | None = None,
        next_page_token: str | None = None,
        limit: int | None = None,
    ) -> str:
        """Search Google Hotels for properties, rates and availability.

        Args:
            query: Search query; use the "<City> hotels" form.
            check_in_date: Check-in date as "YYYY-MM-DD".
            check_out_date: Check-out date as "YYYY-MM-DD".
            gl: Country of the search (ISO 3166-1 alpha-2), e.g. "us".
            hl: UI language (ISO 639-1), e.g. "en".
            currency: Currency code (ISO 4217), e.g. "USD".
            sort_by: 3 lowest price, 8 highest rating, 13 most reviewed.
            min_price: Minimum nightly price.
            max_price: Maximum nightly price.
            rating: 7 for 3.5+, 8 for 4.0+, 9 for 4.5+.
            hotel_class: Comma-separated star ratings 2 to 5, e.g. "4,5".
            amenities: Comma-separated amenity ids.
            property_types: Comma-separated property type ids, "12" is
                vacation rentals.
            free_cancellation: Only properties with free cancellation.
            eco_certified: Only eco-certified properties.
            special_offers: Only properties with special offers.
            next_page_token: Pagination cursor from a prior response.
            limit: Properties per call, 1 to 20.

        Returns:
            JSON string with a flat response: properties with rates, ratings
            and a detail_token for the hotel detail tool.
        """
        client = get_async_client()

        params = _drop_none(
            {
                "query": query,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "gl": gl,
                "hl": hl,
                "currency": currency,
                "sort_by": sort_by,
                "min_price": min_price,
                "max_price": max_price,
                "rating": rating,
                "hotel_class": hotel_class,
                "amenities": amenities,
                "property_types": property_types,
                "free_cancellation": free_cancellation,
                "eco_certified": eco_certified,
                "special_offers": special_offers,
                "next_page_token": next_page_token,
                "limit": limit,
            }
        )

        raw = await client.google.hotels(**params)

        _cap(raw, ("properties",), max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_google_hotels,
        description=(
            "Search Google Hotels for properties and nightly rates "
            "(1 credit). Each property carries a detail_token for the hotel "
            "detail tool."
        ),
    )


def create_google_hotels_detail_tool() -> FunctionTool:
    """Create a Google Hotels detail tool."""

    async def scavio_google_hotels_detail(
        detail_token: str,
        check_in_date: str,
        check_out_date: str,
        gl: str | None = None,
        hl: str | None = None,
        currency: str | None = None,
    ) -> str:
        """Fetch one hotel with its booking sources.

        Args:
            detail_token: detail_token from a property in the hotels tool.
            check_in_date: Check-in date as "YYYY-MM-DD". Must be re-sent, the
                token alone is not enough.
            check_out_date: Check-out date as "YYYY-MM-DD".
            gl: Country of the search (ISO 3166-1 alpha-2), e.g. "us".
            hl: UI language (ISO 639-1), e.g. "en".
            currency: Currency code (ISO 4217), e.g. "USD".

        Returns:
            JSON string with a flat response: property with amenities, images
            and property.booking_sources, the per-site prices.
        """
        client = get_async_client()

        params = _drop_none(
            {
                "detail_token": detail_token,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "gl": gl,
                "hl": hl,
                "currency": currency,
            }
        )

        raw = await client.google.hotels_detail(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_google_hotels_detail,
        description=(
            "Fetch one hotel and its booking sources by detail_token "
            "(1 credit). Re-send both dates with the token."
        ),
    )


def create_google_news_tool(max_results: int = 10) -> FunctionTool:
    """Create a Google News tool with the given configuration."""

    async def scavio_google_news(
        query: str | None = None,
        topic_token: str | None = None,
        section_token: str | None = None,
        story_token: str | None = None,
        publication_token: str | None = None,
        kgmid: str | None = None,
        gl: str | None = None,
        hl: str | None = None,
        google_domain: str | None = None,
        so: int | None = None,
    ) -> str:
        """Fetch Google News results.

        Exactly one of query, topic_token, section_token, story_token,
        publication_token or kgmid must be set. Two or more is an error, not a
        precedence rule.

        Args:
            query: News search query.
            topic_token: Token for a news topic from a prior response.
            section_token: Token for a topic section.
            story_token: Token for a story's full coverage.
            publication_token: Token for a publisher's feed.
            kgmid: Knowledge Graph entity id, e.g. "/m/02_286".
            gl: Country of the search (ISO 3166-1 alpha-2), e.g. "us".
            hl: UI language (ISO 639-1), e.g. "en".
            google_domain: Google domain to query, e.g. "google.co.uk".
            so: Sort order, 0 relevance or 1 date. Only valid with query or
                kgmid.

        Returns:
            JSON string with a flat response: news_results with headlines,
            sources, links and timestamps.
        """
        client = get_async_client()

        params = _drop_none(
            {
                "query": query,
                "topic_token": topic_token,
                "section_token": section_token,
                "story_token": story_token,
                "publication_token": publication_token,
                "kgmid": kgmid,
                "gl": gl,
                "hl": hl,
                "google_domain": google_domain,
                "so": so,
            }
        )

        raw = await client.google.news(**params)

        _cap(raw, ("news_results",), max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_google_news,
        description=(
            "Fetch Google News headlines (1 credit). Set exactly one driver: "
            "query, topic_token, section_token, story_token, "
            "publication_token or kgmid."
        ),
    )


def create_google_trends_tool() -> FunctionTool:
    """Create a Google Trends tool."""

    async def scavio_google_trends(
        query: str,
        geo: str | None = None,
        hl: str | None = None,
        date: str | None = None,
        tz: str | None = None,
        data_type: str | None = None,
        cat: str | None = None,
        gprop: str | None = None,
        region: str | None = None,
    ) -> str:
        """Fetch Google Trends interest data for a term.

        Args:
            query: The search term to chart. Comma-separate up to five terms
                to compare them.
            geo: Region code, uppercase, e.g. "US", "GB", "US-CA". Worldwide
                when omitted. This endpoint has no gl.
            hl: UI language (ISO 639-1), e.g. "en".
            date: Time range, e.g. "today 12-m" or "2024-01-01 2024-12-31".
            tz: Timezone offset in minutes, sent as a string.
            data_type: One of "TIMESERIES", "GEO_MAP", "GEO_MAP_0",
                "RELATED_QUERIES", "RELATED_TOPICS". Uppercase.
            cat: Category id as a string, e.g. "71". A string here; the
                trending tool uses a number instead.
            gprop: Property filter, one of "images", "news", "youtube",
                "froogle". Web search when omitted.
            region: Breakdown granularity, one of "COUNTRY", "REGION", "DMA",
                "CITY". Uppercase.

        Returns:
            JSON string with a flat response: interest_over_time with
            timeline_data, and interest_by_region.
        """
        client = get_async_client()

        params = _drop_none(
            {
                "query": query,
                "geo": geo,
                "hl": hl,
                "date": date,
                "tz": tz,
                "data_type": data_type,
                "cat": cat,
                "gprop": gprop,
                "region": region,
            }
        )

        raw = await client.google.trends(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_google_trends,
        description=(
            "Fetch Google Trends interest over time and by region for a term "
            "(1 credit)."
        ),
    )


def create_google_trending_tool(max_results: int = 10) -> FunctionTool:
    """Create a Google Trending Now tool with the given configuration."""

    async def scavio_google_trending(
        geo: str,
        hl: str | None = None,
        hours: int | None = None,
        cat: int | None = None,
        sort: str | None = None,
        status: str | None = None,
    ) -> str:
        """Fetch what is trending on Google right now for a country.

        Args:
            geo: Country code, e.g. "US". Required: this endpoint has no
                query field.
            hl: UI language (ISO 639-1), e.g. "en".
            hours: Lookback window, one of 4, 24, 48, 168.
            cat: Category id as a number, 0 is all. A number here; the trends
                tool uses a string instead.
            sort: Sort order, one of "relevance", "search_volume", "recency",
                "title". The field is "sort", not "sort_by".
            status: Trend status, "all" or "active".

        Returns:
            JSON string with a flat response: trends with the term, search
            volume and the time it started trending.
        """
        client = get_async_client()

        params = _drop_none(
            {
                "geo": geo,
                "hl": hl,
                "hours": hours,
                "cat": cat,
                "sort": sort,
                "status": status,
            }
        )

        raw = await client.google.trending(**params)

        _cap(raw, ("trends",), max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_google_trending,
        description=(
            "List what is trending on Google right now for a country "
            "(1 credit). geo is required; there is no query on this endpoint."
        ),
    )
