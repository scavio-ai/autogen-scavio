"""Tests for Scavio HEB tools: store_id is forwarded and product_id works alone."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

from autogen_scavio.tools.heb import create_heb_product_tool, create_heb_search_tool

_OK = {"credits_used": 2, "data": {"store": {"store_id": "441", "name": "Uvalde H-E-B"}}}


@patch("autogen_scavio._client._configured_api_key", "test-key")
async def test_search_forwards_store_id():
    mock_client = MagicMock()
    mock_client.heb.search = AsyncMock(return_value=_OK)
    with patch("autogen_scavio._client._async_client", mock_client):
        await create_heb_search_tool().run_json({"query": "whole milk", "store_id": "441"}, None)
    mock_client.heb.search.assert_awaited_once_with(query="whole milk", store_id="441")


@patch("autogen_scavio._client._configured_api_key", "test-key")
async def test_product_id_alone_with_store_id():
    mock_client = MagicMock()
    mock_client.heb.product = AsyncMock(return_value=_OK)
    with patch("autogen_scavio._client._async_client", mock_client):
        await create_heb_product_tool().run_json({"product_id": "314130", "store_id": "441"}, None)
    mock_client.heb.product.assert_awaited_once_with(product_id="314130", store_id="441")
