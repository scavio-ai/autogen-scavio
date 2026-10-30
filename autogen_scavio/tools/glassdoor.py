"""Scavio Glassdoor tools for AutoGen.

4 endpoints. 2 credits flat on all four endpoints. Addressing reviews or salaries by
employer_id takes an extra lookup where the url form does not; the price to you
is 2 either way, but passing back reviews_url / salaries_url is the faster path.

LOOKUP FIRST: create_glassdoor_companies_tool is the entry point. Every other Glassdoor
endpoint is keyed by an id that only exists inside Glassdoor's own URLs, so a caller
holding a name has to resolve it here before anything else will answer.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_glassdoor_companies_tool() -> FunctionTool:
    """Create a Scavio Glassdoor companies tool."""

    async def scavio_glassdoor_companies(
        query: Annotated[str, "Company name to resolve (1-120 characters)."],
    ) -> str:
        """START HERE. Search Glassdoor by company NAME and resolve it to the
        employer_id every other endpoint needs.

        Args:
            query: Company name to resolve (1-120 characters).

        Returns:
            JSON string with lOOKUP: resolves a company NAME to employer_id, ranked by
            Glassdoor and de-duplicated. Start here.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.glassdoor.companies(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_glassdoor_companies,
        description=(
            "START HERE. Resolve a company NAME to the employer_id every other "
            "Glassdoor method is keyed by, ranked by Glassdoor and de-duplicated. "
            "Costs 2 credits."
        ),
    )


def create_glassdoor_company_tool() -> FunctionTool:
    """Create a Scavio Glassdoor company tool."""

    async def scavio_glassdoor_company(
        employer_id: Annotated[
            str | None,
            "Glassdoor employer id (1-50 characters) in any form Glassdoor writes it: "
            "'1699', 'E1699' or 'IE1699'. Must be a STRING - a JSON number is "
            "rejected.",
        ] = None,
        company: Annotated[
            str | None,
            "Employer name as it appears in a Glassdoor slug (1-200 characters). "
            "COSMETIC: the profile resolves on employer_id alone, it is ignored "
            "entirely when url is set, and it does not satisfy the employer_id-or-url "
            "requirement.",
        ] = None,
        url: Annotated[
            str | None,
            "Any glassdoor.com employer URL (1-500 characters): /Overview/, /Reviews/ "
            "or /Salary/. A non-glassdoor.com host is rejected.",
        ] = None,
    ) -> str:
        """Glassdoor employer profile: ratings, star distribution, CEO approval,
        size/revenue bands, awards, five server-rendered reviews, plus reviews_url /
        salaries_url.

        Parameter rule: employer_id or url is required.

        Args:
            employer_id: Glassdoor employer id (1-50 characters) in any form Glassdoor
                writes it: '1699', 'E1699' or 'IE1699'. Must be a STRING - a JSON number
                is rejected.
            company: Employer name as it appears in a Glassdoor slug (1-200 characters).
                COSMETIC: the profile resolves on employer_id alone, it is ignored
                entirely when url is set, and it does not satisfy the employer_id-or-url
                requirement.
            url: Any glassdoor.com employer URL (1-500 characters): /Overview/,
                /Reviews/ or /Salary/. A non-glassdoor.com host is rejected.

        Returns:
            JSON string with employer profile: description, mission, industry, sector,
            HQ, size band, revenue band, stock symbol, year founded, overall +
            per-category ratings, star distribution, CEO approval, awards, FAQ, the five
            server-rendered reviews, AND reviews_url / salaries_url (pass these back as
            `url` to save a fetch).
        """
        client = get_async_client()

        params: dict = {
            "employer_id": employer_id,
            "company": company,
            "url": url,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.glassdoor.company(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_glassdoor_company,
        description=(
            "Glassdoor employer profile: description, mission, industry, sector, HQ, "
            "size and revenue bands, stock symbol, year founded, overall and "
            "per-category ratings, star distribution, CEO approval, awards, FAQ and "
            "the five server-rendered reviews. Also returns reviews_url and "
            "salaries_url, which reviews() and salaries() accept as url to save a "
            "fetch. Provide employer_id or url. Costs 2 credits."
        ),
    )


def create_glassdoor_reviews_tool() -> FunctionTool:
    """Create a Scavio Glassdoor reviews tool."""

    async def scavio_glassdoor_reviews(
        employer_id: Annotated[
            str | None,
            "Glassdoor employer id (1-50 characters): '1699', 'E1699' or 'IE1699'. "
            "Must be a STRING - a JSON number is rejected. Addressing by id takes an extra lookup; the customer price is unchanged.",
        ] = None,
        company: Annotated[
            str | None,
            "Employer name as it appears in a Glassdoor slug (1-200 characters). "
            "COSMETIC: ignored when url is set, and it does not satisfy the "
            "employer_id-or-url requirement.",
        ] = None,
        url: Annotated[
            str | None,
            "Any glassdoor.com employer URL (1-500 characters). Pass back reviews_url "
            "from company() to skip the resolve fetch. A non-glassdoor.com host is "
            "rejected.",
        ] = None,
        category: Annotated[
            Literal[
                "career_development", "compensation", "culture",
                "diversity_and_inclusion", "management", "work_life_balance",
            ]
            | None,
            "Restrict to reviews Glassdoor files under one topic. Closed enum: "
            "Glassdoor IGNORES an unknown value and serves the unfiltered set under a "
            "200. Read filtered_review_count on the response to see how many match.",
        ] = None,
        employment_status: Annotated[
            Literal["full_time", "part_time", "contract", "intern"] | None,
            "Restrict to one kind of employment. Closed enum for the same reason as "
            "category; FREELANCE is deliberately absent because it was never "
            "confirmed to change the result set.",
        ] = None,
    ) -> str:
        """Up to THREE full Glassdoor reviews with per-axis scores, pros, cons, advice,
        employer response - plus complete rating statistics and per-job-title review
        counts.

        Parameter rule: employer_id or url is required. NO `page` param exists.

        Args:
            employer_id: Glassdoor employer id (1-50 characters): '1699', 'E1699' or
                'IE1699'. Must be a STRING - a JSON number is rejected. Addressing by id
                takes an extra lookup; the customer price is unchanged.
            company: Employer name as it appears in a Glassdoor slug (1-200 characters).
                COSMETIC: ignored when url is set, and it does not satisfy the
                employer_id-or-url requirement.
            url: Any glassdoor.com employer URL (1-500 characters). Pass back
                reviews_url from company() to skip the resolve fetch. A
                non-glassdoor.com host is rejected.
            category: Restrict to reviews Glassdoor files under one topic. Closed enum:
                Glassdoor IGNORES an unknown value and serves the unfiltered set under a
                200. Read filtered_review_count on the response to see how many match.
            employment_status: Restrict to one kind of employment. Closed enum for the
                same reason as category; FREELANCE is deliberately absent because it was
                never confirmed to change the result set.

        Returns:
            JSON string with up to THREE full reviews with per-axis scores, pros, cons,
            advice, job title, location, employment status, employer response - plus
            complete rating statistics, star distribution, aggregate pro/con highlight
            terms and per-job-title review counts.
        """
        client = get_async_client()

        params: dict = {
            "employer_id": employer_id,
            "company": company,
            "url": url,
            "category": category,
            "employment_status": employment_status,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.glassdoor.reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_glassdoor_reviews,
        description=(
            "Up to THREE full Glassdoor reviews - the cap is Glassdoor's login wall - "
            "with per-axis scores, pros, cons, advice, job title, location, "
            "employment status and employer response, plus complete rating "
            "statistics, star distribution, aggregate pro/con highlight terms and "
            "per-job-title review counts. There is no page param: move the window "
            "with category and employment_status. Provide employer_id or url. Costs 2 "
            "credits."
        ),
    )


def create_glassdoor_salaries_tool() -> FunctionTool:
    """Create a Scavio Glassdoor salaries tool."""

    async def scavio_glassdoor_salaries(
        employer_id: Annotated[
            str | None,
            "Glassdoor employer id (1-50 characters): '1699', 'E1699' or 'IE1699'. "
            "Must be a STRING - a JSON number is rejected. Addressing by id takes an extra lookup; the customer price is unchanged.",
        ] = None,
        company: Annotated[
            str | None,
            "Employer name as it appears in a Glassdoor slug (1-200 characters). "
            "COSMETIC: ignored when url is set, and it does not satisfy the "
            "employer_id-or-url requirement.",
        ] = None,
        url: Annotated[
            str | None,
            "Any glassdoor.com employer URL (1-500 characters). Pass back "
            "salaries_url from company() to skip the resolve fetch. A "
            "non-glassdoor.com host is rejected.",
        ] = None,
        page: Annotated[
            int | None,
            "Results page, 1-based. Ten job titles per page; page_count on the "
            "response is how many pages exist.",
        ] = None,
    ) -> str:
        """Glassdoor salaries by job title: base-pay and total-pay percentiles P10-P90
        with medians, sample counts, currency, pay period, last-reported date.

        Parameter rule: employer_id or url is required.

        Pagination: page - 10 job titles per page; page_count on the response is how
        many exist.

        Args:
            employer_id: Glassdoor employer id (1-50 characters): '1699', 'E1699' or
                'IE1699'. Must be a STRING - a JSON number is rejected. Addressing by id
                takes an extra lookup; the customer price is unchanged.
            company: Employer name as it appears in a Glassdoor slug (1-200 characters).
                COSMETIC: ignored when url is set, and it does not satisfy the
                employer_id-or-url requirement.
            url: Any glassdoor.com employer URL (1-500 characters). Pass back
                salaries_url from company() to skip the resolve fetch. A
                non-glassdoor.com host is rejected.
            page: Results page, 1-based. Ten job titles per page; page_count on the
                response is how many pages exist.

        Returns:
            JSON string with salaries by job title, 10/page: base-pay and total-pay
            percentiles P10-P90 with medians called out, sample counts, currency, pay
            period, last-reported date.
        """
        client = get_async_client()

        params: dict = {
            "employer_id": employer_id,
            "company": company,
            "url": url,
            "page": page,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.glassdoor.salaries(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_glassdoor_salaries,
        description=(
            "Glassdoor salaries by job title, 10 titles per page: base-pay and "
            "total-pay percentiles P10-P90 with medians called out, sample counts, "
            "currency, pay period and last-reported date. The figures are Glassdoor's "
            "ESTIMATES for the title, not individual reported salaries. Provide "
            "employer_id or url. Costs 2 credits."
        ),
    )
