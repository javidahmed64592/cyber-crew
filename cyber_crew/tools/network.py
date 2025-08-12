"""Command line tools for network enumeration."""

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


class NiktoScanInput(BaseModel):
    """Input schema for NiktoScan."""

    url: str = Field(..., description="The target URL for the scan.")


class NiktoScan(BaseTool):
    """Tool to run a Nikto scan."""

    name: str = "Nikto Scan"
    description: str = "Tool to run a Nikto scan."
    args_schema: type[BaseModel] = NiktoScanInput

    def _run(self, url: str) -> str:
        cmd = f"nikto -h {url}"
        return run_command(cmd)


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
