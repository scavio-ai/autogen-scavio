"""Scavio SEC EDGAR tools for AutoGen.

6 endpoints. 1 credit flat on all six endpoints - SEC EDGAR is an official free JSON
API. include_history can buy up to ten upstream fetches and is still 1 credit.

LOOKUP FIRST: create_sec_lookup_tool is the entry point. Every other SEC EDGAR endpoint
is keyed by an id that only exists inside SEC EDGAR's own URLs, so a caller holding a
name has to resolve it here before anything else will answer.
"""

from __future__ import annotations

from typing import Annotated, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_sec_lookup_tool() -> FunctionTool:
    """Create a Scavio SEC EDGAR lookup tool."""

    async def scavio_sec_lookup(
        query: Annotated[
            str,
            "Ticker ('AAPL', 'BRK.B'), company name, or a fragment of one (1-200 "
            "characters); each row carries its match tier as 'match'.",
        ],
        limit: Annotated[
            int | None,
            "Rows to return, 1-100. Defaults to 10. Sizes the response; it is not a "
            "page param.",
        ] = None,
        exchange: Annotated[
            Literal["NASDAQ", "NYSE", "OTC", "CBOE"] | None,
            "Restrict to one listing venue; matched case-insensitively, so 'Nasdaq' "
            "also works. Filers the SEC lists with no exchange at all are excluded by "
            "any value.",
        ] = None,
    ) -> str:
        """START HERE. Resolve a company name or ticker (AAPL) to the CIK (0000320193)
        every other SEC EDGAR endpoint is keyed by.

        Args:
            query: Ticker ('AAPL', 'BRK.B'), company name, or a fragment of one (1-200
                characters); each row carries its match tier as 'match'.
            limit: Rows to return, 1-100. Defaults to 10. Sizes the response; it is not
                a page param.
            exchange: Restrict to one listing venue; matched case-insensitively, so
                'Nasdaq' also works. Filers the SEC lists with no exchange at all are
                excluded by any value.

        Returns:
            JSON string with lOOKUP: matching filers with symbol, listing exchange, and
            ready-made submissions / company-facts / EDGAR URLs, tiered by match quality
            (each row carries its tier as `match`).
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "limit": limit,
            "exchange": exchange,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.sec.lookup(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_sec_lookup,
        description=(
            "START HERE. Resolve a company name or ticker (AAPL) to the CIK "
            "(0000320193) every other SEC EDGAR endpoint is keyed by. Up to 100 rows, "
            "tiered by match quality. Costs 1 credit."
        ),
    )


def create_sec_company_tool() -> FunctionTool:
    """Create a Scavio SEC EDGAR company tool."""

    async def scavio_sec_company(
        cik: Annotated[
            str | None,
            "Filer CIK in any spelling (1-20 characters): 320193, 0000320193 or "
            "CIK0000320193. A ticker is accepted here too.",
        ] = None,
        ticker: Annotated[
            str | None,
            "Ticker symbol (1-20 characters), dotted or dashed (BRK.B / BRK-B). Wins "
            "over cik when both are given.",
        ] = None,
    ) -> str:
        """SEC filer profile: legal and former names, SIC industry, EIN, LEI, state of
        incorporation, fiscal year end, addresses, every ticker, and a preview of its 10
        most recent filings.

        Parameter rule: cik or ticker is required.

        Args:
            cik: Filer CIK in any spelling (1-20 characters): 320193, 0000320193 or
                CIK0000320193. A ticker is accepted here too.
            ticker: Ticker symbol (1-20 characters), dotted or dashed (BRK.B / BRK-B).
                Wins over cik when both are given.

        Returns:
            JSON string with filer profile: legal and former names, SIC industry, filer
            category, EIN, LEI, state of incorporation, fiscal year end, business and
            mailing addresses, every ticker with its exchange, which forms it files and
            how often, plus a preview of its 10 most recent filings.
        """
        client = get_async_client()

        params: dict = {
            "cik": cik,
            "ticker": ticker,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.sec.company(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_sec_company,
        description=(
            "SEC filer profile: legal and former names, SIC industry, filer category, "
            "EIN, LEI, state of incorporation, fiscal year end, addresses, every "
            "ticker with its exchange, and a preview of its 10 most recent filings. "
            "Provide cik or ticker. Costs 1 credit."
        ),
    )


def create_sec_filings_tool() -> FunctionTool:
    """Create a Scavio SEC EDGAR filings tool."""

    async def scavio_sec_filings(
        cik: Annotated[
            str | None,
            "Filer CIK, zero-padded or bare (1-20 characters). A ticker is accepted "
            "here too.",
        ] = None,
        ticker: Annotated[
            str | None,
            "Ticker symbol (1-20 characters), as an alternative to cik.",
        ] = None,
        form: Annotated[
            str | list[str] | None,
            "Form types to keep: '10-K', ['10-K', '10-Q'] or the comma-joined "
            "'10-K,8-K'; each value 1-50 characters, at most 25 values. Matched "
            "against the form AND its root form, so 10-K also returns 10-K/A "
            "amendments; ask for '10-K/A' to get only amendments.",
        ] = None,
        date_from: Annotated[
            str | None,
            "Earliest filing date, inclusive (YYYY-MM-DD).",
        ] = None,
        date_to: Annotated[
            str | None,
            "Latest filing date, inclusive (YYYY-MM-DD).",
        ] = None,
        page: Annotated[
            int | None,
            "Results page, 1-based; page size is whatever limit is set to. No upper "
            "bound.",
        ] = None,
        limit: Annotated[int | None, "Filings per page, 1-500. Defaults to 50."] = None,
        include_history: Annotated[
            bool | None,
            "Also fetch the archived filing history beyond EDGAR's 'recent' block, "
            "which is not a fixed window (a decade for a quiet filer, about a year "
            "for a prolific one). Off by default; at most 10 archived shards are "
            "fetched, history_truncated says when a filer had more, and it is still 1 "
            "credit.",
        ] = None,
    ) -> str:
        """A page of one filer's filings: accession number, form and root form, filing
        and period dates, 8-K item codes, direct document links.

        Parameter rule: cik or ticker is required.

        Pagination: page + limit.

        Args:
            cik: Filer CIK, zero-padded or bare (1-20 characters). A ticker is accepted
                here too.
            ticker: Ticker symbol (1-20 characters), as an alternative to cik.
            form: Form types to keep: '10-K', ['10-K', '10-Q'] or the comma-joined
                '10-K,8-K'; each value 1-50 characters, at most 25 values. Matched
                against the form AND its root form, so 10-K also returns 10-K/A
                amendments; ask for '10-K/A' to get only amendments.
            date_from: Earliest filing date, inclusive (YYYY-MM-DD).
            date_to: Latest filing date, inclusive (YYYY-MM-DD).
            page: Results page, 1-based; page size is whatever limit is set to. No upper
                bound.
            limit: Filings per page, 1-500. Defaults to 50.
            include_history: Also fetch the archived filing history beyond EDGAR's
                'recent' block, which is not a fixed window (a decade for a quiet filer,
                about a year for a prolific one). Off by default; at most 10 archived
                shards are fetched, history_truncated says when a filer had more, and it
                is still 1 credit.

        Returns:
            JSON string with filings page: accession number, form and root form, filing
            and period dates, 8-K item codes, direct links to primary document / filing
            index / attachment directory. history_truncated when include_history hit the
            shard cap.
        """
        client = get_async_client()

        params: dict = {
            "cik": cik,
            "ticker": ticker,
            "form": form,
            "date_from": date_from,
            "date_to": date_to,
            "page": page,
            "limit": limit,
            "include_history": include_history,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.sec.filings(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_sec_filings,
        description=(
            "A page of one filer's filings: accession number, form and root form, "
            "filing and period dates, 8-K item codes, direct links to the primary "
            "document, filing index and attachment directory. Up to 500 per page. "
            "Provide cik or ticker. Costs 1 credit."
        ),
    )


def create_sec_concept_tool() -> FunctionTool:
    """Create a Scavio SEC EDGAR concept tool."""

    async def scavio_sec_concept(
        concept: Annotated[
            str,
            "XBRL concept tag, CASE-SENSITIVE (1-120 characters, "
            "^[A-Za-z][A-Za-z0-9]*$): 'NetIncomeLoss' matches, 'netincomeloss' is a "
            "404 upstream. Use facts() to list what a filer actually reports.",
        ],
        cik: Annotated[
            str | None,
            "Filer CIK, zero-padded or bare (1-20 characters). A ticker is accepted "
            "here too.",
        ] = None,
        ticker: Annotated[
            str | None,
            "Ticker symbol (1-20 characters), as an alternative to cik.",
        ] = None,
        taxonomy: Annotated[
            str | None,
            "Reporting taxonomy (1-40 characters, ^[A-Za-z][A-Za-z0-9-]*$): us-gaap, "
            "dei, ifrs-full or srt. Defaults to 'us-gaap'.",
        ] = None,
        unit: Annotated[
            str | None,
            "Unit of measure to keep (1-40 characters), e.g. 'USD' vs 'USD/shares'.",
        ] = None,
        form: Annotated[
            str | None,
            "Form to keep (1-50 characters). EXACT match here, unlike filings(), so "
            "'10-K' excludes 10-K/A.",
        ] = None,
        limit: Annotated[
            int | None,
            "Rows to return, 1-2000. Defaults to 250. Sizes the response; it is not a "
            "page param.",
        ] = None,
    ) -> str:
        """Every value a filer reported for one XBRL concept, newest period first, with
        the form and filing each number came from.

        Parameter rule: cik or ticker is required.

        Args:
            concept: XBRL concept tag, CASE-SENSITIVE (1-120 characters,
                ^[A-Za-z][A-Za-z0-9]*$): 'NetIncomeLoss' matches, 'netincomeloss' is a
                404 upstream. Use facts() to list what a filer actually reports.
            cik: Filer CIK, zero-padded or bare (1-20 characters). A ticker is accepted
                here too.
            ticker: Ticker symbol (1-20 characters), as an alternative to cik.
            taxonomy: Reporting taxonomy (1-40 characters, ^[A-Za-z][A-Za-z0-9-]*$):
                us-gaap, dei, ifrs-full or srt. Defaults to 'us-gaap'.
            unit: Unit of measure to keep (1-40 characters), e.g. 'USD' vs 'USD/shares'.
            form: Form to keep (1-50 characters). EXACT match here, unlike filings(), so
                '10-K' excludes 10-K/A.
            limit: Rows to return, 1-2000. Defaults to 250. Sizes the response; it is
                not a page param.

        Returns:
            JSON string with every value a filer reported for one XBRL concept, newest
            period first, with the form and filing each number came from. Restatements
            are KEPT, not collapsed; `latest` disambiguates a quarter from its
            year-to-date twin using the SEC's comparability flag.
        """
        client = get_async_client()

        params: dict = {
            "concept": concept,
            "cik": cik,
            "ticker": ticker,
            "taxonomy": taxonomy,
            "unit": unit,
            "form": form,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.sec.concept(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_sec_concept,
        description=(
            "Every value a filer reported for one XBRL concept, newest period first, "
            "with the form and filing each number came from. Restatements are kept, "
            "not collapsed. Up to 2000 rows. Provide cik or ticker. Costs 1 credit."
        ),
    )


def create_sec_facts_tool() -> FunctionTool:
    """Create a Scavio SEC EDGAR facts tool."""

    async def scavio_sec_facts(
        cik: Annotated[
            str | None,
            "Filer CIK, zero-padded or bare (1-20 characters). A ticker is accepted "
            "here too.",
        ] = None,
        ticker: Annotated[
            str | None,
            "Ticker symbol (1-20 characters), as an alternative to cik.",
        ] = None,
        taxonomy: Annotated[
            str | None,
            "Restrict to one taxonomy (1-40 characters), e.g. 'us-gaap' or 'dei'.",
        ] = None,
        query: Annotated[
            str | None,
            "Case-insensitive substring matched against the tag name and label (1-200 "
            "characters).",
        ] = None,
        limit: Annotated[
            int | None,
            "Rows to return, 1-2000. Defaults to 250. Sizes the response; it is not a "
            "page param.",
        ] = None,
    ) -> str:
        """The index of every XBRL concept a filer reports - tag, label, description,
        units, most recent value. This is how you find what to ask /sec/concept for.

        Parameter rule: cik or ticker is required.

        Args:
            cik: Filer CIK, zero-padded or bare (1-20 characters). A ticker is accepted
                here too.
            ticker: Ticker symbol (1-20 characters), as an alternative to cik.
            taxonomy: Restrict to one taxonomy (1-40 characters), e.g. 'us-gaap' or
                'dei'.
            query: Case-insensitive substring matched against the tag name and label
                (1-200 characters).
            limit: Rows to return, 1-2000. Defaults to 250. Sizes the response; it is
                not a page param.

        Returns:
            JSON string with the index of every XBRL concept a filer reports - tag,
            label, description, units and most recent value - across us-gaap, dei and
            any other taxonomy it uses. This is how you find what to ask /sec/concept
            for.
        """
        client = get_async_client()

        params: dict = {
            "cik": cik,
            "ticker": ticker,
            "taxonomy": taxonomy,
            "query": query,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.sec.facts(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_sec_facts,
        description=(
            "The index of every XBRL concept a filer reports - tag, label, "
            "description, units and most recent value - across us-gaap, dei and any "
            "other taxonomy it uses. This is how you find what to ask concept() for. "
            "Up to 2000 rows. Provide cik or ticker. Costs 1 credit."
        ),
    )


def create_sec_search_tool() -> FunctionTool:
    """Create a Scavio SEC EDGAR search tool."""

    async def scavio_sec_search(
        query: Annotated[
            str | None,
            "Full-text query over filing documents (1-500 characters); a quoted "
            "phrase is matched exactly, bare words as a bag of terms. Optional - a "
            "cik, ticker, form or date filter on its own is a valid search.",
        ] = None,
        cik: Annotated[
            str | list[str] | None,
            "Restrict to one or more filers by CIK: a single value, a list, or a "
            "comma-joined string; each 1-20 characters, at most 25 values. Tickers "
            "are accepted here too.",
        ] = None,
        ticker: Annotated[
            str | list[str] | None,
            "Restrict to one or more filers by ticker symbol: a single value, a list, "
            "or a comma-joined string; each 1-20 characters, at most 25 values.",
        ] = None,
        form: Annotated[
            str | list[str] | None,
            "Form types to keep: '8-K', ['10-K', '10-Q'] or the comma-joined "
            "'10-K,10-Q'; each 1-50 characters, at most 25 values.",
        ] = None,
        date_from: Annotated[
            str | None,
            "Earliest filing date, inclusive (YYYY-MM-DD). Full-text coverage starts "
            "in 2001.",
        ] = None,
        date_to: Annotated[
            str | None,
            "Latest filing date, inclusive (YYYY-MM-DD).",
        ] = None,
        location: Annotated[
            str | list[str] | None,
            "Filer business-address locations as EDGAR's own 2-character codes (CA, "
            "NY, and its alphanumeric codes for foreign jurisdictions): a single "
            "value, a list, or a comma-joined string; at most 25 values.",
        ] = None,
        sort: Annotated[
            Literal["relevance", "newest", "oldest"] | None,
            "Result ordering. Defaults to the index's own relevance ranking.",
        ] = None,
        page: Annotated[
            int | None,
            "Results page, 1-based, 1-100, 100 documents per page. The SEC's index "
            "refuses a result window past 10,000, so 100 is the last page for any "
            "query.",
        ] = None,
    ) -> str:
        """EDGAR full-text search, 2001-today: each hit is the matching DOCUMENT with
        its URL, form, filing date and filer identity, plus facets by company, form,
        industry and state.

        Pagination: page - capped at 100 (100 docs/page) because the index refuses a
        result window past 10,000.

        Args:
            query: Full-text query over filing documents (1-500 characters); a quoted
                phrase is matched exactly, bare words as a bag of terms. Optional - a
                cik, ticker, form or date filter on its own is a valid search.
            cik: Restrict to one or more filers by CIK: a single value, a list, or a
                comma-joined string; each 1-20 characters, at most 25 values. Tickers
                are accepted here too.
            ticker: Restrict to one or more filers by ticker symbol: a single value, a
                list, or a comma-joined string; each 1-20 characters, at most 25 values.
            form: Form types to keep: '8-K', ['10-K', '10-Q'] or the comma-joined
                '10-K,10-Q'; each 1-50 characters, at most 25 values.
            date_from: Earliest filing date, inclusive (YYYY-MM-DD). Full-text coverage
                starts in 2001.
            date_to: Latest filing date, inclusive (YYYY-MM-DD).
            location: Filer business-address locations as EDGAR's own 2-character codes
                (CA, NY, and its alphanumeric codes for foreign jurisdictions): a single
                value, a list, or a comma-joined string; at most 25 values.
            sort: Result ordering. Defaults to the index's own relevance ranking.
            page: Results page, 1-based, 1-100, 100 documents per page. The SEC's index
                refuses a result window past 10,000, so 100 is the last page for any
                query.

        Returns:
            JSON string with eDGAR full-text search 2001-today: each hit is the matching
            DOCUMENT with its URL, form, filing date and filer identity, plus facets
            breaking the whole result set down by company, form, industry and state.
        """
        client = get_async_client()

        params: dict = {
            "query": query,
            "cik": cik,
            "ticker": ticker,
            "form": form,
            "date_from": date_from,
            "date_to": date_to,
            "location": location,
            "sort": sort,
            "page": page,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.sec.search(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_sec_search,
        description=(
            "EDGAR full-text search, coverage starting 2001: each hit is the matching "
            "DOCUMENT with its URL, form, filing date and filer identity, plus facets "
            "by company, form, industry and state. 100 documents per page, last page "
            "is 100. Costs 1 credit."
        ),
    )
