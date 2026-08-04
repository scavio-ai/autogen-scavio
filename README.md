# autogen-scavio

AutoGen integration for the [Scavio Search API](https://scavio.dev?utm_source=autogen_integration), a [search API for AI agents](https://scavio.dev/search-api-for-ai-agents). Provides 46 search tools across Google, Amazon, Walmart, YouTube, Reddit, TikTok, TikTok Shop, and Instagram for use with AutoGen AI agents. Scavio also covers X and LinkedIn; those are not wrapped as AutoGen tools yet, call them through the [Python SDK](https://pypi.org/project/scavio/).

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

## Available Tools

| Provider | Tool | Description |
|----------|------|-------------|
| Google | `scavio_web_search` | Web search with knowledge graphs and related questions |
| Amazon | `scavio_amazon_search` | Product search across 22 marketplaces |
| Amazon | `scavio_amazon_product` | Product details by ASIN |
| Amazon | `scavio_amazon_offers` | Every seller offer for an ASIN, including the buy-box winner |
| YouTube | `scavio_youtube_search` | Video search with filters (2 credits) |
| YouTube | `scavio_youtube_video` | Full video details by ID or watch URL |
| YouTube | `scavio_youtube_comments` | Top-level comments on a video |
| YouTube | `scavio_youtube_transcript` | Transcript as plain text or SRT (8 credits) |
| YouTube | `scavio_youtube_channel` | Channel profile by ID, @handle, or URL |
| YouTube | `scavio_youtube_channel_videos` | A channel's uploaded videos |
| YouTube | `scavio_youtube_streams` | Playable stream URLs for a video (3 credits) |
| Walmart | `scavio_walmart_search` | Product search with price/fulfillment filters |
| Walmart | `scavio_walmart_product` | Product details by ID |
| Reddit | `scavio_reddit_search` | Post search (query and cursor only) |
| Reddit | `scavio_reddit_post` | Post metadata by URL, without comments |
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

Most endpoints cost 1 credit. The exceptions are noted in the table above plus
Instagram, which is priced per endpoint: 10 credits by default, 8 for
`scavio_instagram_post` and `scavio_instagram_comment_replies`, and 2 for
`scavio_instagram_user_posts`.

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
