"""Scavio Capterra Software Reviews tools for AutoGen.

3 endpoints. 2 credits flat on all three endpoints.
"""

from __future__ import annotations

from typing import Annotated

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_capterra_search_tool() -> FunctionTool:
    """Create a Scavio Capterra Software Reviews search tool."""

    async def scavio_capterra_search(
        query: Annotated[
            str | None,
            "Search term (1-200 characters). Required in practice: a term-less "
            "Capterra search serves a fixed popular-products list unrelated to the "
            "caller.",
        ] = None,
        url: Annotated[
            str | None,
            "Full capterra.com search URL, as an alternative to query (1-1000 "
            "characters; the transport also accepts capterra.co.uk and "
            "capterra.com.br hosts).",
        ] = None,
    ) -> str:
        """Search Capterra for B2B software: 20 ranked products with name, vendor
        description, rating, review count, logo, paid-placement flag; each row carries
        product_id and slug.

        Parameter rule: query or url is required.

        Args:
            query: Search term (1-200 characters). Required in practice: a term-less
                Capterra search serves a fixed popular-products list unrelated to the
                caller.
            url: Full capterra.com search URL, as an alternative to query (1-1000
                characters; the transport also accepts capterra.co.uk and
                capterra.com.br hosts).

        Returns:
            JSON string with 20 ranked products: name, vendor description, rating,
            review count, logo, paid-placement flag; each row carries product_id and
            slug. NO PAGINATION.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "url": url,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.capterra.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_capterra_search,
        description=(
            "Search Capterra, the B2B software review site: 20 ranked products with "
            "name, vendor description, rating, review count, logo and paid-placement "
            "flag, each row carrying product_id and slug. The result set is fixed at "
            "20 and does NOT paginate -- Capterra serves identical rows for page 2, "
            "so there is deliberately no page parameter. Provide query or url. Costs "
            "2 credits."
        ),
    )


def create_capterra_product_tool() -> FunctionTool:
    """Create a Scavio Capterra Software Reviews product tool."""

    async def scavio_capterra_product(
        product_id: Annotated[
            str | None,
            "The number in a Capterra product path such as /p/186596/Notion/ (1-50 "
            "characters). Must be a STRING -- a JSON number is rejected.",
        ] = None,
        slug: Annotated[
            str | None,
            "Product slug (1-200 characters). Cosmetic on this endpoint -- a wrong "
            "slug still returns the right profile -- but load-bearing on reviews().",
        ] = None,
        url: Annotated[
            str | None,
            "Full Capterra product URL, as an alternative to product_id (1-1000 "
            "characters).",
        ] = None,
    ) -> str:
        """Full Capterra profile: per-star histogram and the four scored criteria,
        complete pricing table, every rated feature and integration, AI pros/cons with
        the quoted review, buyer profile, PLUS the 25 most recent reviews.

        Parameter rule: product_id or url is required.

        Args:
            product_id: The number in a Capterra product path such as /p/186596/Notion/
                (1-50 characters). Must be a STRING -- a JSON number is rejected.
            slug: Product slug (1-200 characters). Cosmetic on this endpoint -- a wrong
                slug still returns the right profile -- but load-bearing on reviews().
            url: Full Capterra product URL, as an alternative to product_id (1-1000
                characters).

        Returns:
            JSON string with full profile: rating with per-star histogram and the four
            scored criteria, likelihood to recommend, review sentiment and topics, the
            complete pricing table with every plan and its features, every rated
            feature, every integration, AI-derived pros and cons with the quoted review,
            FAQs, screenshots, badges and awards, competitor comparisons and
            alternatives, buyer profile by company size / industry / job function, PLUS
            the 25 most recent reviews. vendor is NULL.
        """
        client = get_async_client()

        params: dict = {
            "product_id": product_id,
            "slug": slug,
            "url": url,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.capterra.product(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_capterra_product,
        description=(
            "Full Capterra profile: rating with per-star histogram and the four "
            "scored criteria, likelihood to recommend, review sentiment and topics, "
            "the complete pricing table with every plan and its features, every rated "
            "feature and integration, AI-derived pros and cons with the quoted "
            "review, FAQs, screenshots, badges and awards, competitor comparisons and "
            "alternatives, and the buyer profile by company size, industry and job "
            "function -- PLUS the 25 most recent reviews at no extra cost. vendor is "
            "always null here: Capterra does not publish it as structured data on the "
            "product page. Provide product_id or url. Costs 2 credits."
        ),
    )


def create_capterra_reviews_tool() -> FunctionTool:
    """Create a Scavio Capterra Software Reviews reviews tool."""

    async def scavio_capterra_reviews(
        product_id: Annotated[
            str | None,
            "Capterra product id as a string (1-50 characters).",
        ] = None,
        slug: Annotated[
            str | None,
            "Product slug (1-200 characters). LOAD-BEARING here: it is case-sensitive "
            "upstream and a wrong one silently serves page one under a billed 200. "
            "Pass back the slug from search() or product().",
        ] = None,
        url: Annotated[
            str | None,
            "Full Capterra reviews URL, as an alternative to product_id (1-1000 "
            "characters). Passing back reviews_url from product() is the reliable way "
            "to page.",
        ] = None,
        page: Annotated[
            int | None,
            "1-based page number (1-100); 25 reviews per page. 100 is a hard cap "
            "whatever the review count says -- past it Capterra answers 200 with page "
            "one.",
        ] = None,
    ) -> str:
        """A page of Capterra reviews: overall score plus five per-criterion scores,
        pros, cons, advice, usage duration, alternatives considered, vendor response -
        plus a rich competitor list with rating histograms and starting prices.

        Parameter rule: product_id or url is required.

        Pagination: page - 25 per page, capped at page 100 (CAPTERRA_MAX_REVIEW_PAGE);
        past it Capterra answers 200 with PAGE ONE and the page quietly dropped from the
        canonical.

        Args:
            product_id: Capterra product id as a string (1-50 characters).
            slug: Product slug (1-200 characters). LOAD-BEARING here: it is
                case-sensitive upstream and a wrong one silently serves page one under a
                billed 200. Pass back the slug from search() or product().
            url: Full Capterra reviews URL, as an alternative to product_id (1-1000
                characters). Passing back reviews_url from product() is the reliable way
                to page.
            page: 1-based page number (1-100); 25 reviews per page. 100 is a hard cap
                whatever the review count says -- past it Capterra answers 200 with page
                one.

        Returns:
            JSON string with a page of reviews: overall score plus five per-criterion
            scores, title, pros, cons, advice, usage duration, incentivized flag,
            alternatives considered and what they switched from, reviewer job title /
            industry / company size, vendor response - plus a rich competitor list with
            rating histograms and starting prices.
        """
        client = get_async_client()

        params: dict = {
            "product_id": product_id,
            "slug": slug,
            "url": url,
            "page": page,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.capterra.reviews(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_capterra_reviews,
        description=(
            "A page of Capterra reviews: overall score plus five per-criterion "
            "scores, title, pros, cons, advice, usage duration, incentivized flag, "
            "alternatives considered and what they switched from, reviewer job title, "
            "industry and company size, and the vendor response -- plus a competitor "
            "list richer than the profile's, each alternative with its own rating "
            "histogram and starting price. 25 reviews per page, capped at page 100. "
            "Page 1 already rides along inside product(), so use this to page past "
            "it. Provide product_id or url. Costs 2 credits."
        ),
    )
