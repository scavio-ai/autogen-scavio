"""Guards for the 93-endpoint fanout batch (22 platforms + the core extract).

Two things this batch can get wrong silently and expensively:

1. A tool that calls the wrong SDK method. Every factory here is hand-written
   over the SDK, so a copy-paste lands on a neighbouring endpoint and still
   returns a plausible 200. FANOUT_ROUTES pins tool -> SDK call for all 93.

2. A flat credit cost on a surface that is not flat. Walmart is priced by
   `domain`, Threads by whether you addressed a user by id or handle, Kuaishou
   per endpoint from 1 to 40, and extract by `mode`. A description that says
   "Costs 1 credit" on any of those is wrong by up to 40x, and the agent budgets
   against the description.
"""

from __future__ import annotations

import json

import pytest
from scavio import _spec

import autogen_scavio

FANOUT_ROUTES: dict[str, tuple[str, str]] = {
    "scavio_extract": ("extract", "/api/v1/extract"),
    "scavio_walmart_search": ("walmart.search", "/api/v1/walmart/search"),
    "scavio_walmart_product": ("walmart.product", "/api/v1/walmart/product"),
    "scavio_walmart_reviews": ("walmart.reviews", "/api/v1/walmart/reviews"),
    "scavio_walmart_category": ("walmart.category", "/api/v1/walmart/category"),
    "scavio_walmart_offers": ("walmart.offers", "/api/v1/walmart/offers"),
    "scavio_walmart_seller": ("walmart.seller", "/api/v1/walmart/seller"),
    "scavio_walmart_seller_products": (
        "walmart.seller_products",
        "/api/v1/walmart/seller-products",
    ),
    "scavio_threads_profile": ("threads.profile", "/api/v1/threads/profile"),
    "scavio_threads_user_posts": ("threads.user_posts", "/api/v1/threads/user/posts"),
    "scavio_threads_user_replies": (
        "threads.user_replies",
        "/api/v1/threads/user/replies",
    ),
    "scavio_threads_post": ("threads.post", "/api/v1/threads/post"),
    "scavio_threads_post_comments": (
        "threads.post_comments",
        "/api/v1/threads/post/comments",
    ),
    "scavio_threads_search_users": (
        "threads.search_users",
        "/api/v1/threads/search/users",
    ),
    "scavio_kuaishou_profile": ("kuaishou.profile", "/api/v1/kuaishou/profile"),
    "scavio_kuaishou_user_posts": (
        "kuaishou.user_posts",
        "/api/v1/kuaishou/user/posts",
    ),
    "scavio_kuaishou_user_live": ("kuaishou.user_live", "/api/v1/kuaishou/user/live"),
    "scavio_kuaishou_user_resolve": (
        "kuaishou.user_resolve",
        "/api/v1/kuaishou/user/resolve",
    ),
    "scavio_kuaishou_video": ("kuaishou.video", "/api/v1/kuaishou/video"),
    "scavio_kuaishou_video_comments": (
        "kuaishou.video_comments",
        "/api/v1/kuaishou/video/comments",
    ),
    "scavio_kuaishou_comment_replies": (
        "kuaishou.comment_replies",
        "/api/v1/kuaishou/video/sub-comments",
    ),
    "scavio_kuaishou_videos_batch": (
        "kuaishou.videos_batch",
        "/api/v1/kuaishou/videos/batch",
    ),
    "scavio_kuaishou_search": ("kuaishou.search", "/api/v1/kuaishou/search"),
    "scavio_kuaishou_search_videos": (
        "kuaishou.search_videos",
        "/api/v1/kuaishou/search/videos",
    ),
    "scavio_kuaishou_search_users": (
        "kuaishou.search_users",
        "/api/v1/kuaishou/search/users",
    ),
    "scavio_kuaishou_search_live": (
        "kuaishou.search_live",
        "/api/v1/kuaishou/search/live",
    ),
    "scavio_kuaishou_tag_feed": ("kuaishou.tag_feed", "/api/v1/kuaishou/tag/feed"),
    "scavio_kuaishou_trending": ("kuaishou.trending", "/api/v1/kuaishou/trending"),
    "scavio_ebay_search": ("ebay.search", "/api/v1/ebay/search"),
    "scavio_ebay_product": ("ebay.product", "/api/v1/ebay/product"),
    "scavio_ebay_seller": ("ebay.seller", "/api/v1/ebay/seller"),
    "scavio_target_search": ("target.search", "/api/v1/target/search"),
    "scavio_target_category": ("target.category", "/api/v1/target/category"),
    "scavio_target_product": ("target.product", "/api/v1/target/product"),
    "scavio_target_reviews": ("target.reviews", "/api/v1/target/reviews"),
    "scavio_home_depot_search": ("home_depot.search", "/api/v1/homedepot/search"),
    "scavio_home_depot_product": ("home_depot.product", "/api/v1/homedepot/product"),
    "scavio_home_depot_reviews": ("home_depot.reviews", "/api/v1/homedepot/reviews"),
    "scavio_zillow_search": ("zillow.search", "/api/v1/zillow/search"),
    "scavio_zillow_property": ("zillow.property", "/api/v1/zillow/property"),
    "scavio_zillow_agent_reviews": ("zillow.agent_reviews", "/api/v1/zillow/reviews"),
    "scavio_booking_search": ("booking.search", "/api/v1/booking/search"),
    "scavio_booking_hotel": ("booking.hotel", "/api/v1/booking/hotel"),
    "scavio_booking_reviews": ("booking.reviews", "/api/v1/booking/reviews"),
    "scavio_tripadvisor_locations": (
        "tripadvisor.locations",
        "/api/v1/tripadvisor/locations",
    ),
    "scavio_tripadvisor_search": ("tripadvisor.search", "/api/v1/tripadvisor/search"),
    "scavio_tripadvisor_location": (
        "tripadvisor.location",
        "/api/v1/tripadvisor/location",
    ),
    "scavio_tripadvisor_reviews": (
        "tripadvisor.reviews",
        "/api/v1/tripadvisor/reviews",
    ),
    "scavio_indeed_search": ("indeed.search", "/api/v1/indeed/search"),
    "scavio_indeed_job": ("indeed.job", "/api/v1/indeed/job"),
    "scavio_indeed_company": ("indeed.company", "/api/v1/indeed/company"),
    "scavio_indeed_company_reviews": (
        "indeed.company_reviews",
        "/api/v1/indeed/company/reviews",
    ),
    "scavio_airbnb_search": ("airbnb.search", "/api/v1/airbnb/search"),
    "scavio_airbnb_listing": ("airbnb.listing", "/api/v1/airbnb/listing"),
    "scavio_airbnb_reviews": ("airbnb.reviews", "/api/v1/airbnb/reviews"),
    "scavio_glassdoor_companies": (
        "glassdoor.companies",
        "/api/v1/glassdoor/companies",
    ),
    "scavio_glassdoor_company": ("glassdoor.company", "/api/v1/glassdoor/company"),
    "scavio_glassdoor_reviews": ("glassdoor.reviews", "/api/v1/glassdoor/reviews"),
    "scavio_glassdoor_salaries": ("glassdoor.salaries", "/api/v1/glassdoor/salaries"),
    "scavio_yelp_search": ("yelp.search", "/api/v1/yelp/search"),
    "scavio_yelp_business": ("yelp.business", "/api/v1/yelp/business"),
    "scavio_yelp_reviews": ("yelp.reviews", "/api/v1/yelp/reviews"),
    "scavio_app_store_search": ("app_store.search", "/api/v1/appstore/search"),
    "scavio_app_store_app": ("app_store.app", "/api/v1/appstore/app"),
    "scavio_app_store_reviews": ("app_store.reviews", "/api/v1/appstore/reviews"),
    "scavio_google_play_search": ("google_play.search", "/api/v1/googleplay/search"),
    "scavio_google_play_app": ("google_play.app", "/api/v1/googleplay/app"),
    "scavio_google_play_reviews": ("google_play.reviews", "/api/v1/googleplay/reviews"),
    "scavio_sec_lookup": ("sec.lookup", "/api/v1/sec/lookup"),
    "scavio_sec_company": ("sec.company", "/api/v1/sec/company"),
    "scavio_sec_filings": ("sec.filings", "/api/v1/sec/filings"),
    "scavio_sec_concept": ("sec.concept", "/api/v1/sec/concept"),
    "scavio_sec_facts": ("sec.facts", "/api/v1/sec/facts"),
    "scavio_sec_search": ("sec.search", "/api/v1/sec/search"),
    "scavio_redfin_search": ("redfin.search", "/api/v1/redfin/search"),
    "scavio_redfin_property": ("redfin.property", "/api/v1/redfin/property"),
    "scavio_redfin_market": ("redfin.market", "/api/v1/redfin/market"),
    "scavio_companies_house_search": (
        "companies_house.search",
        "/api/v1/companieshouse/search",
    ),
    "scavio_companies_house_company": (
        "companies_house.company",
        "/api/v1/companieshouse/company",
    ),
    "scavio_companies_house_officers": (
        "companies_house.officers",
        "/api/v1/companieshouse/officers",
    ),
    "scavio_companies_house_filing_history": (
        "companies_house.filing_history",
        "/api/v1/companieshouse/filing-history",
    ),
    "scavio_g2_search": ("g2.search", "/api/v1/g2/search"),
    "scavio_g2_product": ("g2.product", "/api/v1/g2/product"),
    "scavio_g2_reviews": ("g2.reviews", "/api/v1/g2/reviews"),
    "scavio_capterra_search": ("capterra.search", "/api/v1/capterra/search"),
    "scavio_capterra_product": ("capterra.product", "/api/v1/capterra/product"),
    "scavio_capterra_reviews": ("capterra.reviews", "/api/v1/capterra/reviews"),
    "scavio_google_ads_advertisers": (
        "google_ads.advertisers",
        "/api/v1/googleads/advertisers",
    ),
    "scavio_google_ads_search": ("google_ads.search", "/api/v1/googleads/search"),
    "scavio_google_ads_creative": ("google_ads.creative", "/api/v1/googleads/creative"),
    "scavio_meta_ads_search": ("meta_ads.search", "/api/v1/meta-ads/search"),
    "scavio_meta_ads_advertiser": (
        "meta_ads.advertiser",
        "/api/v1/meta-ads/advertiser",
    ),
    "scavio_meta_ads_ad": ("meta_ads.ad", "/api/v1/meta-ads/ad"),
}


class _RecordingClient:
    """Stands in for AsyncScavioClient and records the attribute path called.

    A MagicMock would answer every path, including the wrong one, so the
    recorded path is the assertion: scavio.extract(...) must land on "extract",
    never "extract.extract".
    """

    def __init__(
        self, calls: list[tuple[str, dict]], path: tuple[str, ...] = ()
    ) -> None:
        self._calls = calls
        self._path = path

    def __getattr__(self, name: str) -> "_RecordingClient":
        return _RecordingClient(self._calls, self._path + (name,))

    async def __call__(self, **kwargs: object) -> dict:
        self._calls.append((".".join(self._path), kwargs))
        return {"data": {"ok": True}, "credits_used": 1}


def _sample(schema: dict) -> object:
    """Build one valid value for a JSON-schema property."""
    if "anyOf" in schema:
        schema = next(s for s in schema["anyOf"] if s.get("type") != "null")
    if "enum" in schema:
        return schema["enum"][0]
    kind = schema.get("type")
    if kind == "array":
        return [_sample(schema.get("items", {"type": "string"}))]
    if kind == "integer":
        return 1
    if kind == "number":
        return 1.5
    if kind == "boolean":
        return True
    return "x"


# Built once, at import: create_scavio_tools() calls configure(), which drops the
# cached client. Building inside a test would therefore throw away the recorder
# the fixture just installed.
_TOOLS = {
    tool.name: tool for tool in autogen_scavio.create_scavio_tools(api_key="test-key")
}


def _tools_by_name() -> dict:
    return _TOOLS


@pytest.fixture
def recorder(monkeypatch):
    calls: list[tuple[str, dict]] = []
    client = _RecordingClient(calls)
    monkeypatch.setattr(autogen_scavio._client, "_async_client", client)
    monkeypatch.setattr(autogen_scavio._client, "_configured_api_key", "test-key")
    return calls


def test_every_fanout_endpoint_has_a_registered_tool():
    registered = set(_tools_by_name())
    missing = sorted(name for name in FANOUT_ROUTES if name not in registered)
    assert missing == []
    assert len(FANOUT_ROUTES) == 93


@pytest.mark.parametrize("tool_name", sorted(FANOUT_ROUTES))
async def test_tool_calls_the_endpoint_it_documents(tool_name, recorder):
    """A tool that reaches a neighbouring endpoint still returns a valid 200."""
    call_path, _ = FANOUT_ROUTES[tool_name]
    tool = _tools_by_name()[tool_name]
    schema = tool.schema["parameters"]
    args = {name: _sample(schema["properties"][name]) for name in schema["required"]}

    result = await tool.run_json(args, None)

    assert [path for path, _ in recorder] == [call_path]
    assert recorder[0][1] == args
    assert json.loads(result)["data"] == {"ok": True}


@pytest.mark.parametrize("tool_name", sorted(FANOUT_ROUTES))
def test_every_parameter_is_described_for_the_model(tool_name):
    """The schema is all the model sees. A description defaulted to the param
    name tells it nothing about the value the endpoint wants."""
    tool = _tools_by_name()[tool_name]
    properties = tool.schema["parameters"]["properties"]
    undocumented = [
        name
        for name, schema in properties.items()
        if schema.get("description", name) == name
    ]
    assert undocumented == []


def test_paths_are_copied_verbatim_never_derived():
    """Four routes in this batch do not match their method name."""
    diverging = {
        "meta_ads_search": "/api/v1/meta-ads/search",
        "meta_ads_advertiser": "/api/v1/meta-ads/advertiser",
        "meta_ads_ad": "/api/v1/meta-ads/ad",
        "walmart_seller_products": "/api/v1/walmart/seller-products",
        "companies_house_filing_history": "/api/v1/companieshouse/filing-history",
        "kuaishou_comment_replies": "/api/v1/kuaishou/video/sub-comments",
    }
    for key, path in diverging.items():
        assert _spec.ENDPOINTS[key].path == path, key

    # And the tools this batch registers really do route to those keys.
    by_call = {call: path for call, path in FANOUT_ROUTES.values()}
    assert by_call["meta_ads.search"] == "/api/v1/meta-ads/search"
    assert by_call["walmart.seller_products"] == "/api/v1/walmart/seller-products"
    assert by_call["kuaishou.comment_replies"] == "/api/v1/kuaishou/video/sub-comments"


def test_extract_is_a_top_level_method_not_a_namespace():
    call_path, path = FANOUT_ROUTES["scavio_extract"]
    assert call_path == "extract"
    assert path == "/api/v1/extract"
    assert "extract" in autogen_scavio._PROVIDER_MAP
    assert len(autogen_scavio._PROVIDER_MAP["extract"]) == 1


class TestBodyPricedSurfacesNeverStateAFlatCost:
    """walmart, threads, kuaishou and extract are priced by the request body."""

    def descriptions(self) -> dict:
        return {name: tool.description for name, tool in _tools_by_name().items()}

    def test_walmart_search_and_category_state_the_domain_rule(self):
        described = self.descriptions()
        for name in ("scavio_walmart_search", "scavio_walmart_category"):
            assert "1 credit" in described[name], name
            assert "2 credits" in described[name], name
            assert "com.mx" in described[name], name

    def test_walmart_endpoints_without_a_domain_say_why_they_are_always_one(self):
        described = self.descriptions()
        for name in (
            "scavio_walmart_product",
            "scavio_walmart_reviews",
            "scavio_walmart_offers",
            "scavio_walmart_seller",
            "scavio_walmart_seller_products",
        ):
            assert "1 credit" in described[name], name

    def test_threads_username_tools_price_the_handle_lookup(self):
        described = self.descriptions()
        for name in (
            "scavio_threads_profile",
            "scavio_threads_user_posts",
            "scavio_threads_user_replies",
        ):
            assert "2 credits" in described[name], name
            assert "4" in described[name], name
            assert "user_id" in described[name], name

    def test_kuaishou_prices_each_endpoint_on_its_own(self):
        described = self.descriptions()
        assert "10 credits" in described["scavio_kuaishou_profile"]
        assert "2 credits" in described["scavio_kuaishou_video"]
        assert "40 credits" in described["scavio_kuaishou_videos_batch"]
        assert "1 credit" in described["scavio_kuaishou_user_posts"]
        for name in (
            "scavio_kuaishou_search",
            "scavio_kuaishou_search_videos",
            "scavio_kuaishou_search_users",
            "scavio_kuaishou_search_live",
        ):
            assert "10 credits" in described[name], name

    def test_extract_prices_by_mode_and_says_failures_are_free(self):
        description = self.descriptions()["scavio_extract"]
        assert "1 credit" in description
        assert "ultra costs 2" in description
        assert "costs nothing" in description


def test_closed_enums_reach_the_schema():
    """An endpoint that silently serves the unfiltered set on a bad value has to
    hand the model the accepted list, not a bare string."""
    tools = _tools_by_name()
    ebay = tools["scavio_ebay_search"].schema["parameters"]["properties"]
    per_page = ebay["per_page"]
    assert _enum_of(per_page) == [60, 120, 240]

    status = tools["scavio_zillow_search"].schema["parameters"]["properties"][
        "listing_status"
    ]
    assert _enum_of(status) == ["for_sale", "for_rent", "sold"]

    mode = tools["scavio_extract"].schema["parameters"]["properties"]["mode"]
    assert _enum_of(mode) == ["normal", "advanced", "ultra"]

    radius = tools["scavio_indeed_search"].schema["parameters"]["properties"]["radius"]
    assert _enum_of(radius) == [0, 5, 10, 15, 25, 35, 50, 100]


def _enum_of(schema: dict) -> list:
    for branch in schema.get("anyOf", [schema]):
        if "enum" in branch:
            return branch["enum"]
    raise AssertionError(f"no enum in {schema}")


def test_lookup_first_platforms_expose_their_entry_point():
    """Five platforms are keyed by ids that only exist inside their own URLs."""
    tools = _tools_by_name()
    for name in (
        "scavio_tripadvisor_locations",
        "scavio_glassdoor_companies",
        "scavio_sec_lookup",
        "scavio_companies_house_search",
        "scavio_google_ads_advertisers",
    ):
        assert name in tools, name
