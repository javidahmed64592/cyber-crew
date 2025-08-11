"""Tool to run a Nmap scan."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from cyber_crew.tools.utils import run_command


class NmapScanInput(BaseModel):
    """Input schema for NmapScan."""

    url: str = Field(..., description="The target URL for the scan.")


class NmapScan(BaseTool):
    """Tool to run a Nmap scan."""

    name: str = "Nmap Scan"
    description: str = "Tool to run a Nmap scan."
    args_schema: type[BaseModel] = NmapScanInput

    def _run(self, url: str) -> str:
        cmd = f"nmap -Pn -sV {url}"
        return run_command(cmd)
