"""Scavio X (formerly Twitter) tools for AutoGen.

All eleven endpoints cost 1 credit per call. Two wire quirks matter: the search
field is `search`, not `query`, and the followings endpoint returns its list
under data.following (singular), not data.followings.
"""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list


def create_x_search_tool(max_results: int = 5) -> FunctionTool:
    """Create an X search tool with the given configuration."""

    async def scavio_x_search(
        search: str,
        search_type: str | None = None,
        cursor: str | None = None,
    ) -> str:
        """Search X for tweets and people.

        Args:
            search: The X search query, 1 to 500 characters. The field is
                search, not query.
            search_type: Result category, one of "Top", "Latest", "People",
                "Photos", "Videos". Capitalized and case-sensitive; defaults
                to "Top".
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with matching tweets under data.timeline, plus
            next_cursor, prev_cursor and has_more.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "search": search,
            "search_type": search_type,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.x.search(**params)

        truncate_list(raw, ["data", "timeline"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_x_search,
        description=(
            "Search X for tweets and people (1 credit). Each result carries "
            "the tweet id, author, text, timestamp and engagement counts. "
            "Page with data.next_cursor while data.has_more."
        ),
    )


def create_x_tweet_tool() -> FunctionTool:
    """Create an X tweet detail tool."""

    async def scavio_x_tweet(tweet_id: str) -> str:
        """Fetch full details for a single tweet.

        Args:
            tweet_id: The numeric tweet ID as a string.

        Returns:
            JSON string with the tweet: text, timestamp, language,
            engagement counts, source, author and reply-to references.
        """
        client = get_async_client()

        raw = await client.x.tweet(tweet_id=tweet_id)

        return format_response(raw)

    return FunctionTool(
        scavio_x_tweet,
        description="Fetch full details for a single tweet by ID (1 credit).",
    )


def create_x_tweet_comments_tool(max_results: int = 10) -> FunctionTool:
    """Create an X tweet replies tool with the given configuration."""

    async def scavio_x_tweet_comments(
        tweet_id: str,
        rank: str | None = None,
        cursor: str | None = None,
    ) -> str:
        """Fetch the replies to a tweet.

        Args:
            tweet_id: The numeric tweet ID as a string.
            rank: "top" for ranked replies (default) or "latest" for
                chronological. Lowercase, unlike search_type.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with replies under data.timeline, plus next_cursor,
            prev_cursor and has_more.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "tweet_id": tweet_id,
            "rank": rank,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.x.tweet_comments(**params)

        truncate_list(raw, ["data", "timeline"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_x_tweet_comments,
        description=(
            "Fetch the replies to a tweet, ranked or chronological "
            "(1 credit). Replies are under data.timeline."
        ),
    )


def create_x_tweet_retweeters_tool(max_results: int = 10) -> FunctionTool:
    """Create an X retweeters tool with the given configuration."""

    async def scavio_x_tweet_retweeters(
        tweet_id: str,
        cursor: str | None = None,
    ) -> str:
        """Fetch the users who retweeted a tweet.

        Args:
            tweet_id: The numeric tweet ID as a string.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with users under data.retweeters, plus next_cursor
            and has_more.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "tweet_id": tweet_id,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.x.tweet_retweeters(**params)

        truncate_list(raw, ["data", "retweeters"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_x_tweet_retweeters,
        description=(
            "Fetch the users who retweeted a tweet (1 credit). The list key "
            "is data.retweeters."
        ),
    )


def create_x_user_tool() -> FunctionTool:
    """Create an X user profile tool."""

    async def scavio_x_user(screen_name: str) -> str:
        """Fetch an X user's profile.

        Args:
            screen_name: The X handle without the leading @, e.g. "elonmusk".

        Returns:
            JSON string with the profile: name, description, follower,
            friends, statuses and media counts, verified flags, location,
            website, avatar and creation date.
        """
        client = get_async_client()

        raw = await client.x.user(screen_name=screen_name)

        return format_response(raw)

    return FunctionTool(
        scavio_x_user,
        description=(
            "Fetch an X user's profile by handle (1 credit). Pass the handle "
            "without the @."
        ),
    )


def create_x_user_tweets_tool(max_results: int = 5) -> FunctionTool:
    """Create an X user timeline tool with the given configuration."""

    async def scavio_x_user_tweets(
        screen_name: str,
        cursor: str | None = None,
    ) -> str:
        """Fetch an X user's tweets.

        Args:
            screen_name: The X handle without the leading @.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with tweets under data.timeline, plus data.pinned,
            data.user, next_cursor and prev_cursor. There is no has_more
            here: stop when next_cursor is absent or the timeline is empty.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "screen_name": screen_name,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.x.user_tweets(**params)

        truncate_list(raw, ["data", "timeline"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_x_user_tweets,
        description=(
            "Fetch an X user's tweets (1 credit). Tweets are under "
            "data.timeline; there is no has_more on this endpoint."
        ),
    )


def create_x_user_replies_tool(max_results: int = 5) -> FunctionTool:
    """Create an X user replies tool with the given configuration."""

    async def scavio_x_user_replies(
        screen_name: str,
        cursor: str | None = None,
    ) -> str:
        """Fetch an X user's tweets and replies.

        Args:
            screen_name: The X handle without the leading @.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with the timeline under data.timeline, plus
            data.user, next_cursor and prev_cursor. No pinned, no has_more.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "screen_name": screen_name,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.x.user_replies(**params)

        truncate_list(raw, ["data", "timeline"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_x_user_replies,
        description=(
            "Fetch an X user's tweets and replies (1 credit). Under "
            "data.timeline; there is no has_more on this endpoint."
        ),
    )


def create_x_user_media_tool(max_results: int = 5) -> FunctionTool:
    """Create an X user media tool with the given configuration."""

    async def scavio_x_user_media(
        screen_name: str,
        cursor: str | None = None,
    ) -> str:
        """Fetch an X user's media tweets, the posts with photos or videos.

        Args:
            screen_name: The X handle without the leading @.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with media tweets under data.timeline, plus
            data.user, next_cursor and prev_cursor. No has_more.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "screen_name": screen_name,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.x.user_media(**params)

        truncate_list(raw, ["data", "timeline"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_x_user_media,
        description=(
            "Fetch an X user's media tweets, the posts with photos or videos "
            "(1 credit)."
        ),
    )


def create_x_user_followers_tool(max_results: int = 10) -> FunctionTool:
    """Create an X followers tool with the given configuration."""

    async def scavio_x_user_followers(
        screen_name: str,
        cursor: str | None = None,
    ) -> str:
        """Fetch an X user's followers.

        Args:
            screen_name: The X handle without the leading @.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with users under data.followers, plus
            followers_count, next_cursor, more_users and has_more.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "screen_name": screen_name,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.x.user_followers(**params)

        truncate_list(raw, ["data", "followers"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_x_user_followers,
        description=(
            "Fetch an X user's followers (1 credit). Page with "
            "data.next_cursor while data.has_more."
        ),
    )


def create_x_user_followings_tool(max_results: int = 10) -> FunctionTool:
    """Create an X followings tool with the given configuration."""

    async def scavio_x_user_followings(
        screen_name: str,
        cursor: str | None = None,
    ) -> str:
        """Fetch the accounts an X user follows.

        Args:
            screen_name: The X handle without the leading @.
            cursor: Pagination cursor from a previous response.

        Returns:
            JSON string with accounts under data.following, singular, not
            followings, plus next_cursor, more_users and has_more.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "screen_name": screen_name,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.x.user_followings(**params)

        truncate_list(raw, ["data", "following"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_x_user_followings,
        description=(
            "Fetch the accounts an X user follows (1 credit). The list key is "
            "data.following, singular."
        ),
    )


def create_x_trending_tool(max_results: int = 10) -> FunctionTool:
    """Create an X trending topics tool with the given configuration."""

    async def scavio_x_trending(country: str | None = None) -> str:
        """Fetch trending topics on X for a country.

        Args:
            country: Country NAME, not an ISO code, e.g. "UnitedStates"
                (default), "UnitedKingdom", "Japan".

        Returns:
            JSON string with data.trends, each with name, description and
            context. No cursor and no has_more on this endpoint.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {"country": country}.items() if v is not None}

        raw = await client.x.trending(**params)

        truncate_list(raw, ["data", "trends"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_x_trending,
        description=(
            "List trending topics on X for a country (1 credit). country is "
            "a country name such as UnitedStates, not an ISO code."
        ),
    )
