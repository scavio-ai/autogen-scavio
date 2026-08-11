"""Scavio Threads tools for AutoGen.

6 endpoints. BODY-PRICED, not flat: profile, user_posts and user_replies cost 2 credits
addressed by user_id and 4 addressed by username - a handle has to be resolved through
people search first, because the upstream handle lookup is dead. Pass user_id whenever
you have it. post, post_comments and search_users have no username form and are always 2
credits.
"""

from __future__ import annotations

from typing import Annotated

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_threads_profile_tool() -> FunctionTool:
    """Create a Scavio Threads profile tool."""

    async def scavio_threads_profile(
        user_id: Annotated[
            str | None,
            "Numeric Threads user id, e.g. '63625256886'. The cheap path: 2 credits.",
        ] = None,
        username: Annotated[
            str | None,
            "Threads handle without the @ (1-60 characters). Costs 2 extra credits (4 "
            "total): the upstream handle lookup is down, so the handle is resolved "
            "through people search first. Pass user_id instead to avoid that.",
        ] = None,
    ) -> str:
        """Profile details for a Threads user, by user_id (2cr) or username (4cr).

        Parameter rule: username or user_id is required.

        Args:
            user_id: Numeric Threads user id, e.g. '63625256886'. The cheap path: 2
                credits.
            username: Threads handle without the @ (1-60 characters). Costs 2 extra
                credits (4 total): the upstream handle lookup is down, so the handle is
                resolved through people search first. Pass user_id instead to avoid
                that.

        Returns:
            JSON string with profile details for a Threads user.
        """
        client = get_async_client()

        params: dict = {
            "user_id": user_id,
            "username": username,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.threads.profile(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_threads_profile,
        description=(
            "Profile details for a Threads user. Costs 2 credits addressed by user_id "
            "and 4 by username; pass user_id whenever you have it."
        ),
    )


def create_threads_user_posts_tool() -> FunctionTool:
    """Create a Scavio Threads user posts tool."""

    async def scavio_threads_user_posts(
        user_id: Annotated[
            str | None,
            "Numeric Threads user id, e.g. '63625256886'. The cheap path: 2 credits.",
        ] = None,
        username: Annotated[
            str | None,
            "Threads handle without the @ (1-60 characters). Costs 2 extra credits (4 "
            "total) because the handle has to be resolved through people search "
            "first.",
        ] = None,
        cursor: Annotated[
            str | None,
            "Pagination cursor from a prior response's next_cursor. Omit for the "
            "first page.",
        ] = None,
    ) -> str:
        """A user's Threads posts, cursor-paginated.

        Parameter rule: username or user_id is required.

        Pagination: cursor -> next_cursor.

        Args:
            user_id: Numeric Threads user id, e.g. '63625256886'. The cheap path: 2
                credits.
            username: Threads handle without the @ (1-60 characters). Costs 2 extra
                credits (4 total) because the handle has to be resolved through people
                search first.
            cursor: Pagination cursor from a prior response's next_cursor. Omit for the
                first page.

        Returns:
            JSON string with a user's Threads posts, cursor-paginated.
        """
        client = get_async_client()

        params: dict = {
            "user_id": user_id,
            "username": username,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.threads.user_posts(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_threads_user_posts,
        description=(
            "A user's Threads posts, cursor-paginated via next_cursor. Costs 2 "
            "credits addressed by user_id and 4 by username."
        ),
    )


def create_threads_user_replies_tool() -> FunctionTool:
    """Create a Scavio Threads user replies tool."""

    async def scavio_threads_user_replies(
        user_id: Annotated[
            str | None,
            "Numeric Threads user id, e.g. '63625256886'. The cheap path: 2 credits.",
        ] = None,
        username: Annotated[
            str | None,
            "Threads handle without the @ (1-60 characters). Costs 2 extra credits (4 "
            "total) because the handle has to be resolved through people search "
            "first.",
        ] = None,
        cursor: Annotated[
            str | None,
            "Pagination cursor from a prior response's next_cursor. Omit for the "
            "first page.",
        ] = None,
    ) -> str:
        """A user's replies, cursor-paginated.

        Parameter rule: username or user_id is required.

        Pagination: cursor -> next_cursor.

        Args:
            user_id: Numeric Threads user id, e.g. '63625256886'. The cheap path: 2
                credits.
            username: Threads handle without the @ (1-60 characters). Costs 2 extra
                credits (4 total) because the handle has to be resolved through people
                search first.
            cursor: Pagination cursor from a prior response's next_cursor. Omit for the
                first page.

        Returns:
            JSON string with a user's replies, cursor-paginated.
        """
        client = get_async_client()

        params: dict = {
            "user_id": user_id,
            "username": username,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.threads.user_replies(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_threads_user_replies,
        description=(
            "A user's Threads replies, cursor-paginated via next_cursor. Costs 2 "
            "credits addressed by user_id and 4 by username."
        ),
    )


def create_threads_post_tool() -> FunctionTool:
    """Create a Scavio Threads post tool."""

    async def scavio_threads_post(
        post_id: Annotated[
            str | None,
            "Threads post id, e.g. '3349029093483693129'.",
        ] = None,
        url: Annotated[
            str | None,
            "Full threads.net post URL (e.g. "
            "'https://www.threads.net/@natgeo/post/C8xY'), as an alternative to "
            "post_id.",
        ] = None,
    ) -> str:
        """A single Threads post by id or threads.net URL.

        Parameter rule: post_id or url is required.

        Args:
            post_id: Threads post id, e.g. '3349029093483693129'.
            url: Full threads.net post URL (e.g.
                'https://www.threads.net/@natgeo/post/C8xY'), as an alternative to
                post_id.

        Returns:
            JSON string with a single post by id or threads.net URL.
        """
        client = get_async_client()

        params: dict = {
            "post_id": post_id,
            "url": url,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.threads.post(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_threads_post,
        description=(
            "A single Threads post, addressed by post_id or by its threads.net URL. "
            "Costs 2 credits. Threads is body-priced by identifier, but this endpoint "
            "has no username form, so it is always 2."
        ),
    )


def create_threads_post_comments_tool() -> FunctionTool:
    """Create a Scavio Threads post comments tool."""

    async def scavio_threads_post_comments(
        post_id: Annotated[str, "Threads post id, e.g. '3349029093483693129'."],
        cursor: Annotated[
            str | None,
            "Pagination cursor from a prior response's next_cursor. Omit for the "
            "first page.",
        ] = None,
    ) -> str:
        """Replies to a Threads post, cursor-paginated.

        Pagination: cursor -> next_cursor.

        Args:
            post_id: Threads post id, e.g. '3349029093483693129'.
            cursor: Pagination cursor from a prior response's next_cursor. Omit for the
                first page.

        Returns:
            JSON string with replies to a post, cursor-paginated.
        """
        client = get_async_client()

        params: dict = {
            "post_id": post_id,
            "cursor": cursor,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.threads.post_comments(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_threads_post_comments,
        description=(
            "Replies to a Threads post, cursor-paginated via next_cursor. Post-keyed "
            "only: there is no username form, so this endpoint always costs 2 "
            "credits."
        ),
    )


def create_threads_search_users_tool() -> FunctionTool:
    """Create a Scavio Threads search users tool."""

    async def scavio_threads_search_users(
        query: Annotated[str, "Name or handle to search for (1-200 characters)."],
    ) -> str:
        """Threads profiles matching a name or handle. This is the ONLY search Threads
        exposes.

        Args:
            query: Name or handle to search for (1-200 characters).

        Returns:
            JSON string with threads profiles matching a name or handle (the ONLY search
            Threads exposes).
        """
        client = get_async_client()

        params: dict = {
            "query": query,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.threads.search_users(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_threads_search_users,
        description=(
            "Search Threads profiles by name or handle. This is the only search "
            "Threads exposes - there is no post or content search - and it returns a "
            "single unpaginated page. Costs 2 credits. Threads is body-priced by "
            "identifier, but this endpoint has no username form, so it is always 2."
        ),
    )
