"""Shared fixtures and mock response builders for Scavio AutoGen tests."""

from __future__ import annotations


def mock_search_response(num_results: int = 10) -> dict:
    """The flat /api/v2/google body: organic_results with link/snippet."""
    return {
        "search_parameters": {"q": "test query"},
        "credits_used": 1,
        "credits_remaining": 999,
        "organic_results": [
            {
                "title": f"Result {i}",
                "link": f"https://example.com/{i}",
                "snippet": f"Snippet {i}",
                "position": i,
            }
            for i in range(1, num_results + 1)
        ],
        "knowledge_graph": {"title": "Test", "subtitle": "A test entity"},
        "related_questions": [{"question": "What is test?", "answer": "A test."}],
        "related_searches": [{"query": "test 2"}],
        "ai_overview": {"text_blocks": [{"snippet": "An overview."}]},
    }


def mock_amazon_search_response(num_products: int = 10) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "products": [
                {
                    "asin": f"B00{i}",
                    "title": f"Product {i}",
                    "price": 29.99 + i,
                    "currency": "USD",
                    "rating": 4.5,
                    "reviews_count": 100 + i,
                }
                for i in range(1, num_products + 1)
            ],
        },
    }


def mock_amazon_product_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "asin": "B001",
            "title": "Test Product",
            "price": 29.99,
            "list_price": 39.99,
            "currency": "USD",
        },
    }


def mock_youtube_search_response(num_results: int = 10) -> dict:
    return {
        "credits_used": 2,
        "data": {
            "results": [
                {
                    "video_id": f"vid_{i}",
                    "title": f"Video {i}",
                    "channel": f"Channel {i}",
                    "view_count": 1000 * i,
                }
                for i in range(1, num_results + 1)
            ],
        },
    }


def mock_youtube_metadata_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "video_id": "vid_1",
            "title": "Test Video",
            "channel": "Test Channel",
            "view_count": 10000,
        },
    }


def mock_youtube_video_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "video_id": "vid_1",
            "title": "Test Video",
            "author": "Test Channel",
            "channel_id": "chan_1",
            "view_count": 10000,
            "length_seconds": 300,
            "captions": [
                {"language_code": "en", "language_name": "English", "url": "https://x/1"},
            ],
        },
    }


def mock_youtube_comments_response(num_comments: int = 10) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "comments": [
                {
                    "comment_id": f"c_{i}",
                    "text": f"Comment {i}",
                    "like_count": i * 10,
                    "reply_count": i,
                    "author": {"channel_id": f"chan_{i}", "name": f"user_{i}"},
                }
                for i in range(1, num_comments + 1)
            ],
            "next_cursor": "next",
            "has_more": True,
        },
    }


def mock_youtube_transcript_response() -> dict:
    return {
        "credits_used": 8,
        "data": {
            "video_id": "vid_1",
            "language_code": "en",
            "language_name": "English",
            "format": "txt",
            "content": "This is a transcript.",
        },
    }


def mock_youtube_channel_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "channel_id": "chan_1",
            "title": "Test Channel",
            "description": "A test channel.",
            "subscriber_count": 509000000,
            "video_count": 993,
            "view_count": 134561410625,
        },
    }


def mock_youtube_channel_videos_response(num_results: int = 10) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "channel_id": "chan_1",
            "results": [
                {
                    "video_id": f"vid_{i}",
                    "title": f"Video {i}",
                    "view_count": 1000 * i,
                    "duration_text": "10:00",
                    "is_live": False,
                }
                for i in range(1, num_results + 1)
            ],
            "next_cursor": "next",
            "has_more": True,
        },
    }


def mock_youtube_streams_response() -> dict:
    return {
        "credits_used": 3,
        "data": {
            "video_id": "vid_1",
            "title": "Test Video",
            "author": "Test Channel",
            "length_seconds": 300,
            "view_count": 10000,
            "is_live": False,
            "formats": [
                {"itag": 18, "url": "https://x/stream", "mime_type": "video/mp4"},
            ],
            "available_qualities": ["720p", "360p"],
        },
    }


def mock_walmart_search_response(num_products: int = 10) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "products": [
                {
                    "product_id": f"WM{i}",
                    "title": f"Product {i}",
                    "price": 19.99 + i,
                }
                for i in range(1, num_products + 1)
            ],
        },
    }


def mock_walmart_product_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "product_id": "WM1",
            "title": "Test Product",
            "price": 19.99,
        },
    }


def mock_reddit_search_response(num_posts: int = 10) -> dict:
    """/reddit/search returns data.results, not data.posts."""
    return {
        "credits_used": 1,
        "data": {
            "results": [
                {
                    "post_id": f"t3_post_{i}",
                    "title": f"Post {i}",
                    "subreddit": "test",
                    "author": f"user_{i}",
                    "score": 10 * i,
                }
                for i in range(1, num_posts + 1)
            ],
            "next_cursor": "next",
            "has_more": True,
        },
    }


def mock_reddit_post_response() -> dict:
    """/reddit/post returns a flat post object and no comments."""
    return {
        "credits_used": 1,
        "data": {
            "post_id": "t3_post_1",
            "title": "Test Post",
            "text": "Test body",
            "url": "https://reddit.com/r/test/comments/post_1/test",
            "subreddit": "test",
            "author": "user_1",
            "score": 42,
            "upvote_ratio": 0.97,
            "num_comments": 3,
            "created_at": "2026-08-01T00:00:00Z",
            "is_nsfw": False,
            "is_video": False,
            "thumbnail": None,
            "media": [],
        },
    }


def mock_reddit_suggestions_response(num_suggestions: int = 10) -> dict:
    """/reddit/search/suggestions returns plain strings."""
    return {
        "credits_used": 1,
        "data": {
            "suggestions": [f"python {i}" for i in range(1, num_suggestions + 1)],
            "total_count": num_suggestions,
        },
    }


def mock_reddit_comments_response(num_comments: int = 10) -> dict:
    """/reddit/post/comments: comments carry depth and reply_cursor."""
    return {
        "credits_used": 1,
        "data": {
            "comments": [
                {
                    "comment_id": f"t1_c_{i}",
                    "text": f"Comment {i}",
                    "author": f"user_{i}",
                    "score": 10 * i,
                    "created_at": "2026-08-01T00:00:00Z",
                    "depth": 0,
                    "reply_cursor": f"reply_{i}",
                }
                for i in range(1, num_comments + 1)
            ],
            "next_cursor": "next",
            "has_more": True,
        },
    }


def mock_reddit_replies_response(num_replies: int = 10) -> dict:
    """/reddit/post/comments/replies returns data.replies, not data.comments."""
    return {
        "credits_used": 1,
        "data": {
            "replies": [
                {
                    "comment_id": f"t1_r_{i}",
                    "text": f"Reply {i}",
                    "author": f"user_{i}",
                    "score": i,
                    "created_at": "2026-08-01T00:00:00Z",
                    "depth": 1,
                    "reply_cursor": None,
                }
                for i in range(1, num_replies + 1)
            ],
            "next_cursor": "next",
            "has_more": True,
        },
    }


def mock_reddit_subreddit_response() -> dict:
    """/reddit/subreddit is a flat object, no posts."""
    return {
        "credits_used": 1,
        "data": {
            "id": "t5_2qh1i",
            "name": "AskReddit",
            "prefixed_name": "r/AskReddit",
            "title": "Ask Reddit...",
            "description": "A place to ask questions.",
            "public_description": "Ask and answer thought-provoking questions.",
            "subscribers": 45000000,
            "active_count": 12000,
            "type": "public",
            "is_nsfw": False,
            "icon": None,
            "banner": None,
            "primary_color": "#0079d3",
            "created_at": "2008-01-25T00:00:00Z",
            "url": "https://www.reddit.com/r/AskReddit/",
        },
    }


def mock_reddit_feed_response(num_posts: int = 10) -> dict:
    """subreddit/posts, user/posts and popular all return data.posts."""
    return {
        "credits_used": 1,
        "data": {
            "posts": [
                {
                    "post_id": f"t3_post_{i}",
                    "title": f"Post {i}",
                    "subreddit": "test",
                    "author": f"user_{i}",
                    "score": 10 * i,
                    "num_comments": i,
                    "url": f"https://reddit.com/r/test/comments/post_{i}/test",
                    "created_at": "2026-08-01T00:00:00Z",
                }
                for i in range(1, num_posts + 1)
            ],
            "next_cursor": "next",
            "has_more": True,
        },
    }


def mock_reddit_user_response() -> dict:
    """/reddit/user is a flat profile object."""
    return {
        "credits_used": 1,
        "data": {
            "id": "t2_1w72",
            "name": "spez",
            "is_employee": True,
            "is_verified": True,
            "account_type": "user",
            "is_accepting_pms": True,
            "is_nsfw": False,
            "avatar": "https://styles.redditmedia.com/avatar.png",
            "karma": 900000,
            "post_karma": 200000,
            "comment_karma": 700000,
            "description": "reddit ceo",
            "created_at": "2005-06-06T00:00:00Z",
        },
    }


def mock_reddit_user_comments_response(num_comments: int = 10) -> dict:
    """/reddit/user/comments nests the post and has no depth or reply_cursor."""
    return {
        "credits_used": 1,
        "data": {
            "comments": [
                {
                    "comment_id": f"t1_uc_{i}",
                    "text": f"User comment {i}",
                    "author": "spez",
                    "post": {"id": f"t3_post_{i}", "title": f"Post {i}"},
                    "score": 5 * i,
                    "created_at": "2026-08-01T00:00:00Z",
                }
                for i in range(1, num_comments + 1)
            ],
            "next_cursor": "next",
            "has_more": True,
        },
    }


def mock_reddit_trending_response(num_trends: int = 10) -> dict:
    """/reddit/trending returns data.trending, not data.trends."""
    return {
        "credits_used": 1,
        "data": {
            "trending": [
                {"query": f"trend {i}", "raw_query": f"trend{i}"}
                for i in range(1, num_trends + 1)
            ],
            "total_count": num_trends,
        },
    }


def mock_tiktok_profile_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "user": {
                "username": "testuser",
                "followers": 1000,
                "following": 500,
            },
        },
    }


def mock_tiktok_video_list_response(
    num_items: int = 10, key: str = "aweme_list"
) -> dict:
    return {
        "credits_used": 1,
        "data": {
            key: [
                {
                    "aweme_id": f"vid_{i}",
                    "desc": f"Video {i}",
                    "statistics": {"play_count": 1000 * i},
                }
                for i in range(1, num_items + 1)
            ],
            "has_more": 1,
        },
    }


def mock_tiktok_comments_response(num_comments: int = 10) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "comments": [
                {
                    "cid": f"c_{i}",
                    "text": f"Comment {i}",
                    "digg_count": i * 10,
                }
                for i in range(1, num_comments + 1)
            ],
            "has_more": 1,
        },
    }


def mock_tiktok_search_videos_response(num_items: int = 10) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "search_item_list": [
                {
                    "aweme_id": f"vid_{i}",
                    "desc": f"Search result {i}",
                }
                for i in range(1, num_items + 1)
            ],
        },
    }


def mock_tiktok_users_response(num_users: int = 10) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "user_list": [
                {
                    "username": f"user_{i}",
                    "followers": 100 * i,
                }
                for i in range(1, num_users + 1)
            ],
        },
    }


def mock_tiktok_hashtag_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "challengeInfo": {
                "challenge": {"title": "test", "video_count": 1000},
            },
        },
    }


def mock_tiktok_followers_response(
    num_items: int = 10, key: str = "followers"
) -> dict:
    return {
        "credits_used": 1,
        "data": {
            key: [
                {"username": f"follower_{i}", "followers": 50 * i}
                for i in range(1, num_items + 1)
            ],
            "has_more": True,
        },
    }


# -- TikTok Shop ------------------------------------------------------------
#
# These are the NORMALIZED shapes the backend emits, produced by running the
# backend's TikTok Shop normalizer over the recorded fixtures in
# backend/tests/fixtures/tiktok-shop/. The key names here are the key names the
# tools must read.


def mock_tiktok_shop_card(i: int = 1) -> dict:
    return {
        "product_id": f"17324831328036832{i:02d}",
        "title": f"Phone Case {i}",
        "url": f"https://shop.tiktok.com/us/pdp/17324831328036832{i:02d}",
        "image": "https://p19-oec-general.ttcdn-us.com/image.webp",
        "price": {
            "current": 4.88,
            "original": None,
            "currency": "USD",
            "discount_percent": None,
            "savings": None,
            "min": 4.88,
            "max": 7.88,
        },
        "rating": {"score": 4.7, "review_count": 15},
        "sold_count": 103,
        "variant_count": 25,
        "brand": None,
        "shop": {
            "shop_id": "7494676034572093351",
            "shop_name": "AmiShell",
            "shop_logo": "https://p16-oec-general.ttcdn-us.com/logo.png",
        },
        "labels": ["Free shipping"],
    }


def mock_tiktok_shop_search_response(num_products: int = 30) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "query": "phone case",
            "products": [mock_tiktok_shop_card(i) for i in range(1, num_products + 1)],
            "shops": [],
            "next_cursor": "eyJrIjoic2VhcmNoIiwibyI6MzB9",
            "has_more": True,
            "degraded": False,
        },
    }


def mock_tiktok_shop_suggestions_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "query": "wireless",
            "region": "GB",
            "suggestions": ["wireless charger", "wireless headphones"],
        },
    }


def mock_tiktok_shop_product_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "product_id": "1732293553906094315",
            "title": "NAD+ EGF Firming Serum",
            "description": "Plain text description.",
            "url": "https://shop.tiktok.com/us/pdp/1732293553906094315",
            "images": ["https://p19-oec-general.ttcdn-us.com/img.webp"],
            # Upstream masks every price on the product page: current and
            # original are always null here.
            "price": {
                "currency": "USD",
                "current": None,
                "original": None,
                "discount_percent": 31,
                "savings": None,
            },
            "rating": {
                "score": 4.7,
                "review_count": 12561,
                "distribution": {
                    "1": 431, "2": 221, "3": 571, "4": 1175, "5": 10163,
                },
            },
            "sold_count": 231615,
            "variants": [
                {
                    "sku_id": "1732293560756310251",
                    "name": "PMEUS43022R00",
                    "in_stock": True,
                    "available_quantity": 64657,
                    "properties": [],
                    "weight_kg": 0.1,
                    "dimensions_cm": {"length": 7.0, "width": 3.0, "height": 3.0},
                }
            ],
            "shipping": {"fee": 4.22, "currency": "USD", "fulfillable": True},
            "shop": {
                "shop_id": "7495514739648989419",
                "shop_name": "medicube US Store",
                "followers_count": 588860,
                "is_official": True,
            },
            "categories": [],
            "breadcrumbs": [],
            "top_reviews": [],
            "seller": {"business_name": "APR US INC", "business_address": "Irvine"},
        },
    }


def mock_tiktok_shop_reviews_response(num_reviews: int = 20) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "product_id": "1732293553906094315",
            "page": 1,
            "page_size": 20,
            "filters_applied": {
                "sort": "relevant",
                "rating": None,
                "has_media": False,
                "verified_only": False,
            },
            "total_reviews": 12561,
            "rating": {
                "score": 4.6,
                "review_count": 12561,
                "distribution": {
                    "1": 431, "2": 221, "3": 571, "4": 1175, "5": 10163,
                },
            },
            "reviews": [
                {
                    "review_id": f"763255059759346663{i}",
                    "rating": 5,
                    "text": f"Review body {i}",
                    "created_at": "2026-04-25T04:34:57.611Z",
                    "reviewer_name": "C**",
                    "reviewer_avatar": "https://p16-common-sign.tiktokcdn-us.com/a.jpg",
                    "images": [],
                    "is_verified_purchase": True,
                    "is_incentivized": False,
                    "variant": "Default",
                    "country": "US",
                }
                for i in range(1, num_reviews + 1)
            ],
            "has_more": True,
        },
    }


def mock_tiktok_shop_categories_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "categories": [
                {
                    "category_id": "601450",
                    "name": "Beauty & Personal Care",
                    "slug": "beauty-personal-care",
                    "level": 1,
                    "parent_id": None,
                    "image": "https://lf16-tiktok-common.tiktokcdn-us.com/b.png",
                    "children": [
                        {
                            "category_id": "849032",
                            "name": "Hand & Foot Care",
                            "slug": "hand-foot-care",
                            "level": 2,
                            "parent_id": "601450",
                            "image": None,
                            "children": [],
                        }
                    ],
                }
            ],
            "total_categories": 240,
        },
    }


def mock_tiktok_shop_category_products_response(num_products: int = 15) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "category_id": "601450",
            "products": [mock_tiktok_shop_card(i) for i in range(1, num_products + 1)],
            "next_cursor": "eyJrIjoiY2F0ZWdvcnkiLCJvIjoyMH0",
            "has_more": True,
        },
    }


def mock_tiktok_shop_shop_products_response(num_products: int = 30) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "shop_id": "7495514739648989419",
            "shop": {
                "shop_id": "7495514739648989419",
                "shop_name": "medicube US Store",
                "shop_logo": "https://p16-oec-general.ttcdn-us.com/logo.png",
            },
            "products": [mock_tiktok_shop_card(i) for i in range(1, num_products + 1)],
            "next_cursor": "eyJrIjoic2hvcCIsInMiOiIzMF9XemN5In0",
            "has_more": True,
        },
    }


def mock_tiktok_shop_resolve_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "type": "product",
            "product_id": "8651224669119091502",
            "shop_id": None,
            "url": "https://shop.tiktok.com/us/pdp/8651224669119091502",
            "resolved_by": "share_link",
        },
    }


# -- Google v2 verticals ----------------------------------------------------
#
# Google responses are FLAT: the payload sits at the top level next to
# credits_used / credits_remaining / cached. There is no data wrapper anywhere
# in this family.


def _flat(payload: dict) -> dict:
    return {"credits_used": 1, "credits_remaining": 999, "cached": False, **payload}


def mock_google_ai_mode_response(num_references: int = 10) -> dict:
    return _flat(
        {
            "text_blocks": [{"type": "paragraph", "snippet": "An answer."}],
            "references": [
                {"title": f"Source {i}", "link": f"https://example.com/{i}"}
                for i in range(1, num_references + 1)
            ],
        }
    )


def mock_google_maps_search_response(num_results: int = 10) -> dict:
    return _flat(
        {
            "local_results": [
                {
                    "position": i,
                    "title": f"Cafe {i}",
                    "place_id": f"ChIJ_{i}",
                    "data_id": f"0x89c2:0x{i}",
                    "rating": 4.5,
                    "address": f"{i} Main St",
                }
                for i in range(1, num_results + 1)
            ],
        }
    )


def mock_google_maps_place_response() -> dict:
    return _flat(
        {
            "place_results": {
                "title": "Cafe 1",
                "place_id": "ChIJ_1",
                "rating": 4.5,
                "phone": "+1 555 0100",
            },
        }
    )


def mock_google_maps_reviews_response(num_reviews: int = 10) -> dict:
    return _flat(
        {
            "place_info": {"title": "Cafe 1"},
            "reviews": [
                {"rating": 5, "snippet": f"Review {i}", "user": {"name": f"user_{i}"}}
                for i in range(1, num_reviews + 1)
            ],
            "pagination": {"next_page_token": "next"},
        }
    )


def mock_google_shopping_response(num_results: int = 10) -> dict:
    return _flat(
        {
            "shopping_results": [
                {
                    "position": i,
                    "title": f"Product {i}",
                    "price": f"${i}.99",
                    "catalog_id": f"cat_{i}",
                }
                for i in range(1, num_results + 1)
            ],
            "pagination": {"next": 60},
        }
    )


def mock_google_shopping_product_response() -> dict:
    return _flat(
        {
            "product_results": {
                "title": "Product 1",
                "rating": 4.4,
                "stores": [{"name": "Store 1", "price": "$9.99"}],
            },
        }
    )


def mock_google_shopping_stores_response(num_stores: int = 10) -> dict:
    return _flat(
        {
            "product_results": {
                "stores": [
                    {"name": f"Store {i}", "price": f"${i}.99"}
                    for i in range(1, num_stores + 1)
                ],
            },
        }
    )


def mock_google_flights_response(num_flights: int = 10) -> dict:
    return _flat(
        {
            "best_flights": [
                {"price": 200 + i, "total_duration": 320}
                for i in range(1, num_flights + 1)
            ],
            "other_flights": [
                {"price": 400 + i, "total_duration": 520}
                for i in range(1, num_flights + 1)
            ],
        }
    )


def mock_google_hotels_response(num_properties: int = 10) -> dict:
    return _flat(
        {
            "properties": [
                {
                    "name": f"Hotel {i}",
                    "detail_token": f"tok_{i}",
                    "rate_per_night": {"lowest": f"${100 + i}"},
                }
                for i in range(1, num_properties + 1)
            ],
        }
    )


def mock_google_hotels_detail_response() -> dict:
    return _flat(
        {
            "property": {
                "name": "Hotel 1",
                "booking_sources": [{"name": "Booking.com", "rate": "$120"}],
            },
        }
    )


def mock_google_news_response(num_results: int = 10) -> dict:
    return _flat(
        {
            "news_results": [
                {
                    "title": f"Headline {i}",
                    "link": f"https://news.example.com/{i}",
                    "source": {"name": f"Source {i}"},
                }
                for i in range(1, num_results + 1)
            ],
        }
    )


def mock_google_trends_response() -> dict:
    return _flat(
        {
            "interest_over_time": {
                "timeline_data": [{"date": "Jan 2026", "values": [{"value": "100"}]}],
            },
            "interest_by_region": [{"location": "California", "value": 100}],
        }
    )


def mock_google_trending_response(num_trends: int = 10) -> dict:
    return _flat(
        {
            "trends": [
                {"query": f"trend {i}", "search_volume": 1000 * i}
                for i in range(1, num_trends + 1)
            ],
        }
    )


# -- YouTube (endpoints added in 0.5.0) -------------------------------------


def mock_youtube_suggestions_response(num_suggestions: int = 10) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "suggestions": [f"python {i}" for i in range(1, num_suggestions + 1)],
            "total_count": num_suggestions,
        },
    }


def mock_youtube_replies_response(num_replies: int = 10) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "replies": [
                {"comment_id": f"r_{i}", "text": f"Reply {i}", "like_count": i}
                for i in range(1, num_replies + 1)
            ],
            "next_cursor": "next",
            "has_more": True,
        },
    }


def mock_youtube_channel_search_response(num_results: int = 10) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "results": [
                {
                    "channel_id": f"chan_{i}",
                    "name": f"Channel {i}",
                    "handle": f"@chan{i}",
                    "subscriber_count": 1000 * i,
                    "verified": True,
                }
                for i in range(1, num_results + 1)
            ],
            "next_cursor": "next",
            "has_more": True,
            "total_count": num_results,
        },
    }


def mock_youtube_channel_community_response(num_posts: int = 10) -> dict:
    """The only YouTube endpoint whose list key is posts, not results."""
    return {
        "credits_used": 1,
        "data": {
            "channel_id": "chan_1",
            "posts": [
                {
                    "post_id": f"p_{i}",
                    "text": f"Community post {i}",
                    "vote_count": 10 * i,
                    "comment_count": i,
                }
                for i in range(1, num_posts + 1)
            ],
            "next_cursor": "next",
            "has_more": True,
        },
    }


def mock_youtube_channel_resolve_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "channel_id": "UCX6OQ3DkcsbYNE6H8uQQuVA",
            "channel_url": "https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA",
        },
    }


# -- X (formerly Twitter) ---------------------------------------------------


def mock_x_tweet(i: int = 1) -> dict:
    return {
        "tweet_id": f"180816860372165036{i}",
        "screen_name": "elonmusk",
        "text": f"Tweet {i}",
        "created_at": "2026-08-01T00:00:00Z",
        "favorites": 100 * i,
        "retweets": 10 * i,
        "replies": i,
        "views": 1000 * i,
        "author": {"user_id": "44196397", "screen_name": "elonmusk"},
        "media": None,
    }


def mock_x_timeline_response(num_tweets: int = 10, has_more: bool = True) -> dict:
    """search / tweet comments / user timelines all return data.timeline."""
    return {
        "credits_used": 1,
        "data": {
            "timeline": [mock_x_tweet(i) for i in range(1, num_tweets + 1)],
            "next_cursor": "next",
            "prev_cursor": None,
            "has_more": has_more,
        },
    }


def mock_x_tweet_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            **mock_x_tweet(1),
            "reply_to": None,
            "in_reply_to_screen_name": None,
            "sensitive": False,
        },
    }


def mock_x_user_brief(i: int = 1) -> dict:
    return {
        "user_id": f"user_{i}",
        "screen_name": f"user_{i}",
        "name": f"User {i}",
        "followers_count": 100 * i,
        "friends_count": 50 * i,
        "profile_image": f"https://x/{i}.jpg",
        "blue_verified": False,
    }


def mock_x_retweeters_response(num_users: int = 10) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "retweeters": [mock_x_user_brief(i) for i in range(1, num_users + 1)],
            "next_cursor": "next",
            "has_more": True,
        },
    }


def mock_x_user_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "user_id": "44196397",
            "screen_name": "elonmusk",
            "name": "Elon Musk",
            "description": "bio",
            "followers_count": 220000000,
            "friends_count": 1000,
            "statuses_count": 50000,
            "media_count": 5000,
            "blue_verified": True,
            "avatar": "https://x/avatar.jpg",
        },
    }


def mock_x_followers_response(num_users: int = 10) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "followers_count": 220000000,
            "followers": [mock_x_user_brief(i) for i in range(1, num_users + 1)],
            "next_cursor": "next",
            "more_users": True,
            "has_more": True,
        },
    }


def mock_x_followings_response(num_users: int = 10) -> dict:
    """Key quirk: the array is `following`, singular, not `followings`."""
    return {
        "credits_used": 1,
        "data": {
            "following": [mock_x_user_brief(i) for i in range(1, num_users + 1)],
            "next_cursor": "next",
            "more_users": True,
            "has_more": True,
        },
    }


def mock_x_trending_response(num_trends: int = 10) -> dict:
    return {
        "credits_used": 1,
        "data": {
            "trends": [
                {"name": f"#trend{i}", "description": None, "context": f"{i}K posts"}
                for i in range(1, num_trends + 1)
            ],
        },
    }


# -- LinkedIn ---------------------------------------------------------------


def mock_linkedin_person_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "id": "251749025",
            "public_identifier": "williamhgates",
            "full_name": "Bill Gates",
            "headline": "Co-chair, Gates Foundation",
            "about": "Sharing things I'm learning.",
            "location": "Seattle",
            "follower_count": 36000000,
            "connection_count": 12,
            "current_company": {"name": "Gates Foundation", "title": "Co-chair"},
            "experiences": [],
            "educations": [],
        },
    }


def mock_linkedin_person_about_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "about": "Sharing things I'm learning.",
            "headline": "Co-chair, Gates Foundation",
            "education_summary": "Harvard University",
            "experiences": [],
            "educations": [],
            "honors_and_awards": [],
            "bio_links": [],
        },
    }


def mock_linkedin_feed_response(num_posts: int = 10) -> dict:
    """person/posts, company/posts and search/jobs all nest under data.data."""
    return {
        "credits_used": 10,
        "data": {
            "data": [
                {
                    "id": f"urn:li:activity:{i}",
                    "text": f"Post {i}",
                    "url": f"https://www.linkedin.com/feed/update/{i}",
                    "num_comments": i,
                    "num_reposts": i,
                    "reactions": {"total": 100 * i},
                }
                for i in range(1, num_posts + 1)
            ],
            "count": num_posts,
            "has_more": True,
            "next_cursor": "next",
        },
    }


def mock_linkedin_company_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "id": "1035",
            "universal_name": "microsoft",
            "name": "Microsoft",
            "website": "https://www.microsoft.com",
            "industries": ["Software Development"],
            "employee_count": 240000,
            "follower_count": 23000000,
            "headquarters": "Redmond, Washington",
            "featured_employees": [
                {"name": "Satya Nadella", "url": "https://www.linkedin.com/in/satyanadella"},
            ],
        },
    }


def mock_linkedin_jobs_response(num_jobs: int = 10) -> dict:
    return {
        "credits_used": 10,
        "data": {
            "data": [
                {
                    "id": f"441542722{i}",
                    "title": f"Software Engineer {i}",
                    "company": f"Company {i}",
                    "location": "Remote",
                    "workplace_type": "Remote",
                    "salary": None,
                }
                for i in range(1, num_jobs + 1)
            ],
            "count": num_jobs,
            "has_more": True,
            "next_cursor": "next",
        },
    }


def mock_linkedin_job_response() -> dict:
    return {
        "credits_used": 30,
        "data": {
            "id": "4415427228",
            "title": "Software Engineer",
            "description": "Build things.",
            "location": "Seattle, WA",
            "employment_type": "Full-time",
            "is_remote": False,
            "applicant_count": 42,
            "company": {"id": "1035", "name": "Microsoft"},
        },
    }


def mock_linkedin_post_response() -> dict:
    return {
        "credits_used": 1,
        "data": {
            "id": "7488618410256523265",
            "text": "A post.",
            "url": "https://www.linkedin.com/feed/update/urn:li:activity:7488618410256523265/",
            "num_likes": 500,
            "num_comments": 30,
            "hashtags": ["ai"],
            "top_comments": [],
            "author": {"public_identifier": "williamhgates", "full_name": "Bill Gates"},
        },
    }


def mock_linkedin_post_comments_response(num_comments: int = 10) -> dict:
    """post/comments pages by number and has no next_cursor."""
    return {
        "credits_used": 10,
        "data": {
            "data": [
                {
                    "text": f"Comment {i}",
                    "created_at": "2026-08-01T00:00:00Z",
                    "is_pinned": False,
                    "author": {"full_name": f"User {i}"},
                    "replies": [],
                }
                for i in range(1, num_comments + 1)
            ],
            "page": 1,
            "total": num_comments,
            "has_more": True,
            "next_page": 2,
        },
    }


class MockNotFoundError(Exception):
    """Stands in for the SDK's NotFoundError, which carries status_code 404."""

    status_code = 404
