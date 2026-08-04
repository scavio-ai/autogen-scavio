"""Scavio LinkedIn tools for AutoGen.

Nine live endpoints across three credit tiers: profile, company and single-post
reads cost 1, the paginated list tools cost 10 per page, and job detail costs
30 -- the most expensive call in the whole API. Each tool states its own cost.

Five endpoints are deliberately not wrapped: person/contact, company/people,
company/jobs, search/people and search/posts have no upstream left and can only
answer 410. A tool that always fails is still a menu item a model will pick, so
it is better absent. Use the company tool's featured_employees in place of
company/people, and the job search tool with a company name in place of
company/jobs.
"""

from __future__ import annotations

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client, truncate_list


def create_linkedin_person_tool() -> FunctionTool:
    """Create a LinkedIn person profile tool."""

    async def scavio_linkedin_person(
        username: str | None = None,
        url: str | None = None,
    ) -> str:
        """Fetch a LinkedIn member's full profile.

        Args:
            username: Public identifier / vanity handle, e.g.
                "williamhgates". Provide this or url.
            url: Full LinkedIn profile URL. Provide this or username.

        Returns:
            JSON string with the profile: headline, about, location,
            follower and connection counts, current_company, experiences,
            educations, honors_and_awards and bio_links.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "username": username,
            "url": url,
        }.items() if v is not None}

        raw = await client.linkedin.person(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_linkedin_person,
        description=(
            "Fetch a LinkedIn member's full profile by username or URL "
            "(1 credit). Includes experience, education and follower counts."
        ),
    )


def create_linkedin_person_about_tool() -> FunctionTool:
    """Create a LinkedIn person about tool."""

    async def scavio_linkedin_person_about(
        username: str | None = None,
        url: str | None = None,
    ) -> str:
        """Fetch the narrative sections of a LinkedIn member's profile.

        Args:
            username: Public identifier / vanity handle. Provide this or url.
            url: Full LinkedIn profile URL. Provide this or username.

        Returns:
            JSON string with about, headline, education_summary,
            experiences, educations, honors_and_awards and bio_links.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "username": username,
            "url": url,
        }.items() if v is not None}

        raw = await client.linkedin.person_about(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_linkedin_person_about,
        description=(
            "Fetch the about / overview slice of a LinkedIn profile "
            "(1 credit). Use instead of the person tool when only the "
            "narrative sections are needed."
        ),
    )


def create_linkedin_person_posts_tool(max_results: int = 5) -> FunctionTool:
    """Create a LinkedIn person posts tool with the given configuration."""

    async def scavio_linkedin_person_posts(
        username: str | None = None,
        url: str | None = None,
        type: str | None = None,
        cursor: str | None = None,
    ) -> str:
        """Fetch a LinkedIn member's posts.

        Args:
            username: Public identifier / vanity handle. Provide this or url.
            url: Full LinkedIn profile URL. Provide this or username.
            type: Which feed, one of "posts" (default, their own posts),
                "comments" (posts they commented on), "reactions" (posts they
                reacted to).
            cursor: Opaque cursor from a prior response's next_cursor.

        Returns:
            JSON string with posts under data.data, plus count, has_more and
            next_cursor. 50 posts per page.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "username": username,
            "url": url,
            "type": type,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.linkedin.person_posts(**params)

        truncate_list(raw, ["data", "data"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_linkedin_person_posts,
        description=(
            "Fetch a LinkedIn member's posts with reactions, comment and "
            "repost counts (10 credits per page). Posts are under data.data; "
            "page with next_cursor."
        ),
    )


def create_linkedin_company_tool() -> FunctionTool:
    """Create a LinkedIn company profile tool."""

    async def scavio_linkedin_company(
        company: str | None = None,
        url: str | None = None,
    ) -> str:
        """Fetch a LinkedIn company profile.

        Args:
            company: Company universal name / slug, e.g. "microsoft".
                Provide this or url.
            url: Full LinkedIn company URL. Provide this or company.

        Returns:
            JSON string with the company: about, website, industries,
            specialties, company_size, employee and follower counts,
            headquarters, locations, similar_companies and
            featured_employees, a 4 to 6 person staff sample.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "company": company,
            "url": url,
        }.items() if v is not None}

        raw = await client.linkedin.company(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_linkedin_company,
        description=(
            "Fetch a LinkedIn company profile by slug or URL (1 credit). "
            "featured_employees is the supported way to sample staff."
        ),
    )


def create_linkedin_company_posts_tool(max_results: int = 5) -> FunctionTool:
    """Create a LinkedIn company posts tool with the given configuration."""

    async def scavio_linkedin_company_posts(
        company: str | None = None,
        url: str | None = None,
        cursor: str | None = None,
    ) -> str:
        """Fetch a LinkedIn company's recent posts.

        Args:
            company: Company universal name / slug. Provide this or url.
            url: Full LinkedIn company URL. Provide this or company.
            cursor: Opaque cursor from a prior response's next_cursor.

        Returns:
            JSON string with posts under data.data, in the same shape as
            member posts, plus count, has_more and next_cursor. 50 per page.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "company": company,
            "url": url,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.linkedin.company_posts(**params)

        truncate_list(raw, ["data", "data"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_linkedin_company_posts,
        description=(
            "Fetch a LinkedIn company's recent posts (10 credits per page). "
            "Posts are under data.data; page with next_cursor."
        ),
    )


def create_linkedin_search_jobs_tool(max_results: int = 5) -> FunctionTool:
    """Create a LinkedIn job search tool with the given configuration."""

    async def scavio_linkedin_search_jobs(
        search: str,
        location: str | None = None,
        cursor: str | None = None,
    ) -> str:
        """Search LinkedIn job listings.

        Args:
            search: Search keyword, e.g. "software engineer". The field is
                search, not query.
            location: Geographic filter, e.g. "United States". Omit to search
                everywhere.
            cursor: Opaque cursor from a prior response's next_cursor.

        Returns:
            JSON string with listings under data.data (id, title, company,
            location, posted_at, workplace_type, salary), plus count,
            has_more and next_cursor. 25 per page; the provider rotates its
            result set, so pages overlap and repeat calls differ -- dedupe by
            job id.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "search": search,
            "location": location,
            "cursor": cursor,
        }.items() if v is not None}

        raw = await client.linkedin.search_jobs(**params)

        truncate_list(raw, ["data", "data"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_linkedin_search_jobs,
        description=(
            "Search LinkedIn job listings by keyword (10 credits per page). "
            "Pass a company name as the search term to approximate a "
            "per-company job list."
        ),
    )


def create_linkedin_job_tool() -> FunctionTool:
    """Create a LinkedIn job detail tool."""

    async def scavio_linkedin_job(
        job_id: str | None = None,
        url: str | None = None,
    ) -> str:
        """Fetch full details for one LinkedIn job listing.

        Args:
            job_id: Job listing ID, e.g. "4415427228". Provide this or url.
            url: Full LinkedIn job URL. Provide this or job_id.

        Returns:
            JSON string with the listing: description, employment_type,
            experience_level, skills, benefits, salary, applicant_count and
            the hiring company. Roughly one job id in five has no detail
            record upstream and returns an unbilled 404.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "job_id": job_id,
            "url": url,
        }.items() if v is not None}

        raw = await client.linkedin.job(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_linkedin_job,
        description=(
            "Fetch one LinkedIn job listing in full (30 credits, the most "
            "expensive Scavio call). Prefer the fields the job search tool "
            "already returns when they are enough."
        ),
    )


def create_linkedin_post_tool() -> FunctionTool:
    """Create a LinkedIn post detail tool."""

    async def scavio_linkedin_post(
        post_id: str | None = None,
        url: str | None = None,
    ) -> str:
        """Fetch full details for one LinkedIn post.

        Args:
            post_id: Post ID or activity urn, e.g. "7488618410256523265".
                Provide this or url.
            url: Full LinkedIn post URL. Provide this or post_id.

        Returns:
            JSON string with the post: text, created_at, hashtags,
            embedded_links, images, videos, like and comment counts,
            tagged_companies, tagged_people, top_comments and the author.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "post_id": post_id,
            "url": url,
        }.items() if v is not None}

        raw = await client.linkedin.post(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_linkedin_post,
        description=(
            "Fetch one LinkedIn post in full by post id or URL (1 credit). "
            "Includes media, tagged entities and top comments."
        ),
    )


def create_linkedin_post_comments_tool(max_results: int = 10) -> FunctionTool:
    """Create a LinkedIn post comments tool with the given configuration."""

    async def scavio_linkedin_post_comments(
        post_id: str | None = None,
        url: str | None = None,
        page: int | None = None,
    ) -> str:
        """Fetch the comments on a LinkedIn post.

        Args:
            post_id: Post ID or activity urn. Provide this or url.
            url: Full LinkedIn post URL. Provide this or post_id.
            page: 1-based page number, default 1. This endpoint pages by
                number, not by cursor.

        Returns:
            JSON string with comments under data.data, each with the author
            and any nested replies, plus page, total and has_more. Page size
            varies upstream, so keep incrementing until a page comes back
            empty.
        """
        client = get_async_client()

        params: dict = {k: v for k, v in {
            "post_id": post_id,
            "url": url,
            "page": page,
        }.items() if v is not None}

        raw = await client.linkedin.post_comments(**params)

        truncate_list(raw, ["data", "data"], max_results)

        return format_response(raw)

    return FunctionTool(
        scavio_linkedin_post_comments,
        description=(
            "Fetch the comments on a LinkedIn post (10 credits per page). "
            "Paginated by a 1-based page number, not a cursor."
        ),
    )
