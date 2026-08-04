# autogen-scavio

AutoGen integration for the [Scavio Search API](https://scavio.dev?utm_source=autogen_integration), a [search API for AI agents](https://scavio.dev/search-api-for-ai-agents). Provides 97 search tools across Google, Amazon, Walmart, YouTube, Reddit, TikTok, TikTok Shop, Instagram, X and LinkedIn for use with AutoGen AI agents.

| Provider | Tools | Coverage |
|----------|------:|----------|
| Google | 14 | Every v2 endpoint: search, AI Mode, Maps, Shopping, Flights, Hotels, News, Trends |
| YouTube | 15 | Every live endpoint |
| Instagram | 12 | Every endpoint |
| Reddit | 12 | Every endpoint |
| TikTok | 11 | Every endpoint |
| X (formerly Twitter) | 11 | Every endpoint |
| LinkedIn | 9 | Every live endpoint |
| TikTok Shop | 8 | Every endpoint |
| Amazon | 3 | Search, product, offers |
| Walmart | 2 | Search, product |

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

# Providers: google, amazon, youtube, walmart, reddit, tiktok, tiktok_shop,
# instagram, x, linkedin

# Individual tool factories
from autogen_scavio import create_web_search_tool, create_amazon_search_tool

web_tool = create_web_search_tool(max_results=10)
amazon_tool = create_amazon_search_tool(max_results=5)
```

> **Amazon changed in 0.4.0 (breaking).** The upstream provider moved. `domain`
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

## Available Tools

| Provider | Tool | Description |
|----------|------|-------------|
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
| YouTube | `scavio_youtube_transcript` | Transcript as plain text or SRT (8 credits) |
| YouTube | `scavio_youtube_related` | Videos related to a video |
| YouTube | `scavio_youtube_channel_search` | Channel search by keyword |
| YouTube | `scavio_youtube_channel` | Channel profile by ID, @handle, or URL |
| YouTube | `scavio_youtube_channel_videos` | A channel's uploaded videos |
| YouTube | `scavio_youtube_channel_shorts` | A channel's Shorts |
| YouTube | `scavio_youtube_channel_community` | A channel's community posts (`data.posts`) |
| YouTube | `scavio_youtube_channel_resolve` | Resolve an @handle or URL to a channel ID |
| YouTube | `scavio_youtube_streams` | Playable stream URLs for a video (3 credits) |
| Walmart | `scavio_walmart_search` | Product search with price/fulfillment filters |
| Walmart | `scavio_walmart_product` | Product details by ID |
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

### Credits

Every tool states its own cost in its description, so the agent sees the price
before it picks. Most endpoints are 1 credit; these are the exceptions:

| Tools | Credits |
|-------|--------:|
| `scavio_youtube_search`, `scavio_youtube_shorts` | 2 |
| `scavio_youtube_streams` | 3 |
| `scavio_youtube_transcript` | 8 |
| `scavio_instagram_user_posts` | 2 |
| `scavio_instagram_post`, `scavio_instagram_comment_replies` | 8 |
| Every other Instagram tool | 10 |
| `scavio_linkedin_person_posts`, `scavio_linkedin_company_posts`, `scavio_linkedin_search_jobs`, `scavio_linkedin_post_comments` | 10 |
| `scavio_linkedin_job` | 30 |

All 14 Google tools, all 11 X tools, the remaining LinkedIn tools and
everything under Amazon, Walmart, Reddit, TikTok and TikTok Shop are 1 credit.

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
- [YouTube API](https://scavio.dev/youtube-transcript-api), [TikTok API](https://scavio.dev/tiktok-api), and [Instagram API](https://scavio.dev/instagram-api) — video and social media data
- TikTok Shop — product detail, reviews, categories, and seller catalogs
- [Reddit API](https://scavio.dev/reddit-api) — posts and threaded comments
- X (formerly Twitter) and LinkedIn — profiles, posts, and search

Get a free [API key](https://dashboard.scavio.dev) and explore the [documentation](https://scavio.dev/docs/introduction). You can also [compare Scavio vs alternatives](https://scavio.dev/compare) on coverage and pricing.
