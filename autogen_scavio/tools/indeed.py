"""Scavio Indeed tools for AutoGen.

4 endpoints. 2 credits flat on all four endpoints.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_indeed_search_tool() -> FunctionTool:
    """Create a Scavio Indeed search tool."""

    async def scavio_indeed_search(
        query: Annotated[
            str | None,
            "Job title, keywords or employer (1-500 characters). Required unless "
            "location is given.",
        ] = None,
        location: Annotated[
            str | None,
            "City and state, postal code, state, country, or 'Remote' (1-200 "
            "characters). Valid on its own with no query.",
        ] = None,
        page: Annotated[
            int | None,
            "Results page, 1-based. 10 postings per page, 1 call each.",
        ] = None,
        radius: Annotated[
            Literal[0, 5, 10, 15, 25, 35, 50, 100] | None,
            "Search radius in miles around location. Closed set: Indeed IGNORES any "
            "other value and returns the unfiltered set. Upstream default 50.",
        ] = None,
        max_age_days: Annotated[
            Literal[1, 3, 7, 14] | None,
            "Maximum posting age in days. Closed set: Indeed IGNORES any other value "
            "and returns postings of every age.",
        ] = None,
        job_type: Annotated[
            Literal["full_time", "part_time", "contract", "temporary", "internship"]
            | None,
            "Employment type filter.",
        ] = None,
        min_salary: Annotated[
            float | None,
            "Minimum annual salary, >= 0. Filters on INDEED'S OWN ESTIMATE for the "
            "role, not a posted figure, so postings publishing no salary still match.",
        ] = None,
        remote: Annotated[bool | None, "Remote postings only."] = None,
    ) -> str:
        """Indeed job postings: title, employer, rating, location, salary range, job
        type, benefits, posting age, apply route.

        Parameter rule: query or location is required.

        Pagination: page - 10 postings per page.

        Args:
            query: Job title, keywords or employer (1-500 characters). Required unless
                location is given.
            location: City and state, postal code, state, country, or 'Remote' (1-200
                characters). Valid on its own with no query.
            page: Results page, 1-based. 10 postings per page, 1 call each.
            radius: Search radius in miles around location. Closed set: Indeed IGNORES
                any other value and returns the unfiltered set. Upstream default 50.
            max_age_days: Maximum posting age in days. Closed set: Indeed IGNORES any
                other value and returns postings of every age.
            job_type: Employment type filter.
            min_salary: Minimum annual salary, >= 0. Filters on INDEED'S OWN ESTIMATE
                for the role, not a posted figure, so postings publishing no salary
                still match.
            remote: Remote postings only.

        Returns:
            JSON string with job postings: title, employer, rating, location, salary
            range, job type, benefits, posting age, apply route.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "location": location,
            "page": page,
            "radius": radius,
            "max_age_days": max_age_days,
            "job_type": job_type,
            "min_salary": min_salary,
            "remote": remote,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.indeed.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_indeed_search,
        description=(
            "Indeed job postings: title, employer, rating, location, salary range, "
            "job type, benefits, posting age, apply route. 10 postings per page. "
            "Provide query or location - a location-only search (every posting in a "
            "metro) is valid. Costs 2 credits."
        ),
    )


def create_indeed_job_tool() -> FunctionTool:
    """Create a Scavio Indeed job tool."""

    async def scavio_indeed_job(
        job_id: Annotated[
            str,
            "16-hex Indeed job key, or any indeed.com URL carrying jk= (/viewjob, "
            "/rc/clk, /pagead/clk).",
        ],
    ) -> str:
        """One Indeed posting in full: description text and HTML, structured salary,
        employment types, benefits, geocoded address, original ATS link.

        Args:
            job_id: 16-hex Indeed job key, or any indeed.com URL carrying jk= (/viewjob,
                /rc/clk, /pagead/clk).

        Returns:
            JSON string with one posting in full: description text and HTML, structured
            salary, employment types, benefits, geocoded address, employer rating,
            applicant count, original ATS link.
        """
        client = get_async_client()

        params: dict = {
            "job_id": job_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.indeed.job(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_indeed_job,
        description=(
            "One Indeed posting in full: description text and HTML, structured "
            "salary, employment types, benefits, geocoded address, employer rating, "
            "applicant count, original ATS link. An unknown job key is a real 404 "
            "that is still billed. Costs 2 credits."
        ),
    )


def create_indeed_company_tool() -> FunctionTool:
    """Create a Scavio Indeed company tool."""

    async def scavio_indeed_company(
        company: Annotated[
            str,
            "indeed.com/cmp/<slug> slug or a full profile URL (1-200 characters); "
            "slugs are untidy, e.g. 'Tata-Consultancy-Services-(tcs)'.",
        ],
    ) -> str:
        """Indeed employer profile: description, industry, HQ, size, revenue, CEO
        approval, per-category ratings, reported salaries, open roles.

        Args:
            company: indeed.com/cmp/<slug> slug or a full profile URL (1-200
                characters); slugs are untidy, e.g. 'Tata-Consultancy-Services-(tcs)'.

        Returns:
            JSON string with employer profile: description, industry, HQ, size, revenue,
            CEO approval, overall and per-category ratings, reported salaries, open
            roles, locations.
        """
        client = get_async_client()

        params: dict = {
            "company": company,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.indeed.company(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_indeed_company,
        description=(
            "Indeed employer profile: description, industry, HQ, size, revenue, CEO "
            "approval, overall and per-category ratings, reported salaries, open "
            "roles, locations. An unknown slug is a real 404 that is still billed. "
            "Costs 2 credits."
        ),
    )


def create_indeed_company_reviews_tool() -> FunctionTool:
    """Create a Scavio Indeed company reviews tool."""

    async def scavio_indeed_company_reviews(
        company: Annotated[
            str,
            "indeed.com/cmp/<slug> slug or a full profile URL (1-200 characters).",
        ],
        page: Annotated[
            int | None,
            "Reviews page, 1-based. 20 reviews per page.",
        ] = None,
    ) -> str:
        """Indeed employee reviews with per-category ratings, pros/cons, reviewer job
        title and location, plus aggregated sentiment and breakdowns.

        Pagination: page - 20 reviews per page.

        Args:
            company: indeed.com/cmp/<slug> slug or a full profile URL (1-200
                characters).
            page: Reviews page, 1-based. 20 reviews per page.

        Returns:
            JSON string with employee reviews, 20/page, with per-category ratings,
            pros/cons, reviewer job title and location, plus aggregated sentiment and
            topic/location/job-title breakdowns.
        """
        client = get_async_client()

        params: dict = {
            "company": company,
            "page": page,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.indeed.company_reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_indeed_company_reviews,
        description=(
            "Indeed employee reviews, 20 per page, with per-category ratings, "
            "pros/cons, reviewer job title and location, plus aggregated sentiment "
            "and topic/location/job-title breakdowns. Costs 2 credits."
        ),
    )
