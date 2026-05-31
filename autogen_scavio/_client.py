"""Scavio API client management for AutoGen tools."""

from __future__ import annotations

import json
import os
from typing import Any

from scavio import AsyncScavioClient

_async_client: AsyncScavioClient | None = None
_configured_api_key: str | None = None


def configure(api_key: str | None = None) -> None:
    """Set the Scavio API key and reset cached clients."""
    global _configured_api_key, _async_client
    _configured_api_key = api_key
    _async_client = None


def get_async_client() -> AsyncScavioClient:
    """Return a cached AsyncScavioClient, creating one if needed."""
    global _async_client
    if _async_client is None:
        key = _configured_api_key or os.getenv("SCAVIO_API_KEY")
        if not key:
            raise ValueError(
                "A Scavio API key is required. Provide it via "
                "configure(api_key=...) or set the SCAVIO_API_KEY "
                "environment variable. Get a free key at "
                "https://dashboard.scavio.dev"
            )
        _async_client = AsyncScavioClient(api_key=key)
    return _async_client


def truncate_list(
    raw: dict[str, Any],
    path: list[str],
    max_results: int,
) -> dict[str, Any]:
    """Truncate a nested list in the response dict.

    path is a list of keys to traverse, e.g. ["data", "products"].
    """
    obj = raw
    for key in path[:-1]:
        obj = obj.get(key, {})
        if not isinstance(obj, dict):
            return raw
    last = path[-1]
    items = obj.get(last)
    if isinstance(items, list) and len(items) > max_results:
        obj[last] = items[:max_results]
    return raw


def format_response(raw: dict[str, Any]) -> str:
    """Serialize a response dict to a JSON string."""
    return json.dumps(raw, indent=2)
