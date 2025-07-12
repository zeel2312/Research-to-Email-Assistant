"""Multi‑source web search: DuckDuckGo → Wikipedia → optional Serper API."""
from __future__ import annotations

import os
import requests
from langchain.tools import BaseTool

# Optional: if user sets SERPER_API_KEY in .env we'll hit Google Search via Serper.
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

class WebSearchTool(BaseTool):
    """Searches the web and returns a concise plaintext summary."""

    name: str = "web_search"
    description: str = (
        "Returns a short, human‑readable paragraph that explains the query topic."
    )

    # ---------------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------------
    def _duckduckgo(self, query: str) -> str | None:
        try:
            resp = requests.get(
                "https://api.duckduckgo.com/",
                params={
                    "q": query,
                    "format": "json",
                    "no_redirect": 1,
                    "no_html": 1,
                },
                timeout=10,
            )
            data = resp.json()
            if (abstract := data.get("Abstract")):
                return abstract

            # scrape up to 3 related topic snippets
            snippets: list[str] = []
            for topic in data.get("RelatedTopics", [])[:3]:
                if isinstance(topic, dict) and topic.get("Text"):
                    snippets.append(topic["Text"])
            if snippets:
                return "".join(snippets)
        except Exception:
            pass
        return None

    def _wikipedia(self, query: str) -> str | None:
        try:
            # 1) use the search API to find the best matching title
            search_resp = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "srlimit": 1,
                    "format": "json",
                },
                timeout=10,
            )
            search_data = search_resp.json()
            if not (search_data["query"]["search"]):
                return None
            title = search_data["query"]["search"][0]["title"]

            # 2) fetch the summary for that title
            summary_resp = requests.get(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}",
                timeout=10,
            )
            if summary_resp.status_code == 200:
                return summary_resp.json().get("extract")
        except Exception:
            pass
        return None

    def _serper(self, query: str) -> str | None:
        """Google-like fallback if SERPER_API_KEY is configured."""
        api_key = os.getenv("SERPER_API_KEY")      # read at call-time
        if not api_key:
            return None
        try:
            resp = requests.post(
                "https://google.serper.dev/search",
                json={"q": query, "num": 5},
                headers={"X-API-KEY": api_key},    # ← use *api_key* here
                timeout=10,
            )
            data = resp.json()
            if items := data.get("organic", []):
                return items[0].get("snippet")
        except Exception:
            pass
        return None

    # ------------------------------------------------------------------
    # Tool entrypoints
    # ------------------------------------------------------------------
    def _run(self, query: str) -> str:  # type: ignore[override]
        # 1) DuckDuckGo Instant Answer
        if (text := self._duckduckgo(query)):
            print("DunkDuckGo:", text)
            return text

        # 2) Wikipedia summary
        if (text := self._wikipedia(query)):
            print("Wikipedia:", text)
            return text

        # 3) Serper Google Search (if key exists)
        if (text := self._serper(query)):
            print("Serper:", text)
            return text

        return "No useful web result found."

    async def _arun(self, query: str):  # type: ignore[override]
        raise NotImplementedError("Async path not implemented.")