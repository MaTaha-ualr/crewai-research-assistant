"""Exa web-search tool using the official Python SDK search method."""

import os

from crewai.tools import BaseTool, tool
from exa_py import Exa


def create_search_tool() -> BaseTool:
    """Create a CrewAI tool using Exa's documented search settings."""
    api_key = os.getenv("EXA_API_KEY")
    if not api_key:
        raise ValueError("EXA_API_KEY is missing. Add it to your .env file.")

    exa = Exa(api_key=api_key)

    @tool("Search the web with Exa")
    def search_web(query: str) -> str:
        """Find trustworthy web sources and return their URLs and highlights."""
        if not query.strip():
            raise ValueError("The Exa search query cannot be empty.")

        response = exa.search(
            query,
            type="auto",
            contents={"highlights": True},
        )
        results = response.results or []
        if not results:
            return "No useful search results were returned for this query."

        formatted_results = []
        for result in results:
            highlights = " ".join(result.highlights or [])
            formatted_results.append(
                f"Title: {result.title or 'Untitled'}\n"
                f"URL: {result.url}\n"
                f"Published: {result.published_date or 'Date unavailable'}\n"
                f"Highlights: {highlights or 'No highlights returned.'}"
            )
        return "\n\n".join(formatted_results)

    return search_web
