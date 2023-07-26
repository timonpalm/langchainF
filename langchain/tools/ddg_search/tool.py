"""Tool for the DuckDuckGo search API."""

import warnings
from typing import Any, Optional

from pydantic import Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.base import BaseTool
from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper


class DuckDuckGoSearchRun(BaseTool):
    """Tool that adds the capability to query the DuckDuckGo search API."""

    name = "duckduckgo_search"
    description = (
        "A wrapper around DuckDuckGo Search. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query."
    )
    api_wrapper: DuckDuckGoSearchAPIWrapper = Field(
        default_factory=DuckDuckGoSearchAPIWrapper
    )

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return self.api_wrapper.run(query)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("DuckDuckGoSearch does not support async")


class DuckDuckGoSearchResults(BaseTool):
    """Tool that queries the Duck Duck Go Search API and get back json."""

    name = "DuckDuckGo Results JSON"
    description = (
        "A wrapper around Duck Duck Go Search. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query. Output is a JSON array of the query results"
    )
    num_results: int = 4
    api_wrapper: DuckDuckGoSearchAPIWrapper = Field(
        default_factory=DuckDuckGoSearchAPIWrapper
    )
    backend: str = Field(default="api")

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        res = self.api_wrapper.results(query, self.num_results, backend=self.backend)

        def dict2str(d: dict):
            items = []
            for k, v in d.items():
                items.append(f"{k}: {v}")
            return ", ".join(items)
        
        res = [f"[{dict2str(r)}]" for r in res]
        return ", ".join(res)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("DuckDuckGoSearchResults does not support async")


def DuckDuckGoSearchTool(*args: Any, **kwargs: Any) -> DuckDuckGoSearchRun:
    """
    Deprecated. Use DuckDuckGoSearchRun instead.

    Args:
        *args:
        **kwargs:

    Returns:
        DuckDuckGoSearchRun
    """
    warnings.warn(
        "DuckDuckGoSearchTool will be deprecated in the future. "
        "Please use DuckDuckGoSearchRun instead.",
        DeprecationWarning,
    )
    return DuckDuckGoSearchRun(*args, **kwargs)
