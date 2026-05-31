"""Scavio Google Search tools for AutoGen."""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list


def create_web_search_tool(
    max_results: int = 5,
    include_knowledge_graph: bool = True,
    include_questions: bool = True,
    include_related: bool = False,
    include_maps_results: bool = False,
    include_ai_overviews: bool = False,
    include_local_results: bool = False,
    include_top_stories: bool = False,
    include_hotel_results: bool = False,
    include_news_results: bool = False,
    include_shopping_ads: bool = False,
    include_top_ads: bool = False,
    include_bottom_ads: bool = False,
    nfpr: bool = False,
    light_request: bool | None = None,
) -> FunctionTool:
    """Create a web search tool with the given configuration."""

    async def scavio_web_search(
        query: str,
        search_type: str = "classic",
        country_code: str | None = None,
        language: str | None = None,
        device: str = "desktop",
        page: int = 1,
    ) -> str:
        """Search the web using the Scavio API.

        Args:
            query: The search query string.
            search_type: Type of search to perform (e.g. "classic").
            country_code: Two-letter country code to localize results.
            language: Language code for results.
            device: Device type, either "desktop" or "mobile".
            page: Page number of results to retrieve.

        Returns:
            JSON string with search results including titles, URLs,
            descriptions, knowledge graphs, and related questions.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "search_type": search_type,
            "device": device,
            "page": page,
            "nfpr": nfpr,
        }
        if country_code is not None:
            params["country_code"] = country_code
        if language is not None:
            params["language"] = language
        if light_request is not None:
            params["light_request"] = light_request

        raw = await client.google.search(**params)

        # Truncate result lists to max_results
        for key in ("results", "maps_results", "local_results", "news_results"):
            if isinstance(raw.get(key), list) and len(raw[key]) > max_results:
                raw[key] = raw[key][:max_results]

        # Pop disabled include_* sections
        if not include_knowledge_graph:
            raw.pop("knowledge_graph", None)
        if not include_questions:
            raw.pop("questions", None)
        if not include_related:
            raw.pop("related_queries", None)
            raw.pop("related_searches", None)
        if not include_maps_results:
            raw.pop("maps_results", None)
        if not include_ai_overviews:
            raw.pop("ai_overviews", None)
        if not include_local_results:
            raw.pop("local_results", None)
        if not include_top_stories:
            raw.pop("top_stories", None)
        if not include_hotel_results:
            raw.pop("hotel_results", None)
        if not include_news_results:
            raw.pop("news_results", None)
        if not include_shopping_ads:
            raw.pop("shopping_ads", None)
        if not include_top_ads:
            raw.pop("top_ads", None)
        if not include_bottom_ads:
            raw.pop("bottom_ads", None)

        return format_response(raw)

    return FunctionTool(
        scavio_web_search,
        description=(
            "Search the web using the Scavio API. Returns search results "
            "with titles, URLs, descriptions, knowledge graphs, and "
            "related questions."
        ),
    )
