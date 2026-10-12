"""Endpoint-coverage guard.

Counts what the package actually registers and exports, so a tool that exists
in a module but is never wired into _PROVIDER_MAP or __all__ fails the suite
instead of shipping invisible.
"""

from __future__ import annotations

import autogen_scavio

# Live billable endpoints per platform, from the Scavio API inventory.
# extract = the one CORE endpoint: not a platform, reads any URL. It is keyed
#           "extract" here and reached as a top-level SDK method, never a
#           namespace - scavio.extract(...), never scavio.extract.extract().
# google  = the 14 v2 endpoints; v1 was retired 2026-08-04 and answers 410.
# youtube = 15 live; /youtube/metadata is a deprecated alias of /youtube/video
#           and is deliberately not registered.
# linkedin = 9 live; the 5 retired 410 endpoints are not wrapped.
# reddit  = all 12 endpoints (search, suggestions, post, comments, replies,
#           subreddit, subreddit feed, user, user posts, user comments,
#           popular, trending).
# walmart = 7 since 0.7.0; it shipped with search and product only.
# The 21 entries below walmart landed whole in 0.7.0 with the 93-endpoint
# fanout batch, which is also where walmart grew from 2 to 7.
EXPECTED_TOOL_COUNTS = {
    "extract": 1,
    "google": 14,
    "amazon": 3,
    "youtube": 15,
    "walmart": 7,
    "reddit": 12,
    "tiktok": 11,
    "tiktok_shop": 8,
    "instagram": 12,
    "x": 11,
    "linkedin": 9,
    "threads": 6,
    "kuaishou": 14,
    "ebay": 3,
    "target": 4,
    "home_depot": 3,
    "zillow": 3,
    "booking": 3,
    "tripadvisor": 4,
    "indeed": 4,
    "airbnb": 3,
    "glassdoor": 4,
    "yelp": 3,
    "app_store": 3,
    "google_play": 3,
    "sec": 6,
    "redfin": 3,
    "companies_house": 4,
    "g2": 3,
    "capterra": 3,
    "google_ads": 3,
    "meta_ads": 3,
    # Opt-in (enable_crawl=True): map, crawl + status, batch + status. Not in
    # the default tool set, because crawl and batch bill per page.
    "crawl": 5,
}

OPT_IN = {"crawl"}
TOTAL_TOOLS = sum(n for p, n in EXPECTED_TOOL_COUNTS.items() if p not in OPT_IN)

# The fanout batch: 92 platform endpoints across 22 platforms, plus extract.
# walmart contributes all 7 of its endpoints to that 92, of which 5 are new.
FANOUT_TOOL_COUNT = 93


def test_provider_map_matches_expected_counts():
    assert {
        provider: len(factories)
        for provider, factories in autogen_scavio._PROVIDER_MAP.items()
    } == EXPECTED_TOOL_COUNTS


def test_default_tool_set_size():
    tools = autogen_scavio.create_scavio_tools(api_key="test-key")
    assert len(tools) == TOTAL_TOOLS == 188


def test_crawl_provider_is_opt_in():
    with_crawl = autogen_scavio.create_scavio_tools(api_key="test-key", enable_crawl=True)
    assert len(with_crawl) == TOTAL_TOOLS + 5 == 193
    assert [t.name for t in with_crawl[-5:]] == [
        "scavio_map_website",
        "scavio_crawl_website",
        "scavio_crawl_status",
        "scavio_batch_extract",
        "scavio_batch_status",
    ]
    only = autogen_scavio.create_scavio_tools(api_key="test-key", providers=["crawl"])
    assert len(only) == 5


def test_extract_leads_the_default_tool_set():
    """It is the only tool that works on a URL no platform endpoint covers."""
    tools = autogen_scavio.create_scavio_tools(api_key="test-key")
    assert tools[0].name == "scavio_extract"
    assert list(autogen_scavio._PROVIDER_MAP)[0] == "extract"


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
        "scavio_youtube_transcript": "5 credits",
        "scavio_youtube_streams": "3 credits",
        "scavio_instagram_profile": "1 credit",
        "scavio_instagram_user_posts": "2 credits",
        "scavio_instagram_post": "2 credits",
        "scavio_instagram_comment_replies": "2 credits",
        "scavio_linkedin_person": "1 credit",
        "scavio_linkedin_person_posts": "10 credits",
        "scavio_linkedin_job": "30 credits",
        "scavio_x_search": "1 credit",
        "scavio_google_trending": "1 credit",
        "scavio_reddit_search": "1 credit",
        # The fanout batch. g2 is the dearest flat platform at 5, home_depot /
        # tripadvisor / indeed / yelp / google_play / capterra are 2, the rest 1.
        "scavio_g2_search": "5 credits",
        "scavio_g2_reviews": "5 credits",
        "scavio_home_depot_search": "2 credits",
        "scavio_tripadvisor_locations": "2 credits",
        "scavio_indeed_search": "2 credits",
        "scavio_yelp_search": "2 credits",
        "scavio_google_play_reviews": "2 credits",
        "scavio_capterra_search": "2 credits",
        "scavio_ebay_search": "1 credit",
        "scavio_sec_lookup": "1 credit",
        "scavio_meta_ads_search": "1 credit",
        "scavio_companies_house_search": "1 credit",
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
