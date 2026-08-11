"""Scavio Companies House tools for AutoGen.

4 endpoints. 1 credit flat on all four endpoints - the official UK registry.

LOOKUP FIRST: create_companies_house_search_tool is the entry point. Every other
Companies House endpoint is keyed by an id that only exists inside Companies House's own
URLs, so a caller holding a name has to resolve it here before anything else will
answer.
"""

from __future__ import annotations

from typing import Annotated

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_companies_house_search_tool() -> FunctionTool:
    """Create a Scavio Companies House search tool."""

    async def scavio_companies_house_search(
        query: Annotated[
            str,
            "Company name or fragment (1-200 characters, non-blank). Matches CURRENT "
            "AND FORMER names.",
        ],
        page: Annotated[
            int | None,
            "Results page, 1-based, 1-50, 20 results per page. Defaults to 1. The "
            "register serves only a 1000-result window per term whatever hit count it "
            "prints, and answers page 51 with HTTP 416.",
        ] = None,
    ) -> str:
        """START HERE. Search the UK register by name and get the company_number every
        other endpoint is keyed by, plus status, incorporation date and registered
        office.

        Pagination: page - 20 per page, CAPPED AT PAGE 50. The register serves a
        1000-result WINDOW per term whatever hit count it prints (it claims 10,000 for a
        broad term then answers page 51 with HTTP 416).

        Args:
            query: Company name or fragment (1-200 characters, non-blank). Matches
                CURRENT AND FORMER names.
            page: Results page, 1-based, 1-50, 20 results per page. Defaults to 1. The
                register serves only a 1000-result window per term whatever hit count it
                prints, and answers page 51 with HTTP 416.

        Returns:
            JSON string with register search results: company number, name, status,
            incorporation or dissolution date, registered office address, matched former
            names. 20 per page.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "page": page,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.companies_house.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_companies_house_search,
        description=(
            "START HERE. Search the UK register by name and get the company_number "
            "every other Companies House endpoint is keyed by, plus status, "
            "incorporation or dissolution date, registered office and matched former "
            "names. 20 per page, last page is 50. Costs 1 credit."
        ),
    )


def create_companies_house_company_tool() -> FunctionTool:
    """Create a Scavio Companies House company tool."""

    async def scavio_companies_house_company(
        company_number: Annotated[
            str,
            "UK company number (1-20 characters), zero-padded and upper-cased for "
            "you, so '445790' and 'sc090312' both work. Registry prefixes supported: "
            "SC, NI, OC, SO, NC, FC, BR, CE.",
        ],
    ) -> str:
        """Full UK register entry: status, type, incorporation and dissolution dates,
        registered office, SIC codes, previous names, accounts and
        confirmation-statement due dates with overdue flags.

        Args:
            company_number: UK company number (1-20 characters), zero-padded and
                upper-cased for you, so '445790' and 'sc090312' both work. Registry
                prefixes supported: SC, NI, OC, SO, NC, FC, BR, CE.

        Returns:
            JSON string with full register entry: status, type, incorporation and
            dissolution dates, registered office, SIC codes, previous names, accounts
            and confirmation-statement due dates with overdue flags, and whether it has
            charges, insolvency history, officers or UK establishments. FC returns home
            registry / legal form / governing law; BR returns the parent; CE returns the
            charity number.
        """
        client = get_async_client()

        params: dict = {
            "company_number": company_number,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.companies_house.company(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_companies_house_company,
        description=(
            "Full UK register entry: status, type, incorporation and dissolution "
            "dates, registered office, SIC codes, previous names, accounts and "
            "confirmation-statement due dates with overdue flags, and whether it has "
            "charges, insolvency history, officers or UK establishments. Costs 1 "
            "credit."
        ),
    )


def create_companies_house_officers_tool() -> FunctionTool:
    """Create a Scavio Companies House officers tool."""

    async def scavio_companies_house_officers(
        company_number: Annotated[
            str,
            "UK company number (1-20 characters), zero-padded and upper-cased for "
            "you.",
        ],
        page: Annotated[
            int | None,
            "Results page, 1-based, 35 per page. Defaults to 1. No upper bound: past "
            "the last page the register answers an ordinary 200 with an empty list, "
            "identical to a company with no officers.",
        ] = None,
    ) -> str:
        """UK company officers current and resigned: name, role, appointment and
        resignation dates, correspondence address, nationality, month-and-year DOB,
        identity-verification status.

        Pagination: page - 35 per page, NO upper page bound. Past the last page the
        register answers an ordinary 200 with an empty list, identical to a company with
        no officers.

        Args:
            company_number: UK company number (1-20 characters), zero-padded and
                upper-cased for you.
            page: Results page, 1-based, 35 per page. Defaults to 1. No upper bound:
                past the last page the register answers an ordinary 200 with an empty
                list, identical to a company with no officers.

        Returns:
            JSON string with officers current and resigned, 35/page: name, role,
            appointment and resignation dates, correspondence address, nationality,
            country of residence, month-and-year DOB, identity-verification status.
        """
        client = get_async_client()

        params: dict = {
            "company_number": company_number,
            "page": page,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.companies_house.officers(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_companies_house_officers,
        description=(
            "UK company officers, current and resigned, 35 per page: name, role, "
            "appointment and resignation dates, correspondence address, nationality, "
            "country of residence, month-and-year date of birth and "
            "identity-verification status. Costs 1 credit."
        ),
    )


def create_companies_house_filing_history_tool() -> FunctionTool:
    """Create a Scavio Companies House filing history tool."""

    async def scavio_companies_house_filing_history(
        company_number: Annotated[
            str,
            "UK company number (1-20 characters), zero-padded and upper-cased for "
            "you.",
        ],
        page: Annotated[
            int | None,
            "Results page, 1-based. Defaults to 1. No upper bound: past the last page "
            "the register answers an ordinary 200 with an empty list.",
        ] = None,
    ) -> str:
        """UK filings, most recent first: date, filing type code (AA, CS01, SH03),
        description, register annotations and child documents, link to the filed PDF
        with page count.

        Pagination: page - NO upper page bound; past the last page it is an ordinary 200
        with an empty list.

        Args:
            company_number: UK company number (1-20 characters), zero-padded and
                upper-cased for you.
            page: Results page, 1-based. Defaults to 1. No upper bound: past the last
                page the register answers an ordinary 200 with an empty list.

        Returns:
            JSON string with filings, most recent first: date, filing type code (AA,
            CS01, SH03), description, register annotations and child documents, link to
            the filed PDF with page count.
        """
        client = get_async_client()

        params: dict = {
            "company_number": company_number,
            "page": page,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.companies_house.filing_history(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_companies_house_filing_history,
        description=(
            "UK filings, most recent first: date, filing type code (AA, CS01, SH03), "
            "description, register annotations and child documents, and a link to the "
            "filed PDF with its page count. A filing the register has not finished "
            "processing carries a processing_note instead of a document. Costs 1 "
            "credit."
        ),
    )
