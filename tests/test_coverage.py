"""Endpoint-coverage guard.

Counts what the package actually registers and exports, so a tool that exists
in a module but is never wired into _PROVIDER_MAP or __all__ fails the suite
instead of shipping invisible.
"""

from __future__ import annotations

import autogen_scavio

# Live billable endpoints per platform, from the Scavio API inventory.
# google  = the 14 v2 endpoints; v1 was retired 2026-08-04 and answers 410.
# youtube = 15 live; /youtube/metadata is a deprecated alias of /youtube/video
#           and is deliberately not registered.
# linkedin = 9 live; the 5 retired 410 endpoints are not wrapped.
# reddit  = all 12 endpoints (search, suggestions, post, comments, replies,
#           subreddit, subreddit feed, user, user posts, user comments,
#           popular, trending).
EXPECTED_TOOL_COUNTS = {
    "google": 14,
    "amazon": 3,
    "youtube": 15,
    "walmart": 2,
    "reddit": 12,
    "tiktok": 11,
    "tiktok_shop": 8,
    "instagram": 12,
    "x": 11,
    "linkedin": 9,
}

TOTAL_TOOLS = sum(EXPECTED_TOOL_COUNTS.values())


def test_provider_map_matches_expected_counts():
    assert {
        provider: len(factories)
        for provider, factories in autogen_scavio._PROVIDER_MAP.items()
    } == EXPECTED_TOOL_COUNTS


def test_default_tool_set_size():
    tools = autogen_scavio.create_scavio_tools(api_key="test-key")
    assert len(tools) == TOTAL_TOOLS == 97


def test_tool_names_are_unique():
    tools = autogen_scavio.create_scavio_tools(api_key="test-key")
    names = [tool.name for tool in tools]
    assert len(names) == len(set(names))


def test_every_registered_factory_is_exported():
    """A tool that is not importable from the package root does not count."""
    exported = {
        name
        for name in autogen_scavio.__all__
        if name.startswith("create_") and name != "create_scavio_tools"
    }
    for name in exported:
        assert hasattr(autogen_scavio, name), name

    registered = {
        factory.__name__
        for factories in autogen_scavio._PROVIDER_MAP.values()
        for factory in factories
    }
    assert registered <= exported
    # The only exported factory that is not registered is the deprecated
    # YouTube metadata alias.
    assert exported - registered == {"create_youtube_metadata_tool"}


def test_every_tool_description_states_its_credit_cost():
    """Agents pick tools off the description, so cost has to be in it."""
    costs = {
        "scavio_youtube_search": "2 credits",
        "scavio_youtube_shorts": "2 credits",
        "scavio_youtube_transcript": "8 credits",
        "scavio_youtube_streams": "3 credits",
        "scavio_instagram_profile": "10 credits",
        "scavio_instagram_user_posts": "2 credits",
        "scavio_instagram_post": "8 credits",
        "scavio_instagram_comment_replies": "8 credits",
        "scavio_linkedin_person": "1 credit",
        "scavio_linkedin_person_posts": "10 credits",
        "scavio_linkedin_job": "30 credits",
        "scavio_x_search": "1 credit",
        "scavio_google_trending": "1 credit",
        "scavio_reddit_search": "1 credit",
    }
    tools = autogen_scavio.create_scavio_tools(api_key="test-key")
    by_name = {tool.name: tool for tool in tools}
    for name, cost in costs.items():
        assert cost in by_name[name].description, name

    # Every tool, not just the sampled ones, names its price.
    assert [tool.name for tool in tools if "credit" not in tool.description] == []


def test_google_tools_take_v2_params_natively():
    """No v1 leftovers: page, country_code and language must not exist."""
    dead = {"page", "country_code", "language", "search_type", "light_request"}
    tools = autogen_scavio.create_scavio_tools(api_key="test-key", providers=["google"])
    for tool in tools:
        params = set(tool.schema["parameters"]["properties"])
        assert params.isdisjoint(dead), (tool.name, params & dead)
