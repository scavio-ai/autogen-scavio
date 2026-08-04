"""Tests for Scavio LinkedIn tools."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import autogen_scavio
from autogen_scavio.tools import linkedin as linkedin_tools
from autogen_scavio.tools.linkedin import (
    create_linkedin_company_posts_tool,
    create_linkedin_company_tool,
    create_linkedin_job_tool,
    create_linkedin_person_about_tool,
    create_linkedin_person_posts_tool,
    create_linkedin_person_tool,
    create_linkedin_post_comments_tool,
    create_linkedin_post_tool,
    create_linkedin_search_jobs_tool,
)
from tests.conftest import (
    mock_linkedin_company_response,
    mock_linkedin_feed_response,
    mock_linkedin_job_response,
    mock_linkedin_jobs_response,
    mock_linkedin_person_about_response,
    mock_linkedin_person_response,
    mock_linkedin_post_comments_response,
    mock_linkedin_post_response,
)


class TestLinkedInPersonTools:
    """Tests for the member-scoped tools."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_person(self, _mock_client):
        mock_client = MagicMock()
        mock_client.linkedin.person = AsyncMock(
            return_value=mock_linkedin_person_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_linkedin_person_tool()
            assert tool.name == "scavio_linkedin_person"
            parsed = json.loads(
                await tool.run_json({"username": "williamhgates"}, None)
            )
            assert parsed["data"]["public_identifier"] == "williamhgates"
            # url was not supplied, so it is not sent as a null.
            assert mock_client.linkedin.person.call_args.kwargs == {
                "username": "williamhgates"
            }

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_person_accepts_url_instead(self, _mock_client):
        mock_client = MagicMock()
        mock_client.linkedin.person = AsyncMock(
            return_value=mock_linkedin_person_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            await create_linkedin_person_tool().run_json(
                {"url": "https://www.linkedin.com/in/williamhgates/"}, None
            )
            assert mock_client.linkedin.person.call_args.kwargs == {
                "url": "https://www.linkedin.com/in/williamhgates/"
            }

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_person_about(self, _mock_client):
        mock_client = MagicMock()
        mock_client.linkedin.person_about = AsyncMock(
            return_value=mock_linkedin_person_about_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_linkedin_person_about_tool()
            assert tool.name == "scavio_linkedin_person_about"
            parsed = json.loads(
                await tool.run_json({"username": "williamhgates"}, None)
            )
            assert parsed["data"]["about"]

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_person_posts(self, _mock_client):
        mock_client = MagicMock()
        mock_client.linkedin.person_posts = AsyncMock(
            return_value=mock_linkedin_feed_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_linkedin_person_posts_tool(max_results=3)
            assert tool.name == "scavio_linkedin_person_posts"
            parsed = json.loads(
                await tool.run_json(
                    {"username": "williamhgates", "type": "reactions"}, None
                )
            )
            # Feed endpoints nest the list under data.data.
            assert len(parsed["data"]["data"]) == 3
            assert parsed["data"]["next_cursor"] == "next"
            assert mock_client.linkedin.person_posts.call_args.kwargs["type"] == (
                "reactions"
            )


class TestLinkedInCompanyTools:
    """Tests for the company-scoped tools."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_company(self, _mock_client):
        mock_client = MagicMock()
        mock_client.linkedin.company = AsyncMock(
            return_value=mock_linkedin_company_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_linkedin_company_tool()
            assert tool.name == "scavio_linkedin_company"
            parsed = json.loads(await tool.run_json({"company": "microsoft"}, None))
            # featured_employees is the supported substitute for the retired
            # company/people endpoint.
            assert parsed["data"]["featured_employees"]

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_company_posts(self, _mock_client):
        mock_client = MagicMock()
        mock_client.linkedin.company_posts = AsyncMock(
            return_value=mock_linkedin_feed_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_linkedin_company_posts_tool(max_results=2)
            assert tool.name == "scavio_linkedin_company_posts"
            parsed = json.loads(await tool.run_json({"company": "microsoft"}, None))
            assert len(parsed["data"]["data"]) == 2


class TestLinkedInJobTools:
    """Tests for the job tools."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_search_jobs_uses_search_not_query(self, _mock_client):
        mock_client = MagicMock()
        mock_client.linkedin.search_jobs = AsyncMock(
            return_value=mock_linkedin_jobs_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_linkedin_search_jobs_tool(max_results=5)
            assert tool.name == "scavio_linkedin_search_jobs"
            parsed = json.loads(
                await tool.run_json(
                    {"search": "software engineer", "location": "United States"}, None
                )
            )
            assert len(parsed["data"]["data"]) == 5
            kwargs = mock_client.linkedin.search_jobs.call_args.kwargs
            assert kwargs["search"] == "software engineer"
            assert "query" not in kwargs
            assert "keywords" not in kwargs

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_job(self, _mock_client):
        mock_client = MagicMock()
        mock_client.linkedin.job = AsyncMock(return_value=mock_linkedin_job_response())

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_linkedin_job_tool()
            assert tool.name == "scavio_linkedin_job"
            parsed = json.loads(await tool.run_json({"job_id": "4415427228"}, None))
            assert parsed["data"]["company"]["name"] == "Microsoft"

    def test_job_description_states_30_credits(self):
        """The most expensive call in the API must say so in its description."""
        assert "30 credits" in create_linkedin_job_tool().description


class TestLinkedInPostTools:
    """Tests for the post tools."""

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_post(self, _mock_client):
        mock_client = MagicMock()
        mock_client.linkedin.post = AsyncMock(
            return_value=mock_linkedin_post_response()
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_linkedin_post_tool()
            assert tool.name == "scavio_linkedin_post"
            parsed = json.loads(
                await tool.run_json({"post_id": "7488618410256523265"}, None)
            )
            assert parsed["data"]["num_likes"] == 500

    @patch("autogen_scavio._client._async_client")
    @patch("autogen_scavio._client._configured_api_key", "test-key")
    async def test_post_comments_pages_by_number(self, _mock_client):
        mock_client = MagicMock()
        mock_client.linkedin.post_comments = AsyncMock(
            return_value=mock_linkedin_post_comments_response(10)
        )

        with patch("autogen_scavio._client._async_client", mock_client):
            tool = create_linkedin_post_comments_tool(max_results=4)
            assert tool.name == "scavio_linkedin_post_comments"
            parsed = json.loads(
                await tool.run_json(
                    {"post_id": "7488618410256523265", "page": 2}, None
                )
            )
            assert len(parsed["data"]["data"]) == 4
            kwargs = mock_client.linkedin.post_comments.call_args.kwargs
            # This endpoint alone pages by a 1-based number, not a cursor.
            assert kwargs["page"] == 2
            assert "cursor" not in kwargs


class TestLinkedInRetiredEndpoints:
    """The five 410 endpoints must not be wrapped as tools."""

    def test_no_factories_for_retired_endpoints(self):
        retired = (
            "person_contact",
            "company_people",
            "company_jobs",
            "search_people",
            "search_posts",
        )
        for name in retired:
            factory = f"create_linkedin_{name}_tool"
            assert not hasattr(linkedin_tools, factory), factory
            assert factory not in autogen_scavio.__all__

    def test_registered_linkedin_tools_are_the_nine_live_ones(self):
        tools = autogen_scavio.create_scavio_tools(
            api_key="test-key", providers=["linkedin"]
        )
        assert {t.name for t in tools} == {
            "scavio_linkedin_person",
            "scavio_linkedin_person_about",
            "scavio_linkedin_person_posts",
            "scavio_linkedin_company",
            "scavio_linkedin_company_posts",
            "scavio_linkedin_search_jobs",
            "scavio_linkedin_job",
            "scavio_linkedin_post",
            "scavio_linkedin_post_comments",
        }
