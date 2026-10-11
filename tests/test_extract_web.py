"""Map, crawl and batch: the opt-in "crawl" provider."""

from __future__ import annotations

import json
from typing import Any

import pytest

import autogen_scavio
from autogen_scavio.tools import extract as extract_module

CRAWL_ID = "crawl_01a12d21-fb42-7000-88cf-6887f653ee5d"
BATCH_ID = "batch_01a12d22-1d54-7000-9210-4263f1735ce9"


def _status(status: str, job_id: str = CRAWL_ID) -> dict:
    return {
        "data": {
            "id": job_id,
            "status": status,
            "credits_used": 2,
            "results": [{"url": "https://hono.dev/docs", "status": "succeeded"}],
            "next_cursor": None,
        }
    }


class _FakeExtract:
    """client.extract (scavio >= 0.23): callable, with map/crawl/batch methods."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple, dict]] = []
        self.statuses: list[dict] = []

    async def __call__(self, **kwargs: Any) -> dict:
        self.calls.append(("extract", (), kwargs))
        return {"data": {"content": "hi"}}

    async def map(self, url: str, **kwargs: Any) -> dict:
        self.calls.append(("map", (url,), kwargs))
        return {"data": {"links": [{"url": url, "source": "page"}]}, "credits_used": 1}

    async def crawl(self, url: str, **kwargs: Any) -> dict:
        self.calls.append(("crawl", (url,), kwargs))
        return {"data": {"id": CRAWL_ID, "status": "queued"}, "credits_used": 0}

    async def batch(self, urls: list, **kwargs: Any) -> dict:
        self.calls.append(("batch", (urls,), kwargs))
        return {"data": {"id": BATCH_ID, "status": "queued"}, "credits_used": 0}

    async def _status(self, name: str, job_id: str, kwargs: dict) -> dict:
        self.calls.append((name, (job_id,), kwargs))
        return self.statuses.pop(0) if self.statuses else _status("completed", job_id)

    async def crawl_status(self, job_id: str, **kwargs: Any) -> dict:
        return await self._status("crawl_status", job_id, kwargs)

    async def batch_status(self, job_id: str, **kwargs: Any) -> dict:
        return await self._status("batch_status", job_id, kwargs)


class _FakeClient:
    def __init__(self) -> None:
        self.extract = _FakeExtract()


_TOOLS = {
    t.name: t
    for t in autogen_scavio.create_scavio_tools(api_key="k", providers=["crawl"])
}


@pytest.fixture
def ext(monkeypatch) -> _FakeExtract:
    client = _FakeClient()
    monkeypatch.setattr(autogen_scavio._client, "_async_client", client)
    monkeypatch.setattr(extract_module, "JOB_POLL_INTERVAL", 0.0)
    return client.extract


async def _run(name: str, args: dict) -> dict:
    return json.loads(await _TOOLS[name].run_json(args, None))


async def test_map_calls_extract_map_and_drops_none(ext):
    out = await _run("scavio_map_website", {"url": "scavio.dev", "limit": 3})
    assert ext.calls == [("map", ("scavio.dev",), {"limit": 3})]
    assert out["credits_used"] == 1


async def test_crawl_waits_until_completed(ext):
    ext.statuses = [_status("running"), _status("completed"), _status("completed")]
    out = await _run(
        "scavio_crawl_website", {"url": "https://hono.dev/docs", "max_pages": 2}
    )
    assert ext.calls[0] == ("crawl", ("https://hono.dev/docs",), {"max_pages": 2})
    assert ext.calls[1] == (
        "crawl_status",
        (CRAWL_ID,),
        {"limit": 1, "include_content": False},
    )
    assert ext.calls[-1] == ("crawl_status", (CRAWL_ID,), {"limit": 10})
    assert len(ext.calls) == 4
    assert out["data"]["status"] == "completed"


async def test_crawl_wait_zero_returns_the_queued_job(ext):
    out = await _run(
        "scavio_crawl_website", {"url": "https://hono.dev/docs", "wait_seconds": 0}
    )
    assert len(ext.calls) == 1
    assert out["data"]["status"] == "queued"


async def test_crawl_stops_waiting_when_time_runs_out(ext, monkeypatch):
    ticks = iter(range(0, 10_000, 10))
    monkeypatch.setattr(extract_module.time, "monotonic", lambda: float(next(ticks)))
    ext.statuses = [_status("running")] * 5
    out = await _run(
        "scavio_crawl_website", {"url": "https://hono.dev/docs", "wait_seconds": 15}
    )
    assert out["data"]["status"] == "running"
    assert len(ext.calls) == 3  # start, one probe, final read


async def test_status_tools_pass_paging_through(ext):
    await _run(
        "scavio_crawl_status",
        {"id": CRAWL_ID, "cursor": "25", "include_content": False},
    )
    assert ext.calls[-1] == (
        "crawl_status",
        (CRAWL_ID,),
        {"cursor": "25", "limit": 10, "include_content": False},
    )
    await _run("scavio_batch_status", {"id": BATCH_ID, "status": "failed"})
    assert ext.calls[-1] == (
        "batch_status",
        (BATCH_ID,),
        {"limit": 10, "status": "failed"},
    )


async def test_batch_starts_and_waits_on_the_batch_job(ext):
    urls = ["https://example.com/", "https://hono.dev/docs"]
    out = await _run("scavio_batch_extract", {"urls": urls, "mode": "normal"})
    assert ext.calls[0] == ("batch", (urls,), {"mode": "normal"})
    assert all(c[0] == "batch_status" for c in ext.calls[1:])
    assert out["data"]["id"] == BATCH_ID


def test_every_parameter_is_described_and_no_fetch_method_is_named():
    banned = ("proxy", "proxies", "residential", "datacenter", "headless", "browser")
    every = autogen_scavio.create_scavio_tools(api_key="k", enable_crawl=True)
    for tool in every:
        if not tool.name.startswith("scavio_extract") and tool.name not in _TOOLS:
            continue
        text = json.dumps(tool.schema).lower()
        assert "credit" in text, tool.name
        for word in banned:
            assert word not in text, (tool.name, word)
        for name, prop in tool.schema["parameters"]["properties"].items():
            assert prop.get("description", name) != name, (tool.name, name)
