# autogen-scavio

AutoGen integration for the [Scavio API](https://scavio.dev?utm_source=autogen_integration), a [search API for AI agents](https://scavio.dev/search-api-for-ai-agents). Provides **194 tools across 33 platforms** -- retail, real estate, travel, jobs, app stores, company filings, ad libraries and social -- plus `scavio_extract`, which reads any URL as clean Markdown, and an opt-in `crawl` provider that maps a site's URLs, crawls a whole site, or batch-extracts a URL list.

| Provider | Tools | Coverage |
|----------|------:|----------|
| [Extract (any URL)](https://scavio.dev/docs/extract) | 1 | Read any page as Markdown, plain text or raw HTML |
| [Google](https://scavio.dev/docs/search-api) | 14 | Every v2 endpoint: search, AI Mode, Maps, Shopping, Flights, Hotels, News, Trends |
| YouTube | 15 | Every live endpoint |
| [Kuaishou](https://scavio.dev/docs/kuaishou-profile) | 14 | Every endpoint |
| Instagram | 12 | Every endpoint |
| Reddit | 12 | Every endpoint |
| TikTok | 11 | Every endpoint |
| X (formerly Twitter) | 11 | Every endpoint |
| LinkedIn | 9 | Every live endpoint |
| TikTok Shop | 8 | Every endpoint |
| [Walmart](https://scavio.dev/docs/walmart-api) | 7 | Every endpoint |
| [Threads](https://scavio.dev/docs/threads-profile) | 6 | Every endpoint |
| [SEC EDGAR](https://scavio.dev/docs/sec-edgar-lookup) | 6 | Every endpoint |
| [Target](https://scavio.dev/docs/target-search) | 5 | Every endpoint |
| [Tripadvisor](https://scavio.dev/docs/tripadvisor-locations) | 4 | Every endpoint |
| [Indeed](https://scavio.dev/docs/indeed-search) | 4 | Every endpoint |
| [Glassdoor](https://scavio.dev/docs/glassdoor-companies) | 4 | Every endpoint |
| [Companies House](https://scavio.dev/docs/companies-house-search) | 4 | Every endpoint |
| Amazon | 3 | Search, product, offers |
| [eBay](https://scavio.dev/docs/ebay-search) | 3 | Every endpoint, live and sold listings |
| [HEB](https://scavio.dev/docs/heb-search) | 3 | Every endpoint |
| [Home Depot](https://scavio.dev/docs/home-depot-search) | 3 | Every endpoint |
| [Kroger](https://scavio.dev/docs/kroger-search) | 2 | Every endpoint |
| [Zillow](https://scavio.dev/docs/zillow-search) | 3 | Every endpoint |
| [Redfin](https://scavio.dev/docs/redfin-search) | 3 | Every endpoint |
| [Booking.com](https://scavio.dev/docs/booking-search) | 3 | Every endpoint |
| [Airbnb](https://scavio.dev/docs/airbnb-search) | 3 | Every endpoint |
| [Yelp](https://scavio.dev/docs/yelp-search) | 3 | Every endpoint |
| [App Store](https://scavio.dev/docs/app-store-search) | 3 | Every endpoint |
| [Google Play](https://scavio.dev/docs/google-play-search) | 3 | Every endpoint |
| [G2](https://scavio.dev/docs/g2-search) | 3 | Every endpoint |
| [Capterra](https://scavio.dev/docs/capterra-search) | 3 | Every endpoint |
| [Google Ads Transparency](https://scavio.dev/docs/google-ads-advertisers) | 3 | Every endpoint |
| [Meta Ad Library](https://scavio.dev/docs/meta-ads-search) | 3 | Every endpoint |

## Installation

```bash
pip install autogen-scavio
```

## Setup

Get a free API key at [dashboard.scavio.dev](https://dashboard.scavio.dev?utm_source=autogen_integration) and set it as an environment variable:

```bash
export SCAVIO_API_KEY="sk_live_..."
```

## Quick Start

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_scavio import create_scavio_tools

tools = create_scavio_tools()

agent = AssistantAgent(
    name="researcher",
    model_client=OpenAIChatCompletionClient(model="gpt-5.5"),
    tools=tools,
    system_message="You are a research assistant with access to search tools.",
)

async def main():
    result = await agent.run(task="What are the top AI agent frameworks in 2026?")
    print(result.messages[-1].content)

asyncio.run(main())
```

## Selective Tool Loading

Load only the providers you need:

```python
# Only Google and Amazon tools
tools = create_scavio_tools(providers=["google", "amazon"])

# Only YouTube
tools = create_scavio_tools(providers=["youtube"])

# Retail price comparison across four marketplaces
tools = create_scavio_tools(providers=["amazon", "walmart", "ebay", "target"])

# Read a page no platform endpoint covers
tools = create_scavio_tools(providers=["extract"])

# Whole sites: map, crawl and batch (opt-in, see below)
tools = create_scavio_tools(providers=["extract", "crawl"])
tools = create_scavio_tools(enable_crawl=True)  # every default provider + crawl

# Providers: extract, google, amazon, youtube, walmart, reddit, tiktok,
# tiktok_shop, instagram, x, linkedin, threads, kuaishou, ebay, target,
# home_depot, zillow, booking, tripadvisor, indeed, airbnb, glassdoor, yelp,
# app_store, google_play, sec, redfin, companies_house, g2, capterra,
# google_ads, meta_ads, and the opt-in crawl

# Individual tool factories
from autogen_scavio import create_web_search_tool, create_extract_tool

web_tool = create_web_search_tool(max_results=10)
extract_tool = create_extract_tool()
```

> **Amazon changed in 0.4.0 (breaking).** The Amazon endpoint changed. `domain`
> is replaced by `country`, a two-letter marketplace code (`us`, `gb` -- the UK
> is `gb`, not `uk` -- `de`, `jp`, ...). `sort_by`, `pages`, `category_id`,
> `merchant_id`, `language`, `currency`, `device`, `zip_code` and
> `autoselect_variant` are gone: the marketplace ignores all of them, and
> `sort_by` was verified to return the identical unordered set for every value,
> so they are removed rather than kept as silent no-ops. Responses are
> normalized -- `price` is a number with a sibling `currency`, and `buybox` is
> gone (use `scavio_amazon_offers`).

> **Google v1 is gone (0.5.0).** `/api/v1/google` was retired on 2026-08-04 and
> now answers 410, so every Google tool calls a `/api/v2/google` endpoint and
> takes v2 params natively: `gl`, `hl`, `start`, `google_domain`, `device`.
> `country_code`, `language` and `page` no longer exist and are not mapped --
> `start` is a zero-based result offset (0, 10, 20), not a 1-based page number,
> so a silent remap would fetch the wrong page. Google responses are flat: the
> payload sits at the top level, there is no `data` wrapper, and organic hits
> carry `link` / `snippet`, not v1's `url` / `content`.

> **Reddit is complete in 0.6.0.** All twelve endpoints are now tools; only
> search and post detail existed before. Three shapes to keep straight when
> chaining them: `scavio_reddit_search` returns `data.results`,
> `scavio_reddit_post` returns a flat post object with **no comments** at all,
> and the subreddit, user and popular feeds return `data.posts`. Read a thread
> with `scavio_reddit_post_comments`, then expand a subtree by passing that
> comment's `reply_cursor` to `scavio_reddit_comment_replies`. Sort values are
> uppercase (`HOT`, `NEW`, `TOP`, `BEST`, `CONTROVERSIAL`); the subreddit feed
> is the only one that also takes `RISING`.

> **0.7.0 adds 91 tools: 21 new platforms, 5 more Walmart endpoints, and
> `scavio_extract`.** Requires `scavio>=0.15.0` -- an older SDK has none of the
> new namespaces and every tool below fails at import. Three things worth
> knowing before you wire them up:
>
> - **`scavio_extract` is the fallback for everything else.** It reads any URL
>   and returns clean Markdown (or plain text, or raw HTML), so an agent that
>   hits a page no platform endpoint covers still has a move. It leads the
>   default tool set for that reason.
> - **Five platforms are lookup-first.** Tripadvisor, Glassdoor, SEC EDGAR,
>   Companies House and Google Ads Transparency are keyed by ids that only exist
>   inside their own URLs, so a caller holding a *name* must resolve it first:
>   `scavio_tripadvisor_locations`, `scavio_glassdoor_companies`,
>   `scavio_sec_lookup`, `scavio_companies_house_search`,
>   `scavio_google_ads_advertisers`.
> - **Four surfaces are priced by the request body, not the route.** Walmart by
>   `domain`, Threads by whether you pass `user_id` or `username`, Kuaishou per
>   endpoint (1 to 40), and extract by `mode`. Every tool description states its
>   own price; see [Credits](#credits).
>
> These tools return the API response verbatim -- `max_results` does not apply
> to them. Each endpoint pages itself (`page`, `cursor`, `per_page`, `limit`,
> `count`), and trimming rows out of a response that still reports `has_more`
> would read as an empty tail.

## Map, Crawl and Batch (opt-in)

The `crawl` provider adds five tools for whole sites. It is **not in the default
tool set** -- crawl and batch bill per page -- so name it in `providers` or pass
`enable_crawl=True`.

| Tool | What it does | Credits |
|------|--------------|---------|
| `scavio_map_website` | A site's page URLs from its sitemaps and start page, deduplicated and path-filtered | 1 on `normal` (up to 2 on `advanced`, up to 10 on `ultra`) |
| `scavio_crawl_website` | Crawl a site from one URL; every page as Markdown, text or HTML | per successful page: 1 / 1 / 2 by `mode` |
| `scavio_crawl_status` | A crawl's progress and page results, cursor-paged | free |
| `scavio_batch_extract` | Extract a list of URLs in one job | per successful page: 1 / 1 / 2 by `mode` |
| `scavio_batch_status` | A batch's progress and page results, cursor-paged | free |

`scavio_crawl_website` and `scavio_batch_extract` start a background job, **wait
up to `wait_seconds` (default 45, max 300)** for it to finish, and return the
job's `id`, `status`, `pages`, `credits_used`, up to `limit` page results
(default 10) and `next_cursor`. A job still `queued` or `running` when the wait
ends keeps going: the agent reads it, and any further pages, with
`scavio_crawl_status` / `scavio_batch_status` and the `id`. That keeps a turn
bounded while a large crawl (up to 6 hours) runs on.

```python
from autogen_scavio import create_scavio_tools

tools = create_scavio_tools(providers=["extract", "crawl"])
crawl = next(t for t in tools if t.name == "scavio_crawl_website")
result = await crawl.run_json(
    {"url": "https://hono.dev/docs", "max_pages": 25, "include_paths": ["/docs/**"]},
    None,
)
```

Crawl and batch bill **per successful page** at extract's price for the mode
(`normal` and `advanced` 1 credit, `ultra` 2); failed and skipped pages are
free, and a job stops cleanly with `stopped_reason: "insufficient_credits"` if
the balance runs out. Reading a job is free. Crawl and map obey the site's
robots.txt; results are kept for 3 days. Plan limits (pages per crawl / active
jobs / URLs per batch): Free 10/1/10, PAYG 100/1/50, Project 500/2/100,
Bootstrap 2,000/3/500, Startup 5,000/5/1,000, Growth 10,000/10/1,000.
Cancellation, webhooks and idempotency keys exist on the
[REST API](https://scavio.dev/docs/extract) and in the `scavio` SDK, but are not
tools here. Requires `scavio>=0.23.0` (0.8.0 raises the floor).

## Available Tools

| Provider | Tool | Description |
|----------|------|-------------|
| Extract | `scavio_extract` | Read ANY URL and get it back as raw HTML, readability Markdown, or plain text (1-2 credits by mode) |
| Google | `scavio_web_search` | Web search with knowledge graph, related questions and AI Overview |
| Google | `scavio_google_ai_mode` | Google AI Mode answer with its cited references |
| Google | `scavio_google_maps_search` | Local businesses and places, with place_id and data_id |
| Google | `scavio_google_maps_place` | Full place details by place_id or data_cid |
| Google | `scavio_google_maps_reviews` | Place reviews, up to 20 per call |
| Google | `scavio_google_shopping` | Product search with prices, sellers and catalog ids |
| Google | `scavio_google_shopping_product` | Product page with its seller offers |
| Google | `scavio_google_shopping_stores` | Next page of sellers for a product |
| Google | `scavio_google_flights` | Itineraries and prices between airports |
| Google | `scavio_google_hotels` | Properties, nightly rates and availability |
| Google | `scavio_google_hotels_detail` | One hotel and its booking sources |
| Google | `scavio_google_news` | Headlines by query, topic, story or publisher |
| Google | `scavio_google_trends` | Interest over time and by region for a term |
| Google | `scavio_google_trending` | What is trending on Google right now, by country |
| Amazon | `scavio_amazon_search` | Product search across 22 marketplaces |
| Amazon | `scavio_amazon_product` | Product details by ASIN |
| Amazon | `scavio_amazon_offers` | Every seller offer for an ASIN, including the buy-box winner |
| YouTube | `scavio_youtube_search` | Video search with filters (2 credits) |
| YouTube | `scavio_youtube_shorts` | Shorts search (2 credits) |
| YouTube | `scavio_youtube_suggestions` | Autocomplete suggestions for a query |
| YouTube | `scavio_youtube_video` | Full video details by ID or watch URL |
| YouTube | `scavio_youtube_comments` | Top-level comments on a video |
| YouTube | `scavio_youtube_comment_replies` | Replies to a comment, by reply_cursor |
| YouTube | `scavio_youtube_transcript` | Transcript as plain text or SRT (5 credits) |
| YouTube | `scavio_youtube_related` | Videos related to a video |
| YouTube | `scavio_youtube_channel_search` | Channel search by keyword |
| YouTube | `scavio_youtube_channel` | Channel profile by ID, @handle, or URL |
| YouTube | `scavio_youtube_channel_videos` | A channel's uploaded videos |
| YouTube | `scavio_youtube_channel_shorts` | A channel's Shorts |
| YouTube | `scavio_youtube_channel_community` | A channel's community posts (`data.posts`) |
| YouTube | `scavio_youtube_channel_resolve` | Resolve an @handle or URL to a channel ID |
| YouTube | `scavio_youtube_streams` | Playable stream URLs for a video (3 credits) |
| Walmart | `scavio_walmart_search` | Search Walmart and get structured product rows (1-2 credits by domain) |
| Walmart | `scavio_walmart_product` | Full Walmart product detail: price, rating, images, specifications, availability, seller |
| Walmart | `scavio_walmart_reviews` | Customer reviews with ratings, text, author, date and the rating breakdown |
| Walmart | `scavio_walmart_category` | Products within a Walmart category, same product shape as search (1-2 credits by domain) |
| Walmart | `scavio_walmart_offers` | Seller offers for a product: price, seller, condition, buy-box flag |
| Walmart | `scavio_walmart_seller` | Marketplace seller storefront: name, rating, review count, Pro Seller badge, business... |
| Walmart | `scavio_walmart_seller_products` | A seller's catalog; ~40 items server-rendered, total_count is the real catalog size |
| Reddit | `scavio_reddit_search` | Post search (query and cursor only, `data.results`) |
| Reddit | `scavio_reddit_search_suggestions` | Autocomplete suggestions for a search query |
| Reddit | `scavio_reddit_post` | Post metadata by URL, without comments |
| Reddit | `scavio_reddit_post_comments` | Top-level comments on a post, with `reply_cursor` |
| Reddit | `scavio_reddit_comment_replies` | Replies to a comment, by `reply_cursor` |
| Reddit | `scavio_reddit_subreddit` | Subreddit profile and subscriber counts |
| Reddit | `scavio_reddit_subreddit_posts` | A subreddit's feed (`data.posts`, sort also takes RISING) |
| Reddit | `scavio_reddit_user` | Redditor profile and karma breakdown |
| Reddit | `scavio_reddit_user_posts` | A redditor's submitted posts |
| Reddit | `scavio_reddit_user_comments` | A redditor's comments, each naming its post |
| Reddit | `scavio_reddit_popular` | The site-wide r/popular feed |
| Reddit | `scavio_reddit_trending` | Search queries trending on Reddit right now |
| TikTok | `scavio_tiktok_profile` | User profile lookup |
| TikTok | `scavio_tiktok_user_posts` | User's posted videos |
| TikTok | `scavio_tiktok_video` | Video details |
| TikTok | `scavio_tiktok_video_comments` | Video comments |
| TikTok | `scavio_tiktok_comment_replies` | Comment replies |
| TikTok | `scavio_tiktok_search_videos` | Video search by keyword |
| TikTok | `scavio_tiktok_search_users` | User search by keyword |
| TikTok | `scavio_tiktok_hashtag` | Hashtag info |
| TikTok | `scavio_tiktok_hashtag_videos` | Videos by hashtag |
| TikTok | `scavio_tiktok_user_followers` | User's followers |
| TikTok | `scavio_tiktok_user_followings` | User's followings |
| TikTok Shop | `scavio_tiktok_shop_search` | Product search by keyword (US), with exact prices |
| TikTok Shop | `scavio_tiktok_shop_search_suggestions` | Keyword autocomplete across 8 regions |
| TikTok Shop | `scavio_tiktok_shop_product` | Full product detail (no price -- upstream masks it) |
| TikTok Shop | `scavio_tiktok_shop_product_reviews` | Paginated reviews, up to 200 per call |
| TikTok Shop | `scavio_tiktok_shop_categories` | Global category tree (240 nodes, 2 levels) |
| TikTok Shop | `scavio_tiktok_shop_category_products` | Products under a category, with exact prices |
| TikTok Shop | `scavio_tiktok_shop_shop_products` | A seller's catalog, with exact prices |
| TikTok Shop | `scavio_tiktok_shop_resolve` | Resolve a Shop URL or share link to an id |
| Instagram | `scavio_instagram_profile` | User profile lookup |
| Instagram | `scavio_instagram_user_posts` | User's posts |
| Instagram | `scavio_instagram_user_reels` | User's reels |
| Instagram | `scavio_instagram_user_tagged` | Posts user is tagged in |
| Instagram | `scavio_instagram_user_stories` | User's active stories |
| Instagram | `scavio_instagram_post` | Post details by url, media_id, or shortcode |
| Instagram | `scavio_instagram_post_comments` | Post comments |
| Instagram | `scavio_instagram_comment_replies` | Comment replies |
| Instagram | `scavio_instagram_search_users` | User search by keyword |
| Instagram | `scavio_instagram_search_hashtags` | Hashtag search by keyword |
| Instagram | `scavio_instagram_user_followers` | User's followers |
| Instagram | `scavio_instagram_user_followings` | User's followings |
| X | `scavio_x_search` | Tweet and people search (`search`, not `query`) |
| X | `scavio_x_tweet` | Full tweet details by ID |
| X | `scavio_x_tweet_comments` | Replies to a tweet, ranked or chronological |
| X | `scavio_x_tweet_retweeters` | Users who retweeted a tweet (`data.retweeters`) |
| X | `scavio_x_user` | User profile by handle |
| X | `scavio_x_user_tweets` | A user's tweets, plus pinned and profile |
| X | `scavio_x_user_replies` | A user's tweets and replies |
| X | `scavio_x_user_media` | A user's posts with photos or videos |
| X | `scavio_x_user_followers` | A user's followers |
| X | `scavio_x_user_followings` | Accounts a user follows (`data.following`, singular) |
| X | `scavio_x_trending` | Trending topics by country name |
| LinkedIn | `scavio_linkedin_person` | Full member profile with experience and education |
| LinkedIn | `scavio_linkedin_person_about` | The narrative sections of a profile |
| LinkedIn | `scavio_linkedin_person_posts` | A member's posts, comments or reactions (10 credits) |
| LinkedIn | `scavio_linkedin_company` | Company profile with featured_employees |
| LinkedIn | `scavio_linkedin_company_posts` | A company's recent posts (10 credits) |
| LinkedIn | `scavio_linkedin_search_jobs` | Job search by keyword (10 credits) |
| LinkedIn | `scavio_linkedin_job` | One job listing in full (30 credits) |
| LinkedIn | `scavio_linkedin_post` | One post with media, tags and top comments |
| LinkedIn | `scavio_linkedin_post_comments` | Comments on a post, paged by number (10 credits) |
| Threads | `scavio_threads_profile` | Profile details for a Threads user, by user_id or username (2-4 credits by identifier) |
| Threads | `scavio_threads_user_posts` | A user's Threads posts, cursor-paginated (2-4 credits by identifier) |
| Threads | `scavio_threads_user_replies` | A user's replies, cursor-paginated (2-4 credits by identifier) |
| Threads | `scavio_threads_post` | A single Threads post by id or threads.net URL (2 credits) |
| Threads | `scavio_threads_post_comments` | Replies to a Threads post, cursor-paginated (2 credits) |
| Threads | `scavio_threads_search_users` | Threads profiles matching a name or handle (2 credits) |
| Kuaishou | `scavio_kuaishou_profile` | Profile details for a Kuaishou user (10 credits) |
| Kuaishou | `scavio_kuaishou_user_posts` | A user's top posts, cursor-paginated |
| Kuaishou | `scavio_kuaishou_user_live` | A user's current live-stream status |
| Kuaishou | `scavio_kuaishou_user_resolve` | Turns a Kuaishou share link into a user id |
| Kuaishou | `scavio_kuaishou_video` | A single Kuaishou video by photo id or URL (2 credits) |
| Kuaishou | `scavio_kuaishou_video_comments` | Comments on a video, cursor-paginated |
| Kuaishou | `scavio_kuaishou_comment_replies` | Replies under a root comment on a Kuaishou video |
| Kuaishou | `scavio_kuaishou_videos_batch` | Several Kuaishou videos in one call, max 20 photo ids (40 credits) |
| Kuaishou | `scavio_kuaishou_search` | Mixed-result search across Kuaishou (10 credits) |
| Kuaishou | `scavio_kuaishou_search_videos` | Kuaishou video search results (10 credits) |
| Kuaishou | `scavio_kuaishou_search_users` | Kuaishou user search results (10 credits) |
| Kuaishou | `scavio_kuaishou_search_live` | Kuaishou live-stream search results (10 credits) |
| Kuaishou | `scavio_kuaishou_tag_feed` | Posts under a Kuaishou hashtag, cursor-paginated |
| Kuaishou | `scavio_kuaishou_trending` | Kuaishou hot / live / shopping / brand / music leaderboards |
| eBay | `scavio_ebay_search` | Search live or SOLD eBay listings: price, condition, bids, shipping, seller, feedback |
| eBay | `scavio_ebay_product` | One eBay listing in full: price, condition, images, item specifics, shipping, returns... |
| eBay | `scavio_ebay_seller` | eBay seller profile card: store name, feedback score and %, items sold, followers... |
| Target | `scavio_target_search` | Search Target.com: prices, ratings, badges and promotions |
| Target | `scavio_target_category` | Products in a Target category, same shape as search plus the category breadcrumb |
| Target | `scavio_target_product` | Target product details by TCIN: price, rating, images, specifications, variants, return... |
| Target | `scavio_target_reviews` | Target reviews with the rating breakdown, per-attribute averages and guest photos |
| Home Depot | `scavio_home_depot_search` | Search Home Depot: price and promotions, brand and model, ratings, badges, per-store... (2 credits) |
| Home Depot | `scavio_home_depot_product` | Full Home Depot item detail: pricing, images and videos, spec table, dimensions, bullets... (2 credits) |
| Home Depot | `scavio_home_depot_reviews` | One page of full Home Depot review bodies, rating distribution, per-attribute ratings... (2 credits) |
| Zillow | `scavio_zillow_search` | Zillow listings in a region: price, beds, baths, living area, Zestimate, coordinates... |
| Zillow | `scavio_zillow_property` | Full Zillow listing: price and price history, Zestimate, tax history, RESO facts, rooms... |
| Zillow | `scavio_zillow_agent_reviews` | A Zillow AGENT's profile and reviews: rating, bodies with sub-ratings, specialties... |
| Booking.com | `scavio_booking_search` | Booking.com properties for a destination and stay: live nightly price, review score, star... |
| Booking.com | `scavio_booking_hotel` | One Booking.com property in full: rooms and rate plans, facilities, house rules... |
| Booking.com | `scavio_booking_reviews` | Booking.com guest reviews with the score breakdown by category and Booking's own... |
| Tripadvisor | `scavio_tripadvisor_locations` | Resolve a place or business NAME to the TripAdvisor geo_id / location_id pair every other... (2 credits) |
| Tripadvisor | `scavio_tripadvisor_search` | Restaurants / hotels / attractions in a TripAdvisor geo, TripAdvisor-ranked; each row... (2 credits) |
| Tripadvisor | `scavio_tripadvisor_location` | One TripAdvisor location in full: rating histogram, sub-ratings, city ranking, amenities... (2 credits) |
| Tripadvisor | `scavio_tripadvisor_reviews` | A page of TripAdvisor reviews: rating, trip date and type, reviewer home town and... (2 credits) |
| Indeed | `scavio_indeed_search` | Indeed job postings: title, employer, rating, location, salary range, job type, benefits... (2 credits) |
| Indeed | `scavio_indeed_job` | One Indeed posting in full: description text and HTML, structured salary, employment... (2 credits) |
| Indeed | `scavio_indeed_company` | Indeed employer profile: description, industry, HQ, size, revenue, CEO approval... (2 credits) |
| Indeed | `scavio_indeed_company_reviews` | Indeed employee reviews with per-category ratings, pros/cons, reviewer job title and... (2 credits) |
| Airbnb | `scavio_airbnb_search` | Airbnb stays: stay-total and per-night price with the full discount ledger, rating... |
| Airbnb | `scavio_airbnb_listing` | One Airbnb listing in full: description, capacity, the complete grouped amenity list... |
| Airbnb | `scavio_airbnb_reviews` | Airbnb review BODIES with per-review rating, date, and reviewer name/photo/location |
| Glassdoor | `scavio_glassdoor_companies` | Search Glassdoor by company NAME and resolve it to the employer_id every other endpoint... (2 credits) |
| Glassdoor | `scavio_glassdoor_company` | Glassdoor employer profile: ratings, star distribution, CEO approval, size/revenue bands... (2 credits) |
| Glassdoor | `scavio_glassdoor_reviews` | Up to THREE full Glassdoor reviews with per-axis scores, pros, cons, advice, employer... (2 credits) |
| Glassdoor | `scavio_glassdoor_salaries` | Glassdoor salaries by job title: base-pay and total-pay percentiles P10-P90 with medians... (2 credits) |
| Yelp | `scavio_yelp_search` | Businesses in Yelp's ranked order: rating, review count, price band, categories, address... (2 credits) |
| Yelp | `scavio_yelp_business` | One Yelp business in full: per-star histogram, price band, address and coordinates... (2 credits) |
| Yelp | `scavio_yelp_reviews` | A page of Yelp reviews: rating, full text, language, author profile and expertise counts... (2 credits) |
| App Store | `scavio_app_store_search` | Up to 200 fully-shaped App Store apps |
| App Store | `scavio_app_store_app` | Full App Store listing: title, description, developer identity, price, all-time and... |
| App Store | `scavio_app_store_reviews` | A page of App Store reviews: star rating, title, full text, author, and the APP VERSION... |
| Google Play | `scavio_google_play_search` | Ranked Google Play apps: package name, title, developer, rating, install count, price and... (2 credits) |
| Google Play | `scavio_google_play_app` | Full Google Play store listing: installs (incl (2 credits) |
| Google Play | `scavio_google_play_reviews` | A page of Google Play reviews: star score, full text, author, thumbs-up count, developer... (2 credits) |
| SEC EDGAR | `scavio_sec_lookup` | Resolve a company name or ticker to the CIK every other SEC EDGAR endpoint is keyed by |
| SEC EDGAR | `scavio_sec_company` | SEC filer profile: legal and former names, SIC industry, EIN, LEI, state of... |
| SEC EDGAR | `scavio_sec_filings` | A page of one filer's filings: accession number, form and root form, filing and period... |
| SEC EDGAR | `scavio_sec_concept` | Every value a filer reported for one XBRL concept, newest period first, with the form and... |
| SEC EDGAR | `scavio_sec_facts` | The index of every XBRL concept a filer reports - tag, label, description, units, most... |
| SEC EDGAR | `scavio_sec_search` | EDGAR full-text search, 2001-today: each hit is the matching DOCUMENT with its URL, form... |
| Redfin | `scavio_redfin_search` | Redfin listings: price, price per sqft, beds, baths, living area, lot size, year built... |
| Redfin | `scavio_redfin_property` | One Redfin listing in full: price, Redfin Estimate and rental estimate, complete MLS fact... |
| Redfin | `scavio_redfin_market` | Redfin housing-market stats for a region: median list and sale price, price per sqft... |
| Companies House | `scavio_companies_house_search` | Search the UK register by name and get the company_number every other endpoint is keyed... |
| Companies House | `scavio_companies_house_company` | Full UK register entry: status, type, incorporation and dissolution dates, registered... |
| Companies House | `scavio_companies_house_officers` | UK company officers current and resigned: name, role, appointment and resignation dates... |
| Companies House | `scavio_companies_house_filing_history` | UK filings, most recent first: date, filing type code, description, register annotations... |
| G2 | `scavio_g2_search` | Search G2 for B2B software products: star rating, review count, vendor, categories... (5 credits) |
| G2 | `scavio_g2_product` | Full G2 software profile: rating and per-star histogram, vendor, pricing editions with... (5 credits) |
| G2 | `scavio_g2_reviews` | A page of G2 software reviews: rating, title, likes/dislikes, problems solved, reviewer... (5 credits) |
| Capterra Software Reviews | `scavio_capterra_search` | Search Capterra for B2B software: 20 ranked products with name, vendor description... (2 credits) |
| Capterra Software Reviews | `scavio_capterra_product` | Full Capterra profile: per-star histogram and the four scored criteria, complete pricing... (2 credits) |
| Capterra Software Reviews | `scavio_capterra_reviews` | A page of Capterra reviews: overall score plus five per-criterion scores, pros, cons... (2 credits) |
| Google Ads | `scavio_google_ads_advertisers` | Resolve a brand name or domain to the advertiser_id /search and /creative are keyed by |
| Google Ads | `scavio_google_ads_search` | Every ad Google is running for one advertiser: the creative, advertiser id and name... |
| Google Ads | `scavio_google_ads_creative` | One Google ad creative in full and the ONLY endpoint carrying its history: every size... |
| Meta Ads | `scavio_meta_ads_search` | Search the Meta Ad Library: 30 ads on page 1 with full creative, then cursor-paginated |
| Meta Ads | `scavio_meta_ads_advertiser` | Every ad a Facebook Page is running, by numeric page id - 30 ads on page 1 with the same... |
| Meta Ads | `scavio_meta_ads_ad` | One Meta ad in full by archive id: creative, advertiser, run dates, platforms, any... |

### Credits

Every tool states its own cost in its description, so the agent sees the price
before it picks. Most endpoints are 1 credit; these are the exceptions:

| Tools | Credits |
|-------|--------:|
| `scavio_youtube_search`, `scavio_youtube_shorts` | 2 |
| `scavio_youtube_streams` | 3 |
| `scavio_youtube_transcript` | 5 |
| `scavio_instagram_user_posts` | 2 |
| `scavio_instagram_post`, `scavio_instagram_comment_replies` | 8 |
| Every other Instagram tool | 10 |
| `scavio_linkedin_person_posts`, `scavio_linkedin_company_posts`, `scavio_linkedin_search_jobs`, `scavio_linkedin_post_comments` | 10 |
| `scavio_linkedin_job` | 30 |
| Every Home Depot, Tripadvisor, Indeed, Glassdoor, Yelp, Google Play and Capterra tool | 2 |
| Every G2 tool | 5 |
| `scavio_kuaishou_video` | 2 |
| `scavio_kuaishou_profile`, `scavio_kuaishou_search`, `scavio_kuaishou_search_videos`, `scavio_kuaishou_search_users`, `scavio_kuaishou_search_live` | 10 |
| `scavio_kuaishou_videos_batch` | 40 |

All 14 Google tools, all 11 X tools, the remaining LinkedIn and Kuaishou tools
and everything under Amazon, Reddit, TikTok, TikTok Shop, eBay, Target, Zillow,
Redfin, Booking.com, Airbnb, App Store, SEC EDGAR, Companies House, Google Ads
Transparency and Meta Ad Library is 1 credit.

**Four surfaces are priced by the request body, so no single number is true for
them:**

| Surface | Price |
|---------|-------|
| Walmart `search` and `category` | 1 credit on `domain` `com` or `ca`, 2 on `com.mx`. The other five Walmart tools take no `domain` and are always 1. |
| Threads `profile`, `user_posts`, `user_replies` | 2 credits addressed by `user_id`, 4 by `username` -- a handle costs a second lookup. Pass `user_id` whenever you have it. The other three Threads tools have no username form and are always 2. |
| Kuaishou | Per endpoint, from 1 to 40. See the table above; a single platform figure would be wrong by up to 40x. |
| `scavio_extract` | 1 credit on `mode` `normal` or `advanced`, 2 on `ultra`. Only a successful extraction is billed -- a dead link, bot wall or timeout costs nothing. |
| `scavio_map_website` *(opt-in)* | 1 credit on `normal`; up to 2 on `advanced`, up to 10 on `ultra`, priced by what the call needed. |
| `scavio_crawl_website`, `scavio_batch_extract` *(opt-in)* | Per successful page: 1 credit on `normal` or `advanced`, 2 on `ultra`. Failed and skipped pages are free; the status tools are free. |

Five LinkedIn endpoints -- `person/contact`, `company/people`, `company/jobs`,
`search/people` and `search/posts` -- were retired upstream and only answer 410,
so they are deliberately not wrapped as tools: a tool that always fails is still
a menu item a model will pick. Use `scavio_linkedin_company`'s
`featured_employees` in place of `company/people`, and `scavio_linkedin_search_jobs`
with a company name in place of `company/jobs`.

`create_youtube_metadata_tool` is still exported but is a deprecated alias of
`scavio_youtube_video` (same endpoint, same response), so it is no longer part
of the default tool set. Use the video tool.

### TikTok Shop caveats

```python
tools = create_scavio_tools(providers=["tiktok_shop"])
```

Two limits are worth knowing before chaining these tools:

- `scavio_tiktok_shop_product` resolves only about 44% of the product ids that
  `scavio_tiktok_shop_search` returns. Upstream has no detail data for the rest,
  so a not-found result is a normal outcome rather than an error -- skip the
  product instead of retrying. Search is a listing source, not the first leg of a
  reliable search-then-detail pipeline.
- `scavio_tiktok_shop_product` does not return a price. Upstream masks the digits
  on the product page, so `price.current` and `price.original` come back null.
  Exact prices are on `scavio_tiktok_shop_search`,
  `scavio_tiktok_shop_shop_products` and `scavio_tiktok_shop_category_products`.

## Configuration

```python
from autogen_scavio import configure

# Set API key programmatically
configure(api_key="sk_live_...")

# Or pass to factory
tools = create_scavio_tools(api_key="sk_live_...", max_results=10)
```


## About Scavio

[Scavio](https://scavio.dev) is a unified [search API](https://scavio.dev/docs/search-api) built for AI agents — one API key, structured JSON, no scraping or proxies. A real-time [Tavily alternative](https://scavio.dev/alternatives/tavily) and [SerpAPI alternative](https://scavio.dev/alternatives/serpapi) with data from:

- [Google Search API](https://scavio.dev/google-search-api) — SERP results, news, images, maps, and knowledge graph
- [Amazon Product API](https://scavio.dev/amazon-product-api) and [Walmart Product API](https://scavio.dev/walmart-product-api) — product search and details
- [eBay API](https://scavio.dev/docs/ebay-search), [Target API](https://scavio.dev/docs/target-search) and [Home Depot API](https://scavio.dev/docs/home-depot-search) — retail listings, product detail and reviews
- [Zillow API](https://scavio.dev/docs/zillow-search) and [Redfin API](https://scavio.dev/docs/redfin-search) — listings, property detail and market stats
- [Booking.com API](https://scavio.dev/docs/booking-search), [Airbnb API](https://scavio.dev/docs/airbnb-search) and [Tripadvisor API](https://scavio.dev/docs/tripadvisor-locations) — stays, rates and guest reviews
- [Indeed API](https://scavio.dev/docs/indeed-search) and [Glassdoor API](https://scavio.dev/docs/glassdoor-companies) — job postings, employer profiles, reviews and salaries
- [G2 API](https://scavio.dev/docs/g2-search) and [Capterra API](https://scavio.dev/docs/capterra-search) — B2B software ratings and review bodies
- [App Store API](https://scavio.dev/docs/app-store-search) and [Google Play API](https://scavio.dev/docs/google-play-search) — app listings, install counts and reviews
- [SEC EDGAR API](https://scavio.dev/docs/sec-edgar-lookup) and [Companies House API](https://scavio.dev/docs/companies-house-search) — US filings, XBRL facts and the UK register
- [Google Ads Transparency API](https://scavio.dev/docs/google-ads-advertisers) and [Meta Ad Library API](https://scavio.dev/docs/meta-ads-search) — live competitor creatives
- [YouTube API](https://scavio.dev/youtube-transcript-api), [TikTok API](https://scavio.dev/tiktok-api), and [Instagram API](https://scavio.dev/instagram-api) — video and social media data
- TikTok Shop — product detail, reviews, categories, and seller catalogs
- [Threads API](https://scavio.dev/docs/threads-profile) and [Kuaishou API](https://scavio.dev/docs/kuaishou-profile) — profiles, posts and search
- [Reddit API](https://scavio.dev/reddit-api) — posts and threaded comments
- X (formerly Twitter) and LinkedIn — profiles, posts, and search
- [Extract](https://scavio.dev/docs/extract) — read any URL as clean Markdown, plain text or raw HTML

Get a free [API key](https://dashboard.scavio.dev) and explore the [documentation](https://scavio.dev/docs/introduction). You can also [compare Scavio vs alternatives](https://scavio.dev/compare) on coverage and pricing.
