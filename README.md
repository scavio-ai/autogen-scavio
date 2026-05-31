# autogen-scavio

AutoGen integration for the [Scavio Search API](https://scavio.dev). Provides 20 search tools across Google, Amazon, Walmart, YouTube, Reddit, and TikTok for use with AutoGen AI agents.

## Installation

```bash
pip install autogen-scavio
```

## Setup

Get a free API key at [dashboard.scavio.dev](https://dashboard.scavio.dev) and set it as an environment variable:

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
    model_client=OpenAIChatCompletionClient(model="gpt-4o"),
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

## Available Tools

| Provider | Tool | Description |
|----------|------|-------------|
| Google | `scavio_web_search` | Web search with knowledge graphs and related questions |
| Amazon | `scavio_amazon_search` | Product search across 20+ marketplaces |
| Amazon | `scavio_amazon_product` | Product details by ASIN |
| YouTube | `scavio_youtube_search` | Video search with filters |
| YouTube | `scavio_youtube_metadata` | Video metadata by ID |
| Walmart | `scavio_walmart_search` | Product search with price/fulfillment filters |
| Walmart | `scavio_walmart_product` | Product details by ID |
| Reddit | `scavio_reddit_search` | Post and comment search |
| Reddit | `scavio_reddit_post` | Post metadata and comments by URL |
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

## Configuration

```python
from autogen_scavio import configure

# Set API key programmatically
configure(api_key="sk_live_...")

# Or pass to factory
tools = create_scavio_tools(api_key="sk_live_...", max_results=10)
```
