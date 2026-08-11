"""Scavio Extract tools for AutoGen.

1 endpoint. TIER-PRICED by mode: normal and advanced cost 1 credit, ultra costs 2.
Billing happens only on a successful extraction - a dead link, bot wall or timeout costs
nothing.
"""

from __future__ import annotations

from typing import Annotated, Literal

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
            "Fetch tier, and the price-bearing parameter: 'normal' plain datacenter "
            "fetch (1 credit), 'advanced' full browser render (1 credit), 'ultra' the "
            "hardest-target tier (2 credits). Server default 'normal'.",
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
            mode: Fetch tier, and the price-bearing parameter: 'normal' plain datacenter
                fetch (1 credit), 'advanced' full browser render (1 credit), 'ultra' the
                hardest-target tier (2 credits). Server default 'normal'.

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
