"""Tool to run a Nikto scan."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from cyber_crew.tools.utils import run_command


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
