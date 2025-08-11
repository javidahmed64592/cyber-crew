"""Tool to run a Gobuster scan."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from cyber_crew.tools.utils import run_command


class GobusterScanInput(BaseModel):
    """Input schema for GobusterScan."""

    url: str = Field(..., description="The target URL for the scan.")
    wordlist: str = Field(..., description="The wordlist to use for the scan.")


class GobusterScan(BaseTool):
    """Tool to run a Gobuster scan."""

    name: str = "Gobuster Scan"
    description: str = "Tool to run a Gobuster scan."
    args_schema: type[BaseModel] = GobusterScanInput

    def _run(self, url: str, wordlist: str) -> str:
        cmd = f"gobuster dir -u {url} -w {wordlist}"
        return run_command(cmd)
