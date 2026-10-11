"""Scavio Extract tools for AutoGen.

extract: 1 endpoint. TIER-PRICED by mode: normal and advanced cost 1 credit, ultra
costs 2. Billing happens only on a successful extraction - a dead link, bot wall or
timeout costs nothing.

map / crawl / batch (the opt-in "crawl" provider): map lists a site's URLs (1 credit
on normal; up to 2 on advanced, up to 10 on ultra). Crawl and batch start a background
job, wait up to ``wait_seconds`` (default 45) for it to finish, and return its status
with the first page of results either way; a job still running keeps going and is read
with the free status tools. Jobs bill per SUCCESSFUL page at extract's price for the
mode.
"""

from __future__ import annotations

import asyncio
import time
from typing import Annotated, Any, Callable, Literal

from autogen_core.tools import FunctionTool

from autogen_scavio._client import format_response, get_async_client


def create_extract_tool() -> FunctionTool:
    """Create the Scavio extract tool: read any URL as Markdown, text or HTML."""

    async def scavio_extract(
        url: Annotated[
            str,
            "Page to read (1-2048 characters). http(s) only; a bare host is upgraded "
            "to https, and loopback, private, link-local and metadata hosts are "
            "rejected with a 400.",
        ],
        format: Annotated[
            Literal["html", "markdown", "text"] | None,
            "Output format: 'html' is the raw page, 'markdown' a readability "
            "extraction, 'text' that markdown flattened to plain text (server default "
            "'markdown').",
        ] = None,
        mode: Annotated[
            Literal["normal", "advanced", "ultra"] | None,
            "Fetch tier, and the price-bearing parameter: 'normal' is the standard "
            "fetch (1 credit), 'advanced' renders JavaScript-built pages (1 credit), "
            "'ultra' reaches the hardest pages (2 credits). Server default 'normal'.",
        ] = None,
    ) -> str:
        """Read ANY URL and get it back as raw HTML, readability Markdown, or plain
        text. The read-a-page primitive: { url, format, mode, content, content_length }.

        Args:
            url: Page to read (1-2048 characters). http(s) only; a bare host is upgraded
                to https, and loopback, private, link-local and metadata hosts are
                rejected with a 400.
            format: Output format: 'html' is the raw page, 'markdown' a readability
                extraction, 'text' that markdown flattened to plain text (server default
                'markdown').
            mode: Fetch tier, and the price-bearing parameter: 'normal' is the standard
                fetch (1 credit), 'advanced' renders JavaScript-built pages (1 credit),
                'ultra' reaches the hardest pages (2 credits). Server default 'normal'.

        Returns:
            JSON string with { url, format, mode, content, content_length } - the page
            as raw HTML, readability Markdown, or plain text.
        """
        client = get_async_client()

        params: dict = {
            "url": url,
            "format": format,
            "mode": mode,
        }
        params = {k: v for k, v in params.items() if v is not None}

        raw = await client.extract(**params)

        return format_response(raw)

    return FunctionTool(
        scavio_extract,
        description=(
            "Read any URL and get the page back as raw HTML, readability Markdown or "
            "plain text: { url, format, mode, content, content_length }. Tier-priced "
            "by mode -- normal and advanced cost 1 credit, ultra costs 2 -- and only "
            "a successful extraction is billed, so a dead link, bot wall or timeout "
            "costs nothing."
        ),
    )


# ---------------------------------------------------------------------------
# Map, crawl and batch (provider "crawl", opt-in)
# ---------------------------------------------------------------------------

JOB_TERMINAL_STATUSES = frozenset({"completed", "failed", "cancelled"})
JOB_POLL_INTERVAL = 3.0
JOB_MAX_WAIT = 300

_MODE = (
    "Fetch tier: 'normal' is the standard fetch, 'advanced' renders JavaScript-built "
    "pages, 'ultra' reaches the hardest pages. Server default 'normal'."
)
_PATHS = (
    "Path globs (max 20): '*' matches within one path segment, '**' across segments, "
    "e.g. ['/blog/**']."
)
_WAIT = (
    "Seconds to wait for the job to finish, 0-300 (default 45). 0 returns the job "
    "id at once; a job still running when the wait ends keeps going."
)
_LIMIT = "Results per response, 1-100 (default 10); page on with next_cursor."
_JOB_PRICE = (
    "Billed per SUCCESSFUL page at extract's price for the mode: normal and advanced 1 "
    "credit, ultra 2 credits. Failed and skipped pages are free, and the job stops "
    "cleanly if the balance runs out."
)


def _clean(params: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in params.items() if v is not None}


async def _wait_for_job(
    status_fn: Callable[..., Any],
    created: dict[str, Any],
    wait_seconds: int,
    limit: int,
) -> dict[str, Any]:
    """Poll a started job until it finishes or the wait runs out, then read it."""
    data = created.get("data")
    job_id = data.get("id") if isinstance(data, dict) else None
    if not job_id or wait_seconds <= 0:
        return created
    deadline = time.monotonic() + min(max(wait_seconds, 0), JOB_MAX_WAIT)
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        await asyncio.sleep(min(JOB_POLL_INTERVAL, remaining))
        probe = await status_fn(job_id, limit=1, include_content=False)
        probe_data = probe.get("data")
        if (
            isinstance(probe_data, dict)
            and probe_data.get("status") in JOB_TERMINAL_STATUSES
        ):
            break
    return await status_fn(job_id, limit=limit)


def create_map_website_tool() -> FunctionTool:
    """Create the Scavio map tool: list a website's page URLs."""

    async def scavio_map_website(
        url: Annotated[str, "The site to map. A bare host is upgraded to https."],
        search: Annotated[
            str | None, "Only return URLs containing every word of this text."
        ] = None,
        limit: Annotated[
            int | None,
            "Maximum links to return, 1-5000. Default 1000 (plan caps: Free 500, PAYG "
            "1,000, paid plans 5,000).",
        ] = None,
        sitemap: Annotated[
            Literal["include", "only", "skip"] | None,
            "'include' (default) combines the site's sitemaps with the start page's "
            "links; 'only' uses sitemaps alone; 'skip' uses page links alone.",
        ] = None,
        include_subdomains: Annotated[
            bool | None, "Also return URLs on subdomains. Default false."
        ] = None,
        include_paths: Annotated[
            list[str] | None, "Keep only URLs matching. " + _PATHS
        ] = None,
        exclude_paths: Annotated[
            list[str] | None, "Drop URLs matching. " + _PATHS
        ] = None,
        ignore_query_parameters: Annotated[
            bool | None,
            "Treat URLs differing only by query string as one. Default true.",
        ] = None,
        mode: Annotated[Literal["normal", "advanced", "ultra"] | None, _MODE] = None,
    ) -> str:
        """List a website's page URLs from its sitemaps and start page.

        Returns:
            JSON string with { url, links: [{ url, source, lastmod }], total_found,
            returned, truncated, sitemaps_read }.
        """
        client = get_async_client()
        params = _clean(
            {
                "search": search,
                "limit": limit,
                "sitemap": sitemap,
                "include_subdomains": include_subdomains,
                "include_paths": include_paths,
                "exclude_paths": exclude_paths,
                "ignore_query_parameters": ignore_query_parameters,
                "mode": mode,
            }
        )
        return format_response(await client.extract.map(url, **params))

    return FunctionTool(
        scavio_map_website,
        description=(
            "List a website's page URLs, gathered from its sitemaps and its start "
            "page, deduplicated, filtered by path or search words and limited: { url, "
            "links, total_found, returned, truncated }. Pages the site's robots.txt "
            "disallows are left out. Use it to find the right pages before extracting "
            "or crawling. Tier-priced: 1 credit on mode 'normal'; 'advanced' costs up "
            "to 2 credits and 'ultra' up to 10, priced by what the call needed."
        ),
    )


def create_crawl_website_tool() -> FunctionTool:
    """Create the Scavio crawl tool: crawl a site from one URL."""

    async def scavio_crawl_website(
        url: Annotated[
            str, "Where the crawl starts. Only pages on the same site are crawled."
        ],
        max_pages: Annotated[
            int | None,
            "Maximum pages to fetch. Default 100. Plan caps: Free 10, PAYG 100, "
            "Project 500, Bootstrap 2,000, Startup 5,000, Growth 10,000.",
        ] = None,
        max_depth: Annotated[
            int | None, "Links away from the start page to follow, 0-10 (default 3)."
        ] = None,
        include_paths: Annotated[
            list[str] | None, "Crawl only paths matching. " + _PATHS
        ] = None,
        exclude_paths: Annotated[
            list[str] | None, "Skip paths matching. " + _PATHS
        ] = None,
        allow_subdomains: Annotated[
            bool | None, "Also crawl subdomains. Default false."
        ] = None,
        ignore_query_parameters: Annotated[
            bool | None,
            "Treat URLs differing only by query string as one page. Default true.",
        ] = None,
        sitemap: Annotated[
            Literal["include", "skip", "only"] | None,
            "'include' (default) also starts from the site's sitemap; 'skip' follows "
            "links only; 'only' fetches sitemap pages without following links.",
        ] = None,
        format: Annotated[
            Literal["html", "markdown", "text"] | None,
            "Format for each page: html, markdown (default) or text.",
        ] = None,
        mode: Annotated[Literal["normal", "advanced", "ultra"] | None, _MODE] = None,
        wait_seconds: Annotated[int, _WAIT] = 45,
        limit: Annotated[int, _LIMIT] = 10,
    ) -> str:
        """Crawl a website from one URL and get its pages as Markdown, text or HTML.

        Returns:
            JSON string with { id, status, pages, credits_used, results, next_cursor }.
        """
        client = get_async_client()
        body = _clean(
            {
                "max_pages": max_pages,
                "max_depth": max_depth,
                "include_paths": include_paths,
                "exclude_paths": exclude_paths,
                "allow_subdomains": allow_subdomains,
                "ignore_query_parameters": ignore_query_parameters,
                "sitemap": sitemap,
                "format": format,
                "mode": mode,
            }
        )
        created = await client.extract.crawl(url, **body)
        return format_response(
            await _wait_for_job(
                client.extract.crawl_status, created, wait_seconds, limit
            )
        )

    return FunctionTool(
        scavio_crawl_website,
        description=(
            "Crawl a website from one start URL: same-site pages are discovered and "
            "extracted breadth-first within the page, depth and path limits, each as "
            "Markdown, text or HTML. Pages the site's robots.txt disallows are "
            "skipped. "
            "Waits up to wait_seconds (default 45) and returns { id, status, pages, "
            "credits_used, results, next_cursor }; if status is still queued or "
            "running, call scavio_crawl_status with the id later. Tier-priced: "
            + _JOB_PRICE
        ),
    )


def _status_tool(kind: str) -> FunctionTool:
    async def job_status(
        id: Annotated[str, "The job id returned when the job was started (data.id)."],
        cursor: Annotated[str | None, "next_cursor from the previous response."] = None,
        limit: Annotated[int, _LIMIT] = 10,
        status: Annotated[
            Literal["succeeded", "failed", "skipped"] | None,
            "Only results with this status.",
        ] = None,
        include_content: Annotated[
            bool | None, "False lists results without their page content. Default true."
        ] = None,
    ) -> str:
        """Read a job's progress and its page results, paged by cursor.

        Returns:
            JSON string with { status, pages, credits_used, results, next_cursor }.
        """
        client = get_async_client()
        fn = (
            client.extract.crawl_status
            if kind == "crawl"
            else client.extract.batch_status
        )
        params = _clean(
            {
                "cursor": cursor,
                "limit": limit,
                "status": status,
                "include_content": include_content,
            }
        )
        return format_response(await fn(id, **params))

    job_status.__name__ = f"scavio_{kind}_status"
    job_status.__qualname__ = job_status.__name__
    return FunctionTool(
        job_status,
        name=f"scavio_{kind}_status",
        description=(
            f"Read a {kind} job's progress and its page results by job id, paged by "
            "cursor: { status, stopped_reason, pages, credits_used, results: [{ url, "
            "status, content }], next_cursor }. Results are kept for 3 days after the "
            f"{kind} finishes. Free: costs 0 credits."
        ),
    )


def create_crawl_status_tool() -> FunctionTool:
    """Create the Scavio crawl status tool (free)."""
    return _status_tool("crawl")


def create_batch_extract_tool() -> FunctionTool:
    """Create the Scavio batch tool: extract a list of URLs in one job."""

    async def scavio_batch_extract(
        urls: Annotated[
            list[str],
            "The pages to extract (duplicates removed). Plan caps: Free 10, PAYG 50, "
            "Project 100, Bootstrap 500, Startup and Growth 1,000.",
        ],
        format: Annotated[
            Literal["html", "markdown", "text"] | None,
            "Format for each page: html, markdown (default) or text.",
        ] = None,
        mode: Annotated[Literal["normal", "advanced", "ultra"] | None, _MODE] = None,
        wait_seconds: Annotated[int, _WAIT] = 45,
        limit: Annotated[int, _LIMIT] = 10,
    ) -> str:
        """Extract a list of URLs in one job, each as Markdown, text or HTML.

        Returns:
            JSON string with { id, status, pages, credits_used, results, next_cursor }.
        """
        client = get_async_client()
        created = await client.extract.batch(
            urls, **_clean({"format": format, "mode": mode})
        )
        return format_response(
            await _wait_for_job(
                client.extract.batch_status, created, wait_seconds, limit
            )
        )

    return FunctionTool(
        scavio_batch_extract,
        description=(
            "Extract a list of URLs (up to 1,000, plan-limited) in one job, each "
            "returned as Markdown, text or HTML exactly like scavio_extract, in input "
            "order. Waits up to wait_seconds (default 45) and returns { id, status, "
            "pages, credits_used, results, next_cursor }; if status is still queued or "
            "running, call scavio_batch_status with the id later. Tier-priced: "
            + _JOB_PRICE
        ),
    )


def create_batch_status_tool() -> FunctionTool:
    """Create the Scavio batch status tool (free)."""
    return _status_tool("batch")
