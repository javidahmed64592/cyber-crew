"""Tool to fetch the content of a URL."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from cyber_crew.tools.utils import run_command


class FetchUrlInput(BaseModel):
    """Input schema for FetchUrl."""

    url: str = Field(..., description="The target URL to fetch.")


class FetchUrl(BaseTool):
    """Tool to fetch the content of a URL."""

    name: str = "Fetch URL"
    description: str = "Tool to fetch the content of a URL."
    args_schema: type[BaseModel] = FetchUrlInput

    def _run(self, url: str) -> str:
        cmd = f"curl -s {url}"
        return run_command(cmd)
